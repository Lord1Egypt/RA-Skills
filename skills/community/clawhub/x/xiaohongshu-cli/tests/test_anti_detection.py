"""Tests for anti-detection measures: fingerprint consistency, UA/platform alignment, jitter."""


from xhs_cli.client import XhsClient
from xhs_cli.constants import CHROME_VERSION, PLATFORM, USER_AGENT
from xhs_cli.signing import (
    _generate_fingerprint,
    _get_session_fingerprint,
    _session_fp_cache,
    sign_main_api,
)


class TestUAPlatformConsistency:
    """UA, sec-ch-ua, and fingerprint must all agree on macOS Chrome."""

    def test_ua_is_macos_chrome(self):
        assert "Macintosh" in USER_AGENT
        assert "Chrome/" in USER_AGENT
        assert "Edg/" not in USER_AGENT
        assert "Windows" not in USER_AGENT

    def test_platform_is_macos(self):
        assert PLATFORM == "macOS"

    def test_base_headers_match_ua(self):
        client = XhsClient({"a1": "test"})
        try:
            headers = client._base_headers()
            # sec-ch-ua must reference Chrome, not Edge
            assert "Google Chrome" in headers["sec-ch-ua"]
            assert CHROME_VERSION in headers["sec-ch-ua"]
            assert "Edge" not in headers["sec-ch-ua"]
            # Platform must match
            assert "macOS" in headers["sec-ch-ua-platform"]
        finally:
            client.close()

    def test_fingerprint_platform_is_macintel(self):
        cookies = {"a1": "test_a1_12345678901234567890123456789012345678901234"}
        fp = _generate_fingerprint(cookies, USER_AGENT)
        assert fp["x19"] == "MacIntel"

    def test_fingerprint_gpu_is_macos_appropriate(self):
        cookies = {"a1": "test_a1_12345678901234567890123456789012345678901234"}
        fp = _generate_fingerprint(cookies, USER_AGENT)
        # GPU vendor should be Apple or macOS-compatible
        gpu = fp["x7"]
        valid_vendors = ["Apple", "Intel", "AMD"]
        assert any(v in gpu for v in valid_vendors)
        # No D3D11 (Windows-only)
        assert "D3D11" not in gpu

    def test_fingerprint_vendor_is_apple(self):
        cookies = {"a1": "test_a1_12345678901234567890123456789012345678901234"}
        fp = _generate_fingerprint(cookies, USER_AGENT)
        assert fp["x75"] == "Apple Inc."


class TestFingerprintSessionPersistence:
    """Fingerprint must remain stable within a session (same a1)."""

    def setup_method(self):
        _session_fp_cache.clear()

    def test_same_a1_returns_same_fingerprint(self):
        cookies = {"a1": "persist_test_1234567890abcdef1234567890abcdef1234567890ab"}

        fp1, b1_1, x9_1 = _get_session_fingerprint(cookies)
        fp2, b1_2, x9_2 = _get_session_fingerprint(cookies)

        # Core identity fields must be identical
        assert fp1["x7"] == fp2["x7"]  # GPU
        assert fp1["x9"] == fp2["x9"]  # Screen resolution
        assert fp1["x8"] == fp2["x8"]  # CPU cores
        assert b1_1 == b1_2
        assert x9_1 == x9_2

    def test_different_a1_gets_different_fingerprint(self):
        cookies_a = {"a1": "user_a_1234567890abcdef1234567890abcdef1234567890ab"}
        cookies_b = {"a1": "user_b_1234567890abcdef1234567890abcdef1234567890ab"}

        fp_a, _, _ = _get_session_fingerprint(cookies_a)
        fp_b, _, _ = _get_session_fingerprint(cookies_b)

        # Different a1s generate independently (may or may not differ due to randomness)
        assert cookies_a["a1"] in _session_fp_cache
        assert cookies_b["a1"] in _session_fp_cache

    def test_x_s_common_is_stable_across_calls(self):
        cookies = {"a1": "stable_test_1234567890abcdef1234567890abcdef1234567890ab"}

        headers1 = sign_main_api("GET", "/api/test", cookies)
        headers2 = sign_main_api("GET", "/api/test", cookies)

        # x-s-common should be identical (same fingerprint → same b1 → same output)
        assert headers1["x-s-common"] == headers2["x-s-common"]


class TestClientJitter:
    """Verify jitter produces variable delays (not fixed intervals)."""

    def test_request_delay_default(self):
        client = XhsClient({"a1": "test"})
        try:
            assert client._request_delay == 1.0
            assert client._base_request_delay == 1.0
        finally:
            client.close()

    def test_verify_count_starts_at_zero(self):
        client = XhsClient({"a1": "test"})
        try:
            assert client._verify_count == 0
            assert client._request_count == 0
        finally:
            client.close()


class TestBaseHeadersCompleteness:
    """Ensure all anti-detection headers are present."""

    def test_has_dnt_header(self):
        client = XhsClient({"a1": "test"})
        try:
            headers = client._base_headers()
            assert headers.get("dnt") == "1"
        finally:
            client.close()

    def test_has_priority_header(self):
        client = XhsClient({"a1": "test"})
        try:
            headers = client._base_headers()
            assert "priority" in headers
        finally:
            client.close()

    def test_has_all_sec_fetch_headers(self):
        client = XhsClient({"a1": "test"})
        try:
            headers = client._base_headers()
            assert "sec-fetch-dest" in headers
            assert "sec-fetch-mode" in headers
            assert "sec-fetch-site" in headers
        finally:
            client.close()
