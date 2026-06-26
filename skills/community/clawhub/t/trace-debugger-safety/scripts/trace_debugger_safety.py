#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import re
import urllib.error
import urllib.request
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def jdump(o: Dict[str, Any]) -> str:
    return json.dumps(o, ensure_ascii=False, separators=(",", ":"))


def http_get_json(url: str, timeout: int = 20) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status != 200:
                return None, f"HTTP {resp.status}"
            data = resp.read().decode("utf-8", errors="replace")
            obj = json.loads(data)
            if not isinstance(obj, dict):
                return None, "response is not json object"
            return obj, None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return None, f"URL error: {getattr(e, 'reason', e)}"
    except Exception as e:
        return None, str(e)


def http_search_json(url: str, body: Dict[str, Any], timeout: int = 20) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        data = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="GET", headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status != 200:
                return None, f"HTTP {resp.status}"
            raw = resp.read().decode("utf-8", errors="replace")
            obj = json.loads(raw)
            if not isinstance(obj, dict):
                return None, "response is not json object"
            return obj, None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return None, f"URL error: {getattr(e, 'reason', e)}"
    except Exception as e:
        return None, str(e)


def tag_map(tags: Any) -> Dict[str, Any]:
    m: Dict[str, Any] = {}
    if isinstance(tags, list):
        for t in tags:
            if isinstance(t, dict) and "key" in t:
                m[str(t.get("key"))] = t.get("value")
    return m


def parent_span_id(refs: Any) -> Optional[str]:
    if not isinstance(refs, list):
        return None
    for r in refs:
        if isinstance(r, dict) and r.get("refType") == "CHILD_OF":
            sid = r.get("spanID")
            return str(sid) if sid is not None else None
    return None


def normalize_jaeger(trace: Dict[str, Any]) -> Dict[str, Any]:
    data = trace.get("data")
    if not isinstance(data, list) or not data or not isinstance(data[0], dict):
        return {"error": "missing data[0]"}
    t = data[0]
    spans = t.get("spans") if isinstance(t.get("spans"), list) else []
    processes = t.get("processes") if isinstance(t.get("processes"), dict) else {}

    out_spans = []
    min_start = None
    max_end = None
    error_count = 0
    services = set()
    roots = 0

    for s in spans:
        if not isinstance(s, dict):
            continue
        sid = str(s.get("spanID", ""))
        pid = parent_span_id(s.get("references"))
        if pid is None:
            roots += 1
        p = processes.get(s.get("processID"), {}) if isinstance(processes, dict) else {}
        svc = str(p.get("serviceName", "unknown")) if isinstance(p, dict) else "unknown"
        services.add(svc)
        op = str(s.get("operationName", ""))
        st = int(s.get("startTime", 0) or 0)
        du = int(s.get("duration", 0) or 0)
        tags = tag_map(s.get("tags"))
        is_err = tags.get("error") is True or str(tags.get("otel.status_code", "")).upper() == "ERROR"
        status = "ERROR" if is_err else "OK"
        if is_err:
            error_count += 1
        out_spans.append({
            "ts_us": st,
            "span_id": sid,
            "parent_span_id": pid,
            "service": svc,
            "operation": op,
            "duration_ms": round(du / 1000.0, 3),
            "status": status,
            "tags": tags,
        })
        min_start = st if min_start is None else min(min_start, st)
        max_end = (st + du) if max_end is None else max(max_end, st + du)

    out_spans.sort(key=lambda x: x["ts_us"])
    total_ms = round(((max_end or 0) - (min_start or 0)) / 1000.0, 3)

    return {
        "spans": out_spans,
        "total_duration_ms": total_ms,
        "has_defect": error_count > 0,
        "chain_count": roots,
        "span_count": len(out_spans),
        "service_count": len(services),
        "error_span_count": error_count,
        "start_us": min_start or 0,
        "end_us": max_end or 0,
    }


def us_to_iso(us: int) -> str:
    ts = dt.datetime.fromtimestamp(us / 1_000_000.0, tz=dt.timezone.utc)
    return ts.strftime("%Y-%m-%dT%H:%M:%SZ")


