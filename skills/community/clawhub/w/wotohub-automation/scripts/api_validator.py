#!/usr/bin/env python3
"""Request validation for WotoHub API."""

from typing import Tuple
from api_types import TaskType


def validate_request(req: dict) -> Tuple[bool, str]:
    """Validate incoming API request structure."""
    if not req.get("requestId"):
        return False, "Missing requestId"
    if req.get("action") not in ("task", "campaign"):
        return False, "Invalid action"
    if not req.get("type"):
        return False, "Missing type"
    if not isinstance(req.get("input"), dict):
        return False, "Invalid input"
    return True, ""


def validate_task_input(task_type: str, input_data: dict) -> Tuple[bool, str]:
    """Validate task-specific input.

    Preferred contracts:
    - search: structured understanding (`modelAnalysis`/`hostAnalysis`/`understanding`) preferred for main execution
    - generate_email: `hostDrafts` preferred; compatibility aliases and brief+bloggers remain legacy-only
    """

    has_understanding = any(key in input_data for key in ("modelAnalysis", "hostAnalysis", "understanding"))
    has_host_drafts = any(key in input_data for key in ("hostDrafts", "emailModelDrafts", "hostEmailDrafts"))
    has_reply_analysis = any(key in input_data for key in ("replyModelAnalysis", "conversationAnalysis"))

    validators = {
        TaskType.PRODUCT_ANALYSIS.value: lambda x: "input" in x,
        TaskType.SEARCH.value: lambda x: "strategy" in x or has_understanding or "input" in x,
        TaskType.RECOMMEND.value: lambda x: "searchResults" in x and ("brief" in x or has_understanding),
        TaskType.GENERATE_EMAIL.value: lambda x: has_host_drafts or ("brief" in x and "bloggers" in x),
        TaskType.SEND_EMAIL.value: lambda x: "emails" in x or "drafts" in x or "generatedDrafts" in x or has_host_drafts,
        TaskType.MONITOR_REPLIES.value: lambda x: "campaignId" in x and has_reply_analysis,
    }
    validator = validators.get(task_type)
    if not validator:
        return False, f"Unknown task type: {task_type}"
    if not validator(input_data):
        return False, f"Invalid input for {task_type}"
    return True, ""


def validate_campaign_input(input_data: dict) -> Tuple[bool, str]:
    """Validate campaign cycle input."""
    if "campaignId" not in input_data:
        return False, "Missing campaignId"
    if "brief" not in input_data and "briefPath" not in input_data:
        return False, "Missing brief or briefPath"
    if "brief" in input_data and not isinstance(input_data["brief"], dict):
        return False, "brief must be dict"
    if "briefPath" in input_data and not isinstance(input_data["briefPath"], str):
        return False, "briefPath must be string"
    return True, ""
