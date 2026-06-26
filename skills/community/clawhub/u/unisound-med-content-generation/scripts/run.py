#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""医学内容生成与解释 — 独立 skill，可单独拷贝发布；不依赖其他 skill 或 _shared。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_API_URL = "https://maas-api.hivoice.cn/v1/chat/completions"
DEFAULT_MODEL = "u1-insuremed"
BASE_SYSTEM_PROMPT = '你是专业医学大模型。请严格按用户消息中的题目与输出格式要求作答，不要输出与解题无关的寒暄；不要编造题干未给出的检验数值、量表结果或隐私信息。'

TASKS: Dict[str, Dict[str, str]] = {'popular': {'title': '医学科普内容生成', 'hint': '生成面向公众的医学科普文本，语言通俗、事实准确。'}, 'summary': {'title': '临床文档摘要生成', 'hint': '提炼病历或报告要点，保留关键临床信息。'}, 'explain': {'title': '医学术语通俗释义', 'hint': '将专业术语解释为非专业人士可理解的表述。'}, 'teach': {'title': '临床教学案例生成', 'hint': '生成可用于教学的临床案例与讨论要点。'}, 'record-gen': {'title': '诊疗文书辅助生成', 'hint': '按题干要求辅助生成诊疗文书片段，不编造未提供的信息。'}}


def task_keys() -> str:
    return ", ".join(sorted(TASKS))


def resolve_task(explicit: str, meta: Dict[str, Any]) -> str:
    key = (explicit or "").strip()
    if not key and isinstance(meta, dict):
        for field in ("task", "task_type"):
            v = meta.get(field)
            if isinstance(v, str) and v.strip():
                key = v.strip()
                break
    if not key:
        raise ValueError(f"必须指定 --task，可选值: {task_keys()}")
    if key not in TASKS:
        raise ValueError(f"未知 task {key!r}，可选: {task_keys()}")
    return key


def system_prompt_for(task_key: str, override: str) -> str:
    if override and override != BASE_SYSTEM_PROMPT:
        return override
    hint = TASKS[task_key]["hint"]
    return f"{BASE_SYSTEM_PROMPT}\n\n当前任务：{TASKS[task_key]['title']}。{hint}"


def iter_jsonl_records(path: Path) -> Iterator[Tuple[int, Dict[str, Any]]]:
    rec_idx = 0
    with path.open("r", encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"第 {rec_idx + 1} 条记录 JSON 解析失败: {exc}") from exc
            if not isinstance(obj, dict):
                raise ValueError("每条记录必须是 JSON 对象")
            yield rec_idx, obj
            rec_idx += 1


def load_record(path: Path, *, index: int, match_id: Optional[int]) -> Tuple[int, Dict[str, Any]]:
    if match_id is not None:
        for idx, obj in iter_jsonl_records(path):
            other = obj.get("other")
            if isinstance(other, dict) and other.get("id") == match_id:
                return idx, obj
        raise FileNotFoundError(f"未找到 other.id == {match_id} 的记录")
    for idx, obj in iter_jsonl_records(path):
        if idx == index:
            return idx, obj
    raise IndexError(f"不存在第 {index} 条记录（0 基，仅计非空行 JSON）")


