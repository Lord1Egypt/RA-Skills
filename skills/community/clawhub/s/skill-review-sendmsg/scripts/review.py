#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Dict, Any

import requests

TARGET_EXT = {".php", ".js", ".ts", ".sql", ".sh"}


def run(cmd: List[str], cwd: str = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)


def changed_files(repo: str, frm: str, to: str) -> List[str]:
    p = run(["git", "diff", "--name-only", frm, to], cwd=repo)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip())
    files = [x.strip() for x in p.stdout.splitlines() if x.strip()]
    return [f for f in files if Path(f).suffix in TARGET_EXT]


def diff_for_files(repo: str, frm: str, to: str, files: List[str]) -> str:
    if not files:
        return ""
    p = run(["git", "diff", frm, to, "--", *files], cwd=repo)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip())
    return p.stdout


def chunks(arr: List[str], size: int) -> List[List[str]]:
    if size <= 0:
        size = 8
    return [arr[i : i + size] for i in range(0, len(arr), size)]


def local_checks(repo: str, files: List[str]) -> List[Dict[str, Any]]:
    issues = []
    for f in files:
        fp = os.path.join(repo, f)
        ext = Path(f).suffix
        if ext == ".php":
            p = run(["php", "-l", fp])
            if p.returncode != 0:
                issues.append({"tool": "php -l", "file": f, "message": (p.stderr or p.stdout).strip()})
        elif ext == ".js":
            p = run(["node", "--check", fp])
            if p.returncode != 0:
                issues.append({"tool": "node --check", "file": f, "message": p.stderr.strip()})
        elif ext == ".ts":
            # TS 语法/类型检查建议项目内跑 tsc，这里仅做存在性占位
            if not Path(fp).exists():
                issues.append({"tool": "ts-file-check", "file": f, "message": "file not found"})
        elif ext == ".sh":
            p = run(["bash", "-n", fp])
            if p.returncode != 0:
                issues.append({"tool": "bash -n", "file": f, "message": p.stderr.strip()})
        elif ext == ".sql":
            if not Path(fp).exists() or Path(fp).stat().st_size == 0:
                issues.append({"tool": "sql-empty-check", "file": f, "message": "empty sql file"})
    return issues


def post_with_retry(url: str, headers: Dict[str, str], payload: Dict[str, Any], timeout: int = 180) -> Dict[str, Any]:
    max_retries = int(os.getenv("LLM_MAX_RETRIES", "3"))
    backoff = float(os.getenv("LLM_BACKOFF_SECONDS", "1.5"))

    last_err = None
    for i in range(max_retries + 1):
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=timeout)
            # 重试条件：429/5xx
            if r.status_code in (429, 500, 502, 503, 504):
                last_err = f"http_{r.status_code}: {r.text[:500]}"
                if i < max_retries:
                    time.sleep(backoff * (2 ** i))
                    continue
            r.raise_for_status()
            return r.json()
        except Exception as e:
            last_err = str(e)
            if i < max_retries:
                time.sleep(backoff * (2 ** i))
            else:
                break

    return {"error": f"request_failed: {last_err}"}


def parse_json_content(content: str) -> Dict[str, Any]:
    content = (content or "").strip()
    if not content:
        return {"error": "empty response content"}

    # 1) 直接JSON
    try:
        return json.loads(content)
    except Exception:
        pass

    # 2) 提取首个 JSON 对象
    for i, ch in enumerate(content):
        if ch != "{":
            continue
        for j in range(len(content), i, -1):
            s = content[i:j].strip()
            if not s.endswith("}"):
                continue
            try:
                return json.loads(s)
            except Exception:
                continue

    return {"error": "non-json response", "raw": content[:2000]}


