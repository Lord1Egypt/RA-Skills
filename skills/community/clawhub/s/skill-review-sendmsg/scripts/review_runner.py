#!/usr/bin/env python3
import json
import os
import re
import subprocess
import time
import uuid
import html
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

import requests
from dotenv import load_dotenv

# 自动加载项目根目录 .env（无需每次手动 source）
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

TARGET_EXT = {".php", ".js", ".ts", ".sql", ".sh"}
EXCLUDE_PREFIX = ("vendor/", "node_modules/", "dist/", "build/")

BASE_DIR = Path(os.getenv("REVIEW_BASE_DIR", "/home/skill/py-review/.state"))
STATE_DIR = BASE_DIR / "state"
WORK_DIR = BASE_DIR / "repos"
LOCK_DIR = BASE_DIR / "lock"

LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_API_URL = os.getenv("LLM_API_URL", "https://api.deepseek.com/v1/chat/completions")
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-chat")
BATCH_SIZE = int(os.getenv("DIFF_BATCH_SIZE", "8"))
MAX_DIFF_CHARS = int(os.getenv("MAX_DIFF_CHARS", "120000"))
REVIEW_MODE = os.getenv("REVIEW_MODE", "full").strip().lower()  # full|local|llm

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "")
TG_CHAT_ID = os.getenv("TG_CHAT_ID", "")

PROJECTS_DATA = os.getenv("PROJECTS_DATA", "")
LOG_DIR = Path(os.getenv("REVIEW_LOG_DIR", "/home/skill/py-review-skill/logs"))
LOG_BASE_URL = os.getenv("REVIEW_LOG_BASE_URL", "").rstrip("/")


def run(cmd: List[str], cwd: Path = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True, capture_output=True)


def notify(msg: str, log_file: str = ""):
    if not TG_BOT_TOKEN or not TG_CHAT_ID:
        return

    # 防止 HTML 解析失败（例如作者字段里的 <email>）
    safe_msg = html.escape(msg)
    safe_msg = safe_msg.replace("&lt;b&gt;", "<b>").replace("&lt;/b&gt;", "</b>")

    try:
        # 单条消息发送：有日志文件时，走 sendDocument + caption；否则 sendMessage
        if log_file and Path(log_file).exists():
            with open(log_file, "rb") as f:
                r = requests.post(
                    f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendDocument",
                    data={
                        "chat_id": TG_CHAT_ID,
                        "caption": safe_msg[:950],  # 预留余量，避免1024上限失败
                        "parse_mode": "HTML",
                    },
                    files={"document": (Path(log_file).name, f, "text/plain")},
                    timeout=30,
                )
            if r.status_code != 200:
                # 降级：至少发一条纯文本，避免“无通知”
                requests.post(
                    f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage",
                    json={"chat_id": TG_CHAT_ID, "text": msg[:3900], "disable_web_page_preview": True},
                    timeout=15,
                )
        else:
            requests.post(
                f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage",
                json={
                    "chat_id": TG_CHAT_ID,
                    "text": safe_msg[:3900],
                    "parse_mode": "HTML",
                    "disable_web_page_preview": True,
                },
                timeout=15,
            )
    except Exception:
        # 最后兜底（纯文本）
        try:
            requests.post(
                f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage",
                json={"chat_id": TG_CHAT_ID, "text": msg[:3900], "disable_web_page_preview": True},
                timeout=15,
            )
        except Exception:
            pass


