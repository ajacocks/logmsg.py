    $ logmsg.py -h
    usage: logmsg.py [-h] (-a {start,begin,stop,end} | -c COMMAND) [-f FILE] -m MESSAGE
    
    Log start/stop messages with optional command execution.
    
    options:
      -h, --help            show this help message and exit
      -a {start,begin,stop,end}, --action {start,begin,stop,end}
                            Action to log: start/begin or
                            stop/end
      -c COMMAND, --command COMMAND
                            Command to execute between start and stop log
                            entries
      -f FILE, --file FILE  Log file to append to (default: stdout)
      -m MESSAGE, --message MESSAGE
                            Message to include in the log entry
    
    examples:
      # create a beginning log statement for a system update
      logmsg.py -a start -m "system update"
      # execute a system update, logging to the file update.log
      logmsg.py -c "yum update -y" -f update.log -m "system update"
