from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def generate_speech(
    merge_output: bool,
    items: null
) -> Dict[str, Any]:
    """
    Generate speech audio from text using Microsoft Edge TTS. Supports multi-role conversations and audio merging.
    
    Args:
        merge_output: If true, merges all speech items into a single MP3 file. If false, returns separate files.
        items: List of speech segments to generate.
    
    Returns:
        
    """
    arguments = {
        "merge_output": merge_output,
        "items": items
    }
    
    return call_api("1777316659830787", "generate_speech", arguments)