def save_review_log(res: Dict[str, Any], project_name: str) -> str:
    ts = datetime.now().strftime('%Y%m%d%H%M%S')
    suffix = uuid.uuid4().hex[:6]
    safe_name = re.sub(r'[\\/:*?"<>|]+', '-', project_name).strip() or "project"
    file_name = f"{safe_name}-{ts}-{suffix}.log"
    p = LOG_DIR / file_name

    status = res.get("status", "")
    lines = [
        "部署更新通知",
        f"项目名称: {project_name}",
        f"代码分支: {res.get('branch', '')}",
        f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"更新人员: {res.get('author', '')}",
        f"更新描述: {res.get('subject', '')}",
        f"返回结果: {status}",
        "",
    ]

    # 本地检测未通过：写清文件、行号、原因
    if status == "fail-local":
        lines.append("【本地检测未通过详情】")
        for i, it in enumerate(res.get("local_issues", []), 1):
            lines.append(f"{i}. 文件: {it.get('file', '?')}")
            lines.append(f"   行号: {it.get('line', 0)}")
            lines.append(f"   工具: {it.get('tool', it.get('code', 'local-check'))}")
            lines.append(f"   原因: {it.get('message', '')}")

    # 规则阻断：写清规则、文件、行号、原因
    if status == "blocked":
        lines.append("【规则阻断详情】")
        for i, it in enumerate(res.get("blocking_items", []), 1):
            lines.append(f"{i}. 规则: {it.get('code', '?')}")
            lines.append(f"   文件: {it.get('file', '?')}")
            lines.append(f"   行号: {it.get('line', 0)}")
            lines.append(f"   原因: {it.get('reason', '')}")

    # 模型未通过：写清文件、行号、原因与建议
    if status == "fail-review":
        llm = res.get("llm", {}) if isinstance(res.get("llm"), dict) else {}
        lines.append("【模型审核未通过详情】")
        lines.append(f"风险级别: {llm.get('risk_level', '未知')}")
        lines.append(f"原因: {llm.get('release', {}).get('reason', '')}")
        issues = llm.get("major_issues", []) or []
        if issues:
            lines.append("主要问题:")
            for i, it in enumerate(issues, 1):
                lines.append(f"{i}. 文件: {it.get('file', '?')}:{it.get('line', 0)}")
                lines.append(f"   严重级别: {it.get('severity', '?')}")
                lines.append(f"   原因: {it.get('reason', '')}")
        suggestions = llm.get("suggestions", []) or []
        if suggestions:
            lines.append("修改建议:")
            for i, it in enumerate(suggestions, 1):
                lines.append(f"{i}. 文件: {it.get('file', '?')}")
                lines.append(f"   建议: {it.get('advice', '')}")

    lines.extend([
        "",
        "--- 完整结果(JSON) ---",
        json.dumps(res, ensure_ascii=False, indent=2),
    ])

    p.write_text("\n".join(lines), encoding="utf-8")
    return file_name


def build_log_link(file_name: str) -> str:
    if LOG_BASE_URL:
        return f"{LOG_BASE_URL}/{file_name}"
    return str((LOG_DIR / file_name).resolve())


def clean_local_reason(msg: str) -> str:
    txt = msg or ""
    txt = re.sub(r"\s+in\s+/.+?\s+on\s+line\s+\d+", "", txt).strip()
    return txt


def ensure_dirs():
    for d in (STATE_DIR, WORK_DIR, LOCK_DIR, LOG_DIR):
        d.mkdir(parents=True, exist_ok=True)


def parse_projects() -> List[Dict[str, str]]:
    rows = []
    for ln in PROJECTS_DATA.splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        parts = ln.split("|")
        if len(parts) < 3:
            continue
        row = {"name": parts[0], "git": parts[1], "branch": parts[2], "chat": parts[3] if len(parts) > 3 else TG_CHAT_ID}
        rows.append(row)
    return rows


def safe_key(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "_", s)


def target_file(path: str) -> bool:
    return Path(path).suffix in TARGET_EXT and not any(path.startswith(p) for p in EXCLUDE_PREFIX)


def get_changed_files(repo: Path, frm: str, to: str) -> List[str]:
    p = run(["git", "diff", "--name-only", frm, to], cwd=repo)
    if p.returncode != 0:
        return []
    return [f.strip() for f in p.stdout.splitlines() if f.strip() and target_file(f.strip())]


