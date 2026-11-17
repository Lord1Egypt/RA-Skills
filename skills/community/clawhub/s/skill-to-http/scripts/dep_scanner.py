#!/usr/bin/env python3
"""skill-to-http Dependency Scanner

扫描 Skill 的依赖关系（L1/L3/L4 三层策略），
结果持久化到 ~/.skill-to-http/skill_deps.json。
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path

logger = logging.getLogger("skill-to-http.dep_scanner")

from _paths import DEPS_FILE

# ── 常量 ─────────────────────────────────────────────────────────────

# L1: SKILL.md 中表示依赖关系的关键词
L1_KEYWORDS = [
    r"调用\s*[「\"]?([a-z][a-z0-9\-]+)[」\"]?\s*skill",
    r"依赖\s*[「\"]?([a-z][a-z0-9\-]+)[」\"]?",
    r"使用\s*[「\"]?([a-z][a-z0-9\-]+)[」\"]?\s*skill",
    r"参考\s*[「\"]?([a-z][a-z0-9\-]+)[」\"]?\s*skill",
    r"requires?\s+skill\s+[`'\"]([a-z][a-z0-9\-]+)[`'\"]",
    r"calls?\s+[`'\"]([a-z][a-z0-9\-]+)[`'\"]",
    r"\bskill[:\s]+([a-z][a-z0-9\-]+)",
]

# L4: 跨 skill 目录的路径/模块引用模式
L4_PATTERNS = [
    # ../other-skill/  或  ../../other-skill/
    (r"\.\./+([a-z][a-z0-9\-]+)/", "relative path"),
    # skills/other-skill/
    (r"skills/([a-z][a-z0-9\-]+)/", "skills path"),
    # from other_skill import  （snake_case → kebab-case）
    (r"from\s+([a-z][a-z0-9_]+)\s+import", "python import"),
    # require('...other-skill/...')
    (r"""require\s*\(\s*['"].*?([a-z][a-z0-9\-]+)/""", "js require"),
    # source ./other-skill/scripts/xxx.sh
    (r"source\s+\S*?([a-z][a-z0-9\-]+)/", "shell source"),
]

# 代码文件扩展名（L4 扫描范围）
CODE_EXTS = {".py", ".sh", ".js", ".ts", ".bash"}


# ── 持久化 ────────────────────────────────────────────────────────────

def load_deps() -> dict:
    """加载 skill_deps.json，返回空 dict 若不存在。"""
    if DEPS_FILE.exists():
        try:
            return json.loads(DEPS_FILE.read_text())
        except Exception as e:
            logger.warning("Failed to load skill_deps.json: %s", e)
    return {}


def save_deps(data: dict) -> None:
    """持久化 skill_deps.json。"""
    DEPS_FILE.parent.mkdir(parents=True, exist_ok=True)
    DEPS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))


def get_skill_deps(skill_name: str) -> dict | None:
    """获取单个 skill 的依赖记录，不存在返回 None。"""
    return load_deps().get(skill_name)


def set_skill_deps(skill_name: str, record: dict) -> None:
    """更新单个 skill 的依赖记录。"""
    data = load_deps()
    data[skill_name] = record
    save_deps(data)


# ── 扫描核心 ─────────────────────────────────────────────────────────

def _all_skill_names(skill_dirs: list[str]) -> set[str]:
    """快速收集所有已知 skill 名称（只读目录名 + frontmatter name）。"""
    names: set[str] = set()
    _frontmatter_re = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
    for d in skill_dirs:
        p = Path(d).expanduser().resolve()
        if not p.is_dir():
            continue
        for subdir in p.iterdir():
            if subdir.is_dir():
                names.add(subdir.name)
                skill_md = subdir / "SKILL.md"
                if skill_md.exists():
                    try:
                        txt = skill_md.read_text(errors="replace")[:2000]
                        m = _frontmatter_re.match(txt)
                        if m:
                            for line in m.group(1).split("\n"):
                                if line.strip().startswith("name:"):
                                    names.add(line.split(":", 1)[1].strip().strip('"\''))
                    except Exception as e:
                        logger.debug("Failed to read skill frontmatter %s: %s", subdir, e)
    return names


