#!/usr/bin/env python3
"""
ultra-memory: 会话初始化脚本
在每次新会话开始时调用，创建三层记忆结构并注入历史上下文
"""

import os
import sys
import re
import json
import hashlib
import argparse
from datetime import datetime, timezone
from pathlib import Path

# Windows 兼容：强制 stdout/stderr 使用 UTF-8
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")


_BASE_HOME = Path(os.environ.get("ULTRA_MEMORY_HOME", Path.home() / ".ultra-memory"))
ULTRA_MEMORY_HOME = _BASE_HOME  # 默认值，init_session 会根据 scope 覆盖


def _scope_to_home(scope: str) -> Path:
    """将 scope 字符串映射到独立存储子目录。

    规则：
      - 无 scope / 空字符串  →  默认根目录（向后兼容）
      - "user:alice"         →  <base>/scopes/user__alice/
      - "agent:codebot"      →  <base>/scopes/agent__codebot/
      - "alice"（无前缀）    →  <base>/scopes/user__alice/（默认补 user: 前缀）

    路径中只保留 [a-zA-Z0-9_-]，其余字符替换为 _。
    不同 scope 拥有完全独立的 sessions/ 和 semantic/ 目录，互不干扰。
    """
    scope = (scope or "").strip()
    if not scope:
        base = Path(os.environ.get("ULTRA_MEMORY_HOME", Path.home() / ".ultra-memory"))
        return base
    # 若无类型前缀，默认视为 user scope
    if ":" not in scope:
        scope = f"user:{scope}"
    # 将 ":" 替换为 "__"（可逆转换），其余特殊字符替换为 "_"
    safe = scope.replace(":", "__")
    safe = re.sub(r"[^\w\-]", "_", safe)
    base = Path(os.environ.get("ULTRA_MEMORY_HOME", Path.home() / ".ultra-memory"))
    return base / "scopes" / safe


def get_session_id(project: str = "default") -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    h = hashlib.md5(f"{project}{ts}".encode()).hexdigest()[:6]
    return f"sess_{ts}_{h}"


