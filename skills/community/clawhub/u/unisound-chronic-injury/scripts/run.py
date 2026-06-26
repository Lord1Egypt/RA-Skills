#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""陈旧伤审核 — 据影像/检查报告题干判断指定部位伤情类别，直连内部医疗大模型；无 _shared 依赖。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

SKILL_TITLE = "陈旧伤审核"
DEFAULT_API_URL = "https://maas-api.hivoice.cn/v1/chat/completions"
DEFAULT_MODEL = "u1-insuremed"
DEFAULT_SYSTEM_PROMPT = (
    f"你是保险理赔与影像、骨科相关临床辅助专家。用户会给出影像或检查报告文字、"
    f"指定部位及任务说明，要求判断该部位伤情类别。\n"
    f"1. 类别只能为：陈旧伤、新伤、无伤、未提及 之一（须与用户题干用词一致）。\n"
    f"2. 严格按用户消息要求的行数与格式输出（常见为两行：「伤情类别：…」「判断依据：…」）；"
    f"不要输出 Markdown、编号、多余空行或任何前缀说明。\n"
    f"3. 判断须基于题干已给出的报告内容，不要编造题干中未出现的检查结论、部位或数值。"
)


def unwrap_record(obj: Any) -> Dict[str, Any]:
    if isinstance(obj, dict):
        return obj
    if isinstance(obj, list) and len(obj) == 1 and isinstance(obj[0], dict):
        return obj[0]
    raise ValueError("JSON 须为对象，或仅含 1 个对象的数组")


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
            try:
                rec = unwrap_record(obj)
            except ValueError as exc:
                raise ValueError(f"第 {rec_idx + 1} 条记录: {exc}") from exc
            yield rec_idx, rec
            rec_idx += 1


def load_record(path: Path, *, index: int, match_id: Optional[int]) -> Tuple[int, Dict[str, Any]]:
    if match_id is not None:
        for idx, obj in iter_jsonl_records(path):
            meta = obj.get("meta") if isinstance(obj.get("meta"), dict) else {}
            other = obj.get("other") if isinstance(obj.get("other"), dict) else {}
            oid = meta.get("id") if isinstance(meta, dict) else None
            if oid is None and isinstance(other, dict):
                oid = other.get("id")
            if oid == match_id:
                return idx, obj
        raise FileNotFoundError(f"未找到 meta.id / other.id == {match_id} 的记录")
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


def extract_meta(rec: Dict[str, Any]) -> Dict[str, Any]:
    m = rec.get("meta")
    if isinstance(m, dict):
        return dict(m)
    o = rec.get("other")
    if isinstance(o, dict):
        return dict(o)
    return {}


def build_user_prompt(record: Dict[str, Any]) -> str:
    inp = record.get("input")
    if isinstance(inp, str) and inp.strip():
        return inp.strip()
    q = record.get("question")
    if isinstance(q, str) and q.strip():
        return q.strip()
    raise ValueError("记录缺少非空字符串字段 input 或 question")


def load_json_question_file(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        obj = json.load(handle)
    rec = unwrap_record(obj)
    if not isinstance(rec, dict):
        raise ValueError(f"JSON 须为对象: {path}")
    try:
        build_user_prompt(rec)
    except ValueError as exc:
        raise ValueError(f"JSON 须含非空 input 或 question: {path}") from exc
    return rec


def parse_stdin_record(raw: str) -> Dict[str, Any]:
    text = raw.strip()
    if not text:
        raise ValueError("stdin 为空")
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        return {"question": text, "meta": {}}
    try:
        rec = unwrap_record(obj)
    except ValueError:
        raise ValueError("stdin JSON 须为对象或单元素对象数组，且含 input 或 question")
    if isinstance(rec, dict) and (isinstance(rec.get("input"), str) or isinstance(rec.get("question"), str)):
        return rec
    raise ValueError("stdin JSON 须含字符串字段 input 或 question")


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
            jobs.append((0, extract_meta(rec), build_user_prompt(rec), "stdin", None))
            return jobs
        path = Path(args.input).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"找不到文件: {path}")
        suf = path.suffix.lower()
        mid: Optional[int] = None if args.match_id < 0 else args.match_id
        if suf == ".jsonl":
            if mid is not None:
                idx, rec = load_record(path, index=0, match_id=mid)
                jobs.append((idx, extract_meta(rec), build_user_prompt(rec), "file", str(path)))
                return jobs
            start = int(args.index)
            batch_n = args.batch if args.batch and args.batch > 0 else 1
            for offset in range(batch_n):
                idx, rec = load_record(path, index=start + offset, match_id=None)
                jobs.append((idx, extract_meta(rec), build_user_prompt(rec), "file", str(path)))
            return jobs
        if suf == ".json":
            rec = load_json_question_file(path)
            if mid is not None:
                meta = extract_meta(rec)
                oid = meta.get("id")
                if oid != mid:
                    raise FileNotFoundError(f"未找到 meta.id / other.id == {mid} 的记录")
            jobs.append((0, extract_meta(rec), build_user_prompt(rec), "file", str(path)))
            return jobs
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            raise ValueError(f"文件为空: {path}")
        jobs.append((0, {}, text, "file-text", str(path)))
        return jobs
    if not sys.stdin.isatty():
        raw = sys.stdin.read()
        rec = parse_stdin_record(raw)
        jobs.append((0, extract_meta(rec), build_user_prompt(rec), "stdin", None))
        return jobs
    raise ValueError(
        "请提供 --question、--input PATH，或在非交互环境下通过 stdin 传入题目（JSON 含 input/question）"
    )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=f"{SKILL_TITLE}：影像/报告题干 + 伤情类别判断，直连内部医疗大模型。")
    p.add_argument("--question", default="", help="题干全文（与 --input、stdin 三选一）。")
    p.add_argument(
        "--input",
        default="",
        help="题目来源：.jsonl / .json（对象或单元素数组，含 input 或 question）/ 纯文本；传 - 则从 stdin 读。",
    )
    p.add_argument("--index", type=int, default=0, help="jsonl 第几条（0 基）。")
    p.add_argument("--match-id", type=int, default=-1, help="按 meta.id 或 other.id 匹配一条。")
    p.add_argument("--batch", type=int, default=0, help="jsonl 从 --index 起连续 N 条，0 表示仅单条。")
    p.add_argument("--appkey", default="", help="内部医疗大模型鉴权 key。")
    p.add_argument("--dry-run", action="store_true", help="不调用模型，仅输出解析后的 JSON。")
    p.add_argument("--api-url", default=DEFAULT_API_URL, help="OpenAI 兼容接口地址")
    p.add_argument("--model", default=DEFAULT_MODEL, help="模型名")
    p.add_argument("--temperature", type=float, default=0.0, help="采样温度")
    p.add_argument("--timeout", type=int, default=120, help="HTTP 超时秒数")
    p.add_argument("--system-prompt", default=DEFAULT_SYSTEM_PROMPT, help="系统提示词")
    p.add_argument("--output", default="", help="写入 UTF-8 结果文件；批量为 NDJSON")
    p.add_argument("--text-only", action="store_true", help="stdout 仅输出模型答案文本")
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
        out: dict[str, Any] = {
            "skill": SKILL_TITLE,
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
            system_prompt=args.system_prompt,
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