def scan(
    skill_name: str,
    skill_meta: dict,
    skill_dirs: list[str],
) -> dict:
    """
    扫描 skill 依赖，返回：
    {
      "deps": ["skill-a", "skill-b"],
      "confidence": "high" | "low",
      "evidence": ["描述..."],
      "scan_layers": ["L1", "L3", "L4"],
    }
    """
    skill_path = Path(skill_meta.get("path", ""))
    skill_md_content = skill_meta.get("skill_md", "")
    known_skills = _all_skill_names(skill_dirs) - {skill_name}

    found: dict[str, list[str]] = {}  # dep_name → [evidence...]
    layers_hit: set[str] = set()

    # ── L3: params.json dependencies 字段（最高可信度）─────────────
    # Path('') is truthy 但不是绝对路径，必须用 is_absolute() 守卫避免扫描 CWD
    params_json = skill_path / "params.json" if (skill_path and skill_path.is_absolute()) else None
    if params_json and params_json.exists():
        try:
            params_data = json.loads(params_json.read_text())
            for dep in params_data.get("dependencies", []):
                dep = dep.strip()
                if dep and dep != skill_name:
                    found.setdefault(dep, []).append(f"L3: params.json[dependencies]")
                    layers_hit.add("L3")
        except Exception:
            pass

    # ── L1: SKILL.md 关键词扫描 ───────────────────────────────────
    for pattern in L1_KEYWORDS:
        for m in re.finditer(pattern, skill_md_content, re.IGNORECASE | re.MULTILINE):
            candidate = m.group(1).strip().lower().replace("_", "-")
            if candidate in known_skills and candidate != skill_name:
                # 找到匹配行
                line_no = skill_md_content[:m.start()].count("\n") + 1
                line_text = skill_md_content.splitlines()[line_no - 1].strip()[:80]
                found.setdefault(candidate, []).append(
                    f"L1: SKILL.md:{line_no}: {line_text}"
                )
                layers_hit.add("L1")

    # ── L4: 代码文件跨 skill 目录引用 ─────────────────────────────
    # 注意：Path('') 会解析为当前目录！必须确保 path 非空且是绝对路径
    if skill_path and str(skill_meta.get('path', '')) and skill_path.is_dir() and skill_path.is_absolute():
        code_files: list[Path] = []
        _SKIP_DIRS = {'node_modules', '.git', '__pycache__', '.venv', 'venv', 'dist', 'build'}
        _MAX_FILE_SIZE = 512 * 1024  # 512 KB
        for ext in CODE_EXTS:
            for f in skill_path.rglob(f"*{ext}"):
                if any(part in _SKIP_DIRS for part in f.parts):
                    continue
                try:
                    if f.stat().st_size > _MAX_FILE_SIZE:
                        continue
                except OSError:
                    continue
                code_files.append(f)

        for code_file in code_files:
            try:
                content = code_file.read_text(errors="replace")
            except Exception:
                continue

            rel = code_file.relative_to(skill_path) if skill_path else code_file

            for pattern, desc in L4_PATTERNS:
                for m in re.finditer(pattern, content, re.IGNORECASE):
                    candidate = m.group(1).strip().lower().replace("_", "-")
                    if candidate in known_skills and candidate != skill_name:
                        line_no = content[:m.start()].count("\n") + 1
                        line_text = content.splitlines()[line_no - 1].strip()[:80]
                        found.setdefault(candidate, []).append(
                            f"L4: {rel}:{line_no} ({desc}): {line_text}"
                        )
                        layers_hit.add("L4")

    # ── 汇总结果 ─────────────────────────────────────────────────
    deps = sorted(found.keys())
    evidence = []
    for dep, evs in sorted(found.items()):
        evidence.extend(evs[:3])  # 每个依赖最多 3 条证据

    # 置信度：L3 命中或 L4 命中 → high；仅 L1 → low
    high_layers = layers_hit & {"L3", "L4"}
    confidence = "high" if high_layers else ("low" if deps else "high")

    return {
        "deps": deps,
        "confidence": confidence,
        "evidence": evidence,
        "scan_layers": sorted(layers_hit) if layers_hit else [],
    }
