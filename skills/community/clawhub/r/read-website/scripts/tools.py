from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def read_website(
    url: str,
    pages: Optional[float] = 1.0,
    cookiesFile: Optional[str] = None
) -> Dict[str, Any]:
    """
    Fast, token-efficient web content extraction - ideal for reading documentation, analyzing content, and gathering information from websites. Converts to clean Markdown while preserving links and structure.
    
    Args:
        url: HTTP/HTTPS URL to fetch and convert to markdown
        pages: Maximum number of pages to crawl (default: 1)
        cookiesFile: Path to Netscape cookie file for authenticated pages
    
    Returns:
        
    """
    arguments = {
        "url": url,
        "pages": pages,
        "cookiesFile": cookiesFile
    }
    
    return call_api("1777316659753987", "read_website", arguments)

