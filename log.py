import asyncio

class Log:
    def __init__(self, file: str, name="log", write_time: int=100):
        self._file = file
        self._name = name
        self._buffer = []
        self._write_time = write_time

    async def write_msg_async():
        pass
