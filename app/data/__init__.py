"""app.data"""
from ..services.location.csbs import CSBSLocationService
from ..services.location.jhu import JhuLocationService
from ..services.location.nyt import NYTLocationService
from ..config import get_settings
from ..caches import RedisCache, SimpleMemoryCache

SETTINGS = get_settings()

if SETTINGS.rediscloud_url:
    REDIS_URL = SETTINGS.rediscloud_url
else:
    REDIS_URL = SETTINGS.local_redis_url

if REDIS_URL:
    CACHE = RedisCache(REDIS_URL)
else:
    CACHE = SimpleMemoryCache()

# Mapping of services to data-sources.
DATA_SOURCES = {
    "jhu": JhuLocationService(CACHE),
    "csbs": CSBSLocationService(CACHE),
    "nyt": NYTLocationService(CACHE),
}


def data_source(source):
    """
    Retrieves the provided data-source service.

    :returns: The service.
    :rtype: LocationService
    """
    return DATA_SOURCES.get(source.lower())
