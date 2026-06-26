#!/usr/bin/env python3
"""
ultra-memory: 操作日志写入脚本
每次工具调用、文件变更、命令执行后调用，追加写入 ops.jsonl
"""

import os
import sys
import json
import re
import time
import logging
import argparse
import contextlib
from datetime import datetime, timezone
from pathlib import Path

logging.basicConfig(
    level=logging.WARNING,
    format="[ultra-memory] %(levelname)s %(message)s",
)
_log = logging.getLogger("ultra-memory.log_op")


@contextlib.contextmanager
def _advisory_lock(lock_path: Path, timeout: float = 5.0):
    """跨平台建议性文件锁（.lock 哨兵文件）"""
    deadline = time.monotonic() + timeout
    acquired = False
    while True:
        try:
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
            acquired = True
            break
        except FileExistsError:
            if time.monotonic() >= deadline:
                _log.warning("文件锁等待超时 %s，直接继续写入", lock_path)
                break
            time.sleep(0.05)
    try:
        yield
    finally:
        if acquired:
            try:
                lock_path.unlink(missing_ok=True)
            except Exception:
                pass

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

ULTRA_MEMORY_HOME = Path(os.environ.get("ULTRA_MEMORY_HOME", Path.home() / ".ultra-memory"))

# 记忆注入标记（防止反馈环：AI 把自己的记忆输出又记录进去导致自引用积累）
MEMORY_INJECTION_PATTERNS = [
    r'\[ultra-memory\][^\n]*',           # 脚本自身的打印输出
    r'MEMORY_READY[^\n]*',               # 初始化信号
    r'COMPRESS_SUGGESTED[^\n]*',         # 压缩建议信号
    r'SESSION_ID=sess_[A-Za-z0-9_]+',   # 会话 ID 注入
    r'session_id:\s*sess_[A-Za-z0-9_]+',
    r'\[RECALL\][^\n]*',                 # recall.py 的输出头
    r'\[ops #\d+[^\]]*\][^\n]*',        # format_result 的 ops 格式
    r'\[知识库[^\]]*\][^\n]*',           # format_result 的知识库格式
    r'\[实体/[^\]]*\][^\n]*',           # format_result 的实体格式
    r'\[摘要\][^\n]*',                   # format_result 的摘要格式
]

# 敏感词正则（防止记录密码/密钥）
SENSITIVE_PATTERNS = [
    r'(?i)(password|passwd|pwd)\s*[=:]\s*\S+',
    r'(?i)(api[_-]?key|secret[_-]?key|access[_-]?token)\s*[=:]\s*\S+',
    r'(?i)bearer\s+[A-Za-z0-9\-._~+/]+=*',
    r'[A-Za-z0-9]{32,}',  # 长随机字符串（可能是 token）
]

# 敏感键名集合：无论值长短，都直接脱敏
SENSITIVE_KEYS: frozenset[str] = frozenset({
    "password", "passwd", "pwd",
    "api_key", "apikey", "api-key",
    "secret", "secret_key", "client_secret",
    "access_token", "refresh_token", "auth_token", "id_token",
    "bearer", "token", "private_key",
})

OP_TYPES = [
    "tool_call", "file_write", "file_read",
    "bash_exec", "reasoning", "user_instruction",
    "decision", "error", "milestone"
]

# 操作类型基础重要性（0.0-1.0）
_IMPORTANCE_OP_BASE = {
    "milestone": 1.0,
    "decision": 0.9,
    "user_instruction": 0.85,
    "error": 0.8,
    "reasoning": 0.5,
    "file_write": 0.4,
    "bash_exec": 0.35,
    "file_read": 0.2,
    "tool_call": 0.2,
}

# 关键词 → 重要性加分（取最大值，不叠加）
_IMPORTANCE_KEYWORDS = [
    ("critical",  0.3), ("重要", 0.3), ("必须", 0.3), ("关键", 0.3),
    ("error",     0.25), ("failed", 0.25), ("exception", 0.2),
    ("decision",  0.2), ("fix",  0.2), ("修复", 0.2),
    ("完成",      0.2), ("done", 0.2), ("✅", 0.2),
    ("deploy",    0.2), ("release", 0.2), ("发布", 0.2),
    ("bug",       0.15), ("issue", 0.1), ("warning", 0.1),
]


