import time

from log import Log

tempature_log = Log(
    "tempature_log.txt",
    "Tempature",
    permission=Log.APPEND,  # Appends to file
    write_interval=5,  # Writes buffer every 5 seconds
    show_time=True,  # Shows time in log
    show_name=True,  # Shows name in log
)


def read_sensor():
    return 65535


def complicated_function(a, b, c):
    time.sleep(5)
    return a + b * c


def start():
    tempature_log.start()

    sensor_val = read_sensor()

    tempature_log.write(f"sensor read {sensor_val}")

    # Times a functions execute time
    tempature_log.time(complicated_function, 5, 3, 5)

    # 5 seconds later the buffer is written to file
    time.sleep(5)

    # Force any unwritten data to be written
    tempature_log.stop(flush=True)

start()

# tempature_log.txt
# [Tempature] [X-XX-XXXX XX:X:XX]: sensor read 65535
# ========================================
# [Tempature]
# (complicated_function(5, 3, 5) -> 20)
# Start Time: [X-XX-XXXX XX:X:XX]:, End Time: [X-XX-XXXX XX:X:XX]:
# Time Elapsed: 5
# ========================================
