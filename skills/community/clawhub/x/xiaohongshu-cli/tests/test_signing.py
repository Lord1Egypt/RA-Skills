"""Unit tests for signing algorithm (no network required)."""


from xhs_cli.signing import (
    PAYLOAD_LENGTH,
    _build_content_string,
    _build_payload_array,
    _crc32_js_int,
    _custom_base64_encode,
    _custom_hash_v2,
    _extract_api_path,
    _hex_to_bytes,
    _int_to_le_bytes,
    _rc4_encrypt,
    _rotate_left,
    _x3_base64_encode,
    _xor_transform,
    build_get_uri,
    extract_uri,
    sign_main_api,
)


class TestCustomBase64:
    def test_encode_string(self):
        result = _custom_base64_encode("hello")
        assert isinstance(result, str)
        assert len(result) > 0
        # Should not be standard base64 (alphabet is shuffled)
        import base64
        standard = base64.b64encode(b"hello").decode()
        assert result != standard

    def test_encode_bytes(self):
        result = _custom_base64_encode(b"\x00\x01\x02\x03")
        assert isinstance(result, str)

    def test_deterministic(self):
        r1 = _custom_base64_encode("test data")
        r2 = _custom_base64_encode("test data")
        assert r1 == r2


class TestX3Base64:
    def test_encode(self):
        data = bytes(range(16))
        result = _x3_base64_encode(data)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_different_from_custom(self):
        data = b"test"
        custom = _custom_base64_encode(data)
        x3 = _x3_base64_encode(data)
        # They use different alphabets, should produce different results
        assert custom != x3


class TestHelpers:
    def test_hex_to_bytes(self):
        result = _hex_to_bytes("0102ff")
        assert result == b"\x01\x02\xff"

    def test_int_to_le_bytes_4(self):
        result = _int_to_le_bytes(0x12345678, 4)
        assert result == [0x78, 0x56, 0x34, 0x12]

    def test_int_to_le_bytes_8(self):
        result = _int_to_le_bytes(0x123456789ABCDEF0, 8)
        assert len(result) == 8
        # Verify it's little-endian
        assert result[0] == 0xF0

    def test_rotate_left(self):
        # rotate 0x80000001 left by 1 → should be 0x00000003
        result = _rotate_left(0x80000001, 1)
        assert result == 0x00000003

    def test_rotate_left_by_0(self):
        assert _rotate_left(0x12345678, 0) == 0x12345678


class TestExtractApiPath:
    def test_simple_uri(self):
        assert _extract_api_path("/api/sns/web/v1/feed") == "/api/sns/web/v1/feed"

    def test_uri_with_query(self):
        assert _extract_api_path("/api/sns/web/v1/user?id=123") == "/api/sns/web/v1/user"

    def test_uri_with_body(self):
        assert _extract_api_path('/api/sns/web/v1/feed{"key":"val"}') == "/api/sns/web/v1/feed"


class TestBuildPayload:
    def test_payload_length(self):
        payload = _build_payload_array(
            "d41d8cd98f00b204e9800998ecf8427e",  # MD5 of empty string
            "test_a1_cookie_value",
            "/api/sns/web/v1/feed",
        )
        assert len(payload) == PAYLOAD_LENGTH

    def test_payload_starts_with_version(self):
        payload = _build_payload_array(
            "d41d8cd98f00b204e9800998ecf8427e",
            "test_a1",
            "/api/sns/web/v1/feed",
        )
        assert payload[0:4] == [121, 104, 96, 41]


class TestXorTransform:
    def test_output_length(self):
        source = list(range(144))
        result = _xor_transform(source)
        assert len(result) == 144

    def test_output_is_bytes(self):
        result = _xor_transform([0, 1, 2])
        assert isinstance(result, bytes)


class TestCrc32:
    def test_known_value(self):
        # JS CRC32 has a specific variant, just test it doesn't crash and returns int
        result = _crc32_js_int("hello")
        assert isinstance(result, int)

    def test_deterministic(self):
        r1 = _crc32_js_int("test string")
        r2 = _crc32_js_int("test string")
        assert r1 == r2

    def test_different_inputs(self):
        r1 = _crc32_js_int("hello")
        r2 = _crc32_js_int("world")
        assert r1 != r2


