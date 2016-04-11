#!/usr/bin/env python

__version__ = '0.0.1'

from optparse import OptionParser
import subprocess
import sys
import re



# Global Variable
unit = ["B", "KB", "MB", "GB"]



def get_adj_order(value, order):

    time = 0
    while(value > 1024 and time < 4):
        value = value/1024
        time += 1

    return value, unit[time]



def print_meminfo(order=2, mem=None):

    if(mem == None):
        print "ERROR: Get memory information"
        sys.exit()

    if(order == -1):
        print 'Wired Memory:\t\t%15.3f %s' % get_adj_order(mem["Pages wired down"], unit[order])
        print 'Active Memory:\t\t%15.3f %s' % get_adj_order(mem["Pages active"], unit[order])
        print 'Inactive Memory:\t%15.3f %s' % get_adj_order(mem["Pages inactive"], unit[order])
        print 'Free Memory:\t\t%15.3f %s' % get_adj_order(mem["Pages free"], unit[order])
        print 'Real Mem Total (ps):\t%15.3f %s' % get_adj_order(mem["real"], unit[order])
    else:
        if(order < 2):
            print 'Wired Memory:\t\t%15d %s' % (int(mem["Pages wired down"]/1024**order), unit[order])
            print 'Active Memory:\t\t%15d %s' % (int(mem["Pages active"]/1024**order), unit[order])
            print 'Inactive Memory:\t%15d %s' % (int(mem["Pages inactive"]/1024**order), unit[order])
            print 'Free Memory:\t\t%15d %s' % (int(mem["Pages free"]/1024**order), unit[order])
            print 'Real Mem Total (ps):\t%15d %s' % (int(mem["real"]/1024**order), unit[order])
        else:
            print 'Wired Memory:\t\t%15.3f %s' % (mem["Pages wired down"]/1024**order, unit[order])
            print 'Active Memory:\t\t%15.3f %s' % (mem["Pages active"]/1024**order, unit[order])
            print 'Inactive Memory:\t%15.3f %s' % (mem["Pages inactive"]/1024**order, unit[order])
            print 'Free Memory:\t\t%15.3f %s' % (mem["Pages free"]/1024**order, unit[order])
            print 'Real Mem Total (ps):\t%15.3f %s' % (mem["real"]/1024**order, unit[order])



if __name__ == '__main__':

    # Parse options
    usage = "usage: %prog [options]"
    version = "Version: %prog-" + __version__
    opts = OptionParser(usage, version=version)

    # Add options
    opts.add_option('-a', '--adjust', action='store_const', const=-1, dest="order", help="Adjusted order", default=3)
    opts.add_option('-b', '--byte', action='store_const', const=0, dest="order", help="Byte order")
    opts.add_option('-k', '--kiro', action='store_const', const=1, dest="order", help="Kiro Byte order")
    opts.add_option('-m', '--mega', action='store_const', const=2, dest="order", help="Mega Byte order")
    opts.add_option('-g', '--giga', action='store_const', const=3, dest="order", help="Giga Byte order")

    # Get Option and Initialize
    opts, args = opts.parse_args()
    mem = {}

    # Get process info
    ps = subprocess.Popen(['ps', '-caxm', '-orss,comm'], stdout=subprocess.PIPE).communicate()[0]
    vm = subprocess.Popen(['vm_stat'], stdout=subprocess.PIPE).communicate()[0]

    # Iterate processes
    processLines = ps.split('\n')
    sep = re.compile('[\s]+')
    mem["real"] = 0.0 # B
    for row in range(1, len(processLines)):
        rowText = processLines[row].strip()
        rowElements = sep.split(rowText)
        try:
            rss = float(rowElements[0]) * 1024 # rowElements[0]'s unit is KB
        except:
            rss = 0 # ignore...
        mem["real"] += rss

    # Process vm_stat
    vmLines = vm.split('\n')
    sep = re.compile(':[\s]+')
    for row in range(1,len(vmLines)-2):
        rowText = vmLines[row].strip()
        rowElements = sep.split(rowText)
        mem[(rowElements[0])] = float(int(rowElements[1].strip('\.')) * 4096)

    # Print
    print_meminfo(opts.order, mem)
