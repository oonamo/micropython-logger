import time

from machine import Timer


def _convert_localtime_to_str(localtime: list[int]) -> str:
    return f"{localtime[1]}-{localtime[2]}-{localtime[0]} {localtime[3]}:{localtime[4]}:{localtime[5]}"


class Log:
    APPEND = "a"
    WRITE = "w"

    def __init__(
        self,
        file: str,
        name: str = "log",
        write_interval: int = 5,
        permission: str = "a",
        show_time: bool = True,
        show_name: bool = True,
    ):
        """Creates an instance of the Log object

        Args:
            file (str): Name of file to write too
            name (str): Name of the logger
            write_interval (int): How often the file is written to disk
            permission (str): Write permissions
            show_time (bool): Whether to show time in the file
            show_name (bool): Whether to show the name in the file
        """
        self._file = file
        self._name = name
        self._write_interval = write_interval
        self._show_time = show_time
        self._show_name = show_name

        self._running = False
        self._buffer = []
        self._timer = None

    def _get_time_str(self, time_secs: int = None) -> str:
        if not self._show_time:
            return ""

        time_str = ""
        if time_secs:
            time_str = _convert_localtime_to_str(time.localtime(time_secs))
        else:
            time_str = _convert_localtime_to_str(time.localtime())
        return "[" + time_str + "]:"

    def write(self, data) -> None:
        """Writes `data` to buffer

        Args:
            data (str): What is written to the buffer
        """

        message = ""
        if self._show_name:
            message += f"[{self._name}] "
        message += f"{self._get_time_str()} {str(data)}\n".strip(" ")
        self._buffer.append(message.strip(" "))

    def time(self, func, *args):
        """Times a function and logs it

        Args:
            func (function): Function to time
            *args: Paramaters to pass ot the function

        Returns:
            The functions output
        """
        start_time_s = time.time()
        time_start = self._get_time_str(start_time_s)
        val = func(*args)
        end_time_s = time.time()
        time_end = self._get_time_str(end_time_s)

        time_elapsed = end_time_s - start_time_s

        paramater_str = "("

        count = 0
        for arg in args:
            paramater_str += str(arg)
            count += 1

            if len(args) != count:
                paramater_str += ", "

        paramater_str += ")"

        if not self._show_time and not self._show_name:
            simple_message = f"({func.__name__}{paramater_str} -> {str(val)}) ({time_elapsed}s)\n"
            self._buffer.append(simple_message)
            return val

        message = "========================================\n"

        if self._show_name:
            message += f"[{self._name}]\n"

        message += f"({func.__name__}{paramater_str} -> {str(val)})\n"

        if self._show_time:
            message += (
                f"Start Time: {time_start}, End Time: {time_end}\n"
                + f"Time Elapsed: {time_elapsed}\n"
                + "========================================\n"
            )

        self._buffer.append(message.strip(" "))

        return val

    def _raw_write(self):
        try:
            with open(self._file, "a") as file:
                for line in self._buffer:
                    file.write(line)
                file.flush()
                self._buffer.clear()
        except Exception as e:
            print(f"Failed to write to file `{self._file}`: {str(e)}")

    def _flush_file(self) -> None:
        if len(self._buffer) != 0:
            self._raw_write()

    def _timer_wrapper(self, *args):
        self._flush_file()

    def start(self) -> None:
        """Starts the logger"""
        self._running = True

        if self._timer:
            self._timer.deinit()

        self._timer = Timer(
            mode=Timer.PERIODIC,
            period=self._write_interval * 1000,
            callback=self._timer_wrapper,
        )

    def stop(self, flush: bool = True) -> None:
        """Stops the logger from running

        Args:
            flush (bool): Optionally, force the logger to flush its buffer to the file
        """
        self._running = False
        if flush:
            self._raw_write()
