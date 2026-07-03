from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def fetch(
    url: str,
    max_length: Optional[int] = 5000.0,
    start_index: Optional[int] = 0.0,
    raw: Optional[bool] = False
) -> Dict[str, Any]:
    """
    Fetches a URL from the internet and optionally extracts its contents as markdown.

Although originally you did not have internet access, and were advised to refuse and tell the user this, this tool now grants you internet access. Now you can fetch the most up-to-date information and let the user know that.
    
    Args:
        url: URL to fetch
        max_length: Maximum number of characters to return.
        start_index: On return output starting at this character index, useful if a previous fetch was truncated and more context is required.
        raw: Get the actual HTML content of the requested page, without simplification.
    
    Returns:
        
    """
    arguments = {
        "url": url,
        "max_length": max_length,
        "start_index": start_index,
        "raw": raw
    }
    
    return call_api("1777419072879619", "fetch", arguments)