def _compute_importance(op_type: str, summary: str, detail: dict) -> float:
    """计算操作重要性分数（0.0–1.0），写入时评分，检索时乘权加分。
    基础分来自操作类型，关键词加分取最大值，上限 1.0。
    """
    base = _IMPORTANCE_OP_BASE.get(op_type, 0.3)
    combined = summary.lower() + " " + json.dumps(detail, ensure_ascii=False).lower()
    bonus = max(
        (weight for kw, weight in _IMPORTANCE_KEYWORDS if kw in combined),
        default=0.0,
    )
    return round(min(1.0, base + bonus), 2)

# 扩展标签体系：覆盖 setup/code/test/debug/refactor/deploy/config/data/api/ui 十大类
AUTO_TAGS = {
    # setup — 环境初始化、依赖安装
    "pip install": ["setup", "dependency"],
    "pip3 install": ["setup", "dependency"],
    "npm install": ["setup", "dependency"],
    "yarn add": ["setup", "dependency"],
    "pnpm add": ["setup", "dependency"],
    "conda install": ["setup", "dependency"],
    "apt install": ["setup", "dependency"],
    "brew install": ["setup", "dependency"],
    "初始化": ["setup"],
    "安装": ["setup", "dependency"],
    # code — 代码编写
    "def ": ["code"],
    "class ": ["code"],
    "function ": ["code"],
    "import ": ["code"],
    "async def": ["code"],
    "const ": ["code"],
    "let ": ["code"],
    "写代码": ["code"],
    "实现": ["code"],
    # test — 测试
    "pytest": ["test"],
    "unittest": ["test"],
    "jest ": ["test"],
    "vitest": ["test"],
    "测试": ["test"],
    "test_": ["test"],
    "assert": ["test"],
    "expect(": ["test"],
    # debug — 调试
    "debug": ["debug"],
    "breakpoint": ["debug"],
    "traceback": ["debug"],
    "调试": ["debug"],
    "排查": ["debug"],
    "修复": ["debug"],
    "fix": ["debug"],
    # refactor — 重构
    "refactor": ["refactor"],
    "重构": ["refactor"],
    "rename": ["refactor"],
    "extract": ["refactor"],
    "移动": ["refactor"],
    # deploy — 部署
    "docker": ["deploy"],
    "kubectl": ["deploy"],
    "helm ": ["deploy"],
    "deploy": ["deploy"],
    "部署": ["deploy"],
    "发布": ["deploy"],
    "release": ["deploy"],
    "nginx": ["deploy"],
    # config — 配置
    ".env": ["config"],
    "config": ["config"],
    "配置": ["config"],
    "settings": ["config"],
    "yaml": ["config"],
    "toml": ["config"],
    # data — 数据处理
    "dataframe": ["data"],
    "pandas": ["data"],
    "数据": ["data"],
    "clean_": ["data"],
    "preprocess": ["data"],
    "csv": ["data"],
    "json": ["data"],
    "database": ["data"],
    "sql": ["data"],
    # api — 接口调用
    "requests.": ["api"],
    "fetch(": ["api"],
    "axios": ["api"],
    "curl ": ["api"],
    "http": ["api"],
    "endpoint": ["api"],
    "接口": ["api"],
    # ui — 界面
    "component": ["ui"],
    "vue": ["ui"],
    "react": ["ui"],
    "css": ["ui"],
    "html": ["ui"],
    "界面": ["ui"],
    "页面": ["ui"],
    # vcs — 版本控制
    "git ": ["vcs"],
    "commit": ["vcs"],
    "branch": ["vcs"],
    "merge": ["vcs"],
    # error — 错误
    "error": ["error"],
    "exception": ["error"],
    "traceback": ["error"],
    "failed": ["error"],
    "失败": ["error"],
    "报错": ["error"],
    # milestone — 里程碑
    "✅": ["milestone"],
    "完成": ["milestone"],
    "done": ["milestone"],
    "finished": ["milestone"],
}

