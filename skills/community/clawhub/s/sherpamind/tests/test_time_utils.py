from sherpamind.time_utils import parse_sherpadesk_timestamp


def test_parse_sherpadesk_timestamp_handles_7_digit_fractional_seconds() -> None:
    dt = parse_sherpadesk_timestamp("2026-03-19T16:56:00.0000000")
    assert dt is not None
    assert dt.year == 2026
    assert dt.tzinfo is not None