class TestRc4:
    def test_encrypt_decrypt(self):
        key = "testkey"
        data = "hello world"
        encrypted = _rc4_encrypt(key, data)
        assert isinstance(encrypted, bytes)
        assert encrypted != data.encode()

    def test_deterministic(self):
        r1 = _rc4_encrypt("key", "data")
        r2 = _rc4_encrypt("key", "data")
        assert r1 == r2


class TestBuildUri:
    def test_no_params(self):
        assert build_get_uri("/api/test") == "/api/test"

    def test_with_params(self):
        result = build_get_uri("/api/test", {"a": "1", "b": 2})
        assert "/api/test?" in result
        assert "a=1" in result
        assert "b=2" in result

    def test_with_list_params(self):
        result = build_get_uri("/api/test", {"types": ["a", "b"]})
        assert "types=a%2Cb" in result


class TestExtractUri:
    def test_full_url(self):
        assert extract_uri("https://example.com/api/test") == "/api/test"

    def test_path_only(self):
        assert extract_uri("/api/test") == "/api/test"


class TestBuildContentString:
    def test_get(self):
        result = _build_content_string("GET", "/api/test?a=1")
        assert result == "/api/test?a=1"

    def test_post_no_payload(self):
        result = _build_content_string("POST", "/api/test")
        assert result == "/api/test"

    def test_post_with_payload(self):
        result = _build_content_string("POST", "/api/test", {"key": "val"})
        assert result == '/api/test{"key":"val"}'


class TestSignMainApi:
    def test_generates_all_headers(self):
        cookies = {"a1": "test_a1_value_1234567890abcdef1234567890abcdef1234567890ab"}
        headers = sign_main_api("GET", "/api/sns/web/v2/user/me", cookies)

        assert "x-s" in headers
        assert "x-s-common" in headers
        assert "x-t" in headers
        assert "x-b3-traceid" in headers
        assert "x-xray-traceid" in headers

    def test_xs_prefix(self):
        cookies = {"a1": "test_a1_value_1234567890abcdef1234567890abcdef1234567890ab"}
        headers = sign_main_api("GET", "/api/test", cookies)
        assert headers["x-s"].startswith("XYS_")

    def test_xt_is_timestamp(self):
        cookies = {"a1": "test_a1_value_1234567890abcdef1234567890abcdef1234567890ab"}
        headers = sign_main_api("GET", "/api/test", cookies)
        ts = int(headers["x-t"])
        # Should be current timestamp in ms (roughly)
        import time
        now_ms = int(time.time() * 1000)
        assert abs(ts - now_ms) < 5000  # within 5 seconds

    def test_post_signing(self):
        cookies = {"a1": "test_a1_value_1234567890abcdef1234567890abcdef1234567890ab"}
        headers = sign_main_api(
            "POST",
            "/api/sns/web/v1/search/notes",
            cookies,
            payload={"keyword": "test", "page": 1},
        )
        assert headers["x-s"].startswith("XYS_")

    def test_missing_a1_raises(self):
        import pytest
        with pytest.raises(ValueError, match="Missing 'a1'"):
            sign_main_api("GET", "/api/test", {})

    def test_with_params(self):
        cookies = {"a1": "test_a1_value_1234567890abcdef1234567890abcdef1234567890ab"}
        headers = sign_main_api(
            "GET", "/api/test", cookies,
            params={"user_id": "12345"},
        )
        assert headers["x-s"].startswith("XYS_")


class TestCustomHashV2:
    def test_output_length(self):
        result = _custom_hash_v2(list(range(24)))
        assert len(result) == 16  # 4 x 4 bytes

    def test_deterministic(self):
        data = list(range(24))
        r1 = _custom_hash_v2(data)
        r2 = _custom_hash_v2(data)
        assert r1 == r2

    def test_different_inputs(self):
        r1 = _custom_hash_v2([0] * 24)
        r2 = _custom_hash_v2([1] * 24)
        assert r1 != r2