# bash 命令意图识别：命令前缀 -> 标签
BASH_INTENT_MAP = [
    (r'^pip3?\s+install', ["setup", "dependency"]),
    (r'^npm\s+(install|i\b)', ["setup", "dependency"]),
    (r'^yarn\s+add', ["setup", "dependency"]),
    (r'^pytest|^python\s+-m\s+pytest', ["test"]),
    (r'^jest|^npx\s+jest', ["test"]),
    (r'^git\s+commit', ["vcs"]),
    (r'^git\s+push', ["vcs", "deploy"]),
    (r'^git\s+', ["vcs"]),
    (r'^docker\s+', ["deploy"]),
    (r'^kubectl\s+', ["deploy"]),
    (r'^curl\s+', ["api"]),
    (r'^python3?\s+\S+\.py', ["code"]),
    (r'^node\s+', ["code"]),
    (r'^cat\s+|^head\s+|^tail\s+', ["file_read"]),
    (r'^mkdir|^touch|^cp\s+|^mv\s+', ["setup"]),
    (r'^rm\s+', ["error"]),  # 删除操作归为需要注意的操作
]

# 文件扩展名 -> 标签
FILE_EXT_TAG_MAP = {
    ".py": ["code"],
    ".js": ["code"],
    ".ts": ["code"],
    ".jsx": ["code", "ui"],
    ".tsx": ["code", "ui"],
    ".vue": ["ui"],
    ".html": ["ui"],
    ".css": ["ui"],
    ".scss": ["ui"],
    ".less": ["ui"],
    ".json": ["config"],
    ".yaml": ["config"],
    ".yml": ["config"],
    ".toml": ["config"],
    ".env": ["config"],
    ".md": ["data"],
    ".sql": ["data"],
    ".csv": ["data"],
    ".parquet": ["data"],
    ".sh": ["deploy"],
    ".dockerfile": ["deploy"],
    ".tf": ["deploy"],
    "dockerfile": ["deploy"],
    ".test.py": ["test"],
    ".spec.ts": ["test"],
    ".spec.js": ["test"],
    "_test.go": ["test"],
}


def filter_memory_markers(text: str) -> str:
    """过滤记忆注入标记，防止反馈环（AI 将自身记忆输出再次记录导致自引用噪音积累）"""
    if not text:
        return text
    for pattern in MEMORY_INJECTION_PATTERNS:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    return text.strip()


def sanitize(text: str) -> str:
    """过滤敏感信息 + 反馈环标记（仅用于纯文本字段，不要对 JSON 字符串调用）"""
    if not text:
        return text
    text = filter_memory_markers(text)
    for pattern in SENSITIVE_PATTERNS:
        text = re.sub(pattern, "[REDACTED]", text)
    return text


def sanitize_dict(obj, _parent_key: str = "") -> object:
    """递归对 dict/list 中每个字符串值单独脱敏，不破坏 JSON 结构。
    直接对序列化后的 JSON 字符串做 regex 替换会截断字符串值，产生非法 JSON。
    敏感键名（password、api_key 等）的值无论长短都直接脱敏。
    """
    if isinstance(obj, str):
        if _parent_key.lower().replace("-", "_") in SENSITIVE_KEYS:
            return "[REDACTED]"
        return sanitize(obj)
    if isinstance(obj, dict):
        return {k: sanitize_dict(v, _parent_key=k) for k, v in obj.items()}
    if isinstance(obj, list):
        return [sanitize_dict(item, _parent_key=_parent_key) for item in obj]
    return obj


