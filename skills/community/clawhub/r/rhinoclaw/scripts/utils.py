#!/usr/bin/env python3
"""
Shared utility functions for RhinoClaw Clawdbot scripts.
"""

from typing import List, Optional


def parse_coords(s: str) -> Optional[List[float]]:
    """Parse 'x,y,z' string to [x, y, z].
    
    Args:
        s: Comma-separated coordinate string, e.g. '1.0,2.5,3.0'
    
    Returns:
        List of floats, or None if input is falsy or invalid.
    """
    if not s:
        return None
    try:
        return [float(x.strip()) for x in s.split(',')]
    except (ValueError, AttributeError):
        return None


def parse_color(s: str) -> Optional[List[int]]:
    """Parse 'r,g,b' string to [r, g, b].
    
    Args:
        s: Comma-separated color string, e.g. '255,128,0'
    
    Returns:
        List of ints (0-255), or None if input is falsy or invalid.
    """
    if not s:
        return None
    try:
        return [int(x.strip()) for x in s.split(',')]
    except (ValueError, AttributeError):
        return None


def parse_ids(s: str) -> List[str]:
    """Parse comma-separated IDs string to list of strings.
    
    Args:
        s: Comma-separated IDs, e.g. 'abc-123,def-456'
    
    Returns:
        List of stripped ID strings. Empty list if input is falsy.
    """
    if not s:
        return []
    return [x.strip() for x in s.split(',') if x.strip()]


def format_point(pt: List[float], decimals: int = 2) -> str:
    """Format a point for display.
    
    Args:
        pt: List of coordinates [x, y, z]
        decimals: Number of decimal places
    
    Returns:
        Formatted string like '(1.00, 2.50, 3.00)'
    """
    formatted = ', '.join(f'{v:.{decimals}f}' for v in pt)
    return f'({formatted})'


def format_result(result: dict, verbose: bool = False) -> str:
    """Format a command result dict for CLI output.
    
    Args:
        result: Result dictionary from RhinoClient
        verbose: If True, include full JSON output
    
    Returns:
        Formatted string for terminal display.
    """
    if not result:
        return "No result"
    
    status = result.get('status', 'unknown')
    
    if verbose:
        import json
        return json.dumps(result, indent=2)
    
    lines = []
    
    if status == 'error':
        msg = result.get('message', 'Unknown error')
        lines.append(f"ERROR: {msg}")
    elif status == 'success':
        lines.append("OK")
        inner = result.get('result', {})
        if isinstance(inner, dict):
            # Show key fields
            for key in ('id', 'object_id', 'name', 'count', 'objects_created'):
                if key in inner:
                    lines.append(f"  {key}: {inner[key]}")
        elif isinstance(inner, list):
            lines.append(f"  ({len(inner)} items)")
    else:
        lines.append(f"Status: {status}")
        msg = result.get('message')
        if msg:
            lines.append(f"  {msg}")
    
    return '\n'.join(lines)
