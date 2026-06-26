#!/usr/bin/env python3
import argparse
import csv
import json
import math
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from typing import Any, Dict, Iterable, List, Optional, Tuple

BASE = "https://sensecraft.seeed.cc/aiserverapi"
DEFAULT_APPID = "131"
DEFAULT_PAGE_SIZE = 100
DEFAULT_TIMEOUT = 30
DEFAULT_SLEEP = 0.1
DEFAULT_RETRIES = 2
USER_AGENT = "openclaw-sensecraft-skill/1.1"


class RequestError(RuntimeError):
    pass


def build_query(params: Dict[str, Any]) -> str:
    items = []
    for k, v in params.items():
        if v is None:
            continue
        if isinstance(v, (list, tuple)):
            for item in v:
                items.append((k, str(item)))
        else:
            items.append((k, str(v)))
    return urllib.parse.urlencode(items)


def http_open(url: str, timeout: int = DEFAULT_TIMEOUT):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    return urllib.request.urlopen(req, timeout=timeout)


def retry_call(fn, retries: int, sleep_s: float):
    last_exc = None
    for attempt in range(retries + 1):
        try:
            return fn()
        except Exception as e:
            last_exc = e
            if attempt >= retries:
                break
            time.sleep(max(sleep_s, 0.2) * (attempt + 1))
    raise last_exc  # type: ignore[misc]


def http_get_json(path: str, params: Dict[str, Any], timeout: int = DEFAULT_TIMEOUT, retries: int = DEFAULT_RETRIES, retry_sleep: float = DEFAULT_SLEEP) -> Dict[str, Any]:
    query = build_query(params)
    url = f"{BASE}{path}?{query}"

    def run():
        with http_open(url, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))

    return retry_call(run, retries=retries, sleep_s=retry_sleep)


def list_models_page(appid: str, page: int, length: int, search: Optional[str], uniform_type: Optional[str], tasks: List[str], timeout: int, retries: int, retry_sleep: float) -> Dict[str, Any]:
    params: Dict[str, Any] = {"appid": appid, "page": page, "length": length}
    if search:
        params["search"] = search
    if uniform_type:
        params["uniform_type"] = uniform_type
    if tasks:
        params["task"] = tasks
    return http_get_json("/model/list_model", params, timeout=timeout, retries=retries, retry_sleep=retry_sleep)


def view_model(appid: str, model_id: str, timeout: int, retries: int, retry_sleep: float) -> Dict[str, Any]:
    return http_get_json("/model/view_model", {"appid": appid, "model_id": model_id}, timeout=timeout, retries=retries, retry_sleep=retry_sleep)


def ensure_ok(payload: Dict[str, Any], context: str) -> Dict[str, Any]:
    code = str(payload.get("code", ""))
    if code != "0":
        raise RequestError(f"{context} failed: code={code} msg={payload.get('msg') or payload.get('message')}")
    return payload.get("data") or {}


def iter_model_ids(appid: str, page_size: int, search: Optional[str], uniform_type: Optional[str], tasks: List[str], timeout: int, retries: int, retry_sleep: float) -> Iterable[str]:
    first = ensure_ok(list_models_page(appid, 1, page_size, search, uniform_type, tasks, timeout, retries, retry_sleep), "list_model")
    total = int(first.get("count") or 0)
    pages = max(1, math.ceil(total / page_size)) if total else 1
    for item in first.get("list") or []:
        yield str(item.get("id"))
    for page in range(2, pages + 1):
        data = ensure_ok(list_models_page(appid, page, page_size, search, uniform_type, tasks, timeout, retries, retry_sleep), f"list_model page {page}")
        for item in data.get("list") or []:
            yield str(item.get("id"))


def normalize_detail(detail: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": detail.get("id"),
        "name": detail.get("name"),
        "description": detail.get("description"),
        "task": detail.get("task"),
        "uniform_types": detail.get("uniform_types"),
        "model_format": detail.get("model_format"),
        "file_url": detail.get("file_url"),
        "pic_url": detail.get("pic_url"),
        "create_time": detail.get("create_time"),
        "update_time": detail.get("update_time"),
        "raw": detail,
    }


def annotate_model(model: Dict[str, Any]) -> Dict[str, Any]:
    row = dict(model)
    file_url = str(row.get("file_url") or "")
    path = urllib.parse.urlparse(file_url).path
    ext = os.path.splitext(path)[1].lower()
    row["filename_hint"] = os.path.basename(path) if path else None
    row["extension_hint"] = ext or None
    row["looks_like_tflite"] = ext == ".tflite" or ".tflite" in file_url.lower()
    return row