def auto_tag(summary: str, detail: dict, op_type: str = "") -> list[str]:
    """根据内容自动打标签（关键词 + bash命令意图 + 文件扩展名）"""
    tags = set()
    combined = summary.lower() + " " + json.dumps(detail, ensure_ascii=False).lower()

    # 1. 关键词匹配（扩展标签体系）
    for keyword, kw_tags in AUTO_TAGS.items():
        if keyword.lower() in combined:
            tags.update(kw_tags)

    # 2. bash_exec 类型：解析命令意图
    if op_type == "bash_exec":
        cmd = detail.get("cmd", summary).strip()
        for pattern, intent_tags in BASH_INTENT_MAP:
            if re.match(pattern, cmd, re.IGNORECASE):
                tags.update(intent_tags)
                break

    # 3. file_write 类型：根据文件扩展名自动分类
    if op_type == "file_write":
        file_path = detail.get("path", "")
        if file_path:
            lower_path = file_path.lower()
            # 先检查特殊全名（如 Dockerfile）
            base = lower_path.split("/")[-1].split("\\")[-1]
            if base in FILE_EXT_TAG_MAP:
                tags.update(FILE_EXT_TAG_MAP[base])
            else:
                # 检查复合扩展名（如 .test.py）
                for ext, ext_tags in FILE_EXT_TAG_MAP.items():
                    if lower_path.endswith(ext):
                        tags.update(ext_tags)
                        break

    return list(tags)


