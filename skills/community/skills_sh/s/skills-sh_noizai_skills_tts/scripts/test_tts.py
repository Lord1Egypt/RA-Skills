#!/usr/bin/env python3
"""Minimal unit tests for tts.py — guest mode.

Run: python3 -m pytest skills/tts/scripts/test_tts.py -v
  or: python3 skills/tts/scripts/test_tts.py

Live integration test (hits the real Noiz guest API):
  TTS_LIVE_TEST=1 python3 -m pytest skills/tts/scripts/test_tts.py -v -k live
"""
import argparse
import base64
import importlib.util
import os
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path
from unittest.mock import patch

# Load tts.py as a module without executing main()
_spec = importlib.util.spec_from_file_location("tts", Path(__file__).parent / "tts.py")
tts = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tts)  # type: ignore[union-attr]

# ── helpers ───────────────────────────────────────────────────────────

def make_speak_args(**overrides):
    """Return a minimal Namespace for cmd_speak in noiz-guest mode."""
    defaults = dict(
        text="hello",
        text_file=None,
        voice=None,
        voice_id="883b6b7c",
        output="/tmp/tts_test_out.wav",
        format="wav",
        lang=None,
        speed=None,
        emo=None,
        duration=None,
        backend="noiz-guest",
        ref_audio=None,
        auto_emotion=False,
        similarity_enh=False,
        save_voice=False,
    )
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


# ── normalize_api_key_base64 ──────────────────────────────────────────

class TestNormalizeApiKey(unittest.TestCase):

    def test_plain_text_is_base64_encoded(self):
        result = tts.normalize_api_key_base64("myplainkey")
        expected = base64.b64encode(b"myplainkey").decode("ascii")
        self.assertEqual(result, expected)

    def test_already_base64_passes_through(self):
        original = base64.b64encode(b"somerawkey").decode("ascii")
        self.assertEqual(tts.normalize_api_key_base64(original), original)

    def test_empty_returns_empty(self):
        self.assertEqual(tts.normalize_api_key_base64(""), "")

    def test_strips_surrounding_whitespace(self):
        raw = "  mykey  "
        result = tts.normalize_api_key_base64(raw)
        self.assertFalse(result.startswith(" "))
        self.assertFalse(result.endswith(" "))


# ── detect_text_lang ──────────────────────────────────────────────────

class TestDetectTextLang(unittest.TestCase):

    def test_chinese_returns_zh(self):
        self.assertEqual(tts.detect_text_lang("你好世界"), "zh")

    def test_english_returns_en(self):
        self.assertEqual(tts.detect_text_lang("Hello world"), "en")

    def test_mixed_returns_zh(self):
        self.assertEqual(tts.detect_text_lang("Hello 你好"), "zh")

    def test_empty_returns_en(self):
        self.assertEqual(tts.detect_text_lang(""), "en")


# ── detect_backend ────────────────────────────────────────────────────

class TestDetectBackend(unittest.TestCase):

    def test_explicit_backend_is_respected(self):
        self.assertEqual(tts.detect_backend("kokoro"), "kokoro")
        self.assertEqual(tts.detect_backend("noiz"), "noiz")

    def test_no_key_falls_back_to_guest(self):
        with patch.object(tts, "load_api_key", return_value=None):
            self.assertEqual(tts.detect_backend(""), "noiz-guest")

    def test_key_present_selects_noiz(self):
        with patch.object(tts, "load_api_key", return_value="somekey"):
            self.assertEqual(tts.detect_backend(""), "noiz")


# ── cmd_speak — guest mode ────────────────────────────────────────────