def collect_models(appid: str, page_size: int, search: Optional[str], uniform_type: Optional[str], tasks: List[str], model_format: Optional[str], timeout: int, sleep_s: float, retries: int, retry_sleep: float, stderr=sys.stderr) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for model_id in iter_model_ids(appid, page_size, search, uniform_type, tasks, timeout, retries, retry_sleep):
        try:
            data = ensure_ok(view_model(appid, model_id, timeout, retries, retry_sleep), f"view_model {model_id}")
        except Exception as e:
            print(f"warn: skip model {model_id}: {e}", file=stderr)
            continue
        model = annotate_model(normalize_detail(data))
        if model_format is not None and str(model.get("model_format")) != str(model_format):
            if sleep_s:
                time.sleep(sleep_s)
            continue
        out.append(model)
        if sleep_s:
            time.sleep(sleep_s)
    return out


def summarize_models(models: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_task: Dict[str, int] = {}
    by_format: Dict[str, int] = {}
    by_uniform_type: Dict[str, int] = {}
    tflite_like = 0
    for m in models:
        task = str(m.get("task") or "")
        fmt = str(m.get("model_format") or "")
        by_task[task] = by_task.get(task, 0) + 1
        by_format[fmt] = by_format.get(fmt, 0) + 1
        for ut in m.get("uniform_types") or []:
            ut_s = str(ut)
            by_uniform_type[ut_s] = by_uniform_type.get(ut_s, 0) + 1
        if m.get("looks_like_tflite"):
            tflite_like += 1
    return {
        "total": len(models),
        "looks_like_tflite": tflite_like,
        "by_task": dict(sorted(by_task.items(), key=lambda kv: kv[0])),
        "by_model_format": dict(sorted(by_format.items(), key=lambda kv: kv[0])),
        "by_uniform_type": dict(sorted(by_uniform_type.items(), key=lambda kv: kv[0])),
    }


def print_table(models: List[Dict[str, Any]], include_url: bool = True) -> None:
    for m in models:
        uts = ",".join(str(x) for x in (m.get("uniform_types") or []))
        parts = [
            str(m.get("id") or ""),
            str(m.get("name") or ""),
            f"task={m.get('task')}",
            f"format={m.get('model_format')}",
            f"uniform_types={uts}",
            f"tflite_like={str(bool(m.get('looks_like_tflite'))).lower()}",
        ]
        if include_url:
            parts.append(str(m.get("file_url") or ""))
        print("\t".join(parts))


def export_csv(models: List[Dict[str, Any]], path: str) -> None:
    fieldnames = [
        "id", "name", "description", "task", "uniform_types", "model_format", "file_url",
        "filename_hint", "extension_hint", "looks_like_tflite", "pic_url", "create_time", "update_time"
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for m in models:
            row = dict(m)
            row["uniform_types"] = json.dumps(row.get("uniform_types") or [], ensure_ascii=False)
            row.pop("raw", None)
            w.writerow({k: row.get(k) for k in fieldnames})


def export_json(data: Any, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def safe_name(text: str) -> str:
    keep = []
    for ch in text:
        if ch.isalnum() or ch in ("-", "_", "."):
            keep.append(ch)
        elif ch.isspace():
            keep.append("-")
    s = "".join(keep).strip("-_")
    return s or "model"


def infer_extension(url: str, headers) -> str:
    parsed = urllib.parse.urlparse(url)
    path_ext = os.path.splitext(parsed.path)[1]
    if path_ext:
        return path_ext

    cd = headers.get("Content-Disposition", "")
    match = re.search(r'filename="?([^";]+)"?', cd)
    if match:
        return os.path.splitext(match.group(1))[1] or ".bin"

    content_type = (headers.get("Content-Type") or "").split(";")[0].strip().lower()
    if content_type == "application/octet-stream":
        return ".bin"
    if "zip" in content_type:
        return ".zip"
    if "json" in content_type:
        return ".json"
    return ".bin"


def download_file(url: str, out_path_base: str, timeout: int, retries: int, retry_sleep: float) -> Tuple[str, Dict[str, Any]]:
    os.makedirs(os.path.dirname(out_path_base) or ".", exist_ok=True)

    def run():
        with http_open(url, timeout=timeout) as resp:
            ext = infer_extension(url, resp.headers)
            out_path = out_path_base if os.path.splitext(out_path_base)[1] else out_path_base + ext
            final_url = resp.geturl()
            content_type = resp.headers.get("Content-Type")
            with open(out_path, "wb") as f:
                while True:
                    chunk = resp.read(1024 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)
            return out_path, {"final_url": final_url, "content_type": content_type}

    return retry_call(run, retries=retries, sleep_s=retry_sleep)


def cmd_list(args: argparse.Namespace) -> int:
    data = ensure_ok(list_models_page(args.appid, args.page, args.length, args.search, args.uniform_type, args.task or [], args.timeout, args.retries, args.retry_sleep), "list_model")
    items = data.get("list") or []
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        for item in items:
            print(f"{item.get('id')}\t{item.get('name')}\ttask={item.get('task')}\tuniform_types={','.join(item.get('uniform_types') or [])}")
    return 0


def cmd_view(args: argparse.Namespace) -> int:
    data = ensure_ok(view_model(args.appid, args.model_id, args.timeout, args.retries, args.retry_sleep), f"view_model {args.model_id}")
    print(json.dumps(annotate_model(normalize_detail(data)), ensure_ascii=False, indent=2))
    return 0


def cmd_index(args: argparse.Namespace) -> int:
    models = collect_models(args.appid, args.length, args.search, args.uniform_type, args.task or [], args.model_format, args.timeout, args.sleep, args.retries, args.retry_sleep)
    summary = summarize_models(models)

    if args.summary_json:
        export_json(summary, args.summary_json)

    if args.summary:
        print(json.dumps(summary, ensure_ascii=False, indent=2), file=sys.stderr)

    if args.format == "json":
        if args.output:
            export_json(models, args.output)
        else:
            print(json.dumps(models, ensure_ascii=False, indent=2))
    elif args.format == "csv":
        if not args.output:
            raise SystemExit("--output is required for --format csv")
        export_csv(models, args.output)
    else:
        print_table(models, include_url=not args.no_url)
    return 0


def cmd_download(args: argparse.Namespace) -> int:
    ids: List[str] = list(args.model_id or [])
    if args.from_index:
        with open(args.from_index, "r", encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            mid = str(item.get("id"))
            if mid and mid not in ids:
                ids.append(mid)
    if not ids:
        raise SystemExit("provide --model-id or --from-index")

    os.makedirs(args.output_dir, exist_ok=True)
    manifest = []
    for model_id in ids:
        try:
            data = ensure_ok(view_model(args.appid, str(model_id), args.timeout, args.retries, args.retry_sleep), f"view_model {model_id}")
        except Exception as e:
            print(f"warn: skip model {model_id}: {e}", file=sys.stderr)
            continue
        model = annotate_model(normalize_detail(data))
        url = model.get("file_url")
        if not url:
            print(f"warn: model {model_id} has no file_url", file=sys.stderr)
            continue
        base_name = f"{model['id']}-{safe_name(str(model.get('name') or 'model'))}"
        out_base = os.path.join(args.output_dir, base_name)
        print(f"download: {model['id']} -> {out_base}", file=sys.stderr)
        download_path, meta = download_file(str(url), out_base, args.timeout, args.retries, args.retry_sleep)
        model["download_path"] = download_path
        model["download_content_type"] = meta.get("content_type")
        model["download_final_url"] = meta.get("final_url")
        manifest.append(model)
        if args.sleep:
            time.sleep(args.sleep)

    summary = summarize_models(manifest)
    if args.manifest:
        export_json(manifest, args.manifest)
    else:
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
    if args.summary_json:
        export_json(summary, args.summary_json)
    if args.summary:
        print(json.dumps(summary, ensure_ascii=False, indent=2), file=sys.stderr)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="SenseCraft public model helper")
    p.add_argument("--appid", default=DEFAULT_APPID)
    p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    p.add_argument("--retries", type=int, default=DEFAULT_RETRIES)
    p.add_argument("--retry-sleep", type=float, default=DEFAULT_SLEEP)

    sub = p.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="list one page of public models")
    p_list.add_argument("--page", type=int, default=1)
    p_list.add_argument("--length", type=int, default=30)
    p_list.add_argument("--search")
    p_list.add_argument("--uniform-type")
    p_list.add_argument("--task", action="append")
    p_list.add_argument("--json", action="store_true")
    p_list.set_defaults(func=cmd_list)

    p_view = sub.add_parser("view", help="view one model detail")
    p_view.add_argument("model_id")
    p_view.set_defaults(func=cmd_view)

    p_index = sub.add_parser("index", help="crawl full public index via list -> view")
    p_index.add_argument("--length", type=int, default=DEFAULT_PAGE_SIZE)
    p_index.add_argument("--search")
    p_index.add_argument("--uniform-type")
    p_index.add_argument("--task", action="append")
    p_index.add_argument("--model-format")
    p_index.add_argument("--sleep", type=float, default=DEFAULT_SLEEP, help="seconds between detail requests")
    p_index.add_argument("--format", choices=["table", "json", "csv"], default="json")
    p_index.add_argument("--output")
    p_index.add_argument("--summary", action="store_true", help="print aggregate summary to stderr")
    p_index.add_argument("--summary-json", help="write aggregate summary JSON")
    p_index.add_argument("--no-url", action="store_true", help="omit file_url in table output")
    p_index.set_defaults(func=cmd_index)

    p_dl = sub.add_parser("download", help="download one or more model files")
    p_dl.add_argument("--model-id", action="append")
    p_dl.add_argument("--from-index", help="load ids from a JSON index file produced by index")
    p_dl.add_argument("--output-dir", default="./downloads")
    p_dl.add_argument("--manifest", help="write downloaded model manifest as JSON")
    p_dl.add_argument("--summary", action="store_true", help="print aggregate summary to stderr")
    p_dl.add_argument("--summary-json", help="write aggregate summary JSON")
    p_dl.add_argument("--sleep", type=float, default=DEFAULT_SLEEP)
    p_dl.set_defaults(func=cmd_download)

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
