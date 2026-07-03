from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_rfc(
    number: str,
    format: Optional[str] = "full"
) -> Dict[str, Any]:
    """
    Fetch an RFC document by its number
    
    Args:
        number: RFC number (e.g. "2616")
        format: Output format (full, metadata, sections)
    
    Returns:
        
    """
    arguments = {
        "number": number,
        "format": format
    }
    
    return call_api("1777316659312643", "get_rfc", arguments)

def search_rfcs(
    query: str,
    limit: Optional[float] = 10.0
) -> Dict[str, Any]:
    """
    Search for RFCs by keyword
    
    Args:
        query: Search keyword or phrase
        limit: Maximum number of results to return
    
    Returns:
        
    """
    arguments = {
        "query": query,
        "limit": limit
    }
    
    return call_api("1777316659312643", "search_rfcs", arguments)

def get_rfc_section(
    number: str,
    section: str
) -> Dict[str, Any]:
    """
    Get a specific section from an RFC
    
    Args:
        number: RFC number (e.g. "2616")
        section: Section title or number to retrieve
    
    Returns:
        
    """
    arguments = {
        "number": number,
        "section": section
    }
    
    return call_api("1777316659312643", "get_rfc_section", arguments)

