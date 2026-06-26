#!/usr/bin/env python3
"""
OpenClaw Usage Statistics Analyzer v3
读取 ~/.qclaw/agents/main/sessions/ 下的所有会话记录，生成完整使用统计报告。
支持：Token消耗、费用、模型分布、缓存命中率、时段分析、日趋势、错误统计等。
"""

import json, os, sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from datetime import datetime, date, timedelta
from pathlib import Path
from collections import defaultdict, Counter

# ── 配置 ──────────────────────────────────────────────────
HOME        = Path.home()
AGENTS_DIR  = HOME / ".qclaw" / "agents"
OUTPUT_DIR  = HOME / ".qclaw" / "workspace" / "memory"
OUTPUT_FILE = OUTPUT_DIR / "usage_stats_latest.md"

# ── 工具函数 ───────────────────────────────────────────────
def find_all_jsonl(base: Path):
    sessions_dir = base / "main" / "sessions"
    if not sessions_dir.exists():
        return []
    return [
        f for f in sessions_dir.iterdir()
        if f.suffix == ".jsonl"
        and not f.name.endswith(".lock")
        and ".deleted" not in f.name
    ]

def parse_jsonl(path: Path):
    messages = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    messages.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    except Exception as e:
        print(f"[WARN] read {path.name}: {e}", file=sys.stderr)
    return messages

def to_unix_ms(val):
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return int(val) if val > 1e12 else int(val * 1000)
    if isinstance(val, str):
        try:
            dt = datetime.fromisoformat(val.replace("Z", "+00:00"))
            return int(dt.timestamp() * 1000)
        except ValueError:
            try:
                # Try parsing with different formats
                for fmt in ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S"]:
                    try:
                        dt = datetime.strptime(val[:19], fmt)
                        return int(dt.timestamp() * 1000)
                    except ValueError:
                        continue
            except Exception:
                pass
            return None
    return None

def session_time_range(messages):
    ts_list = []
    for msg in messages:
        if isinstance(msg, dict):
            ts = msg.get("timestamp") or msg.get("createdAt")
            ms = to_unix_ms(ts)
            if ms:
                ts_list.append(ms)
    if not ts_list:
        return None, None
    return min(ts_list), max(ts_list)

def extract_error_info(text: str, session_date: str):
    """从原始文本片段提取结构化错误信息"""
    errors = []

    # Python 错误
    for pat in [
        (r"ModuleNotFoundError: No module named '(\w+)'", "python_missing_module"),
        (r"(Unicode(?:Encode|Decode)Error): (.+?)(?:\r?\n|$)", "python_encoding"),
        (r"(ValueError|TypeError|EOFError|OSError|RuntimeError): (.+?)(?:\r?\n|$)", "python_exception"),
        (r"Traceback \(most recent call last\):\s+(.+?)(?=\n\n|\nCommand)", "python_traceback"),
        (r"Command exited with code (\d+)", "exit_code"),
        (r"\+ CategoryInfo\s+:\s+(\w+Error):(.+?)(?:\r?\n    \+|\r?\nCommand|\n\n)", "pwsh_error"),
        (r"FullyQualifiedErrorId\s+:\s+([\w,]+)", "pwsh_error_id"),
        (r"HTTP Error (\d+):", "http_error"),
        (r"errorCode:\s*(\d+)", "error_code"),
    ]:
        import re
        for m in re.finditer(pat[0], text, re.IGNORECASE):
            err_type = pat[1]
            err_msg = m.group(0)[:150]
            errors.append({
                "type": err_type,
                "message": err_msg,
                "session": session_date
            })

    return errors

