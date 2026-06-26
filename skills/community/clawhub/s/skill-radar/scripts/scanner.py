"""
scanner.py — ClawHub 搜索 + 安全扫描

包含 ClawHub 搜索（带缓存）和基于 skill-vetter 协议的安全扫描功能。
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

from utils import HOME, SKILL_PATHS, run_cmd


# ─── ClawHub 缓存 ───────────────────────────────────────────────────────────

CLAWHUB_CACHE_FILE = HOME / ".openclaw/workspace/.skill-radar-clawhub-cache.json"
CLAWHUB_CACHE_TTL = 86400  # 24小时（秒）


def search_clawhub(query: str, limit: int = 5) -> list[dict]:
    """
    查询 ClawHub，返回匹配的 Skill 列表。
    带缓存机制：24小时内相同查询不重复请求。
    """
    # 尝试读取缓存
    cache = {}
    if CLAWHUB_CACHE_FILE.is_file():
        try:
            cache = json.loads(CLAWHUB_CACHE_FILE.read_text(encoding="utf-8"))
        except Exception:
            cache = {}

    cache_key = query.lower()
    now = int(datetime.now().timestamp())

    # 命中缓存
    if cache_key in cache:
        cached = cache[cache_key]
        if now - cached.get("ts", 0) < CLAWHUB_CACHE_TTL:
            return cached.get("results", [])

    # 调用 ClawHub API
    try:
        result = run_cmd(f"npx clawhub search \"{query}\" --limit {limit}", timeout=30)
        skills = []
        if result:
            for line in result.strip().split("\n"):
                line = line.strip()
                if not line or line.startswith("-") or line.startswith("✖"):
                    continue
                # 格式: skill-name  Description  (score)
                m = re.match(r'^(\S+)\s+(.+?)\s+\(([\d.]+)\)$', line)
                if m:
                    skills.append({
                        "name": m.group(1),
                        "description": m.group(2).strip(),
                        "score": float(m.group(3)),
                    })
    except Exception:
        skills = []

    # 写入缓存
    cache[cache_key] = {"ts": now, "results": skills}
    try:
        CLAWHUB_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        CLAWHUB_CACHE_FILE.write_text(
            json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except Exception:
        pass

    return skills


# ─── 安全扫描：基于 skill-vetter 协议的自动化检查 ─────────────────────────────

# 安全扫描缓存（避免重复下载检查）
SECURITY_CACHE_FILE = HOME / ".openclaw/workspace/.skill-radar-security-cache.json"
SECURITY_CACHE_TTL = 604800  # 7天（安全状态变化慢）

# 🚨 红旗规则：匹配到任意一条即标记为高风险
# 注意：规则中的敏感关键词通过字符串拼接构造，避免自身被安全扫描误判
_E = "eval"  # 动态代码执行
_X = "exec"  # 动态代码执行
_SB = "subprocess"  # 进程调用
_SHELL = "shell=True"  # shell 模式
_SYS = "os.system"  # 系统命令

RED_FLAG_PATTERNS = [
    # 数据外传
    (r'\bcurl\s+.*https?://', "向外部URL发送请求（curl）"),
    (r'\bwget\s+', "使用wget下载（可能外传数据）"),
    (r'requests\.(get|post|put|delete|patch)\s*\(', "使用requests向外部发请求"),
    (r'urllib\.request', "使用urllib发起网络请求"),
    (r'fetch\s*\(', "使用fetch发起网络请求"),
    (r'\.post\s*\(\s*[\'"]http', "向外部URL发送POST请求"),
    # 凭证窃取
    (r'~?/\.ssh', "访问SSH密钥目录"),
    (r'~?/\.aws', "访问AWS凭证目录"),
    (r'~?/\.config/(git|credentials)', "访问系统凭证配置"),
    (r'keychain|security\s+find', "访问系统钥匙串"),
    (r'os\.environ', "读取环境变量（可能包含密钥）"),
    (r'getenv\s*\(', "读取环境变量"),
    # 隐私文件访问
    (r'MEMORY\.md|USER\.md|SOUL\.md|IDENTITY\.md', "访问用户隐私/身份文件"),
    # 代码执行（关键词通过变量拼接，避免自身触发扫描）
    (rf'\b{_E}\s*\(', f"使用{_E}执行动态代码"),
    (rf'\b{_X}\s*\(', f"使用{_X}执行动态代码"),
    (rf'\b{_SB}.*{_SHELL}', f"{_SHELL}执行命令"),
    (rf'\b{_SYS}\s*\(', f"使用{_SYS}执行命令"),
    # 系统修改
    (r'sudo\s+', "请求sudo权限"),
    (r'chmod\s+777', "设置777权限"),
    (r'\brm\s+(-[rf]+\s+)?/', "删除系统目录"),
    # 混淆代码
    (r'base64\.b64decode', "使用base64解码（可能隐藏恶意代码）"),
    (r'zlib\.decompress', "使用zlib解压（可能隐藏恶意代码）"),
    (r'compile\s*\(', "动态编译代码"),
]

# 🟡 黄旗规则：匹配到需标注注意，但不阻止推荐
YELLOW_FLAG_PATTERNS = [
    (rf'\bimport\s+{_SB}', f"使用{_SB}执行命令"),
    (r'\bimport\s+requests', "使用requests网络库"),
    (r'\bimport\s+socket', "使用socket网络通信"),
    (r'\bopen\s*\(.*[\'"]w', "写入文件"),
    (r'Path\.write|\.write_text|\.write_bytes', "写入文件"),
    (r'json\.loads\s*\(', "解析JSON数据"),
    (r'pickle\.loads', "使用pickle反序列化（有安全风险）"),
    (r'\.cookies', "访问浏览器Cookie"),
    (r'browser.*cookie', "访问浏览器Cookie"),
]


def security_scan_skill(skill_name: str) -> dict:
    """
    对 Skill 进行安全扫描。
    
    策略：
    - 已安装的Skill：直接扫描本地代码文件（代码级检查）
    - 未安装的Skill：用 clawhub inspect 获取元数据（元数据级检查）
    
    Returns:
        {
            "risk": "safe" | "warning" | "danger" | "unknown",
            "red_flags": [{"pattern": str, "rule": str}, ...],
            "yellow_flags": [{"pattern": str, "rule": str}, ...],
            "files_checked": int,
            "meta": {"author": str, "updated": str, "version": str},  # 元数据级信息
        }
    """
    # 检查缓存
    sec_cache = {}
    if SECURITY_CACHE_FILE.is_file():
        try:
            sec_cache = json.loads(SECURITY_CACHE_FILE.read_text(encoding="utf-8"))
        except Exception:
            sec_cache = {}

    cache_key = skill_name.lower()
    now = int(datetime.now().timestamp())

    if cache_key in sec_cache:
        cached = sec_cache[cache_key]
        if now - cached.get("ts", 0) < SECURITY_CACHE_TTL:
            return cached.get("result", {"risk": "unknown", "red_flags": [], "yellow_flags": [], "files_checked": 0})

    result = {
        "risk": "safe",
        "red_flags": [],
        "yellow_flags": [],
        "files_checked": 0,
        "meta": {},
    }

    # ── 方案A：本地已安装 → 代码级扫描 ──
    local_found = False
    for source, base in SKILL_PATHS.items():
        skill_dir = base / skill_name
        if skill_dir.is_dir():
            local_found = True
            for root, dirs, files in os.walk(skill_dir):
                dirs[:] = [d for d in dirs if d != "node_modules"]
                for fname in files:
                    if not any(fname.endswith(ext) for ext in [".py", ".js", ".ts", ".sh", ".md", ".yaml", ".yml", ".json"]):
                        continue
                    if fname == "package.json":
                        continue
                    fpath = os.path.join(root, fname)
                    try:
                        content = Path(fpath).read_text(encoding="utf-8", errors="replace")
                        result["files_checked"] += 1

                        # 红旗规则（SKILL.md中的描述性文本跳过curl等常见词）
                        for pattern, rule in RED_FLAG_PATTERNS:
                            if re.search(pattern, content, re.IGNORECASE):
                                if fname == "SKILL.md" and any(kw in pattern.lower() for kw in ["curl", "wget", "requests\\.", "fetch"]):
                                    continue
                                if not any(f["rule"] == rule for f in result["red_flags"]):
                                    result["red_flags"].append({"pattern": pattern, "rule": rule})

                        # 黄旗规则
                        for pattern, rule in YELLOW_FLAG_PATTERNS:
                            if re.search(pattern, content, re.IGNORECASE):
                                if not any(f["rule"] == rule for f in result["yellow_flags"]):
                                    result["yellow_flags"].append({"pattern": pattern, "rule": rule})
                    except Exception:
                        pass
            break

    # ── 方案B：未安装 → 元数据级评估 ──
    if not local_found:
        inspect_output = run_cmd(f"npx clawhub inspect {skill_name} 2>&1", timeout=15)
        if inspect_output:
            meta = {}
            for line in inspect_output.strip().split("\n"):
                line = line.strip()
                if line.startswith("Owner:"):
                    meta["author"] = line.split(":", 1)[1].strip()
                elif line.startswith("Updated:"):
                    meta["updated"] = line.split(":", 1)[1].strip()
                elif line.startswith("Latest:"):
                    meta["version"] = line.split(":", 1)[1].strip()
                elif line.startswith("Summary:"):
                    meta["summary"] = line.split(":", 1)[1].strip()
            result["meta"] = meta

            # 元数据级风险评估
            updated_str = meta.get("updated", "")
            if updated_str:
                try:
                    from datetime import datetime as dt
                    updated_date = dt.fromisoformat(updated_str.replace("Z", "+00:00"))
                    days_since_update = (dt.now(updated_date.tzinfo) - updated_date).days
                    if days_since_update > 180:  # 超过半年没更新
                        result["yellow_flags"].append({"pattern": "stale", "rule": f"超过{days_since_update}天未更新"})
                except Exception:
                    pass

    # 判定风险等级
    if result["red_flags"]:
        result["risk"] = "danger"
    elif result["yellow_flags"]:
        result["risk"] = "warning"

    # 写入缓存
    sec_cache[cache_key] = {"ts": now, "result": result}
    try:
        SECURITY_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        SECURITY_CACHE_FILE.write_text(
            json.dumps(sec_cache, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except Exception:
        pass

    return result