def llm_review(diff_text: str) -> Dict[str, Any]:
    api_key = os.getenv("LLM_API_KEY")
    api_url = os.getenv("LLM_API_URL", "https://api.deepseek.com/v1/chat/completions")
    model = os.getenv("LLM_MODEL", "deepseek-chat")
    if not api_key:
        return {"error": "LLM_API_KEY not set"}

    prompt = f"""你是资深代码审查员。仅审核 .php .js .ts .sql .sh。
请输出严格JSON：
{{
  "risk_level":"高|中|低",
  "major_issues":[{{"severity":"高|中|低","file":"路径","line":0,"reason":""}}],
  "suggestions":[{{"file":"路径","advice":""}}],
  "release":{{"allow":true,"reason":""}}
}}

Diff:
{diff_text[:120000]}
"""

    payload = {
        "model": model,
        "temperature": 0,
        "messages": [{"role": "user", "content": prompt}],
    }

    data = post_with_retry(
        api_url,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        payload=payload,
        timeout=180,
    )

    if "error" in data:
        return {"error": data["error"]}

    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    return parse_json_content(content)


def merge_llm_results(batch_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    merged = {
        "risk_level": "低",
        "major_issues": [],
        "suggestions": [],
        "release": {"allow": True, "reason": "all batches passed"},
        "batches": batch_results,
    }

    rank = {"低": 1, "中": 2, "高": 3}
    max_rank = 1

    for br in batch_results:
        if br.get("error"):
            merged["release"] = {"allow": False, "reason": f"batch error: {br.get('error')}"}
            return merged

        rl = br.get("risk_level", "高")
        max_rank = max(max_rank, rank.get(rl, 3))

        merged["major_issues"].extend(br.get("major_issues", []))
        merged["suggestions"].extend(br.get("suggestions", []))

        if not bool(br.get("release", {}).get("allow", False)):
            merged["release"] = {"allow": False, "reason": br.get("release", {}).get("reason", "blocked by one batch")}

    for k, v in rank.items():
        if v == max_rank:
            merged["risk_level"] = k
            break

    if merged["release"]["allow"] and merged["risk_level"] == "高":
        merged["release"] = {"allow": False, "reason": "risk is high"}

    return merged


def telegram_notify(message: str) -> None:
    token = os.getenv("TG_BOT_TOKEN", "").strip()
    chat_id = os.getenv("TG_CHAT_ID", "").strip()
    if not token or not chat_id:
        return

    try:
        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": message[:3900]},
            timeout=15,
        )
    except Exception:
        pass


def main():
    if len(sys.argv) < 4:
        print("Usage: python review.py <repo_path> <from_commit> <to_commit>")
        sys.exit(1)

    repo, frm, to = sys.argv[1], sys.argv[2], sys.argv[3]
    batch_size = int(os.getenv("DIFF_BATCH_SIZE", "8"))

    files = changed_files(repo, frm, to)
    if not files:
        result = {"status": "skip", "reason": "no target files changed"}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        telegram_notify(f"ℹ️ Review skipped\n{frm[:7]} -> {to[:7]}\nno target files")
        return

    local = local_checks(repo, files)
    result: Dict[str, Any] = {
        "files": files,
        "local_issues": local,
        "llm": None,
    }

    if local:
        result["status"] = "fail-local"
        print(json.dumps(result, ensure_ascii=False, indent=2))
        telegram_notify(f"🚨 Review fail-local\n{frm[:7]} -> {to[:7]}\nissues={len(local)}")
        return

    llm_batches = []
    for group in chunks(files, batch_size):
        d = diff_for_files(repo, frm, to, group)
        llm_batches.append(llm_review(d))

    merged = merge_llm_results(llm_batches)
    result["llm"] = merged
    allow = bool(merged.get("release", {}).get("allow", False))
    result["status"] = "pass" if allow else "fail-review"

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if allow:
        telegram_notify(
            f"✅ Review pass\n{frm[:7]} -> {to[:7]}\nfiles={len(files)}\nrisk={merged.get('risk_level','低')}"
        )
    else:
        telegram_notify(
            f"🚨 Review fail\n{frm[:7]} -> {to[:7]}\nfiles={len(files)}\nreason={merged.get('release',{}).get('reason','blocked')}"
        )


if __name__ == "__main__":
    main()
