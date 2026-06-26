"""Unit tests for creator signing (no network required)."""

import base64
import json

from xhs_cli.creator_signing import _aes_encrypt, sign_creator


class TestAesEncrypt:
    def test_returns_hex(self):
        result = _aes_encrypt("hello world")
        assert isinstance(result, str)
        # Should be valid hex
        int(result, 16)

    def test_deterministic(self):
        r1 = _aes_encrypt("test data")
        r2 = _aes_encrypt("test data")
        assert r1 == r2

    def test_different_inputs(self):
        r1 = _aes_encrypt("hello")
        r2 = _aes_encrypt("world")
        assert r1 != r2


class TestSignCreator:
    def test_generates_headers(self):
        result = sign_creator("url=/api/test", None, "test_a1")
        assert "x-s" in result
        assert "x-t" in result

    def test_xs_prefix(self):
        result = sign_creator("url=/api/test", None, "test_a1")
        assert result["x-s"].startswith("XYW_")

    def test_xt_is_timestamp(self):
        result = sign_creator("url=/api/test", None, "test_a1")
        ts = int(result["x-t"])
        import time
        now_ms = int(time.time() * 1000)
        assert abs(ts - now_ms) < 5000

    def test_with_data(self):
        result = sign_creator(
            "url=/web_api/sns/v1/search/topic",
            {"keyword": "test"},
            "test_a1",
        )
        assert result["x-s"].startswith("XYW_")

    def test_envelope_structure(self):
        result = sign_creator("url=/api/test", None, "test_a1")
        # Decode the XYW_ envelope
        xs = result["x-s"]
        assert xs.startswith("XYW_")
        envelope_b64 = xs[4:]
        envelope = json.loads(base64.b64decode(envelope_b64))

        assert envelope["signSvn"] == "56"
        assert envelope["signType"] == "x2"
        assert envelope["appId"] == "ugc"
        assert envelope["signVersion"] == "1"
        assert "payload" in envelope

    def test_get_vs_post(self):
        # GET: data is None
        r1 = sign_creator("url=/api/test", None, "a1_val")
        # POST: data is provided
        r2 = sign_creator("url=/api/test", {"key": "val"}, "a1_val")
        # Should produce different signatures because content differs
        # (x-t might also differ so just check x-s)
        # The payloads should be different
        env1 = json.loads(base64.b64decode(r1["x-s"][4:]))
        env2 = json.loads(base64.b64decode(r2["x-s"][4:]))
        assert env1["payload"] != env2["payload"]
