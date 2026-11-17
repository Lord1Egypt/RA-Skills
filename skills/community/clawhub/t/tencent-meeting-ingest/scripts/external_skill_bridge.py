import json
import os
import shlex
import subprocess
from pathlib import Path


def parse_jsonish(value):
    if isinstance(value, (dict, list)):
        return value
    text = str(value or "").strip()
    if not text:
        return text
    try:
        return json.loads(text)
    except Exception:
        return text


def run_external_command(command, extra_args=None, timeout=180):
    if not command:
        raise RuntimeError("外部 skill 命令未配置")
    args = shlex.split(command) + list(extra_args or [])
    completed = subprocess.run(
        args,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )
    stdout = (completed.stdout or "").strip()
    stderr = (completed.stderr or "").strip()
    if completed.returncode != 0:
        raise RuntimeError(stderr or stdout or f"命令退出码 {completed.returncode}")
    return parse_jsonish(stdout)


def scripts_dir():
    return Path(__file__).resolve().parent


def skill_dir():
    return scripts_dir().parent


def skills_root():
    return skill_dir().parent


def find_sibling_file(*parts):
    candidate = skills_root().joinpath(*parts)
    return candidate if candidate.exists() else None


def text_from_any(value, preferred_keys=None, max_chars=120000):
    preferred_keys = preferred_keys or ["text", "content", "summary", "minutes", "paragraph", "transcript", "raw_content"]
    chunks = []

    def walk(node, key_hint=""):
        if sum(len(item) for item in chunks) >= max_chars:
            return
        if isinstance(node, dict):
            for key, child in node.items():
                walk(child, key)
        elif isinstance(node, list):
            for child in node:
                walk(child, key_hint)
        elif isinstance(node, str):
            text = node.strip()
            if not text:
                return
            if key_hint in preferred_keys or len(text) > 40:
                chunks.append(text)

    walk(value)
    return "\n\n".join(chunks)[:max_chars]


def find_first_key(obj, keys):
    if isinstance(obj, dict):
        for key in keys:
            if key in obj and obj[key] not in (None, "", []):
                return obj[key]
        for child in obj.values():
            found = find_first_key(child, keys)
            if found not in (None, "", []):
                return found
    elif isinstance(obj, list):
        for child in obj:
            found = find_first_key(child, keys)
            if found not in (None, "", []):
                return found
    return None