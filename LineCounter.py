#!/usr/bin/env python
# coding=utf-8

import time
import string
import sys
import os

from optparse import OptionParser

filelists = []

whitelist = ['py']


def shouldExclude(full_path, basedir, exclude_list):
    if len(exclude_list) > 0:
        for exclude_path in exclude_list:
            if full_path.startswith(os.path.join(basedir, exclude_path)):
                return True

    return False


def getFile(basedir, suffix_list, exclude_list):

    if len(suffix_list) == 0:
        suffix_list = whitelist

    global filelists
    for parent, dirnames, filenames in os.walk(basedir):
        for filename in filenames:
            if shouldExclude(parent, basedir, exclude_list):
                continue
            ext = filename.split('.')[-1]
            if ext in suffix_list:
                filelists.append(os.path.join(parent, filename))


def count_line(fname):
    count = 0
    for file_line in open(fname).xreadlines():
        if file_line != '' and file_line != '\n':  # 过滤掉空行
            count += 1
    print "%s-----%d"%(fname, count)
    return count


def count_main(path, suffix, exclude_list):
    suffix_list = []

    if len(suffix) > 0:
        suffix_list = suffix.split(',')

    if len(exclude_list) > 0:
        exclude_list = exclude_list.split(',')

    startTime = time.clock()

    getFile(path, suffix_list, exclude_list)

    total_line = 0
    for file_list in filelists:
        total_line = total_line + count_line(file_list)
    print 'Total lines:', total_line
    print 'Done! Cost Time: %0.2f second' % (time.clock() - startTime)


def main(argv=None):
    '''Command line options.'''

    program_name = os.path.basename(sys.argv[0])
    program_version = "v0.1"

    program_version_string = '%%prog %s' % (program_version)

    program_longdesc = "count number of lines in path which ext with suffix, separator is ',',exclude paths with -e" \
                       "\n separator with ','"
    program_license = "Copyright 2018 Songwater (songwater@aliyun.com)                                            \
                Licensed under the Apache License 2.0\nhttp://www.apache.org/licenses/LICENSE-2.0"

    if argv is None:
        argv = sys.argv[1:]
    try:
        # setup option parser
        parser = OptionParser(version=program_version_string, epilog=program_longdesc, description=program_license)
        parser.add_option("-p", "--path", dest="path", help="set path to count[default: %default] separator is ','",
                          metavar="PATH")
        parser.add_option("-s", "--suffix", dest="suffix", help="set file suffix to count[default: %default]",
                          metavar="STRING")
        parser.add_option("-e", "--exclude", dest="exclude_list",
                          help="set exclusion paths which should not count [default: %default] separator is ','",
                          metavar="STRING")

        parser.add_option("-v", "--verbose", dest="verbose", action="count",
                          help="set verbosity level [default: %default]")

        # set defaults
        parser.set_defaults(path=".", suffix="", exclude_list="")

        # process options
        (opts, args) = parser.parse_args(argv)

        # MAIN BODY #
        count_main(opts.path, opts.suffix, opts.exclude_list)

    except Exception, e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2


DEBUG = 0
TESTRUN = 0
PROFILE = 0


if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
    if TESTRUN:
        import doctest

        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats

        profile_filename = 'tools.LineCounter_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
