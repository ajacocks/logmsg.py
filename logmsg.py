#!/usr/bin/env python3

import argparse
import subprocess
from datetime import datetime

class Colorcodes(object):
    """
    Copyright © 2012 Martin Ueding <dev@martin-ueding.de>
    Additions © 2025 Alexander Jacocks <alexander@redhat.com>

    Provides ANSI terminal color codes which are gathered via the ``tput``
    utility. That way, they are portable. If there occurs any error with
    ``tput``, all codes are initialized as an empty string.
    The provides fields are listed below.
    Control:
    - bold
    - dim
    - rev
    - reset
    Colors:
    - brightwhite
    - brightcyan
    - brightmagenta
    - brightblue
    - brightyellow
    - brightgreen
    - brightred
    - grey
    - white
    - cyan
    - magenta
    - blue
    - green
    - orange
    - red
    - black
    :license: MIT
    """
    def __init__(self):
        try:
            self.bold = subprocess.check_output("tput bold".split()).decode()
            self.dim = subprocess.check_output("tput dim".split()).decode()
            self.rev = subprocess.check_output("tput rev".split()).decode()
            self.italic = subprocess.check_output("tput sitm".split()).decode()
            self.reset = subprocess.check_output("tput sgr0".split()).decode()

            self.brightwhite = subprocess.check_output("tput setaf 15".split()).decode()
            self.brightcyan = subprocess.check_output("tput setaf 14".split()).decode()
            self.brightmagenta = subprocess.check_output("tput setaf 13".split()).decode()
            self.brightblue = subprocess.check_output("tput setaf 12".split()).decode()
            self.brightyellow = subprocess.check_output("tput setaf 11".split()).decode()
            self.brightgreen = subprocess.check_output("tput setaf 10".split()).decode()
            self.brightred = subprocess.check_output("tput setaf 9".split()).decode()
            self.grey = subprocess.check_output("tput setaf 8".split()).decode()
            self.white = subprocess.check_output("tput setaf 7".split()).decode()
            self.cyan = subprocess.check_output("tput setaf 6".split()).decode()
            self.magenta = subprocess.check_output("tput setaf 5".split()).decode()
            self.blue = subprocess.check_output("tput setaf 4".split()).decode()
            self.green = subprocess.check_output("tput setaf 2".split()).decode()
            self.orange = subprocess.check_output("tput setaf 3".split()).decode()
            self.red = subprocess.check_output("tput setaf 1".split()).decode()
            self.black = subprocess.check_output("tput setaf 0".split()).decode()
        except subprocess.CalledProcessError as e:
            self.bold = ""
            self.dim = ""
            self.rev = ""
            self.italic = ""
            self.reset = ""

            self.brightwhite = ""
            self.brightcyan = ""
            self.brightmagenta = ""
            self.brightblue = ""
            self.brightyellow = ""
            self.brightgreen = ""
            self.brightred = ""
            self.grey = ""
            self.white = ""
            self.cyan = ""
            self.magenta = ""
            self.blue = ""
            self.green = ""
            self.orange = ""
            self.red = ""
            self.black = ""

def log(lines, logfile):
    output = '\n'.join(lines)
    if logfile:
        with open(logfile, 'a') as f:
            print(output, file=f)
    else:
        print(output)

def log_start(message, logfile):
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    log(['_' * 79, f"{timestamp}: {message} started."], logfile)

def log_stop(message, logfile):
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    log([f"{timestamp}: {message} ended."], logfile)

def main():
    colors = Colorcodes()
    epilog = f"""
{colors.bold}{colors.brightblue}examples:
  {colors.brightred}# create a beginning log statement for a system update
  {colors.magenta}%(prog)s {colors.green}-a {colors.orange}start {colors.green}-m {colors.orange}"system update"
  {colors.brightred}# execute a system update, logging to the file update.log
  {colors.magenta}%(prog)s {colors.green}-c {colors.orange}"yum update -y" {colors.green}-f {colors.orange}update.log {colors.green}-m {colors.orange}"system update"
    """

    parser = argparse.ArgumentParser(
        description=f"{colors.cyan}{colors.bold}Log start/stop messages with optional command execution.{colors.reset}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', '--action', choices=['start', 'begin', 'stop', 'end'],
                       help=f"{colors.cyan}Action to log: {colors.orange}start{colors.cyan}/{colors.orange}begin {colors.cyan}or {colors.orange}stop{colors.cyan}/{colors.orange}end{colors.reset}")
    group.add_argument('-c', '--command',
                       help=f"{colors.cyan}Command to execute between start and stop log entries{colors.reset}")
    parser.add_argument('-f', '--file',
                        help=f"{colors.cyan}Log file to append to {colors.orange}(default: stdout){colors.reset}")
    parser.add_argument('-m', '--message', required=True,
                        help=f"{colors.cyan}Message to include in the log entry{colors.reset}")

    args = parser.parse_args()

    logfile = args.file
    message = args.message

    if args.command is not None:
        log_start(message, logfile)
        out = open(logfile, 'a') if logfile else None
        try:
            result = subprocess.run(args.command, shell=True, stdout=out, stderr=out)
        finally:
            if out:
                out.close()
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        log([f"{timestamp}: {message} exited with return code {result.returncode}."], logfile)
    elif args.action in ('start', 'begin'):
        log_start(message, logfile)
    else:
        log_stop(message, logfile)


if __name__ == '__main__':
    main()