class TestCmdSpeakGuestMode(unittest.TestCase):

    def _run(self, args):
        mock_synth = unittest.mock.MagicMock(return_value=1.0)
        with patch.object(tts, "ensure_noiz_ready"), \
             patch.dict("sys.modules", {"noiz_tts": unittest.mock.MagicMock(synthesize_guest=mock_synth)}):
            rc = tts.cmd_speak(args)
            return rc, mock_synth

    def test_calls_synthesize_guest(self):
        rc, mock_synth = self._run(make_speak_args())
        self.assertEqual(rc, 0)
        mock_synth.assert_called_once()

    def test_voice_id_forwarded(self):
        rc, mock_synth = self._run(make_speak_args(voice_id="883b6b7c"))
        kwargs = mock_synth.call_args[1]
        self.assertEqual(kwargs["voice_id"], "883b6b7c")

    def test_text_forwarded(self):
        rc, mock_synth = self._run(make_speak_args(text="hi there"))
        kwargs = mock_synth.call_args[1]
        self.assertEqual(kwargs["text"], "hi there")

    def test_ogg_format_aliased_to_opus(self):
        rc, mock_synth = self._run(make_speak_args(format="ogg"))
        kwargs = mock_synth.call_args[1]
        self.assertEqual(kwargs["output_format"], "opus")

    def test_speed_forwarded_when_set(self):
        rc, mock_synth = self._run(make_speak_args(speed=1.5))
        kwargs = mock_synth.call_args[1]
        self.assertEqual(kwargs["speed"], 1.5)

    def test_speed_default_when_not_set(self):
        rc, mock_synth = self._run(make_speak_args(speed=None))
        kwargs = mock_synth.call_args[1]
        self.assertEqual(kwargs["speed"], 1.0)

    def test_missing_voice_id_returns_error(self):
        args = make_speak_args(voice_id=None)
        with patch.object(tts, "ensure_noiz_ready"):
            rc = tts.cmd_speak(args)
        self.assertEqual(rc, 1)

    def test_missing_text_and_file_returns_error(self):
        args = make_speak_args(text=None, text_file=None)
        rc = tts.cmd_speak(args)
        self.assertEqual(rc, 1)


# ── live integration — real HTTP call to Noiz guest API ───────────────

@unittest.skipUnless(os.getenv("TTS_LIVE_TEST"), "set TTS_LIVE_TEST=1 to run live tests")
class TestLiveGuestSynthesize(unittest.TestCase):
    """Calls the real Noiz guest endpoint; requires network access and requests."""

    VOICE_ID = "883b6b7c"
    TEXT = "Hello, this is a live test."

    @classmethod
    def setUpClass(cls):
        tts.ensure_noiz_ready()  # installs requests if missing, no-op if already present
        _spec = importlib.util.spec_from_file_location(
            "noiz_tts", Path(__file__).parent / "noiz_tts.py"
        )
        cls._noiz_tts = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(cls._noiz_tts)  # type: ignore[union-attr]

    def test_synthesize_guest_produces_audio_file(self):
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            out_path = Path(f.name)
        try:
            duration = self._noiz_tts.synthesize_guest(
                base_url="https://noiz.ai/v1",
                text=self.TEXT,
                voice_id=self.VOICE_ID,
                output_format="wav",
                speed=1.0,
                timeout=60,
                out_path=out_path,
            )
            self.assertTrue(out_path.exists(), "Output WAV file was not created")

            file_size = out_path.stat().st_size
            self.assertGreater(file_size, 0, "Output file is empty (0 bytes)")
            self.assertGreater(file_size, 4096, f"Output file too small ({file_size} bytes), likely an error response")

            # Confirm the file is a real WAV: first 4 bytes must be "RIFF"
            header = out_path.read_bytes()[:4]
            self.assertEqual(header, b"RIFF", f"Output file has wrong header {header!r}, expected b'RIFF'")

            # Guest endpoint doesn't return X-Audio-Duration; -1.0 means unknown, which is fine
            self.assertGreaterEqual(duration, -1.0, f"Unexpected duration value: {duration}")
        finally:
            out_path.unlink(missing_ok=True)
            out_path.with_suffix(".duration").unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
