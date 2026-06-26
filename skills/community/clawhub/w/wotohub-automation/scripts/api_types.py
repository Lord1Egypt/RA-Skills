#!/usr/bin/env python3
"""Type definitions for WotoHub external API.

Contract direction:
- semantic understanding should come from host-model-produced structured input
- scripts consume structured input and execute deterministically
"""

from typing import TypedDict, Literal, Optional
from enum import Enum


class TaskType(str, Enum):
    """Supported task types."""
    PRODUCT_ANALYSIS = "product_analysis"
    SEARCH = "search"
    RECOMMEND = "recommend"
    GENERATE_EMAIL = "generate_email"
    SEND_EMAIL = "send_email"
    MONITOR_REPLIES = "monitor_replies"


class APIRequest(TypedDict, total=False):
    """Unified API request format."""
    requestId: str
    action: Literal["task", "campaign"]
    type: str
    input: dict
    config: dict
    auth: dict


class APIResponse(TypedDict):
    """Unified API response format."""
    requestId: str
    status: Literal["success", "error"]
    result: Optional[dict]
    error: Optional[dict]
    metadata: dict
