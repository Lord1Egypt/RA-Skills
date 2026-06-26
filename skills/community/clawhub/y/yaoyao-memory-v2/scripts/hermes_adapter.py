"""
Hermes Bridge Adapter — Integration Layer for yaoyao-memory

Bridges hermes-bridge modules into yaoyao-memory:
- Error classification and failover
- Smart model routing
- Structured summarization
- Usage insights
- Token optimization

Usage:
    from hermes_adapter import HermesAdapter

    adapter = HermesAdapter()
    result = adapter.classify_error(429, "rate limit")
    route = adapter.route_query("Hello world")
    summary = adapter.summarize_conversation(messages)
"""

import sys
import os
from pathlib import Path

# Add hermes-bridge to path
HERMES_BRIDGE_PATH = Path(__file__).parent.parent.parent / "hermes-bridge"
if HERMES_BRIDGE_PATH.exists():
    sys.path.insert(0, str(HERMES_BRIDGE_PATH))

from typing import Any, Dict, List, Optional, Tuple

# ============================================================================
# Error Classification & Failover
# ============================================================================

def classify_api_error(
    status_code: int,
    error_message: str,
    provider: str = ""
) -> Dict[str, Any]:
    """
    Classify API error and determine recovery action.

    Args:
        status_code: HTTP status code
        error_message: Error message
        provider: API provider name

    Returns:
        Dict with reason, retryable, should_compress, should_rotate_credential
    """
    try:
        from error_classifier import classify_error
        result = classify_error(status_code, error_message, provider)
        return {
            "reason": result.reason.value,
            "retryable": result.retryable,
            "should_compress": result.should_compress,
            "should_rotate_credential": result.should_rotate_credential,
            "action": _determine_action(result),
        }
    except ImportError:
        return _fallback_classify(status_code, error_message)


def _determine_action(result) -> str:
    """Determine recovery action from error class."""
    if result.should_rotate_credential:
        return "rotate_credential"
    elif result.should_compress:
        return "compress_context"
    elif result.retryable:
        return "retry_with_backoff"
    else:
        return "abort"


def _fallback_classify(status_code: int, message: str) -> Dict[str, Any]:
    """Fallback classification when hermes-bridge not available."""
    if status_code == 429:
        return {"reason": "rate_limit", "retryable": True, "action": "retry_with_backoff"}
    elif status_code == 401:
        return {"reason": "auth", "retryable": False, "action": "rotate_credential"}
    elif status_code == 500:
        return {"reason": "server_error", "retryable": True, "action": "retry"}
    return {"reason": "unknown", "retryable": False, "action": "abort"}


# ============================================================================
# Smart Model Routing
# ============================================================================

def route_query(
    query: str,
    current_model: str = "gpt-4",
    current_provider: str = "openai",
) -> Dict[str, Any]:
    """
    Determine if query should use cheap or strong model.

    Args:
        query: User query text
        current_model: Current model in use
        current_provider: Current provider

    Returns:
        Dict with use_cheap, model, provider, reason
    """
    try:
        from smart_routing import should_use_cheap_model, RoutingConfig

        config = RoutingConfig(
            enabled=True,
            cheap_model=os.getenv("CHEAP_MODEL", "gpt-3.5-turbo"),
            cheap_provider=os.getenv("CHEAP_PROVIDER", "openai"),
        )

        is_simple, reason = should_use_cheap_model(query, config)
        if is_simple:
            return {
                "use_cheap": True,
                "model": config.cheap_model,
                "provider": config.cheap_provider,
                "reason": reason,
            }
        return {
            "use_cheap": False,
            "model": current_model,
            "provider": current_provider,
            "reason": reason,
        }
    except ImportError:
        return {
            "use_cheap": False,
            "model": current_model,
            "provider": current_provider,
            "reason": "hermes-bridge not available",
        }


# ============================================================================
# Sensitive Information Redaction
# ============================================================================

def redact_sensitive_data(text: str) -> str:
    """
    Redact sensitive information from text.

    Args:
        text: Text to redact

    Returns:
        Redacted text
    """
    try:
        from redact import redact_sensitive_text
        return redact_sensitive_text(text)
    except ImportError:
        return text


