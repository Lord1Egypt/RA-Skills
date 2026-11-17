#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""yt2podcast 卡住自愈:找出"没在跑、也没结束"的 job,从断点续跑。

背景:worker 由宿主托管(OpenClaw exec background / 终端),Gateway 重启、Mac 重启、
或宿主被回收都会让它中途消失——job 会停在某个 stage,且不会再有完成通知。
job 文件本身是幂等的断点,所以只要"发现 + 重新调用 worker"就能接着做,不重复消耗
NotebookLM 生成配额。

用法:
    resume-stalled.py                 # 只检查,输出 JSON 列表(默认 --json)
    resume-stalled.py --max-age 20    # 判定"多久没更新算卡住",默认 20 分钟
    resume-stalled.py --resume        # 就地续跑(前台,顺序执行;交给宿主托管更稳)
    resume-stalled.py --dry-run       # 连 --resume 也只看不写

退出码: 0 = 没有需要处理的; 10 = 有卡住的 job(仅检查模式); 1 = 续跑中有失败。
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

SKILL_DIR = Path(__file__).resolve().parent
WORKER = SKILL_DIR / "worker.py"
ROOT = Path(os.environ.get("YT2PODCAST_ROOT", "~/.openclaw/workspace/yt2podcast")).expanduser()
JOBS_DIR = ROOT / "jobs"
STAGES = ["sourcing", "generating", "postprocess", "uploading"]
# awaiting_upload: 音频已就绪、在等用户点头上传 —— 不是卡住,不许自动续跑
TERMINAL = ("done", "failed", "awaiting_upload")


def parse_ts(value: Optional[str]) -> Optional[float]:
    if not value:
        return None
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%SZ"):
        try:
            return datetime.strptime(value, fmt).timestamp()
        except ValueError:
            continue
    return None


def worker_running(job_id: str) -> Optional[int]:
    """worker.py <job_id> 还在跑就返回 pid。"""
    try:
        out = subprocess.run(
            ["pgrep", "-f", r"worker\.py %s(\s|$)" % job_id],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=10,
        ).stdout.decode()
    except (OSError, subprocess.SubprocessError):
        return None
    for line in out.split():
        try:
            return int(line)
        except ValueError:
            continue
    return None


def resume_point(job: Dict[str, Any]) -> str:
    """根据已落盘的产物决定从哪个阶段接着跑(产物即真相)。"""
    job_dir = JOBS_DIR / job.get("job_id", "")
    m4a = job_dir / "episode.m4a"
    wav = job_dir / "audio.wav"
    if job.get("episode_url"):
        return "uploading"
    if m4a.exists() and m4a.stat().st_size > 0:
        return "uploading"
    if wav.exists() and wav.stat().st_size > 0:
        return "postprocess"
    if job.get("source_id"):
        return "generating"
    return "sourcing"


def stages_before(stage: str) -> List[str]:
    if stage not in STAGES:
        return []
    return STAGES[: STAGES.index(stage)]


def scan(max_age_min: float) -> List[Dict[str, Any]]:
    found: List[Dict[str, Any]] = []
    now = time.time()
    for path in sorted(JOBS_DIR.glob("*.json")):
        try:
            job = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        stage = job.get("stage") or "pending"
        if stage in TERMINAL:
            continue
        pid = worker_running(job.get("job_id", ""))
        if pid:
            continue
        updated = parse_ts(job.get("updated_at")) or path.stat().st_mtime
        age_min = (now - updated) / 60.0
        if age_min < max_age_min:
            continue
        target = resume_point(job)
        found.append({
            "job_id": job.get("job_id"),
            "stage": stage,
            "stalled_minutes": round(age_min, 1),
            "resume_stage": target,
            "title": job.get("title"),
            "job_file": str(path),
            "error": (job.get("error") or {}).get("code"),
        })
    return found


def resume(item: Dict[str, Any], dry_run: bool) -> bool:
    path = Path(item["job_file"])
    job = json.loads(path.read_text(encoding="utf-8"))
    target = item["resume_stage"]
    if not dry_run:
        job["stages_done"] = stages_before(target)
        job["stage"] = target
        job.pop("error", None)
        job.pop("failed_stage", None)
        job.pop("failed_at", None)
        job["updated_at"] = datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")
        tmp = path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(job, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(tmp, path)
        print("[resume] %s -> %s" % (item["job_id"], target), file=sys.stderr)
        code = subprocess.call([sys.executable, str(WORKER), item["job_id"]])
        return code == 0
    print("[dry-run] %s would resume at %s" % (item["job_id"], target), file=sys.stderr)
    return True


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description="yt2podcast 卡住自愈")
    parser.add_argument("--max-age", type=float, default=20.0, help="多少分钟没更新算卡住(默认 20)")
    parser.add_argument("--resume", action="store_true", help="就地续跑(前台顺序执行)")
    parser.add_argument("--dry-run", action="store_true", help="只看不动")
    parser.add_argument("--quiet", action="store_true",
                        help="没有卡住的 job 时不输出任何内容(心跳/定时任务里用,省 token)")
    args = parser.parse_args(argv)

    if not JOBS_DIR.is_dir():
        print(json.dumps({"ok": True, "stalled": [], "note": "no jobs dir: %s" % JOBS_DIR}, ensure_ascii=False))
        return 0

    stalled = scan(args.max_age)

    if stalled:
        print(json.dumps({"ok": True, "stalled": stalled, "count": len(stalled)}, ensure_ascii=False, indent=2))
    elif not args.quiet:
        print(json.dumps({"ok": True, "stalled": [], "count": 0}, ensure_ascii=False, indent=2))

    if not stalled:
        return 0
    if not args.resume:
        return 10
    ok = True
    for item in stalled:
        ok = resume(item, args.dry_run) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
