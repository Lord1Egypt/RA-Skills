#!/usr/bin/env python3
"""skill-to-http-flash v2.0 params + entry 解析器

职责：
  1. resolve_entry(skill_dir, frontmatter, skill_name) — 解析 skill 入口
     优先级：frontmatter.flash.entry → 启发式扫描 → 报错
  2. extract_params(skill_name, skill_md) — LLM 提取入参 schema，失败兜底
"""

from __future__ import annotations

import json
import logging
import os
import re
import urllib.request
from pathlib import Path

logger = logging.getLogger("flash.params-gen")

# ────────────────────────────────────────────────────────────────
# FALLBACK schema：当 LLM 提不到时，给一个最小可用的 schema
# v2.0 默认 message=空字段（脚本不需要时也不会报）
# ────────────────────────────────────────────────────────────────
FALLBACK_SCHEMA: dict = {
    "type": "object",
    "properties": {},
    "required": [],
    "additionalProperties": True,
}


# ============================================================
# Entry 解析（v2.0 新增）
# ============================================================

# 启发式候选入口（按优先级）
_HEURISTIC_CANDIDATES = [
    "scripts/{name}.py",
    "scripts/cli.py",
    "scripts/main.py",
    "scripts/run.py",
    "{name}.py",
    "main.py",
    "cli.py",
]


def _parse_flash_block(skill_md: str) -> dict:
    """从 SKILL.md frontmatter 解析 flash: 块（YAML 缩进格式）。

    支持：
        flash:
          entry: scripts/foo.py
          interpreter: python3
    """
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", skill_md, re.DOTALL)
    if not fm_match:
        return {}
    fm_text = fm_match.group(1)

    flash_match = re.search(r"^flash:\s*\n((?:[ \t]+\S.*\n?)+)", fm_text, re.MULTILINE)
    if not flash_match:
        return {}

    block = flash_match.group(1)
    result: dict = {}
    for line in block.split("\n"):
        if not line.strip():
            continue
        m = re.match(r"^[ \t]+([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(.*)$", line)
        if m:
            key = m.group(1)
            val = m.group(2).strip().strip('"').strip("'")
            result[key] = val
    return result


def resolve_entry(skill_dir: Path, skill_name: str, skill_md: str) -> tuple[Path, str, str]:
    """解析 skill 入口。

    Returns:
        (absolute_entry_path, relative_entry, interpreter)

    Raises:
        FileNotFoundError: 找不到任何入口。错误信息包含 SKILL.md frontmatter patch 建议。
    """
    flash_cfg = _parse_flash_block(skill_md)

    # 1. frontmatter 显式 entry
    if entry_rel := flash_cfg.get("entry"):
        entry_path = (skill_dir / entry_rel).resolve()
        if entry_path.suffix == ".sh":
            raise FileNotFoundError(
                f"Frontmatter declares shell entry '{entry_rel}', but flash v2.0 "
                f"only supports .py entries. Wrap your shell script in a Python launcher."
            )
        if entry_path.suffix != ".py":
            raise FileNotFoundError(
                f"Frontmatter declares non-Python entry '{entry_rel}'. "
                f"flash v2.0 only supports .py entries."
            )
        if not entry_path.exists():
            raise FileNotFoundError(
                f"Frontmatter declares entry '{entry_rel}' but file not found at: {entry_path}"
            )
        interpreter = flash_cfg.get("interpreter", "python3")
        return entry_path, entry_rel, interpreter

    # 2. 启发式扫描
    found_sh = []
    for pattern in _HEURISTIC_CANDIDATES:
        cand_rel = pattern.format(name=skill_name)
        cand_path = skill_dir / cand_rel
        if cand_path.exists():
            if cand_path.suffix == ".py":
                return cand_path.resolve(), cand_rel, "python3"
            elif cand_path.suffix == ".sh":
                found_sh.append(cand_rel)

    # 3. 没找到 .py 入口 → 报错
    msg_lines = [
        f"Could not find a Python entry for skill '{skill_name}' in {skill_dir}.",
        "",
        "flash v2.0 needs an explicit entry. Please add this to your SKILL.md frontmatter:",
        "",
        "    ---",
        f"    name: {skill_name}",
        "    ...",
        "    flash:",
        "      entry: scripts/<your-script>.py",
        "      # interpreter: python3  # optional, default python3",
        "    ---",
        "",
        f"Heuristic searched: {[p.format(name=skill_name) for p in _HEURISTIC_CANDIDATES]}",
    ]
    if found_sh:
        msg_lines += [
            "",
            f"Found shell entries (not supported by flash v2.0): {found_sh}",
            "Wrap them in a Python launcher (e.g. scripts/cli.py) that does subprocess.run(['bash', ...]).",
        ]
    raise FileNotFoundError("\n".join(msg_lines))


