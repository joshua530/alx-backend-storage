#!/usr/bin/env python3
"""
Exercise Module

Contains simple cache implementation
"""

from functools import wraps
from typing import Callable, Union
import redis
import uuid


def count_calls(method: Callable) -> Callable:
    """Decorator for counting number of calls"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(method.__qualname__, 1)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator for recording method call history"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        inp = "{}:inputs".format(method.__qualname__)
        out = "{}:outputs".format(method.__qualname__)
        self._redis.rpush(inp, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(out, output)
        return output
    return wrapper


def replay(method: Callable) -> None:
    """Replays the history of a method call"""
    redis_obj = redis.Redis()
    fn_name = method.__qualname__
    inputs = redis_obj.lrange("{}:inputs".format(fn_name), 0, -1)
    outputs = redis_obj.lrange("{}:outputs".format(fn_name), 0, -1)

    try:
        count = redis_obj.get(fn_name).decode("utf-8")
    except Exception:
        count = 0

    print("{} was called {} times:".format(fn_name, count))
    for key, value in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(
            fn_name, key.decode("utf-8"), value.decode("utf-8")))


class Cache:
    """
    Cache class
    """

    def __init__(self) -> None:
        """Init method"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, int, float, bytes]) -> str:
        """Stores item in redis db"""
        rand = str(uuid.uuid4())
        self._redis.set(rand, data)
        return rand

    def get(self, key: str, fn: Callable = None) -> Union[
        str, int, float, bytes
    ]:
        """Fetches str, int, float or bytes from redis"""
        if not fn:
            value = self._redis.get(key)
            return value
        return fn(self._redis.get(key))

    def get_str(self, key: str) -> str:
        """Fetches string from redis"""
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """Fetches int from redis"""
        return self.get(key, int)
