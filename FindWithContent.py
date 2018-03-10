#!/usr/bin/env python
# encoding: utf-8
'''
tools.FindWithContent -- shortdesc

tools.FindWithContent is a find files with giving content

It defines classes_and_methods

@author:     Songwater

@copyright:  2015 S.T.Y. All rights reserved.

@license:    GPL

@contact:    sty_email@163.com
@deffield    updated: Updated
'''

import string
import sys
import os

from optparse import OptionParser

__all__ = []
__version__ = 0.1
__date__ = '2015-03-13'
__updated__ = '2015-03-13'

DEBUG = 0
TESTRUN = 0
PROFILE = 0

text_characters = "".join(map(chr, range(32, 127)) + list("\n\r\t\b"))
_null_trans = string.maketrans("","")

def istextfile(filename, blocksize = 512):
    return istext(open(filename).read(blocksize))

def istext(s):
    if "\0" in s:
        return 0
   
    if not s:  # Empty files are considered text
        return 1

    # Get the non-text characters (maps a character to itself then
    # use the ‘remove’ option to get rid of the text characters.)
    t = s.translate(_null_trans, text_characters)

    # If more than 30% non-text characters, then
    # this is considered a binary file
    if len(t)/len(s) > 0.30:
        return 0
    return 1

def find(path,content,suffix):
    if os.path.exists(path):
        total = 0
        for curDir,subDirs,files in os.walk(path):
            for fileTmp in files:
                if suffix :
                    ext = os.path.splitext(fileTmp)[1][1:]
                    if ext != suffix:
                        continue
                fullFileName = os.path.join(curDir,fileTmp) 
                  
                try:
                    fileFd = open(fullFileName,'r')
                    if not istext(fileFd.read(512)):
                        continue
                    num = 0
                    while True:
                        line = fileFd.readline()
                        if not line:
                            break
                        if line.find(content)!= -1:
                            num += 1
                    if num > 0:
                        print '{} : {}'.format(fullFileName,num)    
                        total += num  
                except IOError: 
                    print '{} read failed!'.format(fullFileName)
                    continue  
                finally:
                    if not fileFd:
                        fileFd.close()
                        
        if total > 0 :
            print "found '{}' {} times for .{} files in path {}".format(content,total,suffix,path)   
        else:
            print "'{}' not found for .{} files in path {}!".format(content,suffix,path)                          
                
    else:
        print path,'is not exist!'

def main(argv=None):
    '''Command line options.'''

    program_name = os.path.basename(sys.argv[0])
    program_version = "v0.1"
    program_build_date = "%s" % __updated__

    program_version_string = '%%prog %s (%s)' % (program_version, program_build_date)
    #program_usage = '''usage: spam two eggs''' # optional - will be autogenerated by optparse
    program_longdesc = '''''' # optional - give further explanation about what the program does
    program_license = "Copyright 2015 Sty (sty_email@163.com)                                            \
                Licensed under the Apache License 2.0\nhttp://www.apache.org/licenses/LICENSE-2.0"

    if argv is None:
        argv = sys.argv[1:]
    try:
        # setup option parser
        parser = OptionParser(version=program_version_string, epilog=program_longdesc, description=program_license)
        parser.add_option("-p", "--path", dest="path", help="set path to find[default: %default]", metavar="PATH")
        parser.add_option("-s", "--suffix", dest="suffix", help="set file suffix to find[default: %default]", metavar="STRING")
        parser.add_option("-c", "--content", dest="content", help="set content to find in file [default: %default]", metavar="STRING")
        parser.add_option("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %default]")

        # set defaults
        parser.set_defaults(path=".", content="",suffix="")

        # process options
        (opts, args) = parser.parse_args(argv)

#         if opts.verbose > 0:
#             print("verbosity level = %d" % opts.verbose)
#         if opts.path:
#             print("path = %s" % opts.path)
#         if opts.content:
#             print("content = %s" % opts.content)

        # MAIN BODY #
        find(opts.path,opts.content,opts.suffix)
        
    except Exception, e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2


if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'tools.FindWithContent_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())