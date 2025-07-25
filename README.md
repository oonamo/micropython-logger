# Micropython-Logger
A logger for use with micropython

## Usage
```py
from log import Log
import math
import random
from time import sleep


debugger = log("debug.log", "Debugger")

TOLERANCE = 0.02
TARGET = 7.23

def broken_function():
    return random.uniform(0, 12)

def slow_function():
    sleep(5)
    return 5

def main():
    debugger.start()
    while True:
        val = broken_function()
        debugger.write(val)
        sleep(0.1)

        if val - TARGET < TOLERANCE:
            debugger.write(f"got target value {TARGET}")
            break

        intermediate_val = debugger.time(slow_function)

    debugger.stop()
```