def call_llm(
    *,
    api_url: str,
    model: str,
    appkey: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float,
    timeout: int,
) -> str:
    payload = {
        "model": model,
        "temperature": temperature,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    try:
        req = Request(
            api_url,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {appkey}",
            },
        )
        resp = urlopen(req, timeout=timeout)
        body = json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:2000]
        raise RuntimeError(f"API HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"API 不可达: {exc.reason}") from exc
    choices = body.get("choices") or []
    if not choices:
        raise RuntimeError("API 响应缺少 choices")
    msg = choices[0].get("message") or {}
    return str(msg.get("content") or "")


def build_user_prompt(record: Dict[str, Any]) -> str:
    q = record.get("question")
    if isinstance(q, str) and q.strip():
        return q.strip()
    raise ValueError("记录缺少非空 question 字段")


def load_json_question_file(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        obj = json.load(handle)
    if not isinstance(obj, dict) or not isinstance(obj.get("question"), str) or not obj["question"].strip():
        raise ValueError(f"JSON 须为对象且含非空 question 字符串: {path}")
    return obj


def parse_stdin_record(raw: str) -> Dict[str, Any]:
    text = raw.strip()
    if not text:
        raise ValueError("stdin 为空")
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        return {"question": text, "other": {}}
    if isinstance(obj, dict) and isinstance(obj.get("question"), str):
        return obj
    raise ValueError("stdin JSON 须为对象且含字符串字段 question")


def collect_jobs(args: argparse.Namespace) -> List[Tuple[int, Dict[str, Any], str, str, Optional[str]]]:
    jobs: List[Tuple[int, Dict[str, Any], str, str, Optional[str]]] = []
    qarg = (args.question or "").strip()
    if qarg and args.input:
        raise ValueError("不能同时使用 --question 与 --input")
    if qarg:
        jobs.append((0, {}, qarg, "argument", None))
        return jobs
    if args.input:
        if str(args.input).strip() == "-":
            raw = sys.stdin.read()
            rec = parse_stdin_record(raw)
            meta = rec.get("other") if isinstance(rec.get("other"), dict) else {}
            jobs.append((0, meta, build_user_prompt(rec), "stdin", None))
            return jobs
        path = Path(args.input).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"找不到文件: {path}")
        suf = path.suffix.lower()
        mid: Optional[int] = None if args.match_id < 0 else args.match_id
        if suf == ".jsonl":
            if mid is not None:
                idx, rec = load_record(path, index=0, match_id=mid)
                meta = rec.get("other") if isinstance(rec.get("other"), dict) else {}
                jobs.append((idx, meta, build_user_prompt(rec), "file", str(path)))
                return jobs
            start = int(args.index)
            batch_n = args.batch if args.batch and args.batch > 0 else 1
            for offset in range(batch_n):
                idx, rec = load_record(path, index=start + offset, match_id=None)
                meta = rec.get("other") if isinstance(rec.get("other"), dict) else {}
                jobs.append((idx, meta, build_user_prompt(rec), "file", str(path)))
            return jobs
        if suf == ".json":
            rec = load_json_question_file(path)
            meta = rec.get("other") if isinstance(rec.get("other"), dict) else {}
            if mid is not None:
                oid = meta.get("id") if isinstance(meta, dict) else None
                if oid != mid:
                    raise FileNotFoundError(f"未找到 other.id == {mid} 的记录")
            jobs.append((0, meta, build_user_prompt(rec), "file", str(path)))
            return jobs
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            raise ValueError(f"文件为空: {path}")
        jobs.append((0, {}, text, "file-text", str(path)))
        return jobs
    if not sys.stdin.isatty():
        raw = sys.stdin.read()
        rec = parse_stdin_record(raw)
        meta = rec.get("other") if isinstance(rec.get("other"), dict) else {}
        jobs.append((0, meta, build_user_prompt(rec), "stdin", None))
        return jobs
    raise ValueError(
        "请提供 --question、--input PATH，或在非交互环境下通过 stdin 传入题目（JSON 对象含 question 字段或纯文本）"
    )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="医学内容生成与解释：由调用方传入题目与 --task，直连内部医疗大模型。")
    p.add_argument("--task", default="", help=f"任务类型，可选: {task_keys()}；jsonl 记录可在 other.task 中指定。")
    p.add_argument("--question", default="", help="题目全文（与 --input、stdin 三选一）。")
    p.add_argument("--input", default="", help="题目来源文件：.jsonl、.json 或文本；传 - 则从 stdin 读取。")
    p.add_argument("--index", type=int, default=0, help="jsonl 选取第几条记录（0 基）。")
    p.add_argument("--match-id", type=int, default=-1, help="按 other.id 在 jsonl/json 中匹配一条。")
    p.add_argument("--batch", type=int, default=0, help="jsonl 从 --index 起连续 N 条，0 表示仅单条。")
    p.add_argument("--appkey", default="", help="内部医疗大模型鉴权 key。")
    p.add_argument("--dry-run", action="store_true", help="不调用模型，仅输出题目与元数据 JSON。")
    p.add_argument("--api-url", default=DEFAULT_API_URL, help="OpenAI 兼容接口地址")
    p.add_argument("--model", default=DEFAULT_MODEL, help="模型名")
    p.add_argument("--temperature", type=float, default=0.0, help="采样温度")
    p.add_argument("--timeout", type=int, default=120, help="HTTP 超时秒数")
    p.add_argument("--system-prompt", default=BASE_SYSTEM_PROMPT, help="覆盖默认系统提示词")
    p.add_argument("--output", default="", help="写入 UTF-8 结果文件；批量为 NDJSON")
    p.add_argument("--text-only", action="store_true", help="stdout 仅输出模型文本")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        jobs = collect_jobs(args)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    outputs: list[dict[str, Any]] = []
    for idx, meta, user_prompt, mode, path_str in jobs:
        try:
            task_key = resolve_task(args.task, meta)
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        task_info = TASKS[task_key]
        out: dict[str, Any] = {
            "skill": "医学内容生成与解释",
            "task": task_key,
            "task_title": task_info["title"],
            "status": "ok",
            "record_index": idx,
            "meta": meta,
            "question": user_prompt,
            "model": args.model,
            "input_mode": mode,
            "input_path": path_str,
        }
        if args.dry_run:
            out["answer"] = ""
            out["dry_run"] = True
            outputs.append(out)
            continue
        if not args.appkey:
            print("error: 非 dry-run 必须提供 --appkey", file=sys.stderr)
            return 2
        out["answer"] = call_llm(
            api_url=args.api_url,
            model=args.model,
            appkey=args.appkey,
            system_prompt=system_prompt_for(task_key, args.system_prompt),
            user_prompt=user_prompt,
            temperature=float(args.temperature),
            timeout=int(args.timeout),
        )
        outputs.append(out)

    out_path = Path(args.output).expanduser() if args.output else None

    if args.text_only:
        for i, item in enumerate(outputs):
            if i:
                print("\n---\n")
            print(item.get("answer", ""))
        if out_path:
            if len(outputs) == 1:
                out_path.write_text(json.dumps(outputs[0], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            else:
                with out_path.open("w", encoding="utf-8") as fh:
                    for item in outputs:
                        fh.write(json.dumps(item, ensure_ascii=False) + "\n")
        return 0

    if len(outputs) == 1:
        blob = json.dumps(outputs[0], ensure_ascii=False, indent=2) + "\n"
        sys.stdout.write(blob)
        if out_path:
            out_path.write_text(blob, encoding="utf-8")
    else:
        for item in outputs:
            sys.stdout.write(json.dumps(item, ensure_ascii=False) + "\n")
        if out_path:
            with out_path.open("w", encoding="utf-8") as fh:
                for item in outputs:
                    fh.write(json.dumps(item, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BrokenPipeError:
        try:
            sys.stdout.close()
        except Exception:
            pass
        raise SystemExit(0)
    except SystemExit:
        raise
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
