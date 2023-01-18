#!/usr/bin/env python3
"""
Web page caching
"""

from datetime import timedelta
from typing import Callable
import redis
import requests
from functools import wraps


cache = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """Counts the number of requests"""
    @wraps(method)
    def wrapper(*args, **kwargs):
        cache.incr("count:{}".format(args[0]), 1)
        return method(*args, **kwargs)
    return wrapper


@count_requests
def get_page(url: str) -> str:
    """Fetch a web page and cache it"""
    if not cache.exists(url):
        res = requests.get(url)
        cache.setex(url, timedelta(seconds=10), res.content)
        return res.content
    return cache.get(url)