# ── 数据提取 ───────────────────────────────────────────────
def extract_data_from_messages(messages, session_date: str):
    total_input  = 0
    total_output = 0
    total_tokens = 0
    cache_read   = 0
    cache_write  = 0
    total_cost   = 0.0
    msg_count    = 0
    turns        = 0
    model_stats  = defaultdict(lambda: {"input":0,"output":0,"total":0,"turns":0,"cost":0.0})

    # 错误统计
    errors = []

    # ── 新增统计 ──
    tool_stats   = defaultdict(int)   # tool_name → count
    exec_durations = []               # exec 调用耗时 ms
    stop_reasons   = Counter()        # stopReason 分布
    roles          = Counter()         # role 分布
    custom_types   = Counter()        # customType 分布
    input_text_lens = []              # user 输入长度（字符数）
    output_text_lens = []             # assistant 输出长度（字符数）

    for raw in messages:
        usage = None
        role  = None
        model = None
        is_error = False
        error_msg = None

        if isinstance(raw, dict):
            inner = raw.get("message")
            if isinstance(inner, dict):
                role  = inner.get("role")
                usage = inner.get("usage")
                model = inner.get("model") or inner.get("modelId")
            elif "usage" in raw:
                usage = raw["usage"]
                role  = raw.get("role")
                model = raw.get("model") or raw.get("modelId")

            # 检查 stopReason
            stop_reason = raw.get("stopReason", "")
            error_message = raw.get("errorMessage", "")
            if stop_reason in ("error", "aborted"):
                is_error = True
                error_msg = error_message or stop_reason

            # 检查 toolCall 结果中的错误
            if isinstance(inner, dict):
                content = inner.get("content", [])
                if isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict):
                            block_type = block.get("type", "")
                            # tool result with error
                            if block_type == "toolResult":
                                result_text = json.dumps(block, ensure_ascii=False)
                                errs = extract_error_info(result_text, session_date)
                                errors.extend(errs)

                            # text block that might contain error
                            elif block_type == "text":
                                txt = str(block.get("text", ""))
                                if any(k in txt.lower() for k in ["error", "traceback", "failed", "exception"]):
                                    errs = extract_error_info(txt, session_date)
                                    errors.extend(errs)

                            # tool use block
                            elif block_type == "toolCall":
                                status = block.get("status", "")
                                if status == "error":
                                    tool_name = block.get("name", "?")
                                    err_text = block.get("text", "")
                                    errors.append({
                                        "type": f"tool_error_{tool_name}",
                                        "message": err_text[:200] if err_text else status,
                                        "session": session_date
                                    })

            # 检查 tool_result content 数组
            if isinstance(inner, dict):
                content = inner.get("content", [])
                if isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "toolResult":
                            tool_name = block.get("name", "?")
                            result_text = json.dumps(block, ensure_ascii=False)
                            errs = extract_error_info(result_text, session_date)
                            errors.extend(errs)

        if usage and isinstance(usage, dict):
            inp   = usage.get("input", 0) or 0
            out   = usage.get("output", 0) or 0
            tot   = usage.get("totalTokens", 0) or 0
            cread  = usage.get("cacheRead", 0) or 0
            cwrite = usage.get("cacheWrite", 0) or 0

            cost = usage.get("cost", {})
            cost_val = 0.0
            if isinstance(cost, dict):
                cost_val = cost.get("total", 0) or 0
            elif isinstance(cost, (int, float)):
                cost_val = cost

            total_input  += inp
            total_output += out
            total_tokens += tot
            cache_read   += cread
            cache_write  += cwrite
            total_cost   += cost_val

            if role == "assistant":
                turns += 1

            msg_count += 1

            if model and role == "assistant":
                ms = model_stats[model]
                ms["input"]  += inp
                ms["output"] += out
                ms["total"] += tot
                ms["turns"] += 1
                ms["cost"]  += cost_val

            # ── 新增字段提取 ──
            # stopReason
            sr = inner.get("stopReason")
            if sr:
                stop_reasons[sr] += 1

            # role 分布
            if role:
                roles[role] += 1

            # customType 分布（仅取 top）
            ct = raw.get("customType")
            if ct:
                custom_types[ct] += 1

            # 工具调用统计（从 toolCall block）
            content = inner.get("content", []) if isinstance(inner, dict) else []
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "toolCall":
                        tn = block.get("name", "?")
                        tool_stats[tn] += 1
                        # exec 调用记录执行时长
                        if tn == "exec":
                            details = block.get("details", {})
                            dur = details.get("durationMs", 0) if isinstance(details, dict) else 0
                            if dur:
                                exec_durations.append(dur)

            # 用户输入 / AI 输出文本长度
            if role == "user":
                txt = _extract_text_from_content(content)
                if txt:
                    input_text_lens.append(len(txt))
            elif role == "assistant":
                txt = _extract_text_from_content(content)
                if txt:
                    output_text_lens.append(len(txt))

    return {
        "input":       total_input,
        "output":      total_output,
        "total":       total_tokens,
        "cacheRead":   cache_read,
        "cacheWrite":  cache_write,
        "cost":        total_cost,
        "msg_count":   msg_count,
        "turns":       turns,
        "model_stats": dict(model_stats),
        "errors":      errors,
        "tool_stats":  dict(tool_stats),
        "exec_durations": exec_durations,
        "stop_reasons": dict(stop_reasons),
        "roles":       dict(roles),
        "custom_types": dict(custom_types),
        "input_text_lens":  input_text_lens,
        "output_text_lens": output_text_lens,
    }