def get_diff(repo: Path, frm: str, to: str, files: List[str]) -> str:
    if not files:
        return ""
    p = run(["git", "diff", frm, to, "--", *files], cwd=repo)
    return p.stdout if p.returncode == 0 else ""


def local_checks(repo: Path, files: List[str]) -> List[Dict[str, Any]]:
    issues = []
    for f in files:
        fp = str(repo / f)
        ext = Path(f).suffix
        if ext == ".php":
            p = run(["php", "-l", fp])
            if p.returncode != 0:
                issues.append({"code": "PHP_LINT", "file": f, "line": 0, "message": (p.stderr or p.stdout).strip()})
        elif ext == ".js":
            p = run(["node", "--check", fp])
            if p.returncode != 0:
                issues.append({"code": "JS_CHECK", "file": f, "line": 0, "message": p.stderr.strip()})
        elif ext == ".sh":
            p = run(["bash", "-n", fp])
            if p.returncode != 0:
                issues.append({"code": "SH_CHECK", "file": f, "line": 0, "message": p.stderr.strip()})
        elif ext == ".sql":
            if not Path(fp).exists() or Path(fp).stat().st_size == 0:
                issues.append({"code": "SQL_EMPTY", "file": f, "line": 0, "message": "empty sql file"})
    return issues


def hard_rules(repo: Path, files: List[str]) -> List[Dict[str, Any]]:
    findings = []
    for f in files:
        fp = repo / f
        try:
            text = fp.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        for m in re.finditer(r"->\s*sdiff(store)?\s*\(", text):
            findings.append({"code": "BLOCK-001", "file": f, "line": text.count("\n", 0, m.start()) + 1, "reason": "禁止 sdiff/sdiffstore"})

        for m in re.finditer(r"static\s+\$cache\s*=\s*\[", text):
            findings.append({"code": "BLOCK-002", "file": f, "line": text.count("\n", 0, m.start()) + 1, "reason": "禁止业务数组缓存"})

        reqs = list(re.finditer(r"request\s*\(|curl_exec\s*\(", text))
        has_timeout = re.search(r"timeout|connect_timeout|CURLOPT_TIMEOUT|CURLOPT_CONNECTTIMEOUT", text) is not None
        if reqs and not has_timeout:
            for m in reqs:
                findings.append({"code": "BLOCK-003", "file": f, "line": text.count("\n", 0, m.start()) + 1, "reason": "外部调用缺少 timeout"})

        # 直接递归粗检
        fn_names = re.findall(r"function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", text)
        for fn in fn_names:
            if re.search(rf"function\s+{fn}\s*\([^)]*\)\s*\{{[\s\S]*?\b{fn}\s*\(", text):
                line = text.find(f"function {fn}")
                findings.append({"code": "WARN-004", "file": f, "line": text.count("\n", 0, line) + 1, "reason": f"疑似递归(仅提示): {fn}"})
                break

    return findings


def llm_review(diff_text: str) -> Dict[str, Any]:
    if not LLM_API_KEY:
        return {"error": "LLM_API_KEY not set"}
    prompt = f"""你是资深代码审查员，仅审核 .php .js .ts .sql .sh。\n返回严格JSON：
{{
  \"risk_level\":\"高|中|低\",
  \"major_issues\":[{{\"severity\":\"高|中|低\",\"file\":\"\",\"line\":0,\"reason\":\"\"}}],
  \"suggestions\":[{{\"file\":\"\",\"advice\":\"\"}}],
  \"release\":{{\"allow\":true,\"reason\":\"\"}}
}}
Diff:\n{diff_text[:MAX_DIFF_CHARS]}
"""
    payload = {"model": LLM_MODEL, "temperature": 0, "messages": [{"role": "user", "content": prompt}]}

    retries = int(os.getenv("LLM_MAX_RETRIES", "3"))
    for i in range(retries + 1):
        try:
            r = requests.post(
                LLM_API_URL,
                headers={"Authorization": f"Bearer {LLM_API_KEY}", "Content-Type": "application/json"},
                json=payload,
                timeout=180,
            )
            if r.status_code in (429, 500, 502, 503, 504) and i < retries:
                time.sleep(1.5 * (2 ** i))
                continue
            data = r.json()
            if "error" in data:
                return {"error": data["error"]}
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            try:
                return json.loads(content)
            except Exception:
                # extract first json object
                for a, ch in enumerate(content):
                    if ch != "{":
                        continue
                    for b in range(len(content), a, -1):
                        s = content[a:b].strip()
                        if not s.endswith("}"):
                            continue
                        try:
                            return json.loads(s)
                        except Exception:
                            pass
                return {"error": "non-json response", "raw": content[:800]}
        except Exception as e:
            if i >= retries:
                return {"error": f"request_failed: {e}"}
            time.sleep(1.5 * (2 ** i))
    return {"error": "llm_unknown"}