# ============================================================
# Params schema extraction (LLM + fallback)
# ============================================================

EXTRACTION_SYSTEM_PROMPT = """You are a JSON schema generator. Given a SKILL.md file content, extract all configurable parameters that the skill's CLI entry script expects as input.

Output ONLY a valid JSON object (no markdown fences, no extra text) with this structure:

{
  "type": "object",
  "properties": {
    "param_name": {
      "type": "string|number|boolean|array|object",
      "description": "参数说明",
      "default": null
    }
  },
  "required": ["param1"],
  "additionalProperties": false
}

Rules:
- Extract parameters that map to CLI flags (--foo value / --bar)
- Field names MUST be lowercase snake_case (match [a-z][a-z0-9_]*)
- Use the skill's documented parameter names
- Mark required params in the "required" array
- If no clear params can be inferred, return: {"type":"object","properties":{},"required":[],"additionalProperties":true}
- Output pure JSON, no markdown backticks, no commentary
"""


def extract_params(skill_name: str, skill_md: str, llm_config: dict | None = None) -> dict:
    """为指定 Skill 提取参数 schema。"""
    schema = _extract_with_llm(skill_name, skill_md, llm_config)
    if schema:
        return schema
    import copy
    logger.info(f"Using fallback schema for '{skill_name}'")
    return copy.deepcopy(FALLBACK_SCHEMA)


def _extract_with_llm(skill_name: str, skill_md: str, llm_config: dict | None = None) -> dict | None:
    cfg = llm_config or _load_config()
    llm_cfg = cfg.get("llm", {})

    base_url = _resolve_env(llm_cfg.get("base_url", ""))
    api_key = _resolve_env(llm_cfg.get("api_key", ""))
    model = llm_cfg.get("model", "gpt-4o")

    if not base_url or not api_key:
        logger.debug("LLM not configured, skipping params extraction")
        return None

    skill_md_truncated = skill_md[:6000]

    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": EXTRACTION_SYSTEM_PROMPT},
            {"role": "user", "content": f"SKILL.md for '{skill_name}':\n\n{skill_md_truncated}"},
        ],
        "temperature": 0.1,
        "max_tokens": 2000,
    }).encode("utf-8")

    chat_url = f"{base_url.rstrip('/')}/chat/completions"

    req = urllib.request.Request(
        chat_url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
        content = data["choices"][0]["message"]["content"].strip()
        if content.startswith("```"):
            lines = content.split("\n")
            content = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
        schema = json.loads(content)
        if isinstance(schema, dict) and "type" in schema:
            logger.info(f"LLM extraction succeeded for '{skill_name}'")
            return schema
    except json.JSONDecodeError as e:
        logger.warning(f"Failed to parse LLM response for '{skill_name}': {e}")
    except Exception as e:
        logger.warning(f"LLM extraction failed for '{skill_name}': {e}")

    return None


def _detect_workspace_dir(env_var: str, subdir: str) -> Path:
    if env := os.environ.get(env_var):
        return Path(env).expanduser()
    workspace = os.environ.get(
        "OPENCLAW_WORKSPACE",
        str(Path.home() / ".openclaw" / "workspace"),
    )
    ws_path = Path(workspace)
    if ws_path.exists() and (ws_path / "skills").exists():
        return ws_path / subdir
    return Path.home() / subdir


def _load_config() -> dict:
    """从 flash 数据目录加载 LLM config，兼容 v1.x skill-to-http 路径。"""
    flash_dir = _detect_workspace_dir("OPENCLAW_FLASH_DATA_DIR", ".skill-to-http-flash")
    s2h_dir = _detect_workspace_dir("OPENCLAW_S2H_DATA_DIR", ".skill-to-http")
    for cfg_path in [
        flash_dir / "config.json",
        s2h_dir / "config.json",
        Path.home() / ".skill-to-http-flash" / "config.json",
        Path.home() / ".skill-to-http" / "config.json",
    ]:
        if cfg_path.exists():
            try:
                return json.loads(cfg_path.read_text())
            except Exception:
                pass
    return {}


def _resolve_env(value: str) -> str:
    if value.startswith("${") and value.endswith("}"):
        return os.environ.get(value[2:-1], "")
    return value
