"""棋谱下载源集合"""

from .base import (
    BaseSourceFetcher,
    FetchResult,
    get_fetcher_for_url,
    get_fetcher_by_name,
    list_fetchers,
    register_fetcher,
)

# 自动导入所有源
from . import fetch_ogs
from . import fetch_fox
from . import fetch_101
from . import fetch_yike
from . import fetch_yuanluobo
from . import fetch_1919
from . import fetch_izis
from . import fetch_yike_shaoer
from . import fetch_eweiqi
from . import fetch_txwq
from . import fetch_xinboduiyi
from . import fetch_dzqzd

__all__ = [
    'BaseSourceFetcher',
    'FetchResult',
    'get_fetcher_for_url',
    'get_fetcher_by_name',
    'list_fetchers',
    'register_fetcher',
]
