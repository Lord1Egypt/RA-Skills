"""Tests for the request lifecycle state machine."""

import pytest

from zim.request_state import (
    FulfillmentState,
    InvalidTransitionError,
    PaymentState,
    RequestState,
    TravelRequest,
)


class TestRequestState:
    def test_create_default(self):
        req = TravelRequest()
        assert req.state == RequestState.INTENT_RECEIVED
        assert req.payment_state == PaymentState.PENDING
        assert req.fulfillment_state == FulfillmentState.PENDING
        assert req.tenant_id == "default"
        assert len(req.id) == 16

    def test_valid_forward_transitions(self):
        req = TravelRequest()
        req.transition_to(RequestState.SEARCHING)
        assert req.state == RequestState.SEARCHING

        req.transition_to(RequestState.OPTIONS_READY)
        assert req.state == RequestState.OPTIONS_READY

        req.transition_to(RequestState.OPTION_SELECTED)
        assert req.state == RequestState.OPTION_SELECTED

        req.transition_to(RequestState.AWAITING_INFO)
        assert req.state == RequestState.AWAITING_INFO

        req.transition_to(RequestState.AWAITING_APPROVAL)
        assert req.state == RequestState.AWAITING_APPROVAL

        req.transition_to(RequestState.READY_TO_EXECUTE)
        assert req.state == RequestState.READY_TO_EXECUTE

        req.transition_to(RequestState.EXECUTING)
        assert req.state == RequestState.EXECUTING

        req.transition_to(RequestState.COMPLETED)
        assert req.state == RequestState.COMPLETED

    def test_skip_info_and_approval(self):
        """Option selected can go directly to ready_to_execute."""
        req = TravelRequest(state=RequestState.OPTION_SELECTED)
        req.transition_to(RequestState.READY_TO_EXECUTE)
        assert req.state == RequestState.READY_TO_EXECUTE

    def test_needs_changes_loops_back(self):
        req = TravelRequest(state=RequestState.AWAITING_APPROVAL)
        req.transition_to(RequestState.OPTIONS_READY)
        assert req.state == RequestState.OPTIONS_READY

    def test_cancel_from_any_non_terminal(self):
        for state in RequestState:
            if state in (RequestState.COMPLETED, RequestState.CANCELLED, RequestState.FAILED):
                continue
            req = TravelRequest(state=state)
            req.transition_to(RequestState.CANCELLED)
            assert req.state == RequestState.CANCELLED

    def test_fail_from_any_non_terminal(self):
        for state in RequestState:
            if state in (RequestState.COMPLETED, RequestState.CANCELLED, RequestState.FAILED):
                continue
            req = TravelRequest(state=state)
            req.transition_to(RequestState.FAILED)
            assert req.state == RequestState.FAILED

    def test_cannot_transition_from_terminal(self):
        for terminal in (RequestState.COMPLETED, RequestState.CANCELLED, RequestState.FAILED):
            req = TravelRequest(state=terminal)
            with pytest.raises(InvalidTransitionError):
                req.transition_to(RequestState.SEARCHING)

    def test_options_ready_to_intent_received_allowed_for_retry(self):
        # OPTIONS_READY → INTENT_RECEIVED is valid for the retry flow
        req = TravelRequest(state=RequestState.OPTIONS_READY)
        req.transition_to(RequestState.INTENT_RECEIVED)
        assert req.state == RequestState.INTENT_RECEIVED

    def test_invalid_backward_transition(self):
        # A genuinely invalid backward transition (OPTION_SELECTED → INTENT_RECEIVED)
        req = TravelRequest(state=RequestState.OPTION_SELECTED)
        with pytest.raises(InvalidTransitionError):
            req.transition_to(RequestState.INTENT_RECEIVED)

    def test_invalid_skip_transition(self):
        req = TravelRequest(state=RequestState.INTENT_RECEIVED)
        with pytest.raises(InvalidTransitionError):
            req.transition_to(RequestState.OPTIONS_READY)

    def test_updated_at_changes_on_transition(self):
        req = TravelRequest()
        original = req.updated_at
        req.transition_to(RequestState.SEARCHING)
        assert req.updated_at >= original

    def test_serialization_roundtrip(self):
        req = TravelRequest(
            tenant_id="acme",
            traveler_id="robin",
            raw_message="fly me to the moon",
            parsed_intent={"travel_type": "flight", "destination": "moon"},
        )
        data = req.model_dump(mode="json")
        restored = TravelRequest.model_validate(data)
        assert restored.id == req.id
        assert restored.tenant_id == "acme"
        assert restored.parsed_intent["destination"] == "moon"
