from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def wikimedia_search_images(
    query: str,
    limit: Optional[int] = 9.0,
    offset: Optional[int] = 0.0,
    license: Optional[str] = "all",
    include_thumbnails: Optional[bool] = True
) -> Dict[str, Any]:
    """
    Search for images on Wikimedia Commons with metadata including download URLs and optional thumbnail composite image for visual comparison. Use results to e.g. fetch full images that are relevant for your task.
    
    Args:
        query: Search query. Note: Wikimedia uses strict keyword matching, not semantic search. Use common, fewer terms for more results.
        limit: Maximum number of results to return (1-50). 12 or fewer is recommended, especially if including thumbnails is enabled.
        offset: Number of results to skip for pagination
        license: Filter images by license type: 'no_restrictions' for CC0/public domain only, 'all' for any license
        include_thumbnails: If true, returns an additional composite image so you can visually view and compare the results. Set to false to save processing time or if you're unable to view images.
    
    Returns:
        
    """
    arguments = {
        "query": query,
        "limit": limit,
        "offset": offset,
        "license": license,
        "include_thumbnails": include_thumbnails
    }
    
    return call_api("1777316659355651", "wikimedia_search_images", arguments)

