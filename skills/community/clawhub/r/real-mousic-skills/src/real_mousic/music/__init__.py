"""歌曲下载模块 - 支持歌曲海网站搜索和下载"""

from .search import search_songs, get_download_links, SearchResult

__all__ = ["search_songs", "get_download_links", "SearchResult"]
