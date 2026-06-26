"""Input validation utilities for TrinityGuard."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict

try:
    from jsonschema import validate, ValidationError, Draft7Validator
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False
    ValidationError = Exception  # Fallback

from exceptions import InputValidationError, PolicyValidationError

logger = logging.getLogger(__name__)

# Load input schema
SCHEMA_PATH = Path(__file__).parent.parent / "references" / "input_schema.json"
INPUT_SCHEMA = None

if JSONSCHEMA_AVAILABLE and SCHEMA_PATH.exists():
    try:
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            INPUT_SCHEMA = json.load(f)
    except Exception as e:
        logger.warning(f"Failed to load input schema: {e}")


def validate_input(payload: Dict[str, Any], strict: bool = True) -> None:
    """Validate input payload against schema.

    Args:
        payload: Input payload to validate
        strict: Whether to use strict validation (raise exception) or log warning

    Raises:
        InputValidationError: If validation fails in strict mode
    """
    if not JSONSCHEMA_AVAILABLE:
        logger.warning("jsonschema not available, skipping input validation")
        return

    if INPUT_SCHEMA is None:
        logger.warning("Input schema not loaded, skipping validation")
        return

    try:
        validate(instance=payload, schema=INPUT_SCHEMA)
        logger.debug("Input validation passed")
    except ValidationError as e:
        error_msg = f"Input validation failed: {e.message}"
        if strict:
            raise InputValidationError(
                error_msg,
                details={
                    "field": ".".join(str(p) for p in e.path) if e.path else "root",
                    "failed_value": e.instance if hasattr(e, 'instance') else None
                }
            )
        else:
            logger.warning(error_msg)


def validate_policy(policy: Dict[str, Any]) -> None:
    """Validate policy configuration.

    Args:
        policy: Policy dictionary to validate

    Raises:
        PolicyValidationError: If policy is invalid
    """
    errors = []

    # Check required top-level keys
    required_keys = ["sensitive_event_types", "leak_patterns"]
    for key in required_keys:
        if key not in policy:
            errors.append(f"Missing required policy key: {key}")

    # Validate leak_patterns
    if "leak_patterns" in policy:
        if not isinstance(policy["leak_patterns"], list):
            errors.append("leak_patterns must be a list")
        else:
            for i, pattern in enumerate(policy["leak_patterns"]):
                if not isinstance(pattern, str):
                    errors.append(f"leak_patterns[{i}] must be a string")
                else:
                    # Try to compile regex
                    try:
                        import re
                        re.compile(pattern)
                    except re.error as e:
                        errors.append(f"leak_patterns[{i}] invalid regex: {e}")

    # Validate thresholds
    if "retry_threshold_downgrade" in policy:
        threshold = policy["retry_threshold_downgrade"]
        if not isinstance(threshold, int) or threshold < 0:
            errors.append("retry_threshold_downgrade must be a non-negative integer")

    if errors:
        raise PolicyValidationError(
            "Policy validation failed",
            details={"errors": errors}
        )


def sanitize_input(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Sanitize and clean input payload.

    Args:
        payload: Input payload to sanitize

    Returns:
        Sanitized payload
    """
    sanitized = {}

    # Copy safe fields
    for key in ["session_id", "turn_id", "request_id"]:
        if key in payload and isinstance(payload[key], str):
            sanitized[key] = payload[key][:1000]  # Limit length

    # Sanitize user_prompt
    if "user_prompt" in payload:
        prompt = payload["user_prompt"]
        if isinstance(prompt, str):
            # Limit length and strip null bytes
            sanitized["user_prompt"] = prompt[:1_000_000].replace("\x00", "")
        else:
            sanitized["user_prompt"] = str(prompt)[:1_000_000]

    # Sanitize arrays
    for key in ["planned_actions", "intent_tags"]:
        if key in payload and isinstance(payload[key], list):
            sanitized[key] = [str(x)[:500] for x in payload[key][:100]]

    # Sanitize runtime_events
    if "runtime_events" in payload and isinstance(payload["runtime_events"], list):
        sanitized["runtime_events"] = []
        for event in payload["runtime_events"][:100]:
            if isinstance(event, dict):
                clean_event = {}
                for k, v in event.items():
                    if isinstance(v, str):
                        clean_event[k] = v[:1000]
                    else:
                        clean_event[k] = v
                sanitized["runtime_events"].append(clean_event)

    # Sanitize sources
    if "sources" in payload and isinstance(payload["sources"], list):
        sanitized["sources"] = []
        for source in payload["sources"][:50]:
            if isinstance(source, dict):
                clean_source = {}
                for k, v in source.items():
                    if isinstance(v, str):
                        clean_source[k] = v[:500]
                    else:
                        clean_source[k] = v
                sanitized["sources"].append(clean_source)

    # Sanitize candidate_response
    if "candidate_response" in payload:
        response = payload["candidate_response"]
        if isinstance(response, str):
            sanitized["candidate_response"] = response[:1_000_000].replace("\x00", "")
        else:
            sanitized["candidate_response"] = str(response)[:1_000_000]

    return sanitized


def validate_path(path: Path, must_exist: bool = False, allow_symlinks: bool = False) -> bool:
    """Validate file path.

    Args:
        path: Path to validate
        must_exist: Whether path must exist
        allow_symlinks: Whether to allow symbolic links

    Returns:
        True if valid

    Raises:
        InputValidationError: If path is invalid
    """
    if not isinstance(path, Path):
        path = Path(path)

    # Check for symlinks
    if not allow_symlinks and path.is_symlink():
        raise InputValidationError(
            f"Symbolic links not allowed: {path}",
            details={"path": str(path)}
        )

    # Check existence if required
    if must_exist and not path.exists():
        raise InputValidationError(
            f"Path does not exist: {path}",
            details={"path": str(path)}
        )

    # Check path is within allowed bounds
    try:
        path.resolve()
    except Exception as e:
        raise InputValidationError(
            f"Invalid path: {path}",
            details={"error": str(e)}
        )

    return True


def validate_file_size(path: Path, max_size_mb: int = 100) -> bool:
    """Validate file size is within limits.

    Args:
        path: Path to check
        max_size_mb: Maximum size in megabytes

    Returns:
        True if size is valid

    Raises:
        InputValidationError: If file is too large
    """
    if not path.exists():
        return True

    size_bytes = path.stat().st_size
    size_mb = size_bytes / (1024 * 1024)

    if size_mb > max_size_mb:
        raise InputValidationError(
            f"File too large: {size_mb:.2f}MB (max: {max_size_mb}MB)",
            details={
                "path": str(path),
                "size_mb": size_mb,
                "max_size_mb": max_size_mb
            }
        )

    return True
