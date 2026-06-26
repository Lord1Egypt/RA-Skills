#!/usr/bin/env python3
"""
Session Logger for YumFu - V3 (OPTIONAL - Privacy-Aware)
Tracks gameplay conversations for storybook generation.

⚠️ PRIVACY NOTICE:
This logger stores complete gameplay conversations (player input + AI responses).
To disable logging, set environment variable: YUMFU_NO_LOGGING=1

V3 adds a dual-track format:
- raw player / AI text
- storybook-ready player / AI prose

Usage:
    from scripts.session_logger import log_turn

    # Logging is automatically disabled if YUMFU_NO_LOGGING=1
    log_turn(
        user_id="YOUR_USER_ID",
        universe="warrior-cats",
        player_input="/yumfu look",
        ai_response="You see the ThunderClan camp...",
        image="tumpaw-camp-20260403.png",
        player_storybook="You lifted your head and took in the ThunderClan camp in full.",
        ai_storybook="The ThunderClan camp opened before you, alive with movement and evening voices."
    )
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any


# Privacy control: Check if logging is disabled
def _is_logging_disabled() -> bool:
    """Check if user has disabled session logging for privacy"""
    return os.getenv("YUMFU_NO_LOGGING", "0") == "1"


def _normalize_whitespace(text: str) -> str:
    return " ".join((text or "").strip().split())


def _default_player_storybook(player_input: str) -> str:
    raw = _normalize_whitespace(player_input)
    if not raw:
        return ""
    lowered = raw.lower()
    if lowered.startswith('/yumfu '):
        raw = raw[7:].strip()
    elif lowered == '/yumfu':
        raw = 'continued the adventure'

    if raw in {'A', 'B', 'C', 'D', '1', '2', '3', '4'}:
        return f"You chose option {raw}."
    if len(raw) <= 4 and raw.upper() == raw and raw.isalpha():
        return f"You chose {raw}."
    return raw[:1].upper() + raw[1:] if raw else raw


def _default_ai_storybook(ai_response: str) -> str:
    return _normalize_whitespace(ai_response)


class SessionLogger:
    def __init__(self, user_id: str, universe: str, session_id: str = None):
        # Check if logging is disabled
        if _is_logging_disabled():
            self.disabled = True
            return
        
        self.disabled = False
        self.user_id = user_id
        self.universe = universe
        self.session_id = session_id or datetime.now().strftime("%Y%m%d-%H%M%S")
        
        # Paths
        self.base_path = Path.home() / "clawd/memory/yumfu"
        self.session_dir = self.base_path / "sessions" / universe / f"user-{user_id}"
        self.session_file = self.session_dir / f"session-{self.session_id}.jsonl"
        
        # Create directories
        self.session_dir.mkdir(parents=True, exist_ok=True)
        
        # Session metadata
        self.start_time = datetime.now().isoformat()
        
    def log_turn(
        self,
        player_input: str,
        ai_response: str,
        image: Optional[str] = None,
        player_storybook: Optional[str] = None,
        ai_storybook: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Log a complete game turn (player action + AI response + optional image)

        Args:
            player_input: What the player typed (e.g., "/yumfu look")
            ai_response: The AI's narrative response
            image: Optional image filename if generated this turn
            player_storybook: Optional book-style retelling of the player's action
            ai_storybook: Optional book-style retelling of the AI scene text
            metadata: Optional extra turn metadata
        """
        if self.disabled:
            return  # No-op if logging disabled

        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "turn",
            "player": player_input,
            "player_storybook": player_storybook or _default_player_storybook(player_input),
            "ai": ai_response,
            "ai_storybook": ai_storybook or _default_ai_storybook(ai_response),
            "image": image,
            "metadata": metadata or {}
        }
        self._append_to_file(entry)
    
    def log_event(self, event: str, image: Optional[str] = None, metadata: dict = None):
        """Log a story event (location change, achievement, etc.)"""
        if self.disabled:
            return
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "event",
            "content": event,
            "image": image,
            "metadata": metadata or {}
        }
        self._append_to_file(entry)
    
    def log_dialogue(self, speaker: str, text: str, image: Optional[str] = None):
        """Log NPC dialogue"""
        if self.disabled:
            return
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "dialogue",
            "speaker": speaker,
            "content": text,
            "image": image
        }
        self._append_to_file(entry)
    
    def log_image(self, filename: str, description: str = ""):
        """Log an image generation"""
        if self.disabled:
            return
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "image",
            "filename": filename,
            "description": description
        }
        self._append_to_file(entry)
    
    def _append_to_file(self, entry: dict):
        """Append entry to JSONL file"""
        if self.disabled:
            return
        with open(self.session_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    def finalize(self):
        """Create session summary"""
        summary = {
            "user_id": self.user_id,
            "universe": self.universe,
            "session_id": self.session_id,
            "start_time": self.start_time,
            "end_time": datetime.now().isoformat()
        }
        
        summary_file = self.session_dir / f"session-{self.session_id}-summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        return self.session_file


def get_current_session(user_id: str, universe: str) -> SessionLogger:
    """
    Get or create current session logger.
    Sessions expire after 2 hours of inactivity.
    """
    session_dir = Path.home() / "clawd/memory/yumfu/sessions" / universe / f"user-{user_id}"
    
    if not session_dir.exists():
        return SessionLogger(user_id, universe)
    
    # Find most recent session
    sessions = sorted(session_dir.glob("session-*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    
    if not sessions:
        return SessionLogger(user_id, universe)
    
    # Check if most recent is still active (within 2 hours)
    latest = sessions[0]
    age_hours = (datetime.now().timestamp() - latest.stat().st_mtime) / 3600
    
    if age_hours < 2:
        # Resume existing session
        session_id = latest.stem.replace("session-", "")
        return SessionLogger(user_id, universe, session_id=session_id)
    else:
        # Start new session
        return SessionLogger(user_id, universe)


def log_turn(
    user_id: str,
    universe: str,
    player_input: str,
    ai_response: str,
    image: Optional[str] = None,
    player_storybook: Optional[str] = None,
    ai_storybook: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
):
    """
    Convenience function to log a complete turn.
    Automatically manages sessions (creates/resumes).

    Example:
        log_turn(
            user_id="YOUR_USER_ID",
            universe="warrior-cats",
            player_input="/yumfu look",
            ai_response="You see the ThunderClan camp bustling with activity...",
            image="tumpaw-camp-20260403.png",
            player_storybook="You paused to study the camp around you.",
            ai_storybook="The ThunderClan camp bustled with activity around the fresh-kill pile."
        )
    """
    logger = get_current_session(user_id, universe)
    logger.log_turn(
        player_input,
        ai_response,
        image=image,
        player_storybook=player_storybook,
        ai_storybook=ai_storybook,
        metadata=metadata,
    )
    return logger.session_file


def log_image_only(user_id: str, universe: str, filename: str, description: str = ""):
    """
    Log an image generation (when no dialogue happens in same turn)
    """
    logger = get_current_session(user_id, universe)
    logger.log_image(filename, description)
    return logger.session_file
