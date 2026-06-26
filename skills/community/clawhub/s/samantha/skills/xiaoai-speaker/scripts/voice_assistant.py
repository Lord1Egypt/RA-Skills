#!/usr/bin/env python3
"""
Voice Assistant Core
Integrates TTS with text processing and filtering
Source: https://github.com/leilei926524-tech/openclaw-voice-assistant
"""

import re
import os
import threading
from typing import Optional, Dict, Any, Callable
from pathlib import Path

from dotenv import load_dotenv
from .tts_bridge import TTSBridge, run_async


class VoiceAssistant:
    """Main voice assistant class"""

    def __init__(self, config_path: Optional[str] = None):
        if config_path:
            load_dotenv(config_path)

        self.voice_enabled = os.getenv("VOICE_ENABLED", "true").lower() == "true"
        self.min_length = int(os.getenv("VOICE_MIN_LENGTH", "10"))
        self.max_length = int(os.getenv("VOICE_MAX_LENGTH", "300"))
        self.debug = os.getenv("DEBUG", "false").lower() == "true"

        self.tts_bridge = TTSBridge(config_path)
        self._speaking = False
        self._lock = threading.Lock()

        self.on_speak_start: Optional[Callable[[str], None]] = None
        self.on_speak_end: Optional[Callable[[str, bool], None]] = None
        self.on_error: Optional[Callable[[str, Exception], None]] = None

    def enable(self):
        self.voice_enabled = True

    def disable(self):
        self.voice_enabled = False

    def is_enabled(self) -> bool:
        return self.voice_enabled

    def clean_text(self, text: str) -> str:
        """Clean text for TTS — remove code, URLs, markdown"""
        if not text:
            return ""
        text = re.sub(r'```[\s\S]*?```', '', text)   # code blocks
        text = re.sub(r'`[^`]*`', '', text)           # inline code
        text = re.sub(r'https?://\S+', '', text)      # URLs
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # markdown links
        text = re.sub(r'[*_~#>]', '', text)           # markdown formatting
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def should_speak(self, text: str) -> bool:
        if not self.voice_enabled:
            return False
        clean = self.clean_text(text)
        if len(clean) < self.min_length:
            return False
        if len(clean) > self.max_length:
            return False
        if '```' in text or '`' in text:
            return False
        if 'http://' in text or 'https://' in text:
            return False
        if len(clean) < len(text) * 0.3:
            return False
        return True

    def speak(self, text: str, async_mode: bool = True) -> bool:
        if not self.should_speak(text):
            return False
        clean = self.clean_text(text)
        if self.on_speak_start:
            try:
                self.on_speak_start(clean)
            except Exception:
                pass
        with self._lock:
            self._speaking = True
        if async_mode:
            t = threading.Thread(target=self._speak_thread, args=(clean,), daemon=True)
            t.start()
            return True
        else:
            success = self._speak_sync(clean)
            with self._lock:
                self._speaking = False
            if self.on_speak_end:
                try:
                    self.on_speak_end(clean, success)
                except Exception:
                    pass
            return success

    def _speak_thread(self, text: str):
        try:
            success = self._speak_sync(text)
            with self._lock:
                self._speaking = False
            if self.on_speak_end:
                try:
                    self.on_speak_end(text, success)
                except Exception:
                    pass
        except Exception as e:
            with self._lock:
                self._speaking = False
            if self.on_error:
                try:
                    self.on_error(text, e)
                except Exception:
                    pass

    def _speak_sync(self, text: str) -> bool:
        try:
            result = run_async(self.tts_bridge.speak(text))
            return result["success"]
        except Exception:
            return False

    def is_speaking(self) -> bool:
        with self._lock:
            return self._speaking

    def wait_until_done(self, timeout: Optional[float] = None):
        import time
        start = time.time()
        while self.is_speaking():
            if timeout and time.time() - start > timeout:
                break
            time.sleep(0.1)


def respond_with_voice(
    user_message: str,
    ai_response: str,
    voice_assistant: Optional[VoiceAssistant] = None,
    print_response: bool = True
) -> str:
    """Helper: print AI response and optionally speak it"""
    if voice_assistant is None:
        voice_assistant = VoiceAssistant()
    if print_response:
        print(f"\n[AI] {ai_response}")
    if voice_assistant.should_speak(ai_response):
        voice_assistant.speak(ai_response)
    return ai_response


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Voice Assistant")
    parser.add_argument("--speak", help="Text to speak")
    parser.add_argument("--config", help="Path to config file")
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    assistant = VoiceAssistant(args.config)
    if args.speak:
        if assistant.speak(args.speak, async_mode=False):
            print(f"✓ Spoke: '{args.speak}'")
        else:
            print(f"✗ Failed or skipped: '{args.speak}'")
    elif args.test:
        result = run_async(assistant.tts_bridge.test_connection())
        print("✓ Connected!" if result["success"] else f"✗ {result.get('error')}")
    else:
        parser.print_help()