def normalize_es_logs(es_resp: Dict[str, Any]) -> List[Dict[str, Any]]:
    hits = es_resp.get("hits", {}).get("hits", [])
    if not isinstance(hits, list):
        return []

    logs: List[Dict[str, Any]] = []
    for h in hits:
        if not isinstance(h, dict):
            continue
        src = h.get("_source") if isinstance(h.get("_source"), dict) else {}
        fields = src.get("fields") if isinstance(src.get("fields"), dict) else {}
        ts = src.get("@timestamp")
        msg = src.get("msg") or src.get("message") or src.get("log") or ""
        logs.append({
            "ts": str(ts) if ts is not None else "",
            "service": src.get("fields.service") or fields.get("service") or src.get("service") or "unknown",
            "span_id": src.get("span_id") or "",
            "level": src.get("level") or "",
            "msg": str(msg),
            "error": src.get("error") or "",
            "caller": src.get("caller") or "",
            "raw": src,
        })

    logs.sort(key=lambda x: x.get("ts", ""))
    return logs


def parse_codex_sections(codex_result: Optional[str]) -> Tuple[List[str], List[str]]:
    reasons: List[str] = []
    suggestions: List[str] = []
    if not codex_result:
        return reasons, suggestions

    m1 = re.search(r"1\)\s*Bug原因[:：]\s*(.+)", codex_result)
    m3 = re.search(r"3\)\s*解决方案[:：]\s*(.+)", codex_result)
    if m1:
        reasons.append(m1.group(1).strip())
    if m3:
        suggestions.append(m3.group(1).strip())
    return reasons, suggestions


def repo_hint_analysis(repo_path: str, logs: List[Dict[str, Any]]) -> List[str]:
    hints: List[str] = []
    if not repo_path or not os.path.isabs(repo_path) or not os.path.isdir(repo_path):
        return hints

    corpus = " ".join([(l.get("msg") or "") + " " + (l.get("error") or "") for l in logs]).lower()
    tokens = [t for t in re.findall(r"[a-zA-Z_]{4,}", corpus) if t not in {"error", "failed", "timeout", "panic", "trace"}]
    uniq = []
    for t in tokens:
        if t not in uniq:
            uniq.append(t)
        if len(uniq) >= 8:
            break

    matches = []
    for root, _, files in os.walk(repo_path):
        for fn in files:
            if not fn.endswith(".go"):
                continue
            fp = os.path.join(root, fn)
            try:
                with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                for tk in uniq:
                    if tk in content.lower():
                        matches.append((fp, tk))
                        break
            except Exception:
                continue
            if len(matches) >= 10:
                break
        if len(matches) >= 10:
            break

    for fp, tk in matches[:10]:
        hints.append(f"代码命中关键词 `{tk}`: {fp}")
    return hints


def collect_caller_context(repo_path: str, logs: List[Dict[str, Any]], max_items: int = 8) -> List[str]:
    if not repo_path or not os.path.isdir(repo_path):
        return []

    out: List[str] = []
    seen = set()
    for l in logs:
        caller = str(l.get("caller") or "")
        m = re.match(r"^(.+?):(\d+)$", caller)
        if not m:
            continue
        rel, line_s = m.group(1), m.group(2)
        key = f"{rel}:{line_s}"
        if key in seen:
            continue
        seen.add(key)

        fp = os.path.join(repo_path, rel)
        if not os.path.isfile(fp):
            # basename fallback
            base = os.path.basename(rel)
            found = None
            for root, _, files in os.walk(repo_path):
                if base in files:
                    found = os.path.join(root, base)
                    break
            if found:
                fp = found

        if not os.path.isfile(fp):
            continue

        try:
            line_no = int(line_s)
            with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
            idx = max(0, min(len(lines) - 1, line_no - 1))
            code = lines[idx].strip()
            out.append(f"{caller} -> {fp} :: {code}")
        except Exception:
            continue

        if len(out) >= max_items:
            break

    return out


