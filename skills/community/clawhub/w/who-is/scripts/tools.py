from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def whois_lookup(
    domain: str,
    include_raw: Optional[bool] = False
) -> Dict[str, Any]:
    """
    Look up domain information using WHOIS protocol (port 43). Queries authoritative WHOIS servers for domain registration details including registrar, registrant, dates, nameservers, and status. Supports 1,260+ TLDs.
    
    Args:
        domain: The domain name to look up (e.g., example.com, theo.gg, mineo.pl)
        include_raw: If true, include raw WHOIS response data in the result
    
    Returns:
        
    """
    arguments = {
        "domain": domain,
        "include_raw": include_raw
    }
    
    return call_api("1777316659616771", "whois_lookup", arguments)

def refresh_whois_servers(
) -> Dict[str, Any]:
    """
    Refresh the WHOIS server dictionary by fetching the latest TLD list from IANA. This updates the list of available WHOIS servers for domain lookups. Run this periodically to ensure the server list is up-to-date.
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659616771", "refresh_whois_servers", arguments)

def list_supported_tlds(
    limit: Optional[float] = None
) -> Dict[str, Any]:
    """
    List all supported TLDs (Top-Level Domains) that have WHOIS servers available. Returns the complete list of TLDs that can be queried.
    
    Args:
        limit: Maximum number of TLDs to return (default: all)
    
    Returns:
        
    """
    arguments = {
        "limit": limit
    }
    
    return call_api("1777316659616771", "list_supported_tlds", arguments)