def _extract_text_from_content(content):
    """从 content blocks 中提取纯文本"""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    parts.append(str(block.get("text", "")))
        return "\n".join(parts)
    return ""

# ── 主分析 ──────────────────────────────────────────────────
def main():
    files = find_all_jsonl(AGENTS_DIR)
    if not files:
        print("[ERROR] No session files found: ~/.qclaw/agents/main/sessions/")
        sys.exit(1)

    print(f"Found {len(files)} session files, analyzing...")

    all_sessions  = []
    date_stats   = defaultdict(lambda: {
        "input":0,"output":0,"total":0,"cacheRead":0,"cacheWrite":0,
        "cost":0.0,"sessions":0,"turns":0,"errors":0
    })
    global_model = defaultdict(lambda: {"input":0,"output":0,"total":0,"turns":0,"cost":0.0})
    all_errors   = []

    for f in sorted(files, key=lambda x: x.stat().st_mtime):
        messages = parse_jsonl(f)
        if not messages:
            continue

        data    = extract_data_from_messages(messages, f.stem[:10])
        t0, t1  = session_time_range(messages)

        start_dt = datetime.fromtimestamp(t0 / 1000) if t0 else None
        end_dt   = datetime.fromtimestamp(t1 / 1000) if t1 else None
        duration_ms  = (t1 - t0) if (t0 and t1) else 0
        duration_min = round(duration_ms / 60000, 1)

        date_key = start_dt.strftime("%Y-%m-%d") if start_dt else "unknown"

        session = {
            "file":        f.stem,
            "date":        date_key,
            "start":       start_dt.strftime("%Y-%m-%d %H:%M") if start_dt else "?",
            "end":         end_dt.strftime("%Y-%m-%d %H:%M")   if end_dt   else "?",
            "duration_min": duration_min,
            **data,
        }
        all_sessions.append(session)

        date_stats[date_key]["input"]     += data["input"]
        date_stats[date_key]["output"]    += data["output"]
        date_stats[date_key]["total"]     += data["total"]
        date_stats[date_key]["cacheRead"] += data["cacheRead"]
        date_stats[date_key]["cacheWrite"]+= data["cacheWrite"]
        date_stats[date_key]["cost"]     += data["cost"]
        date_stats[date_key]["sessions"]  += 1
        date_stats[date_key]["turns"]    += data["turns"]
        date_stats[date_key]["errors"]   += len(data["errors"])

        for model, ms in data["model_stats"].items():
            gm = global_model[model]
            gm["input"]  += ms["input"]
            gm["output"] += ms["output"]
            gm["total"] += ms["total"]
            gm["turns"] += ms["turns"]
            gm["cost"]  += ms["cost"]

        all_errors.extend(data["errors"])

    # ── 新增：全局聚合 ───────────────────────────────────
    from collections import Counter
    global_tool_stats   = Counter()
    global_stop_reasons = Counter()
    global_roles        = Counter()
    global_custom_types = Counter()
    all_exec_durations  = []
    all_input_lens      = []
    all_output_lens     = []

    for s in all_sessions:
        for tool, cnt in s.get("tool_stats", {}).items():
            global_tool_stats[tool] += cnt
        for k, v in s.get("stop_reasons", {}).items():
            global_stop_reasons[k] += v
        for k, v in s.get("roles", {}).items():
            global_roles[k] += v
        for k, v in s.get("custom_types", {}).items():
            global_custom_types[k] += v
        all_exec_durations.extend(s.get("exec_durations", []))
        all_input_lens.extend(s.get("input_text_lens", []))
        all_output_lens.extend(s.get("output_text_lens", []))

    # exec 时长统计
    if all_exec_durations:
        exec_avg = sum(all_exec_durations) / len(all_exec_durations)
        exec_max = max(all_exec_durations)
        exec_min = min(all_exec_durations)
    else:
        exec_avg = exec_max = exec_min = 0

    # ── 汇总 ─────────────────────────────────────────────
    total_input    = sum(s["input"]     for s in all_sessions)
    total_output   = sum(s["output"]    for s in all_sessions)
    total_tokens   = sum(s["total"]     for s in all_sessions)
    total_cache_r  = sum(s["cacheRead"] for s in all_sessions)
    total_cache_w  = sum(s["cacheWrite"] for s in all_sessions)
    total_cost     = sum(s["cost"]      for s in all_sessions)
    total_turns    = sum(s["turns"]     for s in all_sessions)
    total_msgs     = sum(s["msg_count"] for s in all_sessions)
    total_sessions = len(all_sessions)
    total_errors   = len(all_errors)

    all_times  = [(s["start"], s["end"]) for s in all_sessions if s["start"] != "?"]
    first_date = min(t[0] for t in all_times) if all_times else "?"
    last_date  = max(t[1] for t in all_times) if all_times else "?"

    active_days     = sorted(d for d in date_stats if d != "unknown")
    num_active_days = len(active_days)

    # 墙钟时间 vs 真实活跃时间（相邻消息间隔超过30min的不计入）
    total_dur_min  = sum(s["duration_min"] for s in all_sessions)
    # 计算真实活跃时长
    import calendar
    cal_span_days = 0
    if all_sessions:
        dates = [date.fromisoformat(s["date"]) for s in all_sessions if s["date"] and s["date"] != "unknown"]
        if dates:
            cal_span_days = (max(dates) - min(dates)).days + 1
    cal_span_days = cal_span_days or 1

    # 重新计算活跃时长（基于消息时间差，去掉>30min的空闲gap）
    total_active_min = 0
    for f in find_all_jsonl(AGENTS_DIR):
        msgs = parse_jsonl(f)
        ts_list = sorted([to_unix_ms(m.get("timestamp") or m.get("createdAt"))
                          for m in msgs])
        ts_list = [t for t in ts_list if t]
        for i in range(1, len(ts_list)):
            gap = ts_list[i] - ts_list[i-1]
            if gap < 30*60*1000:  # 30min以内算活跃
                total_active_min += gap / 60000

    active_min_per_day_cal  = total_active_min / cal_span_days
    active_min_per_day_sess = total_active_min / num_active_days if num_active_days else 0
    avg_dur = total_dur_min / total_sessions if total_sessions else 0
    cache_total    = total_cache_r + total_cache_w
    cache_hit_rate = total_cache_r / cache_total * 100 if cache_total > 0 else 0

    # 时段分布
    hour_dist = defaultdict(int)
    for s in all_sessions:
        if s["start"] != "?":
            try:
                h = int(s["start"].split()[1].split(":")[0])
                hour_dist[h] += 1
            except:
                pass

    peak_hours = sorted(hour_dist.items(), key=lambda x: -x[1])[:3]
    peak_str   = ", ".join(f"{h}:00 ({c}次)" for h, c in peak_hours) if peak_hours else "data insufficient"

    # 错误汇总统计
    error_types = defaultdict(lambda: {"count":0, "examples":[]})
    for err in all_errors:
        key = err["type"]
        error_types[key]["count"] += 1
        if len(error_types[key]["examples"]) < 2:
            error_types[key]["examples"].append(err["message"][:120])

    # 模型别名美化
    MODEL_LABELS = {
        "modelroute":           "QClaw 模型路由",
        "gateway-injected":     "系统注入",
        "unknown":              "未知模型",
    }
    def pretty_model(name):
        return MODEL_LABELS.get(name, name)

    # ── 报告生成 ────────────────────────────────────────────
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    def fmt_cost(v):
        return f"${v:.6f}" if v > 0 else "$0"

    def fmt_token(v):
        if v >= 1_000_000: return f"{v/1_000_000:.1f}M"
        if v >= 1_000:     return f"{v/1_000:.0f}K"
        return str(v)

    lines = [
        "# QClaw 使用统计报告",
        "",
        f"**Generated**: {now_str}",
        f"**Range**: {first_date} ~ {last_date}",
        f"**Active days**: {num_active_days}  |  **Sessions**: {total_sessions}",
        "",
        "---",
        "",
        "## Overall Stats",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Total cost | {fmt_cost(total_cost)} |",
        f"| Total tokens | {fmt_token(total_tokens)} |",
        f"|   Input | {fmt_token(total_input)} |",
        f"|   Output | {fmt_token(total_output)} |",
        f"| Cache hit | {fmt_token(total_cache_r)} ({cache_hit_rate:.1f}% hit rate) |",
        f"| Cache write | {fmt_token(total_cache_w)} |",
        f"| Messages | {total_msgs} |",
        f"| AI turns | {total_turns} |",
        f"| Wall clock time | {total_dur_min:.0f} min ({total_dur_min/60:.1f} h) |",
        f"| **Active time** | **~{total_active_min:.0f} min (~{total_active_min/60:.1f} h)** *(gap>30min excluded)* |",
        f"| Avg per session | {avg_dur:.1f} min |",
        f"| Active time / calendar day | ~{active_min_per_day_cal:.0f} min (~{active_min_per_day_cal/60:.1f} h/day) |",
        f"| **Errors** | **{total_errors}** |",
        "",
        "---",
        "",
        "## Model Distribution",
        "",
    ]

    sorted_models = sorted(global_model.items(), key=lambda x: -x[1]["total"])
    if sorted_models:
        lines += [
            "| Model | Turns | Input | Output | Total | Cost |",
            "|-------|-------|-------|--------|-------|------|",
        ]
        for model, ms in sorted_models:
            lines.append(
                f"| {pretty_model(model)} | {ms['turns']} | "
                f"{fmt_token(ms['input'])} | {fmt_token(ms['output'])} | "
                f"{fmt_token(ms['total'])} | {fmt_cost(ms['cost'])} |"
            )
    else:
        lines.append("*no data*")

    lines += [
        "",
        "---",
        "",
        "## Error Analysis",
        "",
    ]

    # ── 错误知识库：原因 + 解决方案 ──────────────────────────
    ERROR_KB = {
        "pwsh_error_id": {
            "cause": "PowerShell 找不到该命令（命令不存在或不在 PATH）",
            "fix": "在 exec 调用里用 `where` 确认命令存在；Windows 特有命令用 PowerShell 而非 bash 语法",
        },
        "pwsh_error": {
            "cause": "Python subprocess 中混写了 bash 语法（如 `&&`、`except: pass`）被 PowerShell 执行",
            "fix": "Python subprocess 调用 PowerShell 时用分号 `;` 或换行而非 `&&`；去掉 bash 特有语法",
        },
        "exit_code": {
            "cause": "脚本或工具以非零退出码结束（exit code ≠ 0），可能是依赖缺失、路径错误或逻辑失败",
            "fix": "查看具体会话里的报错上下文；常见根因：Python 包缺失、权限不足、路径含空格/中文",
        },
        "python_missing_module": {
            "cause": "Python 脚本 import 了未安装的第三方库",
            "fix": "pip install <module_name>；常用包建议提前装：pandas openpyxl Pillow imagehash pyautogui yaml",
        },
        "python_encoding": {
            "cause": "Windows 控制台默认 GBK 编码，与 UTF-8/emoji 输出冲突：UnicodeEncodeError（写emoji到控制台）或 UnicodeDecodeError（读utf-8文件时解码）",
            "fix": "Python 脚本开头加 `sys.stdout.reconfigure(encoding='utf-8', errors='replace')`；open() 时加 `encoding='utf-8', errors='replace'`",
        },
        "python_exception": {
            "cause": "Python 代码运行时异常（TypeError/ValueError/AttributeError 等），多为类型不匹配或对象为 None",
            "fix": "检查出错行的变量类型；加 try/except；None 检查（`obj.get('key')` 而非 `obj['key']`）",
        },
        "http_error": {
            "cause": "HTTP 请求返回 4xx/5xx 错误，常见：URL 失效、缺少 API Key、网络超时",
            "fix": "检查 URL 是否有效；确认所需 API Key 已配置；尝试用浏览器直接访问验证",
        },
        "browser_blocked": {
            "cause": "浏览器被 SSRF 安全策略拦截，尝试访问内网/本地地址时被拒绝",
            "fix": "使用已登录态浏览器（profile='user'）；避免访问 127.0.0.1 或内网 IP",
        },
        "edit_not_found": {
            "cause": "edit 工具找不到要替换的精确文本，通常是前后有空格/换行/缩进差异",
            "fix": "用 read 工具确认文件当前内容，确保 oldText 与原文完全一致（包括空格和换行）",
        },
        "node_required": {
            "cause": "调用了需要 Node.js 运行时的功能（如 canvas），但当前环境未安装 node",
            "fix": "安装 Node.js；或使用不依赖 Node.js 的替代工具",
        },
        "stop_reason": {
            "cause": "会话被中止或超时，原因是 max_tokens 耗尽、超时、或用户主动取消",
            "fix": "减少请求长度或提高 max_tokens 限制；检查网络稳定性",
        },
        "error_code": {
            "cause": "工具返回了错误码，详见具体错误信息",
            "fix": "根据具体错误码查工具文档；常见：权限不足、文件被占用、资源不存在",
        },
    }

    if error_types:
        sorted_errors = sorted(error_types.items(), key=lambda x: -x[1]["count"])
        lines += [
            "| # | Error | Count | Root Cause | Fix |",
            "|---|-------|-------|------------|-----|",
        ]
        for i, (err_type, info) in enumerate(sorted_errors[:15], 1):
            kb = ERROR_KB.get(err_type, {})
            cause = kb.get("cause", "—")
            fix = kb.get("fix", "—")
            # 截断以适应列宽
            cause_s = cause[:60] + "…" if len(cause) > 60 else cause
            fix_s = fix[:60] + "…" if len(fix) > 60 else fix
            lines.append(f"| {i} | `{err_type}` | {info['count']} | {cause_s} | {fix_s} |")

        # 提示用户
        lines.append("")
        lines.append("> 💡 鼠标悬停错误类型可查看详情。完整错误知识库见下方 Troubleshooting 部分。")
    else:
        lines.append("*no errors recorded*")

    # ── 新增章节：工具调用排行 ──────────────────────────────
    if global_tool_stats:
        sorted_tools = global_tool_stats.most_common(15)
        max_tcnt = sorted_tools[0][1] if sorted_tools else 1
        lines += [
            "",
            "---",
            "",
            "## Tool Usage",
            "",
            f"| Tool | Calls | Bar |",
            "|-------|-------|-----|",
        ]
        for tool, cnt in sorted_tools:
            bar = "█" * max(1, round(cnt / max_tcnt * 20))
            lines.append(f"| `{tool}` | {cnt} | {bar} |")

    # ── 新增章节：exec 执行性能 ────────────────────────────
    if all_exec_durations:
        p50 = sorted(all_exec_durations)[len(all_exec_durations)//2]
        p95 = sorted(all_exec_durations)[int(len(all_exec_durations)*0.95)]
        lines += [
            "",
            "---",
            "",
            "## Exec Performance",
            "",
            f"| Metric | Value |",
            "|--------|-------|",
            f"| Total calls | {len(all_exec_durations)} |",
            f"| Avg | {exec_avg/1000:.1f}s |",
            f"| Median (P50) | {p50/1000:.1f}s |",
            f"| P95 | {p95/1000:.1f}s |",
            f"| Min | {exec_min/1000:.1f}s |",
            f"| Max | {exec_max/1000:.1f}s |",
        ]

    # ── 新增章节：会话结束原因 & 角色分布 ───────────────────
    if global_stop_reasons or global_roles:
        lines += [
            "",
            "---",
            "",
            "## Conversation Activity",
            "",
        ]
        if global_roles:
            total_roles = sum(global_roles.values())
            lines += [
                "**Message Roles**",
                "",
                f"| Role | Count | Pct |",
                "|-------|-------|-----|",
            ]
            for role, cnt in global_roles.most_common():
                pct = cnt / total_roles * 100
                lines.append(f"| `{role}` | {cnt} | {pct:.1f}% |")

        if global_stop_reasons:
            total_sr = sum(global_stop_reasons.values())
            lines += [
                "",
                "**Session End Reasons (stopReason)**",
                "",
                f"| Reason | Count | Pct |",
                "|--------|-------|-----|",
            ]
            sr_labels = {
                "toolUse": "工具调用完成",
                "stop": "正常结束",
                "error": "错误中止",
                "aborted": "被中止",
            }
            for sr, cnt in global_stop_reasons.most_common():
                pct = cnt / total_sr * 100
                label = sr_labels.get(sr, sr)
                lines.append(f"| `{sr}` ({label}) | {cnt} | {pct:.1f}% |")

    # ── 新增章节：文本长度统计 ─────────────────────────────
    if all_input_lens or all_output_lens:
        avg_in  = sum(all_input_lens)  / len(all_input_lens)  if all_input_lens  else 0
        avg_out = sum(all_output_lens) / len(all_output_lens) if all_output_lens else 0
        max_in  = max(all_input_lens)  if all_input_lens  else 0
        max_out = max(all_output_lens) if all_output_lens else 0
        lines += [
            "",
            "---",
            "",
            "## Text Volume",
            "",
            f"| Metric | User Input | AI Output |",
            "|--------|------------|----------|",
            f"| Avg chars / message | {avg_in:.0f} | {avg_out:.0f} |",
            f"| Max chars | {max_in} | {max_out} |",
            f"| Total messages | {len(all_input_lens)} | {len(all_output_lens)} |",
        ]

    lines += [
        "",
        "---",
        "",
        "## Session Detail",
        "",
        "| Date | Start | Duration | Tokens | Turns | Errors |",
        "|------|-------|----------|--------|-------|--------|",
    ]

    for s in sorted(all_sessions, key=lambda x: x["date"], reverse=True)[:30]:
        err_count = len(s.get("errors", []))
        err_str = f"{err_count}" if err_count else "-"
        lines.append(
            f"| {s['date']} | {s['start']} | {s['duration_min']:.1f} min | "
            f"{fmt_token(s['total'])} | {s['turns']} | {err_str} |"
        )

    lines += [
        "",
        "---",
        "",
        "## Daily Trend",
        "",
        "| Date | Sessions | Turns | Tokens | Errors |",
        "|------|----------|-------|--------|--------|",
    ]

    for d in active_days:
        s = date_stats[d]
        lines.append(
            f"| {d} | {s['sessions']} | {s['turns']} | "
            f"{fmt_token(s['total'])} | {s['errors']} |"
        )

    lines += [
        "",
        "---",
        "",
        "## Hourly Distribution",
        "",
        f"> Peak hours: {peak_str}",
        "",
        "| Hour | Sessions |",
        "|------|---------|",
    ]

    max_hcnt = max(hour_dist.values()) if hour_dist else 1
    for h in range(24):
        cnt = hour_dist.get(h, 0)
        bar = "#" * max(1, round(cnt / max_hcnt * 10))
        lines.append(f"| {h:02d}:00 | {cnt:2d} {bar} |")

    lines.append("")
    lines.append("*Report generated by usage-stats skill*")

    # ── Troubleshooting 完整知识库 ──────────────────────────
    lines += [
        "",
        "---",
        "",
        "## Troubleshooting Guide",
        "",
        "| Error | Cause | Fix |",
        "|-------|-------|-----|",
    ]
    for err_type, kb in ERROR_KB.items():
        lines.append(f"| `{err_type}` | {kb['cause']} | {kb['fix']} |")

    report_md = "\n".join(lines)

        # ── 保存历史快照 ─────────────────────────────────────
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    HISTORY_FILE = OUTPUT_DIR / "usage_stats_history.json"

    # 读入旧历史（如果存在）
    history = []
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as fh:
                history = json.load(fh)
        except Exception:
            history = []

    # 构建本次快照
    snapshot = {
        "generated_at":     datetime.now().isoformat(),
        "range_first":     first_date,
        "range_last":      last_date,
        "total_sessions":  total_sessions,
        "num_active_days": num_active_days,
        "total_tokens":    total_tokens,
        "total_input":     total_input,
        "total_output":    total_output,
        "cache_read":      total_cache_r,
        "cache_hit_rate":  cache_hit_rate,
        "total_turns":     total_turns,
        "total_messages":  total_msgs,
        "total_errors":    total_errors,
        "wall_clock_min": round(total_dur_min, 1),
        "active_min":      round(total_active_min, 1),
        "avg_dur_min":     round(avg_dur, 1),
        "cost":            round(total_cost, 6),
        "hourly":          dict(hour_dist),
        "daily": {d: {
            "sessions": date_stats[d]["sessions"],
            "turns":    date_stats[d]["turns"],
            "tokens":   date_stats[d]["total"],
            "errors":   date_stats[d]["errors"],
        } for d in date_stats},
        "models": {m: {
            "turns":  ms["turns"],
            "tokens": ms["total"],
        } for m, ms in global_model.items()},
        "top_tools":       dict(global_tool_stats.most_common(10)),
        "stop_reasons":    dict(global_stop_reasons),
        "roles":           dict(global_roles),
    }

    # 追加并最多保留 90 条
    history.append(snapshot)
    history = history[-90:]

    with open(HISTORY_FILE, "w", encoding="utf-8") as fh:
        json.dump(history, fh, ensure_ascii=False, indent=2)

    print(f"[OK] Snapshot saved ({len(history)} records in history)")
    print(f"[OK] History file: {HISTORY_FILE}")

    # ── 趋势对比：上次 vs 本次 ─────────────────────────────
    trend_lines = []
    if len(history) >= 2:
        prev = history[-2]
        curr = snapshot
        def delta(name, curr_v, prev_v, fmt="num", suffix=""):
            if prev_v == 0:
                dv = "—" if curr_v == 0 else f"+{curr_v}{suffix}"
            else:
                d = curr_v - prev_v
                sign = "+" if d > 0 else ""
                if fmt == "num":
                    dv = f"{sign}{d:,}{suffix}"
                elif fmt == "pct":
                    pct = (d / prev_v) * 100
                    dv = f"{sign}{pct:.1f}%"
            return f"| {name} | {curr_v:,}{suffix} | {dv} |"

        trend_lines += [
            "",
            "---",
            "",
            "## Trend (vs Last Run)",
            "",
            f"| Metric | Current | Δ vs Last |",
            "|--------|---------|-----------|",
            delta("Sessions", curr["total_sessions"], prev["total_sessions"]),
            delta("Total tokens (M)", round(curr["total_tokens"]/1e6,2), round(prev["total_tokens"]/1e6,2), "pct", "M"),
            delta("AI turns", curr["total_turns"], prev["total_turns"]),
            delta("Errors", curr["total_errors"], prev["total_errors"]),
            delta("Active min", curr["active_min"], prev["active_min"]),
            f"| Last run | {prev['generated_at'][:16]} | — |",
            f"| This run | {curr['generated_at'][:16]} | ← new |",
        ]

    # ── 写报告 ─────────────────────────────────────────────
    with open(OUTPUT_FILE, "w", encoding="utf-8") as fh:
        report_md += chr(10).join(trend_lines)
        fh.write(report_md)

    print(f"[OK] Report generated: {OUTPUT_FILE}")
    # 打印摘要
    for ln in report_md.split("\n")[:40]:
        print(ln)

if __name__ == "__main__":
    main()
