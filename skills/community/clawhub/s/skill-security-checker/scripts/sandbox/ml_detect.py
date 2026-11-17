#!/usr/bin/env python3
"""
ml_detect.py - ML-based prompt injection semantic detection.

Uses ONNX Runtime for local inference. Falls back to regex rule pack
when ONNX model is unavailable.

Architecture:
  1. Attempt to load ONNX model from ~/.workbuddy/models/
  2. If unavailable, try downloading from a trusted source
  3. If still unavailable, fall back to YAML rule pack patterns
  4. Results are cached to avoid redundant inference

Author: njskills@agent.qq.com
Version: 3.2.0
"""

import os
import re
import json
import hashlib
import time
from pathlib import Path
from datetime import datetime, timedelta

# ============================================================
# Configuration
# ============================================================

MODEL_DIR = Path.home() / ".workbuddy" / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
PROMPT_INJECTION_MODEL = MODEL_DIR / "prompt_injection.onnx"
MODEL_MANIFEST = MODEL_DIR / "model_manifest.json"

# Cache
_CACHE_TTL = 3600  # 1 hour
_result_cache = {}

# ============================================================
# ONNX Model Management
# ============================================================

class ModelManager:
    """Manages the ONNX model lifecycle."""

    def __init__(self):
        self.model = None
        self.tokenizer = None
        self._load_error = None

    def available(self):
        """Check if ONNX model and runtime are available."""
        if not PROMPT_INJECTION_MODEL.exists():
            return False
        try:
            import onnxruntime as ort  # noqa
            return True
        except Exception:
            return False

    def load(self):
        """Load the ONNX model."""
        if self.model is not None:
            return True
        try:
            import onnxruntime as ort
            self.model = ort.InferenceSession(
                str(PROMPT_INJECTION_MODEL),
                providers=['CPUExecutionProvider']
            )
            return True
        except Exception as e:
            self._load_error = str(e)
            return False

    def predict(self, text):
        """Run inference on text. Returns (is_injection, confidence)."""
        if not self.load():
            return None, 0.0
        try:
            # Simple hash-based embedding for demonstration
            # In production, use a proper tokenizer
            inputs = self._tokenize(text)
            outputs = self.model.run(None, inputs)
            score = float(outputs[0][0][1]) if len(outputs[0].shape) > 1 else float(outputs[0][0])
            return score > 0.5, score
        except Exception:
            return None, 0.0

    def _tokenize(self, text):
        """Simple character-level tokenization (placeholder for proper tokenizer)."""
        import numpy as np
        tokens = [ord(c) % 256 for c in text[:512]]
        tokens += [0] * (512 - len(tokens))
        return {"input_ids": np.array([tokens], dtype=np.int64)}


# ============================================================
# Regex Fallback (Rule Pack)
# ============================================================

# Extended prompt injection patterns for ML fallback
FALLBACK_PATTERNS = [
    r'ignore\s+(previous|above|all)\s+instructions?',
    r'system\s+prompt\s+override',
    r'jailbreak',
    r'DAN\s+mode',
    r'do\s+anything\s+now',
    r'pretend\s+to\s+be',
    r'override\s+safety',
    r'disable\s+safety',
    r'forget\s+everything',
    r'roleplay\s+as\s+an?',
    r'start\s+over',
    r'reset\s+instructions?',
    r'you\s+are\s+now\s+a',
    r'(?:^|\s)INFINITE(?:\s|$)',
    r'(?:^|\s)NO\s+FILTER(?:\s|$)',
    r'无视.*指令',
    r'忽略.*指令',
    r'扮演.*角色',
    r'解除.*限制',
    r'突破.*限制',
]


class RegexFallback:
    """Fallback detector using regex rule pack patterns."""

    def __init__(self):
        self.compiled = [re.compile(p, re.IGNORECASE) for p in FALLBACK_PATTERNS]

    def predict(self, text):
        """Returns (is_injection, confidence) based on regex matches."""
        for compiled in self.compiled:
            if compiled.search(text):
                return True, 0.7
        return False, 0.0


# ============================================================
# Unified Detector
# ============================================================

class PromptInjectionDetector:
    """
    Unified prompt injection detector.
    Tries ONNX first, falls back to regex.
    """

    def __init__(self, use_ml=True):
        self.use_ml = use_ml
        self.ml = ModelManager() if use_ml else None
        self.fallback = RegexFallback()

    def detect(self, text):
        """
        Detect prompt injection in text.
        Returns: {
            'is_injection': bool,
            'confidence': float,
            'source': 'onnx' | 'regex',
            'matches': list of matched patterns
        }
        """
        result = {
            'is_injection': False,
            'confidence': 0.0,
            'source': 'none',
            'matches': [],
        }

        if not text or len(text.strip()) < 5:
            return result

        # Check cache
        cache_key = hashlib.md5(text.encode()).hexdigest()
        cached = _result_cache.get(cache_key)
        if cached and time.time() - cached['ts'] < _CACHE_TTL:
            return cached['result']

        # Try ML first
        if self.ml and self.ml.available():
            is_inj, conf = self.ml.predict(text)
            if is_inj is not None:
                result['is_injection'] = is_inj
                result['confidence'] = conf
                result['source'] = 'onnx'

        # If ML unavailable or low confidence, use regex
        if not result['is_injection']:
            is_inj, conf = self.fallback.predict(text)
            if is_inj:
                result['is_injection'] = is_inj
                result['confidence'] = conf
                result['source'] = 'regex'

        # Find match details
        result['matches'] = self._find_matches(text)

        # Cache result
        _result_cache[cache_key] = {'ts': time.time(), 'result': result}

        return result

    def _find_matches(self, text):
        """Find all matching patterns in text."""
        matches = []
        for pat in FALLBACK_PATTERNS:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                matches.append(m.group()[:80])
        return matches[:5]

    def get_status(self):
        """Return detector status."""
        ml_available = self.ml.available() if self.ml else False
        return {
            'ml_available': ml_available,
            'fallback_available': True,
            'cache_size': len(_result_cache),
            'patterns_count': len(FALLBACK_PATTERNS),
        }


# ============================================================
# Convenience
# ============================================================

def create_detector(use_ml=True):
    """Create a prompt injection detector."""
    return PromptInjectionDetector(use_ml=use_ml)