def redact_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Redact sensitive fields from dict.

    Args:
        data: Dict to redact

    Returns:
        Redacted dict
    """
    try:
        from redact import redact_dict as _redact_dict
        return _redact_dict(data)
    except ImportError:
        return data


# ============================================================================
# Rate Limit Tracking
# ============================================================================

def parse_rate_limit_headers(
    headers: Dict[str, str],
    provider: str = "openai"
) -> Optional[Dict[str, Any]]:
    """
    Parse rate limit headers.

    Args:
        headers: HTTP response headers
        provider: Provider name

    Returns:
        Rate limit state dict or None
    """
    try:
        from rate_limit import parse_headers, format_compact

        state = parse_headers(headers, provider)
        if state:
            return {
                "requests_min_remaining": state.requests_min.remaining,
                "requests_min_limit": state.requests_min.limit,
                "tokens_min_remaining": state.tokens_min.remaining,
                "tokens_min_limit": state.tokens_min.limit,
                "reset_seconds": state.requests_min.reset_seconds,
                "compact": format_compact(state),
            }
        return None
    except ImportError:
        return None


# ============================================================================
# Context Compression (Structured Summarization)
# ============================================================================

def compress_conversation(
    messages: List[Dict[str, Any]],
    system_prompt: Optional[str] = None,
    context_length: int = 128000,
    threshold_percent: float = 0.75,
) -> Dict[str, Any]:
    """
    Compress conversation with structured summarization.

    Args:
        messages: Conversation messages
        system_prompt: Optional system prompt
        context_length: Context window size
        threshold_percent: Compression threshold

    Returns:
        Compression result with summary and compressed messages
    """
    try:
        from compressor import compress_context, estimate_compression_savings

        # Check if compression needed
        estimate = estimate_compression_savings(
            messages,
            context_length=context_length,
            threshold_percent=threshold_percent,
        )

        if not estimate.get("exceeds_threshold"):
            return {
                "needed": False,
                "original_tokens": estimate.get("total_tokens", 0),
                "threshold": estimate.get("threshold", 0),
                "message": "Under threshold, no compression needed",
            }

        # Compress
        result = compress_context(messages, system_prompt)

        return {
            "needed": True,
            "original_count": result.original_count,
            "compressed_count": result.compressed_count,
            "pruned_count": result.pruned_count,
            "tokens_saved": result.tokens_saved,
            "summary": result.summary,
            "preserved_head": result.preserved_head,
            "preserved_tail": result.preserved_tail,
        }
    except ImportError as e:
        return {
            "needed": False,
            "error": f"hermes-bridge not available: {e}",
        }


# ============================================================================
# Usage Insights
# ============================================================================

def generate_insights_report(
    sessions: List[Dict[str, Any]],
    days: int = 30
) -> Dict[str, Any]:
    """
    Generate usage insights from sessions.

    Args:
        sessions: List of session dicts
        days: Days to analyze

    Returns:
        Insights report dict
    """
    try:
        from insights import InsightsEngine, format_insights, format_compact

        engine = InsightsEngine()
        engine.load_sessions(sessions)
        report = engine.generate(days=days)

        return {
            "empty": report.empty,
            "total_sessions": report.total_sessions,
            "total_messages": report.total_messages,
            "total_tokens": report.total_tokens,
            "total_cost_usd": report.total_cost_usd,
            "avg_tokens_per_session": report.avg_tokens_per_session,
            "avg_cost_per_session": report.avg_cost_per_session,
            "model_breakdown": report.model_breakdown,
            "provider_breakdown": report.provider_breakdown,
            "compact": format_compact(report),
        }
    except ImportError:
        return {"error": "hermes-bridge not available"}


# ============================================================================
# Trajectory Recording
# ============================================================================

def record_trajectory(
    session_id: str,
    model: str,
    provider: str,
    turns: List[Dict[str, Any]],
    completed: bool,
    failure_reason: Optional[str] = None,
) -> Optional[str]:
    """
    Record conversation trajectory.

    Args:
        session_id: Session identifier
        model: Model name
        provider: Provider name
        turns: Conversation turns
        completed: Whether completed successfully
        failure_reason: If not completed, reason

    Returns:
        Path to saved file or None
    """
    try:
        from trajectory import TrajectoryRecorder

        recorder = TrajectoryRecorder(session_id, model, provider)
        for turn in turns:
            role = turn.get("role", "")
            content = turn.get("content", "")
            if role in ("user", "assistant"):
                recorder.add_turn(role, content)

        return recorder.save(
            completed=completed,
            output_dir=str(Path("~/.openclaw/trajectories").expanduser()),
            failure_reason=failure_reason,
        )
    except ImportError:
        return None


# ============================================================================
# Unified Hermes Adapter Class
# ============================================================================

class HermesAdapter:
    """
    Unified adapter for hermes-bridge modules.

    Usage:
        adapter = HermesAdapter()

        # Error handling
        error_info = adapter.classify_error(429, "rate limit")

        # Model routing
        route = adapter.route_query("Hello!")

        # Compression
        result = adapter.compress(messages)

        # Insights
        insights = adapter.get_insights(sessions)
    """

    def __init__(self):
        self._hermes_available = HERMES_BRIDGE_PATH.exists()

    @property
    def hermes_available(self) -> bool:
        """Check if hermes-bridge is available."""
        return self._hermes_available

    def classify_error(self, status_code: int, message: str, provider: str = "") -> Dict[str, Any]:
        """Classify API error."""
        return classify_api_error(status_code, message, provider)

    def route_query(self, query: str, model: str = "gpt-4", provider: str = "openai") -> Dict[str, Any]:
        """Route query to appropriate model."""
        return route_query(query, model, provider)

    def compress(
        self,
        messages: List[Dict[str, Any]],
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Compress conversation."""
        return compress_conversation(messages, system_prompt)

    def get_insights(self, sessions: List[Dict[str, Any]], days: int = 30) -> Dict[str, Any]:
        """Generate insights report."""
        return generate_insights_report(sessions, days)

    def redact(self, text: str) -> str:
        """Redact sensitive data."""
        return redact_sensitive_data(text)

    def record(
        self,
        session_id: str,
        model: str,
        provider: str,
        turns: List[Dict[str, Any]],
        completed: bool,
    ) -> Optional[str]:
        """Record trajectory."""
        return record_trajectory(session_id, model, provider, turns, completed)


# ============================================================================
# Convenience Singleton
# ============================================================================

_default_adapter: Optional[HermesAdapter] = None


def get_adapter() -> HermesAdapter:
    """Get singleton adapter instance."""
    global _default_adapter
    if _default_adapter is None:
        _default_adapter = HermesAdapter()
    return _default_adapter
