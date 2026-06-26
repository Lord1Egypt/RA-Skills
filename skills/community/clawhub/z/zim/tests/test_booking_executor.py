"""Tests for zim.booking_executor — placeholder executor and interfaces."""

from zim.booking_executor import (
    BookingExecutionRequest,
    BookingExecutionResult,
    PlaceholderExecutor,
    get_executor,
)


class TestBookingExecutionResult:
    def test_is_confirmed(self) -> None:
        r = BookingExecutionResult(
            booking_id="b1",
            category="flight",
            provider_status="confirmed",
            provider_confirmation_code="PNR123",
        )
        assert r.is_confirmed is True
        assert r.is_failed is False

    def test_is_failed(self) -> None:
        r = BookingExecutionResult(
            booking_id="b1",
            category="flight",
            provider_status="failed",
            error_message="API timeout",
        )
        assert r.is_failed is True
        assert r.is_confirmed is False


class TestPlaceholderExecutor:
    def test_execute_returns_pending(self) -> None:
        executor = PlaceholderExecutor()
        request = BookingExecutionRequest(
            booking_id="booking_123",
            category="flight",
            provider_name="EK",
            provider_link="https://aviasales.com/search?q=JFK-DXB",
        )

        result = executor.execute(request)
        assert result.provider_status == "pending_provider_integration"
        assert result.provider_confirmation_code is None
        assert result.booking_id == "booking_123"
        assert result.provider_raw_response is not None
        assert result.provider_raw_response["manual_action_required"] is True
        assert "https://aviasales.com" in result.provider_raw_response["booking_link"]

    def test_check_status_returns_pending(self) -> None:
        executor = PlaceholderExecutor()
        result = executor.check_status("b1", "PNR123")
        assert result.provider_status == "pending_provider_integration"

    def test_cancel_returns_pending(self) -> None:
        executor = PlaceholderExecutor()
        result = executor.cancel("b1", "PNR123")
        assert result.provider_status == "pending_provider_integration"


class TestGetExecutor:
    def test_default_is_travelpayouts(self) -> None:
        from zim.booking_executor import TravelpayoutsExecutor
        executor = get_executor()
        assert isinstance(executor, TravelpayoutsExecutor)

    def test_explicit_placeholder(self) -> None:
        executor = get_executor("placeholder")
        assert isinstance(executor, PlaceholderExecutor)

    def test_explicit_travelpayouts(self) -> None:
        from zim.booking_executor import TravelpayoutsExecutor
        executor = get_executor("travelpayouts")
        assert isinstance(executor, TravelpayoutsExecutor)

    def test_env_var_placeholder(self, monkeypatch) -> None:
        monkeypatch.setenv("ZIM_EXECUTOR", "placeholder")
        executor = get_executor()
        assert isinstance(executor, PlaceholderExecutor)