def md_table(headers: List[str], rows: List[List[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        out.append("| " + " | ".join([c.replace("|", "\\|").replace("\n", " ") for c in r]) + " |")
    return "\n".join(out)


def run_codex_analysis(repo_path: str, logs: List[Dict[str, Any]]) -> Tuple[Optional[str], Optional[str]]:
    if not repo_path or not os.path.isdir(repo_path):
        return None, "repo_path 不存在，跳过 codex 分析"

    # 控制上下文长度，避免提示词过大
    picked = logs[:200]
    payload = "\n".join([json.dumps(l, ensure_ascii=False) for l in picked])
    prompt = (
        "这是我的日志，请根据日志结合代码帮我排查分析bug，输出bug原因及解决方案,必须保持固定的格式。\n"
        "固定格式如下：\n"
        "1) Bug原因：<...>\n"
        "2) 证据：<...>\n"
        "3) 解决方案：<...>\n\n"
        "日志如下（JSON Lines）：\n" + payload
    )

    try:
        p = subprocess.run(
            ["codex", "exec", prompt],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=240,
        )
        if p.returncode != 0:
            return None, f"codex 执行失败: rc={p.returncode}, stderr={p.stderr[:500]}"
        return p.stdout.strip(), None
    except Exception as e:
        return None, f"codex 执行异常: {e}"


def main() -> int:
    ap = argparse.ArgumentParser(description="trace_debuger")
    ap.add_argument("--trace-id", required=True)
    ap.add_argument("--jaeger-url", default="http://127.0.0.1:16686")
    ap.add_argument("--es-url", default="http://127.0.0.1:9200")
    ap.add_argument("--repo-path", default="/Users/noodles/Desktop/code/go-components/examples/tracer")
    ap.add_argument("--output-path", default="")
    ap.add_argument("--es-index", default="filebeat-tracer-*")
    ap.add_argument("--es-size", type=int, default=2000)
    args = ap.parse_args()

    trace_id = args.trace_id
    output_path = args.output_path or f"./trace_debug_report_{trace_id}.md"

    # 1) Jaeger
    jaeger_url = args.jaeger_url.rstrip("/") + f"/api/traces/{trace_id}"
    j_raw, j_err = http_get_json(jaeger_url)

    summary = {
        "total_duration_ms": 0.0,
        "has_defect": False,
        "chain_count": 0,
        "span_count": 0,
        "service_count": 0,
        "error_span_count": 0,
        "start_us": 0,
        "end_us": 0,
    }
    spans: List[Dict[str, Any]] = []

    if j_raw is not None:
        nj = normalize_jaeger(j_raw)
        if "error" not in nj:
            summary.update({k: nj[k] for k in summary.keys() if k in nj})
            spans = nj.get("spans", [])
        else:
            j_err = nj["error"]

    # 2) ES logs
    logs: List[Dict[str, Any]] = []
    es_err = None
    if summary["start_us"] and summary["end_us"]:
        start_iso = us_to_iso(max(0, int(summary["start_us"]) - 30 * 1_000_000))
        end_iso = us_to_iso(max(0, int(summary["end_us"]) + 30 * 1_000_000))
    else:
        start_iso, end_iso = None, None

    filters = [{"bool": {"should": [{"term": {"trace_id.keyword": trace_id}}, {"term": {"trace_id": trace_id}}], "minimum_should_match": 1}}]
    if start_iso and end_iso:
        filters.append({"range": {"@timestamp": {"gte": start_iso, "lte": end_iso}}})

    es_query = {
        "query": {"bool": {"filter": filters}},
        "sort": [{"@timestamp": {"order": "asc"}}],
        "size": int(args.es_size),
    }
    es_search_url = args.es_url.rstrip("/") + f"/{args.es_index}/_search"
    es_raw, es_err = http_search_json(es_search_url, es_query)
    if es_raw is not None:
        logs = normalize_es_logs(es_raw)

    # 3) Bug analysis（由 Codex 日志+代码联合分析主导）
    code_hints = repo_hint_analysis(args.repo_path, logs) if args.repo_path else []
    caller_context = collect_caller_context(args.repo_path, logs) if args.repo_path else []

    codex_result, codex_err = run_codex_analysis(args.repo_path, logs) if logs else (None, None)
    reasons, suggestions = parse_codex_sections(codex_result)

    # de-duplicate while preserving order
    reasons = list(dict.fromkeys(reasons))
    suggestions = list(dict.fromkeys(suggestions))

    status = "PASS"
    if j_err or es_err:
        status = "WARN"
    if summary.get("has_defect") or reasons:
        status = "WARN"
    if summary.get("error_span_count", 0) > 0:
        status = "FAIL"

    # 4) markdown
    lines: List[str] = []
    lines.append(f"# Trace Debug Report: {trace_id}")
    lines.append("")
    lines.append("## 1. 链路概览")
    lines.append("")
    lines.append(f"- 结论状态: **{status}**")
    lines.append(f"- 整条链路耗时: {summary.get('total_duration_ms', 0.0)} ms")
    lines.append(f"- 是否存在缺陷: {'是' if summary.get('has_defect') else '否'}")
    lines.append(f"- 链路数(root spans): {summary.get('chain_count', 0)}")
    lines.append(f"- span数: {summary.get('span_count', 0)}")
    lines.append(f"- 服务数: {summary.get('service_count', 0)}")
    lines.append(f"- error spans: {summary.get('error_span_count', 0)}")
    lines.append(f"- 日志数: {len(logs)}")
    if j_err:
        lines.append(f"- Jaeger 查询异常: {j_err}")
    if es_err:
        lines.append(f"- ES 查询异常: {es_err}")
    lines.append("")

    lines.append("## 2. Jaeger Span 明细（时间升序）")
    lines.append("")
    if spans:
        rows = []
        for s in spans:
            rows.append([
                str(s.get("ts_us", "")),
                str(s.get("service", "")),
                str(s.get("operation", "")),
                str(s.get("span_id", "")),
                str(s.get("parent_span_id", "")),
                str(s.get("duration_ms", "")),
                str(s.get("status", "")),
            ])
        lines.append(md_table(["start_us", "service", "operation", "span_id", "parent_span_id", "duration_ms", "status"], rows))
    else:
        lines.append("无 span 数据。")
    lines.append("")

    lines.append("## 3. ES 日志明细（时间升序）")
    lines.append("")
    if logs:
        rows = []
        for l in logs:
            rows.append([
                str(l.get("ts", "")),
                str(l.get("service", "")),
                str(l.get("span_id", "")),
                str(l.get("level", "")),
                str(l.get("msg", ""))[:300],
                str(l.get("error", ""))[:300],
                str(l.get("caller", ""))[:200],
            ])
        lines.append(md_table(["ts", "service", "span_id", "level", "msg", "error", "caller"], rows))
    else:
        lines.append("无日志数据。")
    lines.append("")

    lines.append("## 4. Bug 分析与修复建议")
    lines.append("")
    lines.append("> ⚠️ CAUTION: 主要风险在于 codex exec 的 prompt 注入面。不建议在不可信日志环境下直接使用。")
    lines.append("")
    lines.append("")
    if reasons:
        lines.append("### 可能原因")
        for r in reasons:
            lines.append(f"- {r}")
    else:
        lines.append("- 当前未识别到明显 bug 特征。")
    lines.append("")

    lines.append("### 修复建议")
    if suggestions:
        for s in suggestions:
            lines.append(f"- {s}")
    else:
        lines.append("- 建议补充结构化日志与错误码，提升可观测性。")
    lines.append("")

    lines.append("### Codex 分析结果（日志+代码）")
    if codex_result:
        lines.append("```text")
        lines.append(codex_result)
        lines.append("```")
    else:
        lines.append(f"- Codex 分析未产出结果：{codex_err or 'unknown error'}")
    lines.append("")

    if args.repo_path:
        lines.append("### 代码仓库关联分析")
        lines.append(f"- repo_path: {args.repo_path}")
        if code_hints:
            for h in code_hints:
                lines.append(f"- {h}")
        else:
            lines.append("- 未在仓库中找到与日志关键词高度相关的 Go 文件命中。")

        lines.append("")
        lines.append("### 代码行级证据（来自日志 caller）")
        if caller_context:
            for c in caller_context:
                lines.append(f"- {c}")
        else:
            lines.append("- 未能根据 caller 定位到代码行，请检查日志 caller 与仓库相对路径是否一致。")
        lines.append("")

    lines.append("---")
    lines.append(f"Generated at: {dt.datetime.now(dt.timezone.utc).isoformat()}")

    p = Path(output_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")

    status_out = "FAIL" if status == "FAIL" else "SUCCESS"
    codex_summary = ""
    if codex_result:
        first = codex_result.splitlines()[0].strip()
        codex_summary = first[:120]
    key_summary = "；".join(reasons[:2]) if reasons else "未发现明确异常关键词，建议继续结合上下游调用与参数排查"
    if codex_summary:
        key_summary = f"{key_summary}；Codex: {codex_summary}"

    print(f"trace_id: {trace_id}")
    print(f"status: {status_out}")
    print(f"jaeger_url: {args.jaeger_url}")
    print(f"es_url: {args.es_url}")
    print(f"代码仓库路径：{args.repo_path if args.repo_path else 'N/A'}")
    print(f"关键结论摘要：{key_summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