def merge_llm(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    merged = {"risk_level": "低", "major_issues": [], "suggestions": [], "release": {"allow": True, "reason": "ok"}}
    rank = {"低": 1, "中": 2, "高": 3}
    max_r = 1
    for r in results:
        if r.get("error"):
            return {"error": r.get("error")}
        merged["major_issues"].extend(r.get("major_issues", []))
        merged["suggestions"].extend(r.get("suggestions", []))
        rl = r.get("risk_level", "高")
        max_r = max(max_r, rank.get(rl, 3))
        if not bool(r.get("release", {}).get("allow", False)):
            merged["release"] = {"allow": False, "reason": r.get("release", {}).get("reason", "blocked")}
    merged["risk_level"] = [k for k, v in rank.items() if v == max_r][0]
    if merged["risk_level"] == "高":
        merged["release"] = {"allow": False, "reason": "risk is high"}
    return merged


def review_project(proj: Dict[str, str]) -> Dict[str, Any]:
    name, git_url, branch = proj["name"], proj["git"], proj["branch"]
    key = safe_key(f"{name}_{branch}")
    repo = WORK_DIR / key
    state_file = STATE_DIR / f"{key}.last"

    meta = {
        "project": name,
        "branch": branch,
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "author": "",
        "subject": "",
    }

    if not repo.exists():
        p = run(["git", "clone", "--no-checkout", git_url, str(repo)])
        if p.returncode != 0:
            return {**meta, "status": "clone-failed", "error": p.stderr.strip()}

    p = run(["git", "fetch", "--prune", "origin"], cwd=repo)
    if p.returncode != 0:
        return {**meta, "status": "fetch-failed", "error": p.stderr.strip()}

    p = run(["git", "rev-parse", f"origin/{branch}"], cwd=repo)
    if p.returncode != 0:
        return {**meta, "status": "branch-not-found", "error": p.stderr.strip()}
    new = p.stdout.strip()

    last = state_file.read_text().strip() if state_file.exists() else ""
    if not last:
        state_file.write_text(new)
        return {**meta, "status": "init", "new": new}
    if last == new:
        return {**meta, "status": "noop", "new": new}

    # 获取本次提交信息（更新人员/更新描述）
    pa = run(["git", "show", "-s", "--format=%an <%ae>", new], cwd=repo)
    if pa.returncode == 0:
        meta["author"] = pa.stdout.strip()
    ps = run(["git", "show", "-s", "--format=%s", new], cwd=repo)
    if ps.returncode == 0:
        meta["subject"] = ps.stdout.strip()

    files = get_changed_files(repo, last, new)
    if not files:
        state_file.write_text(new)
        return {**meta, "status": "skip", "reason": "no target files", "last": last, "new": new}

    run(["git", "checkout", "-f", new], cwd=repo)

    local_issues = []
    if REVIEW_MODE in ("full", "local"):
        local_issues = local_checks(repo, files)
        if local_issues:
            state_file.write_text(new)
            return {**meta, "status": "fail-local", "last": last, "new": new, "files": files, "local_issues": local_issues}

    blocks = []
    warns = []
    if REVIEW_MODE in ("full", "local"):
        findings = hard_rules(repo, files)
        blocks = [x for x in findings if str(x.get("code", "")).startswith("BLOCK-")]
        warns = [x for x in findings if str(x.get("code", "")).startswith("WARN-")]
        if blocks:
            state_file.write_text(new)
            return {**meta, "status": "blocked", "last": last, "new": new, "files": files, "blocking_items": blocks, "warnings": warns}

    if REVIEW_MODE == "local":
        state_file.write_text(new)
        return {**meta, "status": "pass-local-only", "last": last, "new": new, "files": files, "warnings": warns}

    llm_batch = []
    for i in range(0, len(files), BATCH_SIZE):
        part = files[i:i + BATCH_SIZE]
        diff_text = get_diff(repo, last, new, part)
        llm_batch.append(llm_review(diff_text))

    merged = merge_llm(llm_batch)
    status = "pass"
    if merged.get("error"):
        status = "fail-llm"
    elif not bool(merged.get("release", {}).get("allow", False)):
        status = "fail-review"

    state_file.write_text(new)
    return {**meta, "status": status, "last": last, "new": new, "files": files, "llm": merged, "warnings": warns}


def brief(res: Dict[str, Any], name: str, branch: str, review_id: str, log_link: str) -> str:
    s = res.get("status")
    frm_full = res.get('last', '')
    to_full = res.get('new', '')
    frm = frm_full[:7]
    to = to_full[:7]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    author = res.get("author", "")
    subject = res.get("subject", "")

    # 检测执行状态汇总（通知里统一展示）
    if s in ("fail-local", "blocked"):
        local_info = "已执行（未通过）"
        gpt_info = "未执行（本地未通过）"
    elif s == "pass-local-only":
        local_info = "已执行（通过）"
        gpt_info = "未执行（本地模式）"
    elif s in ("pass", "fail-review"):
        local_info = "已执行（通过）" if REVIEW_MODE in ("full", "local") else "未执行（llm模式）"
        gpt_info = "已执行（通过）" if s == "pass" else "已执行（未通过）"
    elif s == "fail-llm":
        local_info = "已执行（通过）" if REVIEW_MODE in ("full", "local") else "未执行（llm模式）"
        gpt_info = "已执行（失败）"
    else:
        local_info = "未执行"
        gpt_info = "未执行"

    if s == "pass":
        return (
            f"📣 <b>部署更新通知</b>\n"
            f"<b>项目名称</b>: {name}\n"
            f"<b>代码分支</b>: {branch}\n"
            f"<b>更新时间</b>: {now}\n"
            f"<b>更新人员</b>: {author}\n"
            f"<b>更新描述</b>: {subject}\n"
            f"<b>本地检测</b>: {local_info}\n"
            f"<b>模型检测</b>: {gpt_info}\n"
            f"<b>模型</b>: {LLM_MODEL}\n"
            f"<b>风险级别</b>: {res.get('llm', {}).get('risk_level', '低')}\n"
            f"<b>返回结果</b>: ✅ 成功"
        )

    if s == "fail-local":
        item = res.get("local_issues", [{}])[0]
        return (
            f"📣 <b>部署更新通知</b>\n"
            f"<b>项目名称</b>: {name}\n"
            f"<b>代码分支</b>: {branch}\n"
            f"<b>更新时间</b>: {now}\n"
            f"<b>更新人员</b>: {author}\n"
            f"<b>更新描述</b>: {subject}\n"
            f"<b>本地检测</b>: {local_info}\n"
            f"<b>模型检测</b>: {gpt_info}\n"
            f"<b>模型</b>: 服务检测引擎\n"
            f"<b>风险级别</b>: 高\n"
            f"<b>返回结果</b>: ❌ 未通过"
        )

    if s == "blocked":
        item = res.get("blocking_items", [{}])[0]
        return (
            f"📣 <b>部署更新通知</b>\n"
            f"<b>项目名称</b>: {name}\n"
            f"<b>代码分支</b>: {branch}\n"
            f"<b>更新时间</b>: {now}\n"
            f"<b>更新人员</b>: {author}\n"
            f"<b>更新描述</b>: {subject}\n"
            f"<b>本地检测</b>: {local_info}\n"
            f"<b>模型检测</b>: {gpt_info}\n"
            f"<b>模型</b>: 服务检测引擎\n"
            f"<b>风险级别</b>: 高\n"
            f"<b>返回结果</b>: ❌ 未通过"
        )

    if s == "fail-review":
        llm = res.get('llm', {}) or {}
        risk_level = llm.get('risk_level', '未知')
        return (
            "📣 <b>部署更新通知</b>\n"
            f"<b>项目名称</b>: {name}\n"
            f"<b>代码分支</b>: {branch}\n"
            f"<b>更新时间</b>: {now}\n"
            f"<b>更新人员</b>: {author}\n"
            f"<b>更新描述</b>: {subject}\n"
            f"<b>本地检测</b>: {local_info}\n"
            f"<b>模型检测</b>: {gpt_info}\n"
            f"<b>模型</b>: {LLM_MODEL}\n"
            f"<b>风险级别</b>: {risk_level}\n"
            f"<b>返回结果</b>: ❌ 未通过"
        )

    if s == "fail-llm":
        return (
            f"📣 <b>部署更新通知</b>\n"
            f"<b>项目名称</b>: {name}\n"
            f"<b>代码分支</b>: {branch}\n"
            f"<b>更新时间</b>: {now}\n"
            f"<b>更新人员</b>: {author}\n"
            f"<b>更新描述</b>: {subject}\n"
            f"<b>本地检测</b>: {local_info}\n"
            f"<b>模型检测</b>: {gpt_info}\n"
            f"<b>模型</b>: {LLM_MODEL}\n"
            f"<b>返回结果</b>: ⚠️ 模型审核失败\n"
            f"<b>错误</b>: {res.get('llm',{}).get('error','llm error')}"
        )

    if s == "skip":
        return (
            f"📣 <b>部署更新通知</b>\n"
            f"<b>项目名称</b>: {name}\n"
            f"<b>代码分支</b>: {branch}\n"
            f"<b>更新时间</b>: {now}\n"
            f"<b>更新人员</b>: {author}\n"
            f"<b>更新描述</b>: {subject}\n"
            f"<b>本地检测</b>: {local_info}\n"
            f"<b>模型检测</b>: {gpt_info}\n"
            f"<b>返回结果</b>: ℹ️ 已跳过（无目标后缀文件变更）"
        )

    if s == "pass-local-only":
        return (
            f"📣 <b>部署更新通知</b>\n"
            f"<b>项目名称</b>: {name}\n"
            f"<b>代码分支</b>: {branch}\n"
            f"<b>更新时间</b>: {now}\n"
            f"<b>更新人员</b>: {author}\n"
            f"<b>更新描述</b>: {subject}\n"
            f"<b>本地检测</b>: {local_info}\n"
            f"<b>模型检测</b>: {gpt_info}\n"
            f"<b>返回结果</b>: ✅ 成功（本地模式）\n"
            f"<b>文件数</b>: {len(res.get('files', []))}"
        )

    return f"ℹ️ {name} 状态: {s}"


def main():
    ensure_dirs()
    projects = parse_projects()
    if not projects:
        print("No projects. Set PROJECTS_DATA env as lines: name|git|branch|chat(optional)")
        return

    all_results = []
    for p in projects:
        res = review_project(p)
        all_results.append({"project": p["name"], "result": res})

        # noop/init 不通知，不写详情日志
        if res.get("status") in ("noop", "init"):
            continue

        log_name = save_review_log(res, p["name"])
        log_link = build_log_link(log_name)
        log_file = str(LOG_DIR / log_name)
        notify(brief(res, p["name"], p["branch"], "", log_link), log_file)

    print(json.dumps(all_results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