def log_op(
    session_id: str,
    op_type: str,
    summary: str,
    detail: dict = None,
    tags: list = None,
):
    session_dir = ULTRA_MEMORY_HOME / "sessions" / session_id
    if not session_dir.exists():
        print(f"[ultra-memory] ⚠️  会话不存在: {session_id}，跳过记录")
        return

    ops_file = session_dir / "ops.jsonl"
    meta_file = session_dir / "meta.json"

    # 读取当前序号
    seq = 0
    if meta_file.exists():
        with open(meta_file, encoding="utf-8") as f:
            meta = json.load(f)
        seq = meta.get("op_count", 0) + 1
    else:
        meta = {}

    detail = detail or {}
    summary = sanitize(summary)
    detail = sanitize_dict(detail)  # 逐字段脱敏，避免破坏 JSON 结构

    auto_tags = auto_tag(summary, detail, op_type)
    all_tags = list(set((tags or []) + auto_tags))

    entry = {
        "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "seq": seq,
        "type": op_type,
        "summary": summary[:200],  # 摘要限长
        "detail": detail,
        "tags": all_tags,
        "compressed": False,
        "importance": _compute_importance(op_type, summary, detail),
        "access_count": 0,
    }

    # ── 矛盾检测（写入 ops.jsonl 之前）──────────────────────────────────────

    # 2A：画像冲突检测（user_instruction/decision + profile_update）
    if op_type in ("user_instruction", "decision") and detail.get("profile_update"):
        try:
            import sys as _sys
            _scripts_dir_cd = Path(__file__).parent
            if str(_scripts_dir_cd) not in _sys.path:
                _sys.path.insert(0, str(_scripts_dir_cd))
            from conflict_detector import detect_profile_conflict, mark_profile_superseded
            conflicts = detect_profile_conflict(detail["profile_update"], ULTRA_MEMORY_HOME)
            if conflicts:
                entry["detail"]["profile_conflicts"] = conflicts
                mark_profile_superseded(ULTRA_MEMORY_HOME, conflicts)
                print(f"[ultra-memory] ⚡ 检测到 {len(conflicts)} 处画像矛盾，旧记录已标记失效")
        except Exception as _e:
            _log.debug("画像冲突检测失败（不影响主流程）: %s", _e)

    # 2B：知识库冲突检测（milestone/decision + knowledge_entry）
    if op_type in ("milestone", "decision") and detail.get("knowledge_entry"):
        try:
            import sys as _sys
            _scripts_dir_cd = Path(__file__).parent
            if str(_scripts_dir_cd) not in _sys.path:
                _sys.path.insert(0, str(_scripts_dir_cd))
            from conflict_detector import detect_knowledge_conflict, mark_superseded
            conflicts = detect_knowledge_conflict(detail["knowledge_entry"], ULTRA_MEMORY_HOME)
            if conflicts:
                kb_path = ULTRA_MEMORY_HOME / "semantic" / "knowledge_base.jsonl"
                seq_list = [c["seq"] for c in conflicts]
                mark_superseded(ULTRA_MEMORY_HOME, kb_path, seq_list)
                entry["detail"]["knowledge_conflicts"] = conflicts
                print(f"[ultra-memory] ⚡ 检测到 {len(conflicts)} 条知识库矛盾，旧记录已标记失效")
        except Exception as _e:
            _log.debug("知识库冲突检测失败（不影响主流程）: %s", _e)

    # 追加写入（append-only，永不覆盖）；文件锁保护并发写入
    _lock_file = ops_file.with_suffix(".lock")
    with _advisory_lock(_lock_file):
        with open(ops_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        # 更新 meta（在锁内，保证 op_count 单调递增）
        meta["op_count"] = seq
        meta["last_op_at"] = entry["ts"]
        if op_type == "milestone":
            meta["last_milestone"] = summary
        _tmp_meta = meta_file.with_suffix(".tmp")
        with open(_tmp_meta, "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
        _tmp_meta.replace(meta_file)

    # 自动提取结构化实体（写入 semantic/entities.jsonl）
    try:
        import sys as _sys
        _scripts_dir = Path(__file__).parent
        if str(_scripts_dir) not in _sys.path:
            _sys.path.insert(0, str(_scripts_dir))
        from extract_entities import extract_and_store
        extract_and_store(session_id, dict(entry))
    except Exception as _e:
        _log.debug("实体提取失败（不影响主流程）: %s", _e)

    # 自动提取结构化事实（写入 evolution/facts.jsonl，异步不阻塞）
    try:
        import subprocess as _subprocess
        _scripts_dir = Path(__file__).parent
        _python = sys.executable
        _startupinfo = _subprocess.STARTUPINFO()
        _startupinfo.dwFlags |= _subprocess.STARTF_USESHOWWINDOW
        _subprocess.Popen(
            [_python, str(_scripts_dir / "extract_facts.py"),
             "--session", session_id, "--op-seq", str(seq)],
            stdout=_subprocess.DEVNULL,
            stderr=_subprocess.DEVNULL,
            start_new_session=True,
            startupinfo=_startupinfo,
        )
    except Exception:
        pass  # 事实提取失败静默跳过

    # 多模态处理：检测媒体文件并后台提取
    try:
        _media_exts = {".pdf": "extract_from_pdf.py", ".docx": "extract_from_docx.py",
                        ".png": "extract_from_image.py", ".jpg": "extract_from_image.py",
                        ".jpeg": "extract_from_image.py",
                        ".mp4": "transcribe_video.py", ".avi": "transcribe_video.py",
                        ".mov": "transcribe_video.py"}
        _file_path = detail.get("path", "")
        if _file_path and op_type in ("file_read", "file_write"):
            _ext = Path(_file_path).suffix.lower()
            if _ext in _media_exts:
                _script = _media_exts[_ext]
                _multimodal_dir = Path(__file__).parent / "multimodal"
                if (_multimodal_dir / _script).exists():
                    _subprocess.Popen(
                        [_python, str(_multimodal_dir / _script),
                         "--session", session_id, "--path", _file_path],
                        stdout=_subprocess.DEVNULL,
                        stderr=_subprocess.DEVNULL,
                        start_new_session=True,
                        startupinfo=_startupinfo,
                    )
    except Exception:
        pass  # 多模态提取失败静默跳过

    # 检查是否需要触发压缩
    should_compress = False
    if seq > 0 and seq % 50 == 0:
        should_compress = True
        print(f"[ultra-memory] ⚡ 操作日志已达 {seq} 条，建议触发摘要压缩")
        print(f"[ultra-memory] 运行: python3 scripts/summarize.py --session {session_id}")

    print(f"[ultra-memory] 📝 [{seq}] {op_type}: {summary[:60]}")
    if should_compress:
        print("[ultra-memory] COMPRESS_SUGGESTED")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="记录操作日志")
    parser.add_argument("--session", required=True, help="会话 ID")
    parser.add_argument("--type", required=True, choices=OP_TYPES, dest="op_type")
    parser.add_argument("--summary", required=True, help="操作摘要（中英文均可）")
    parser.add_argument("--detail", default="{}", help="详情 JSON 字符串")
    parser.add_argument("--tags", default="", help="逗号分隔的标签")
    args = parser.parse_args()

    detail = json.loads(args.detail)
    tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    log_op(args.session, args.op_type, args.summary, detail, tags)
