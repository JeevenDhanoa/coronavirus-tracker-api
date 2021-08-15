"""app.caches.py"""
import functools
import logging
import aiocache

from abc import ABC, abstractmethod

LOGGER = logging.getLogger(name="app.caches")

class Caches(ABC):

    @property
    def cache(self):
        raise NotImplementedError

    @abstractmethod
    def get_cache(self):
      raise NotImplementedError

    @abstractmethod
    async def check_cache(self, data_id):
        raise NotImplementedError

    @abstractmethod
    async def load_cache(self, data_id, data):
        raise NotImplementedError

class RedisCache(Caches):
    cache = None

    def init(self, redis_url):
        self.cache = aiocache.RedisCache(
            endpoint=redis_url.host,
            port=redis_url.port,
            password=redis_url.password,
            create_connection_timeout=5,
        )
    
    @functools.lru_cache()
    def get_cache(self):
        return self.cache
    
    async def check_cache(self, data_id):
        cache = self.get_cache()
        result = await cache.get(data_id, None)
        LOGGER.info(f"{data_id} cache pulled")
        await cache.close()
        return result
    
    async def load_cache(self, data_id, data):
        cache = self.get_cache()
        await cache.set(data_id, data, ttl=3600)
        LOGGER.info(f"{data_id} cache loaded")
        await cache.close()

class SimpleMemoryCache(Caches):
    cache = None

    def __init__(self):
        self.cache = aiocache.SimpleMemoryCache()

    @functools.lru_cache()
    def get_cache(self):
        return self.cache

    async def check_cache(self, data_id):
        cache = self.get_cache()
        result = await cache.get(data_id, None)
        LOGGER.info(f"{data_id} cache pulled")
        await cache.close()
        return result

    async def load_cache(self, data_id, data):
        cache = self.get_cache()
        await cache.set(data_id, data, ttl=3600)
        LOGGER.info(f"{data_id} cache loaded")
        await cache.close()
