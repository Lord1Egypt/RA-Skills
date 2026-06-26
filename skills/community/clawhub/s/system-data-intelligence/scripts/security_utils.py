#!/usr/bin/env python3
"""
Security utilities — data masking, temp file cleanup, memory release.
Usage:
    from scripts.security_utils import DataMasker, SecureCleanup, secure_context
"""

import gc
import os
import re
import shutil
import logging
import tempfile
import atexit
from pathlib import Path
from contextlib import contextmanager
from typing import Optional

import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

SENSITIVE_PATTERNS = {
    'phone_cn':       (re.compile(r'1[3-9]\d{9}'), lambda m: m.group()[:3] + '****' + m.group()[-4:]),
    'id_card_cn':     (re.compile(r'\d{17}[\dXx]'), lambda m: m.group()[:6] + '********' + m.group()[-4:]),
    'email':          (re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+'),
                       lambda m: m.group()[0] + '***@' + m.group().split('@')[1]),
    'bank_card':      (re.compile(r'\d{16,19}'), lambda m: m.group()[:4] + ' **** **** ' + m.group()[-4:]),
    'ip_address':     (re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'),
                       lambda m: '.'.join(m.group().split('.')[:2]) + '.*.*'),
    'credit_card':    (re.compile(r'\b(?:4\d{15}|5[1-5]\d{14}|3[47]\d{13})\b'),
                       lambda m: m.group()[:4] + ' **** **** ' + m.group()[-4:]),
}


class DataMasker:
    def __init__(self, patterns=None):
        self.patterns = patterns or SENSITIVE_PATTERNS

    def mask_string(self, text, pattern_keys=None):
        keys = pattern_keys or list(self.patterns.keys())
        for key in keys:
            if key not in self.patterns:
                continue
            regex, replacer = self.patterns[key]
            text = regex.sub(replacer, text)
        return text

    def mask_dataframe(self, df, columns=None, pattern_keys=None):
        df = df.copy()
        target_cols = columns or df.select_dtypes(include=['object']).columns.tolist()
        for col in target_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).apply(lambda v: self.mask_string(v, pattern_keys))
        return df

    def detect_sensitive(self, df):
        findings = {}
        str_cols = df.select_dtypes(include=['object']).columns
        sample = df[str_cols].head(100)
        for col in str_cols:
            detected = []
            text_blob = ' '.join(sample[col].dropna().astype(str))
            for key, (regex, _) in self.patterns.items():
                if regex.search(text_blob):
                    detected.append(key)
            if detected:
                findings[col] = detected
        return findings


class SecureCleanup:
    def __init__(self):
        self._temp_paths = []
        atexit.register(self.cleanup_all)

    def create_temp_dir(self, prefix='sdi_'):
        d = Path(tempfile.mkdtemp(prefix=prefix))
        self._temp_paths.append(d)
        return d

    def create_temp_file(self, suffix='.tmp', prefix='sdi_'):
        fd, path = tempfile.mkstemp(suffix=suffix, prefix=prefix)
        os.close(fd)
        p = Path(path)
        self._temp_paths.append(p)
        return p

    def cleanup_all(self):
        for p in reversed(self._temp_paths):
            try:
                if p.is_dir():
                    shutil.rmtree(p, ignore_errors=True)
                elif p.exists():
                    p.unlink(missing_ok=True)
            except Exception:
                pass
        self._temp_paths.clear()

    def release_memory(self, *objects):
        for obj in objects:
            del obj
        gc.collect()


@contextmanager
def secure_context():
    class _Ctx:
        def __init__(self):
            self.masker = DataMasker()
            self.cleanup = SecureCleanup()
    ctx = _Ctx()
    try:
        yield ctx
    finally:
        ctx.cleanup.cleanup_all()
        gc.collect()
