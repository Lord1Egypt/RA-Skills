from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def read_pdf(
    path: str
) -> Dict[str, Any]:
    """
    Read and extract text content from a PDF file. Returns the full text content and metadata.
    
    Args:
        path: Absolute or relative path to the PDF file, or a URL (http:// or https://)
    
    Returns:
        
    """
    arguments = {
        "path": path
    }
    
    return call_api("1777316659716099", "read_pdf", arguments)

def read_pdf_page(
    path: str,
    page: Optional[float] = None,
    startPage: Optional[float] = None,
    endPage: Optional[float] = None
) -> Dict[str, Any]:
    """
    Read a specific page or range of pages from a PDF file.
    
    Args:
        path: Absolute or relative path to the PDF file, or a URL (http:// or https://)
        page: Page number to read (1-indexed)
        startPage: Start page for range (1-indexed)
        endPage: End page for range (1-indexed)
    
    Returns:
        
    """
    arguments = {
        "path": path,
        "page": page,
        "startPage": startPage,
        "endPage": endPage
    }
    
    return call_api("1777316659716099", "read_pdf_page", arguments)

def get_pdf_metadata(
    path: str
) -> Dict[str, Any]:
    """
    Get metadata information from a PDF file without reading all content.
    
    Args:
        path: Absolute or relative path to the PDF file, or a URL (http:// or https://)
    
    Returns:
        
    """
    arguments = {
        "path": path
    }
    
    return call_api("1777316659716099", "get_pdf_metadata", arguments)

def search_pdf(
    path: str,
    query: str,
    caseSensitive: Optional[bool] = False
) -> Dict[str, Any]:
    """
    Search for specific text within a PDF file.
    
    Args:
        path: Absolute or relative path to the PDF file, or a URL (http:// or https://)
        query: Text to search for
        caseSensitive: Whether search should be case-sensitive
    
    Returns:
        
    """
    arguments = {
        "path": path,
        "query": query,
        "caseSensitive": caseSensitive
    }
    
    return call_api("1777316659716099", "search_pdf", arguments)

