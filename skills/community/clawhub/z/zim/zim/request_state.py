"""Request lifecycle state machine for Zim middleware API.

Implements the PRD state model as first-class entities:
- RequestState: intent_received → searching → options_ready → ... → completed
- PaymentState: pending → authorized → paid → failed → refunded
- FulfillmentState: pending → link_sent → confirmed → failed

TravelRequest is the top-level entity that tracks a single travel
request through its full lifecycle.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# State enums
# ---------------------------------------------------------------------------

class RequestState(str, Enum):
    INTENT_RECEIVED = "intent_received"
    SEARCHING = "searching"
    OPTIONS_READY = "options_ready"
    OPTION_SELECTED = "option_selected"
    AWAITING_INFO = "awaiting_info"
    AWAITING_APPROVAL = "awaiting_approval"
    READY_TO_EXECUTE = "ready_to_execute"
    EXECUTING = "executing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class PaymentState(str, Enum):
    PENDING = "pending"
    AUTHORIZED = "authorized"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"


class FulfillmentState(str, Enum):
    PENDING = "pending"
    LINK_SENT = "link_sent"
    CONFIRMED = "confirmed"
    PARTIALLY_CONFIRMED = "partially_confirmed"
    FAILED = "failed"


# Valid forward transitions. Cancel and fail are allowed from any non-terminal state.
_VALID_TRANSITIONS: dict[RequestState, set[RequestState]] = {
    RequestState.INTENT_RECEIVED: {RequestState.SEARCHING},
    RequestState.SEARCHING: {RequestState.OPTIONS_READY},
    RequestState.OPTIONS_READY: {RequestState.OPTION_SELECTED, RequestState.INTENT_RECEIVED},
    RequestState.OPTION_SELECTED: {
        RequestState.AWAITING_INFO,
        RequestState.AWAITING_APPROVAL,
        RequestState.READY_TO_EXECUTE,
    },
    RequestState.AWAITING_INFO: {
        RequestState.AWAITING_APPROVAL,
        RequestState.READY_TO_EXECUTE,
    },
    RequestState.AWAITING_APPROVAL: {
        RequestState.READY_TO_EXECUTE,
        RequestState.OPTIONS_READY,  # needs_changes loops back
    },
    RequestState.READY_TO_EXECUTE: {RequestState.EXECUTING},
    RequestState.EXECUTING: {RequestState.COMPLETED},
    # Retry: failed requests can be re-searched
    RequestState.FAILED: {RequestState.INTENT_RECEIVED},
}

_TERMINAL_STATES = {RequestState.COMPLETED, RequestState.CANCELLED}


class InvalidTransitionError(Exception):
    """Raised when a state transition is not allowed."""

    def __init__(self, current: RequestState, target: RequestState) -> None:
        self.current = current
        self.target = target
        super().__init__(f"Cannot transition from {current.value} to {target.value}")


# ---------------------------------------------------------------------------
# TravelRequest model
# ---------------------------------------------------------------------------

class TravelRequest(BaseModel):
    """Top-level travel request entity tracking full lifecycle."""

    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    tenant_id: str = "default"
    traveler_id: str = "default"

    # Intent
    raw_message: Optional[str] = None
    parsed_intent: dict[str, Any] = Field(default_factory=dict)

    # State
    state: RequestState = RequestState.INTENT_RECEIVED
    payment_state: PaymentState = PaymentState.PENDING
    fulfillment_state: FulfillmentState = FulfillmentState.PENDING

    # Timestamps
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

    # Search results
    itinerary: Optional[dict[str, Any]] = None
    ranked_scores: dict[str, Any] = Field(default_factory=dict)

    # Selection
    selected_options: dict[str, int] = Field(default_factory=dict)

    # Traveler info
    traveler_info: Optional[dict[str, Any]] = None

    # Approval
    approval_id: Optional[str] = None
    approval_decision: Optional[str] = None
    approval_notes: Optional[str] = None

    # Payment & execution
    payment_session_id: Optional[str] = None
    checkout_url: Optional[str] = None
    execution_results: list[dict[str, Any]] = Field(default_factory=list)

    # Fulfillment details (confirmation numbers, PNRs, etc.)
    fulfillment_details: dict[str, Any] = Field(default_factory=dict)

    # Metadata
    metadata: dict[str, Any] = Field(default_factory=dict)

    def transition_to(self, target: RequestState) -> None:
        """Transition to a new state with validation.

        Cancel and fail are allowed from any non-terminal state.
        Failed requests can be retried (FAILED → INTENT_RECEIVED).
        Other transitions must follow the valid transition graph.

        Raises:
            InvalidTransitionError: If the transition is not allowed.
        """
        if self.state in _TERMINAL_STATES:
            raise InvalidTransitionError(self.state, target)

        # Cancel always allowed from non-terminal, non-failed states
        if target == RequestState.CANCELLED:
            self.state = target
            self.updated_at = datetime.now(UTC).isoformat()
            return

        # Fail allowed from any non-terminal state
        if target == RequestState.FAILED:
            self.state = target
            self.updated_at = datetime.now(UTC).isoformat()
            return

        allowed = _VALID_TRANSITIONS.get(self.state, set())
        if target not in allowed:
            raise InvalidTransitionError(self.state, target)

        self.state = target
        self.updated_at = datetime.now(UTC).isoformat()