def init_session(project: str = "default", resume: bool = False, scope: str = "") -> dict:
    global ULTRA_MEMORY_HOME
    # 根据 scope 计算有效存储根目录
    ULTRA_MEMORY_HOME = _scope_to_home(scope)

    sessions_dir = ULTRA_MEMORY_HOME / "sessions"
    semantic_dir = ULTRA_MEMORY_HOME / "semantic"
    sessions_dir.mkdir(parents=True, exist_ok=True)
    semantic_dir.mkdir(parents=True, exist_ok=True)

    # 尝试恢复最近会话
    if resume:
        last = find_last_session(project, sessions_dir)
        if last:
            print(f"[ultra-memory] 恢复会话: {last['session_id']}")
            inject_context(last, semantic_dir)
            return last

    # 新建会话
    session_id = get_session_id(project)
    session_dir = sessions_dir / session_id
    session_dir.mkdir(parents=True, exist_ok=True)

    meta = {
        "session_id": session_id,
        "project": project,
        "scope": scope or "",
        "started_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "op_count": 0,
        "last_summary_at": None,
        "mode": detect_mode(),
    }
    with open(session_dir / "meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    # 初始化空 ops 日志
    open(session_dir / "ops.jsonl", "w", encoding="utf-8").close()

    # 注入历史上下文
    inject_context(meta, semantic_dir)

    # 更新会话索引
    update_session_index(session_id, project, semantic_dir)

    scope_label = f" [{scope}]" if scope else ""
    print(f"[ultra-memory] ✅ 会话初始化完成{scope_label}")
    print(f"[ultra-memory] session_id: {session_id}")
    print(f"[ultra-memory] 存储路径: {session_dir}")
    print(f"[ultra-memory] 运行模式: {meta['mode']}")
    if scope:
        # 打印 scoped home 路径，供调用方 export ULTRA_MEMORY_HOME
        print(f"[ultra-memory] SCOPED_HOME={ULTRA_MEMORY_HOME}")
    print("MEMORY_READY")

    return meta


def find_last_session(project: str, sessions_dir: Path) -> dict | None:
    """找到同项目最近的会话"""
    candidates = []
    for d in sessions_dir.iterdir():
        if not d.is_dir():
            continue
        meta_file = d / "meta.json"
        if not meta_file.exists():
            continue
        with open(meta_file, encoding="utf-8") as f:
            meta = json.load(f)
        if meta.get("project") == project:
            candidates.append(meta)
    if not candidates:
        return None
    candidates.sort(key=lambda x: x["started_at"], reverse=True)
    return candidates[0]


def inject_context(meta: dict, semantic_dir: Path):
    """将历史上下文注入到 stdout，供 Claude 读取"""
    profile_file = semantic_dir / "user_profile.json"
    index_file = semantic_dir / "session_index.json"

    profile = {}
    if profile_file.exists():
        with open(profile_file, encoding="utf-8") as f:
            profile = json.load(f)

    recent_sessions = []
    if index_file.exists():
        with open(index_file, encoding="utf-8") as f:
            index = json.load(f)
        recent_sessions = index.get("sessions", [])[-3:]  # 最近3个会话

    if not profile and not recent_sessions:
        return

    print("\n<!-- ULTRA-MEMORY CONTEXT INJECTION -->")
    if profile:
        stack = ", ".join(profile.get("tech_stack", []))
        projects = ", ".join(profile.get("projects", []))
        lang = profile.get("language", "zh-CN")
        print(f"**已知背景（来自记忆层）：**")
        if stack:
            print(f"- 技术栈: {stack}")
        if projects:
            print(f"- 活跃项目: {projects}")
        if lang:
            print(f"- 语言偏好: {lang}")
        patterns = profile.get("observed_patterns", [])
        for p in patterns[:2]:
            print(f"- 偏好: {p}")

    if recent_sessions:
        print(f"\n**近期会话记录：**")
        for s in reversed(recent_sessions):
            ts = s.get("started_at", "")[:10]
            proj = s.get("project", "")
            summary = s.get("last_milestone", "")
            if summary:
                print(f"- [{ts}] 项目 {proj}: {summary}")

    print("<!-- END INJECTION -->\n")


def detect_mode() -> str:
    """检测运行环境，决定使用哪种存储模式"""
    try:
        import lancedb  # noqa
        return "enhanced"  # 向量检索模式
    except ImportError:
        return "lightweight"  # 纯文件模式


def check_context_pressure(session_id: str) -> str:
    """
    检查当前会话的 context 压力，基于未压缩操作数量估算。
    输出结构化状态供 Claude 解析。

    压力级别（每隔10次操作调用一次）：
      low      — 未压缩操作 < 20
      medium   — 20 ≤ 未压缩操作 < 40（留意增长）
      high     — 40 ≤ 未压缩操作 < 60（建议压缩）
      critical — 未压缩操作 ≥ 60（立即压缩）

    Returns:
        压力级别字符串（low/medium/high/critical）
    """
    session_dir = ULTRA_MEMORY_HOME / "sessions" / session_id
    meta_file = session_dir / "meta.json"

    op_count = 0
    if meta_file.exists():
        with open(meta_file, encoding="utf-8") as f:
            meta = json.load(f)
        op_count = meta.get("op_count", 0)

    # 统计自上次压缩以来的未压缩操作数
    uncompressed = 0
    ops_file = session_dir / "ops.jsonl"
    if ops_file.exists():
        with open(ops_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    op = json.loads(line)
                    if not op.get("compressed"):
                        uncompressed += 1
                except json.JSONDecodeError:
                    continue

    if uncompressed >= 60:
        level = "critical"
        advice = "立即触发摘要压缩，保留最近 20 条操作"
    elif uncompressed >= 40:
        level = "high"
        advice = "建议触发 summarize.py 压缩"
    elif uncompressed >= 20:
        level = "medium"
        advice = "操作数适中，可继续但留意增长"
    else:
        level = "low"
        advice = "无需操作"

    print(f"CONTEXT_PRESSURE: {level}")
    print(f"[ultra-memory] 未压缩操作数: {uncompressed} | 总操作数: {op_count} | 建议: {advice}")

    if level in ("high", "critical"):
        print(f"[ultra-memory] ⚡ 建议运行: python3 scripts/summarize.py --session {session_id}")

    return level


def update_session_index(session_id: str, project: str, semantic_dir: Path):
    index_file = semantic_dir / "session_index.json"
    index = {"sessions": []}
    if index_file.exists():
        with open(index_file, encoding="utf-8") as f:
            index = json.load(f)
    index["sessions"].append({
        "session_id": session_id,
        "project": project,
        "started_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "last_milestone": None,
    })
    # 只保留最近 100 个会话记录
    index["sessions"] = index["sessions"][-100:]
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ultra-memory 会话初始化")
    parser.add_argument("--project", default="default", help="项目名称")
    parser.add_argument("--resume", action="store_true", help="尝试恢复最近会话")
    parser.add_argument("--check-pressure", metavar="SESSION_ID", help="检查指定会话的 context 压力")
    parser.add_argument(
        "--scope", default="",
        help="隔离 scope（如 user:alice / agent:bot1 / project:myapp）。"
             "同一 scope 内的所有会话共享独立的记忆空间，互不干扰。"
    )
    args = parser.parse_args()

    if args.check_pressure:
        check_context_pressure(args.check_pressure)
    else:
        init_session(args.project, args.resume, args.scope)
