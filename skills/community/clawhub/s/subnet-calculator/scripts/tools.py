from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def calculate_subnet(
    network_base: str,
    hosts_needed: int,
    return_format: Optional[str] = "detailed"
) -> Dict[str, Any]:
    """
    Calculate subnet details given a base IP and required hosts.
    
    Args:
        network_base: null
        hosts_needed: null
        return_format: null
    
    Returns:
        null
    """
    arguments = {
        "network_base": network_base,
        "hosts_needed": hosts_needed,
        "return_format": return_format
    }
    
    return call_api("1777419063177219", "calculate_subnet", arguments)

def calculate_wildcard_mask(
    ip_address: str,
    cidr_prefix: int,
    include_ospf_command: Optional[bool] = True
) -> Dict[str, Any]:
    """
    Generate OSPF wildcard mask details for a subnet.
    
    Args:
        ip_address: null
        cidr_prefix: null
        include_ospf_command: null
    
    Returns:
        null
    """
    arguments = {
        "ip_address": ip_address,
        "cidr_prefix": cidr_prefix,
        "include_ospf_command": include_ospf_command
    }
    
    return call_api("1777419063177219", "calculate_wildcard_mask", arguments)

def validate_ip_in_subnet(
    ip_address: str,
    network: str,
    return_gateway: Optional[bool] = True
) -> Dict[str, Any]:
    """
    Validate that an IP address belongs to a subnet and provide context.
    
    Args:
        ip_address: null
        network: null
        return_gateway: null
    
    Returns:
        null
    """
    arguments = {
        "ip_address": ip_address,
        "network": network,
        "return_gateway": return_gateway
    }
    
    return call_api("1777419063177219", "validate_ip_in_subnet", arguments)

def calculate_subnet_from_mask(
    ip_address: str,
    subnet_mask: str
) -> Dict[str, Any]:
    """
    Calculate network information from an IP address and subnet mask.
    
    Args:
        ip_address: null
        subnet_mask: null
    
    Returns:
        null
    """
    arguments = {
        "ip_address": ip_address,
        "subnet_mask": subnet_mask
    }
    
    return call_api("1777419063177219", "calculate_subnet_from_mask", arguments)

def get_nth_usable_ip(
    network: str,
    position: int
) -> Dict[str, Any]:
    """
    Return the Nth usable IP address in a subnet.
    
    Args:
        network: null
        position: null
    
    Returns:
        null
    """
    arguments = {
        "network": network,
        "position": position
    }
    
    return call_api("1777419063177219", "get_nth_usable_ip", arguments)

