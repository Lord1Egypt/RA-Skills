#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
snapshot.py
-----------
在 skill 调用前后打 token 快照，计算 delta。

用法:
    # skill 调用前
    python3 snapshot.py before --label "html-extractor KStack文章"
    # → 输出 snapshot_id: snap_20260317_145301

    # skill 调用后
    python3 snapshot.py after --id snap_20260317_145301

    # 查看历史
    python3 snapshot.py history --limit 10
"""

import argparse
import json
import sys
import time
import tiktoken
from datetime import datetime
from pathlib import Path
from typing import Optional

# ─────────────────────────────────────────────
# 配置
# ─────────────────────────────────────────────

OPENCLAW_DIR = Path.home() / ".openclaw"
RESULTS_DIR  = OPENCLAW_DIR / "skills" / "skill-perf" / "results"
PENDING_FILE = OPENCLAW_DIR / "skills" / "skill-perf" / "pending_reports.json"
REPORTS_DIR  = OPENCLAW_DIR / "skills" / "skill-perf" / "reports"

# 所有 Agent 的 sessions 文件
AGENT_SESSION_FILES = [
    OPENCLAW_DIR / "agents" / "main"          / "sessions" / "sessions.json",
    OPENCLAW_DIR / "agents" / "xuexiguaishou" / "sessions" / "sessions.json",
    OPENCLAW_DIR / "agents" / "codeflicker"   / "sessions" / "sessions.json",
]

# ─────────────────────────────────────────────
# 底噪配置（从本机标定文件读取，未标定则用默认值）
# ─────────────────────────────────────────────

def _load_calibration() -> dict:
    """从本机 calibration.json 读取历史标定记录（仅用于展示，不作为兜底值）"""
    config_file = OPENCLAW_DIR / "skills" / "skill-perf" / "calibration.json"
    if config_file.exists():
        try:
            with open(config_file, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


MEASUREMENT_OVERHEAD_TOKENS = 0  # 废弃：不使用固定兜底值，底噪必须来自本次 calib 实测


def _append_calib_to_history(noise: int, calib_session_key: str = "") -> None:
    """把本次 calib 实测值追加到 calibration.json 的 subagent_history，保留最近 20 条。"""
    from datetime import datetime, timezone
    config_file = OPENCLAW_DIR / "skills" / "skill-perf" / "calibration.json"
    try:
        data = json.loads(config_file.read_text(encoding="utf-8")) if config_file.exists() else {}
    except Exception:
        data = {}
    history = data.get("subagent_history", [])
    entry = {
        "noise": noise,
        "calibrated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M"),
        "session_key": calib_session_key[:60] if calib_session_key else "",
    }
    history.append(entry)
    history = history[-20:]  # 只保留最近 20 条
    data["subagent_history"] = history
    try:
        config_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass

# ─────────────────────────────────────────────
# 读当前 session token 计数
# ─────────────────────────────────────────────

def read_current_tokens(session_key: str = None) -> dict:
    """
    从所有 agent sessions.json 中找目标 session，
    返回其当前 token 计数快照。
    
    session_key=None 时找 totalTokens 最大的（当前活跃主会话）
    """
    all_sessions = []
    for sf in AGENT_SESSION_FILES:
        if not sf.exists():
            continue
        try:
            with open(sf, encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue

        for key, val in data.items():
            if not isinstance(val, dict) or "totalTokens" not in val:
                continue
            all_sessions.append({
                "session_key":   key,
                "agent":         sf.parts[-3],
                "updated_at":    val.get("updatedAt", 0),
                "input_tokens":  val.get("inputTokens", 0),
                "output_tokens": val.get("outputTokens", 0),
                "total_tokens":  val.get("totalTokens", 0),
                "cache_read":    val.get("cacheRead", 0),
                "cache_write":   val.get("cacheWrite", 0),
                "model":         val.get("model", ""),
            })

    if not all_sessions:
        raise RuntimeError("未找到任何 session，请确认 OpenClaw 正在运行")

    if session_key:
        # 找指定的 session
        matches = [s for s in all_sessions if s["session_key"] == session_key]
        if not matches:
            raise RuntimeError(f"未找到 session: {session_key}")
        return matches[0]
    else:
        # 找最近更新的（最活跃的），优先选 main session
        main_sessions = [s for s in all_sessions if ":main:" in s["session_key"] and not s["session_key"].endswith(":main")]
        # 找 key 以 "agent:XXX:main" 结尾的主会话
        primary = [s for s in all_sessions if s["session_key"].endswith(":main") or s["session_key"].count(":") == 2]
        if primary:
            return max(primary, key=lambda x: x["updated_at"])
        return max(all_sessions, key=lambda x: x["updated_at"])


def estimate_file_tokens(path: str) -> int:
    """用 tiktoken 估算文件内容的 token 数"""
    try:
        enc = tiktoken.get_encoding("cl100k_base")
        text = Path(path).read_text(encoding="utf-8")
        return len(enc.encode(text))
    except Exception:
        return -1


def estimate_file_tokens_text(text: str) -> int:
    """用 tiktoken 估算字符串的 token 数"""
    try:
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except Exception:
        return 0


# ─────────────────────────────────────────────
# 诊断分析引擎
# ─────────────────────────────────────────────

def _read_full_session(session_key: str, fallback_session_id: str = None) -> Optional[dict]:
    """从 sessions.json 读取 session 的完整原始数据（含 skills list 等）

    若 sessions.json 中找不到（session 已被 OpenClaw 清除），尝试用 fallback_session_id
    从 .jsonl.deleted.* 文件恢复 usage 数据（totalTokens / input / output / cacheRead / cacheWrite）。
    """
    for sf in AGENT_SESSION_FILES:
        if not sf.exists():
            continue
        try:
            with open(sf, encoding="utf-8") as f:
                data = json.load(f)
            # 精确匹配
            matched_key = session_key if session_key in data else None
            # 精确匹配失败时，尝试前缀模糊匹配（防止 agent 输出时截断了末尾字符）
            if not matched_key and len(session_key) >= 20:
                for k in data:
                    if k.startswith(session_key) or session_key.startswith(k[:len(session_key)]):
                        if isinstance(data[k], dict):
                            matched_key = k
                            print(f"  ℹ️  session key 前缀匹配：{session_key!r} → {k!r}")
                            break
            if matched_key and isinstance(data[matched_key], dict):
                entry = data[matched_key]
                # 总是尝试用 .jsonl 的值验证 sessions.json 的 totalTokens
                # OpenClaw 已知 bug：sessions.json 有时只记录最后一次 usage 而非累计值
                sid = entry.get("sessionId", "")
                if sid:
                    jsonl_data = _read_total_tokens_from_jsonl_with_details(sid, sf.parent)
                    if jsonl_data:
                        jsonl_total = jsonl_data.get("totalTokens", 0)
                        sess_total = entry.get("totalTokens", 0)
                        if jsonl_total > sess_total:
                            if sess_total > 0:
                                print(f"  ⚠️  sessions.json totalTokens={sess_total:,} < .jsonl totalTokens={jsonl_total:,}"
                                      f"，以 .jsonl 值为准")
                            entry = {**entry, **jsonl_data}
                return entry
        except Exception:
            continue

    # sessions.json 未找到，尝试从 .jsonl.deleted.* 恢复
    # fallback_session_id 未传时，尝试从 session_key 里提取 UUID（格式：agent:x:subagent:{uuid}）
    if not fallback_session_id:
        _parts = session_key.split(":")
        if len(_parts) >= 4:
            fallback_session_id = _parts[3]
        else:
            return None

    for sf in AGENT_SESSION_FILES:
        sess_dir = sf.parent
        deleted_files = sorted(sess_dir.glob(f"{fallback_session_id}*.deleted*"))
        if not deleted_files:
            continue
        # 取最新的 deleted 文件
        df = deleted_files[-1]
        best_total = 0
        best_cache_r = 0
        max_total_usage = None
        max_cache_usage = None
        try:
            for line in df.read_text(encoding="utf-8", errors="replace").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    usage = obj.get("message", {}).get("usage", {})
                    t = usage.get("totalTokens", 0)
                    cr = usage.get("cacheRead", 0)
                    if t and t > best_total:
                        best_total = t
                        max_total_usage = usage
                    if cr and cr > best_cache_r:
                        best_cache_r = cr
                        max_cache_usage = usage
                except Exception:
                    pass
        except Exception:
            pass
        if max_total_usage and best_total > 0:
            # totalTokens 取最大值（最终累计），cacheRead 取各 turn 最大值
            print(f"  ℹ️  sessions.json 中未找到 session，从 .deleted 文件恢复数据 (total={best_total:,}, cacheR={best_cache_r:,})")
            return {
                "totalTokens": best_total,
                "inputTokens":  max_total_usage.get("input", max_total_usage.get("inputTokens", 0)),
                "outputTokens": max_total_usage.get("output", max_total_usage.get("outputTokens", 0)),
                "cacheRead":    best_cache_r,
                "cacheWrite":   max_total_usage.get("cacheWrite", 0),
                "updatedAt":    int(df.stat().st_mtime * 1000),
                "_from_deleted": True,
            }

    return None


def generate_diagnostics(tokens: dict, session_key: str = None,
                         duration_sec: float = 0,
                         is_delta: bool = False,
                         noise_override: int = None,
                         fallback_session_id: str = None) -> dict:
    """
    生成诊断分析报告。

    tokens: dict 包含 input_tokens, output_tokens, total_tokens, cache_read, cache_write
    session_key: 可选，用于读取完整 session 数据（skills list 等）
    duration_sec: 执行耗时（秒）
    is_delta: True 表示 tokens 是增量（before/after差值），False 表示是绝对值
    """
    input_t  = tokens.get("input_tokens", tokens.get("input", 0))
    output_t = tokens.get("output_tokens", tokens.get("output", 0))
    total_t  = tokens.get("total_tokens", tokens.get("total", 0))
    cache_r  = tokens.get("cache_read", 0)
    cache_w  = tokens.get("cache_write", 0)

    diag = {
        "cache_analysis": {},
        "efficiency": {},
        "anomalies": [],
        "recommendations": [],
    }

    # ── 1. Cache 分析 ───────────────────────────
    ca = diag["cache_analysis"]
    if input_t > 0:
        ca["cache_hit_rate"] = round(cache_r / max(1, cache_r + input_t) * 100, 1)
    else:
        ca["cache_hit_rate"] = 0.0

    if cache_r > 0 and cache_w == 0:
        ca["cache_status"] = "warm"     # 全部命中，无新写入
        ca["cache_note"] = "缓存完全命中，system prompt 已被缓存"
    elif cache_w > 0 and cache_r == 0:
        ca["cache_status"] = "cold"     # 首次运行，全部写入
        ca["cache_note"] = "首次运行/缓存过期，system prompt 全部写入缓存"
    elif cache_r > 0 and cache_w > 0:
        ca["cache_status"] = "partial"  # 部分命中
        ca["cache_note"] = "部分缓存命中，可能 system prompt 有变化"
    else:
        ca["cache_status"] = "none"     # 无缓存活动
        ca["cache_note"] = "无缓存活动（可能 cacheRetention=none 或模型不支持）"

    # 估算 cache 节省的 tokens
    # cacheRead 按约 10% 价格计费，相比全价可节省 ~90%
    if cache_r > 0:
        ca["estimated_savings"] = round(cache_r * 0.9)  # 节省了 90% 的 cacheRead tokens
        ca["savings_pct"] = round(ca["estimated_savings"] / max(1, total_t + ca["estimated_savings"]) * 100, 1)
    else:
        ca["estimated_savings"] = 0
        ca["savings_pct"] = 0.0

    # ── 2. 效率指标 ─────────────────────────────
    eff = diag["efficiency"]

    # I/O 比：output / total，越高说明越多 token 用于生成
    eff["output_ratio"] = round(output_t / max(1, total_t) * 100, 1)

    # 净消耗比：net / total，越低说明底噪占比越大（skill 本身贡献小）
    effective_noise = noise_override if noise_override is not None else 0
    net = max(0, total_t - effective_noise)
    eff["net_ratio"] = round(net / max(1, total_t) * 100, 1)

    # 速度
    if duration_sec > 0:
        eff["tokens_per_sec"] = round(total_t / duration_sec, 1)
        eff["output_tokens_per_sec"] = round(output_t / duration_sec, 1)

    # 有效 input（total - output = 扣除 output 后计费 input）
    eff["effective_input"] = max(0, total_t - output_t)

    # ── 3. 异常检测 ─────────────────────────────
    anomalies = diag["anomalies"]

    # 3a. cache_write 异常高（应该只在首次有大量写入）
    if cache_w > 50000:
        anomalies.append({
            "level": "warn",
            "code": "HIGH_CACHE_WRITE",
            "message": f"cache_write={cache_w:,}，异常偏高。可能原因：system prompt 频繁变化、cacheRetention 配置不当",
        })

    # 3b. output 异常高（超过 total 的 50%）
    if output_t > total_t * 0.5 and total_t > 1000:
        anomalies.append({
            "level": "warn",
            "code": "HIGH_OUTPUT_RATIO",
            "message": f"output 占比 {eff['output_ratio']}%，超过 50%。LLM 产出大量内容，检查是否必要",
        })

    # 3c. 无 cache 命中（连续运行应有 cache）
    if cache_r == 0 and cache_w == 0 and total_t > 5000:
        anomalies.append({
            "level": "info",
            "code": "NO_CACHE_ACTIVITY",
            "message": "无 prompt cache 活动。可能 cacheRetention=none 或模型/提供商不支持 cache",
        })

    # 3d. total 远大于预期底噪（可能 skill 消耗过高）
    if False:  # MEASUREMENT_OVERHEAD_TOKENS 已废弃，此条件不再触发
        anomalies.append({
            "level": "info",
            "code": "HIGH_CONSUMPTION",
            "message": f"totalTokens={total_t:,}，超过底噪的 3 倍。skill 消耗较大",
        })

    # 3e-pre. output 极低（subagent 可能未完整执行任务）
    if output_t < 200 and total_t > 5000:
        anomalies.append({
            "level": "warn",
            "code": "LOW_OUTPUT_TOKENS",
            "message": f"outputTokens={output_t:,}（极低）。LLM 几乎没有生成内容，test subagent 可能提前终止或未完整执行任务。建议检查 subagent 日志",
        })

    # 3e. 速率异常低（可能 API 限速）
    if duration_sec > 0 and output_t > 0:
        out_per_sec = output_t / duration_sec
        if out_per_sec < 5 and duration_sec > 30:
            anomalies.append({
                "level": "warn",
                "code": "SLOW_OUTPUT",
                "message": f"输出速率 {out_per_sec:.1f} tokens/s，低于 5 tokens/s。可能遭遇 API 限速或模型响应慢",
            })

    # ── 4. 优化建议 ─────────────────────────────
    recs = diag["recommendations"]

    if ca["cache_status"] == "cold" and total_t > 10000:
        recs.append("考虑设置 cacheRetention='long' + heartbeat 保持缓存温暖，减少首次 cache_write 成本")

    if ca["cache_status"] == "none" and total_t > 10000:
        recs.append("当前无 cache 活动。检查模型/提供商是否支持 Prompt Cache，或在 openclaw.json 中启用 cacheRetention")

    if net > 20000:
        recs.append("净消耗 >20,000 tokens。考虑精简 skill 的 SKILL.md 或减少工具调用的数据量")

    if eff["output_ratio"] > 40:
        recs.append("LLM 输出占比高。如不需要详细输出，在 payload.message 中加 '简洁回复' 指令")

    # ── 5. Session 元数据（从完整 session 数据读取）─
    if session_key:
        raw = _read_full_session(session_key)
        if raw:
            meta = {}
            if "model" in raw:
                meta["model"] = raw["model"]
            if "modelProvider" in raw:
                meta["model_provider"] = raw["modelProvider"]
            if "contextTokens" in raw:
                meta["context_window"] = raw["contextTokens"]
                # 上下文使用率
                ctx = raw["contextTokens"]
                if ctx > 0:
                    usage_pct = round(input_t / ctx * 100, 1)
                    meta["context_usage_pct"] = usage_pct
                    if usage_pct > 80:
                        anomalies.append({
                            "level": "warn",
                            "code": "CONTEXT_NEAR_LIMIT",
                            "message": f"上下文使用率 {usage_pct}%，接近窗口上限 {ctx:,}。可能触发 context truncation",
                        })
            if "label" in raw:
                meta["label"] = raw["label"]
            if "sessionId" in raw:
                meta["session_id"] = raw["sessionId"]

            # 统计注册的 skills 数量
            skills_data = raw.get("skills", {})
            if isinstance(skills_data, dict) and "data" in skills_data:
                skill_list = skills_data["data"]
                if isinstance(skill_list, list):
                    meta["registered_skills_count"] = len(skill_list)
                    meta["registered_skills"] = [s.get("name", "?") for s in skill_list]

            diag["session_metadata"] = meta

    return diag


def generate_confidence_analysis(net: int, calib_noise: int, test_total: int,
                                  is_subagent_mode: bool = False,
                                  calib_note: str = "") -> dict:
    """
    生成数据置信度分析。
    
    Args:
        net: 净消耗 tokens（test_total - calib_noise）
        calib_noise: 本轮底噪（calibration subagent 或 calibration.json）
        test_total: 被测 session 的 totalTokens
        is_subagent_mode: 是否使用了双 subagent 标定模式
        calib_note: 底噪来源说明
    
    Returns:
        {
            "level": "high" | "medium" | "low",
            "score": 0-100,
            "factors": [...],
            "warnings": [...],
            "interpretation": "..."
        }
    """
    score = 100
    factors = []
    warnings = []

    # ── 因素1：底噪来源（最重要）────────────────────────────────
    if is_subagent_mode:
        factors.append({
            "name": "底噪来源",
            "icon": "✅",
            "value": "双 subagent 动态标定",
            "detail": "本轮 calib subagent 与 test subagent 同 parent、同 bootstrap context，底噪误差极小",
            "impact": "score+0（最优）",
        })
    else:
        score -= 20
        factors.append({
            "name": "底噪来源",
            "icon": "⚠️",
            "value": f"固定标定值 {calib_noise:,} tokens",
            "detail": calib_note or "来自 calibration.json，非本轮动态测量。模型/工具变更时底噪可能漂移",
            "impact": "score-20",
        })
        warnings.append("底噪使用固定值，推荐改用双 subagent 动态标定（见 spec 2.2）")

    # ── 因素2：净消耗绝对值 ──────────────────────────────────────
    net_ratio = net / max(1, test_total)
    if net_ratio < 0.01:
        score -= 30
        factors.append({
            "name": "净消耗比例",
            "icon": "⚠️",
            "value": f"{net:,} tokens（占 total 的 {net_ratio*100:.1f}%）",
            "detail": "净消耗极低（<1%），接近底噪误差范围。结果可能不稳定，需多轮验证",
            "impact": "score-30",
        })
        warnings.append(f"net={net:,} 仅占 total 的 {net_ratio*100:.1f}%，建议连续测量 ≥3 次取平均")
    elif net_ratio < 0.05:
        score -= 10
        factors.append({
            "name": "净消耗比例",
            "icon": "🟡",
            "value": f"{net:,} tokens（占 total 的 {net_ratio*100:.1f}%）",
            "detail": "净消耗偏低（1-5%），建议多轮验证排除底噪抖动",
            "impact": "score-10",
        })
        warnings.append(f"net={net:,} 较小，建议至少测量 3 轮取中位数")
    else:
        factors.append({
            "name": "净消耗比例",
            "icon": "✅",
            "value": f"{net:,} tokens（占 total 的 {net_ratio*100:.1f}%）",
            "detail": "净消耗占比适中，高于底噪误差范围",
            "impact": "score+0",
        })

    # ── 因素3：底噪与被测 total 的差值稳定性 ────────────────────
    noise_gap = test_total - calib_noise
    if noise_gap < 0:
        score -= 50
        factors.append({
            "name": "底噪稳定性",
            "icon": "❌",
            "value": f"底噪 {calib_noise:,} > test_total {test_total:,}，差值为负",
            "detail": "底噪高于被测 session，net 被强制截断为 0。结果无效",
            "impact": "score-50",
        })
        warnings.append("⚠️ 底噪>test_total，net=0（无效）。请检查底噪来源是否与被测 session 环境一致")
    else:
        factors.append({
            "name": "底噪稳定性",
            "icon": "✅",
            "value": f"差值 {noise_gap:,} tokens（正数，结果有效）",
            "detail": "test_total > calib_noise，net 计算有效",
            "impact": "score+0",
        })

    # ── 因素4：运行轮次（单次 vs 多轮）─────────────────────────
    # 这里无法直接感知轮次，作为提示性 factor
    factors.append({
        "name": "运行轮次",
        "icon": "ℹ️",
        "value": "当前为单次测量",
        "detail": "单次测量受随机因素影响。建议多轮（≥3次）取中位数以消除波动",
        "impact": "提示",
    })

    # ── 综合评级 ─────────────────────────────────────────────────
    score = max(0, min(100, score))
    if score >= 80:
        level = "high"
        level_text = "高"
        level_icon = "🟢"
        interpretation = f"结果可信。net={net:,} tokens 可作为 {calib_note or 'skill'} 的参考消耗值。"
    elif score >= 50:
        level = "medium"
        level_text = "中"
        level_icon = "🟡"
        interpretation = f"结果基本可信，但建议多轮验证。net={net:,} tokens 可作为初步参考。"
    else:
        level = "low"
        level_text = "低"
        level_icon = "🔴"
        interpretation = f"结果置信度低（score={score}），请排查警告项后重新测量。"

    return {
        "level": level,
        "score": score,
        "level_text": level_text,
        "level_icon": level_icon,
        "interpretation": interpretation,
        "factors": factors,
        "warnings": warnings,
        "net": net,
        "calib_noise": calib_noise,
        "test_total": test_total,
        "net_ratio_pct": round(net_ratio * 100, 1),
    }


def format_confidence(conf: dict) -> str:
    """将置信度分析格式化为人类可读文本"""
    lines = []
    lines.append("")
    lines.append(f"  【数据置信度分析】")
    lines.append("")
    lines.append(f"    综合评级:  {conf['level_icon']} {conf['level_text']}（score={conf['score']}/100）")
    lines.append(f"    解读:      {conf['interpretation']}")
    lines.append("")
    lines.append(f"    影响因素:")
    for f in conf.get("factors", []):
        lines.append(f"      {f['icon']} {f['name']}: {f['value']}")
        lines.append(f"         └─ {f['detail']}")
    if conf.get("warnings"):
        lines.append("")
        lines.append(f"    ⚠️  注意事项:")
        for w in conf["warnings"]:
            lines.append(f"      · {w}")
    return "\n".join(lines)


def format_diagnostics(diag: dict) -> str:
    """将诊断分析格式化为人类可读文本"""
    lines = []
    sep = "─" * 52

    ca = diag.get("cache_analysis", {})
    eff = diag.get("efficiency", {})
    anomalies = diag.get("anomalies", [])
    recs = diag.get("recommendations", [])
    meta = diag.get("session_metadata", {})

    lines.append("")
    lines.append(f"  【诊断分析】")
    lines.append("")

    # Cache 分析
    status_icons = {"warm": "🟢", "cold": "🔵", "partial": "🟡", "none": "⚪"}
    icon = status_icons.get(ca.get("cache_status", ""), "⚪")
    lines.append(f"  Cache:")
    lines.append(f"    状态:         {icon} {ca.get('cache_status', '?')}（{ca.get('cache_note', '')}）")
    lines.append(f"    命中率:       {ca.get('cache_hit_rate', 0):.1f}%")
    if ca.get("estimated_savings", 0) > 0:
        lines.append(f"    节省估算:     ~{ca['estimated_savings']:,} tokens（{ca.get('savings_pct', 0):.1f}% 节省）")

    # 效率
    lines.append(f"  效率:")
    lines.append(f"    output 占比:  {eff.get('output_ratio', 0):.1f}%（LLM 生成 / 总计费）")
    lines.append(f"    净消耗占比:   {eff.get('net_ratio', 0):.1f}%（扣底噪后 / 总计费）")
    if "tokens_per_sec" in eff:
        lines.append(f"    总速率:       {eff['tokens_per_sec']:.0f} tokens/s")
        lines.append(f"    输出速率:     {eff['output_tokens_per_sec']:.1f} tokens/s")

    # Session 元数据
    if meta:
        lines.append(f"  Session:")
        if "model" in meta:
            lines.append(f"    模型:         {meta['model'][:50]}")
        if "model_provider" in meta:
            lines.append(f"    提供商:       {meta['model_provider']}")
        if "context_window" in meta:
            lines.append(f"    上下文窗口:   {meta['context_window']:,} tokens")
        if "context_usage_pct" in meta:
            lines.append(f"    上下文使用率: {meta['context_usage_pct']:.1f}%")
        if "registered_skills_count" in meta:
            lines.append(f"    注册技能数:   {meta['registered_skills_count']}")

    # 异常
    if anomalies:
        lines.append(f"  异常:")
        for a in anomalies:
            icon = "⚠️" if a["level"] == "warn" else "ℹ️"
            lines.append(f"    {icon} [{a['code']}] {a['message']}")

    # 建议
    if recs:
        lines.append(f"  建议:")
        for i, r in enumerate(recs, 1):
            lines.append(f"    {i}. {r}")

    return "\n".join(lines)


# ─────────────────────────────────────────────
# before / after
# ─────────────────────────────────────────────

def cmd_fetch_tokens(label: str = "", latest_n: int = 2):
    """从 sessions.json 直接读取最近完成的 subagent 的精确 totalTokens。

    按 updatedAt 降序，输出最新 N 个 subagent session 的精确数据。
    用于替代 announce 手动抄写，确保精确值。

    输出格式（每行一个，机器可读）：
      totalTokens=14234 sessionKey=agent:main:subagent:xxx label=calib-html-extractor
    """
    all_entries = []
    for sf in AGENT_SESSION_FILES:
        if not sf.exists():
            continue
        try:
            with open(sf, encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue
        for key, val in data.items():
            if not isinstance(val, dict) or "totalTokens" not in val:
                continue
            if ":subagent:" not in key or ":run:" in key:
                continue
            total = val.get("totalTokens", 0)
            if total <= 0:
                continue
            entry_label = val.get("label", "")
            all_entries.append({
                "key":          key,
                "total_tokens": total,
                "updated_at_ms":val.get("updatedAt", 0),
                "label":        entry_label,
            })

    all_entries.sort(key=lambda x: x["updated_at_ms"], reverse=True)

    # 过滤 label 关键词
    if label:
        filtered = [e for e in all_entries if label.lower() in e["label"].lower()]
        if filtered:
            all_entries = filtered

    shown = all_entries[:latest_n]
    if not shown:
        print("ERROR: 未找到任何已完成的 subagent session，请确认 subagent 已运行完毕")
        return

    for e in shown:
        ts = datetime.fromtimestamp(e["updated_at_ms"] / 1000).strftime("%H:%M:%S") if e["updated_at_ms"] else "?"
        print(f"totalTokens={e['total_tokens']} sessionKey={e['key']} label={e['label']!r} updatedAt={ts}")


def cmd_sessions(latest_subagent: bool = False, subagent_of: str = ""):
    """列出所有 session 及 token 计数。
    
    latest_subagent=True: 只输出最新完成的 subagent session key
    subagent_of=<parent_key>: 通过 spawnedBy 字段精确找到 parent spawn 的 subagent
    """
    all_entries = []  # 原始条目，含 spawnedBy
    for sf in AGENT_SESSION_FILES:
        if not sf.exists():
            continue
        try:
            with open(sf, encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue
        for key, val in data.items():
            if not isinstance(val, dict) or "totalTokens" not in val:
                continue
            all_entries.append({
                "key":          key,
                "total_tokens": val.get("totalTokens", 0),
                "input_tokens": val.get("inputTokens", 0),
                "output_tokens":val.get("outputTokens", 0),
                "updated_at_ms":val.get("updatedAt", 0),
                "updated_at":   datetime.fromtimestamp(val.get("updatedAt", 0)/1000).strftime("%H:%M:%S"),
                "model":        val.get("model", "")[:30],
                "spawned_by":   val.get("spawnedBy", ""),
            })

    if subagent_of:
        # 通过 spawnedBy 精确匹配 parent spawn 的 subagent（零额外 token 开销）
        matches = [s for s in all_entries
                   if ":subagent:" in s["key"] and ":run:" not in s["key"]
                   and s["spawned_by"] == subagent_of
                   and s["total_tokens"] > 0]
        matches.sort(key=lambda x: x["updated_at_ms"], reverse=True)
        if matches:
            print(matches[0]["key"])
        else:
            print("")
        return

    if latest_subagent:
        # 只看 subagent sessions（非 :run: 子条目），按更新时间降序
        subagents = [s for s in all_entries
                     if ":subagent:" in s["key"] and ":run:" not in s["key"]
                     and s["total_tokens"] > 0]
        subagents.sort(key=lambda x: x["updated_at_ms"], reverse=True)
        if subagents:
            print(subagents[0]["key"])
        else:
            print("")
        return

    all_entries.sort(key=lambda x: x["total_tokens"], reverse=True)
    print(f"\n{'Session Key':<55} {'Total':>8} {'Input':>10} {'Output':>8} {'Updated':>10}")
    print("-" * 100)
    for s in all_entries:
        print(f"{s['key']:<55} {s['total_tokens']:>8,} {s['input_tokens']:>10,} {s['output_tokens']:>8,} {s['updated_at']:>10}")
    print(f"\n提示: 用 --session <key> 指定目标 session\n")


def cmd_history(limit: int = 10):
    """打印最近 N 条测量结果"""
    if not RESULTS_DIR.exists():
        print(json.dumps({"error": "暂无历史记录"}, ensure_ascii=False))
        return

    files = sorted(RESULTS_DIR.glob("snap_*.json"), reverse=True)[:limit]
    rows = []
    for f in files:
        try:
            with open(f, encoding="utf-8") as fp:
                d = json.load(fp)
            if d.get("phase") != "complete":
                continue
            r = d.get("after", {})
            rows.append({
                "id":       d["id"],
                "label":    d["label"],
                "duration": f"{r.get('duration_sec', '?')}s",
                "total_delta": r.get("summary", {}).get("total_delta", "?"),
                "net_tokens":  r.get("summary", {}).get("net_skill_tokens", "?"),
            })
        except Exception:
            continue

    if not rows:
        print("暂无完成的测量记录（before/after 均已完成的）")
        return

    print(f"\n{'Label':<35} {'Duration':>10} {'Total Δ':>10} {'Net tokens':>12}")
    print("-" * 70)
    for r in rows:
        print(f"{r['label']:<35} {r['duration']:>10} {str(r['total_delta']):>10} {str(r['net_tokens']):>12}")
    print()


_BOOTSTRAP_FILES = [
    "AGENTS.md", "SOUL.md", "TOOLS.md", "IDENTITY.md",
    "USER.md", "HEARTBEAT.md", "MEMORY.md", "BOOTSTRAP.md",
]

def _get_agent_workspace(agent_id: str) -> Optional[Path]:
    """从 openclaw.json 读取指定 agent 的 workspace 路径"""
    cfg_path = OPENCLAW_DIR / "openclaw.json"
    if not cfg_path.exists():
        return None
    try:
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        agents = cfg.get("agents", {}).get("list", [])
        for a in agents:
            if a.get("id") == agent_id:
                ws = a.get("workspace", "")
                if ws:
                    p = Path(ws).expanduser()
                    return p if p.is_absolute() else OPENCLAW_DIR / p
        # 默认 workspace
        default_ws = cfg.get("agents", {}).get("defaults", {}).get("workspace", "")
        if default_ws:
            p = Path(default_ws).expanduser()
            return p if p.is_absolute() else OPENCLAW_DIR / p
    except Exception:
        pass
    return OPENCLAW_DIR / "workspace"


def _scan_bootstrap_files(agent_id: str) -> list:
    """
    扫描 agent workspace 中的 bootstrap 文件，返回：
    [{"name": "AGENTS.md", "path": "...", "chars": 1234, "tokens": 456, "exists": True}, ...]
    """
    ws = _get_agent_workspace(agent_id)
    result = []
    for fname in _BOOTSTRAP_FILES:
        fpath = ws / fname if ws else None
        if fpath and fpath.exists():
            try:
                text = fpath.read_text(encoding="utf-8", errors="replace")
                chars = len(text)
                tokens = estimate_file_tokens_text(text)
                result.append({
                    "name": fname, "path": str(fpath),
                    "chars": chars, "tokens": tokens, "exists": True,
                })
            except Exception:
                result.append({"name": fname, "path": str(fpath), "chars": 0, "tokens": 0, "exists": True})
        else:
            result.append({"name": fname, "path": str(fpath) if fpath else "", "chars": 0, "tokens": 0, "exists": False})
    return result


def _read_system_prompt_breakdown(agent_id: str) -> dict:
    """
    从同 agent 的 main session 读取 systemPromptReport，提取各部分 chars/tokens 数据。
    用于 cacheRead 饼图分解的参考数据。
    返回:
    {
        "bootstrap_tokens": 2363,
        "skills_list_tokens": 3898,
        "tools_tokens": 1265,
        "framework_tokens": <推算>,
        "total_reported_chars": 32301,
        "tools_count": 44,
        "skills_count": 27,
    }
    """
    # 找 agent 的 main session
    for sf in AGENT_SESSION_FILES:
        if not sf.exists():
            continue
        # 检查路径是否对应 agent_id
        if agent_id not in str(sf):
            continue
        try:
            data = json.loads(sf.read_text(encoding="utf-8"))
        except Exception:
            continue
        # main session key: agent:<agentId>:main
        main_key = f"agent:{agent_id}:main"
        s = data.get(main_key, {})
        spr = s.get("systemPromptReport", {})
        if not spr:
            continue
        sp = spr.get("systemPrompt", {})
        files = spr.get("injectedWorkspaceFiles", [])
        tools = spr.get("tools", {})
        sk = s.get("skillsSnapshot", {})

        # bootstrap tokens (用 tiktoken 实测)
        bs_tokens = 0
        for f in files:
            fpath = Path(f.get("path", ""))
            if fpath.exists():
                try:
                    bs_tokens += estimate_file_tokens(str(fpath))
                except Exception:
                    pass

        # skills prompt tokens
        skills_prompt = sk.get("prompt", "") if isinstance(sk, dict) else ""
        skills_tokens = estimate_file_tokens_text(skills_prompt) if skills_prompt else 0

        # tools (tiktoken on full JSON)
        tools_entries = tools.get("entries", []) if isinstance(tools, dict) else []
        tools_tokens_val = estimate_file_tokens_text(json.dumps(tools_entries)) if tools_entries else 0

        total_chars = sp.get("chars", 0)
        return {
            "bootstrap_tokens": bs_tokens,
            "skills_list_tokens": skills_tokens,
            "tools_tokens": tools_tokens_val,
            "tools_count": len(tools_entries) if isinstance(tools_entries, list) else 0,
            "skills_count": len(sk.get("skills", [])) if isinstance(sk, dict) else 0,
            "total_reported_chars": total_chars,
            "project_context_chars": sp.get("projectContextChars", 0),
            "non_project_context_chars": sp.get("nonProjectContextChars", 0),
        }
    return {}


def _analyze_step_breakdown(session_key: str) -> list:
    """
    从 subagent session 的 .jsonl transcript 文件直接读取各步骤 token 估算。

    策略：
    1. 从 sessions.json 的 sessionFile 字段找到实际 .jsonl 路径（session_key uuid 和文件名 uuid 不一致）
    2. 找不到或文件已被 OpenClaw 清理时返回空列表

    注意：OpenClaw 会在 session 结束约 5 分钟后自动删除 .jsonl 文件，report 命令建议在此之前运行。
    估算方法：消息内容字符数 ÷ 2.67（按 50% 中文 + 50% 英文混合比例，中文 ~2 chars/token，英文 ~4 chars/token，加权平均 ~2.67 chars/token，误差约 ±20%）。
    """
    parts = session_key.split(":")
    if len(parts) < 4:
        return []
    agent_id = parts[1] if len(parts) >= 2 else "main"

    # 通过 sessions.json 的 sessionFile 字段找到实际 .jsonl 路径
    # （subagent 的 session_key uuid 和文件名 uuid 是两个不同的 uuid）
    sessions_json = OPENCLAW_DIR / "agents" / agent_id / "sessions" / "sessions.json"
    jsonl_file = None
    if sessions_json.exists():
        try:
            data = json.loads(sessions_json.read_text(encoding="utf-8"))
            entry = data.get(session_key, {})
            session_file_path = entry.get("sessionFile", "")
            if session_file_path:
                jsonl_file = Path(session_file_path)
        except Exception:
            pass

    if not jsonl_file or not jsonl_file.exists():
        return []  # 文件未找到或已被 OpenClaw 自动清理

    try:
        lines = jsonl_file.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return []

    # 逐行解析，提取所有 message 记录（type=="message"）
    # 同时建立 toolCallId → arguments 映射（用于 read 工具等无 details 的工具取参数）
    import re as _re
    raw_messages = []
    toolcall_args: dict = {}  # toolCallId → {"name": ..., "arguments": ...}

    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        if obj.get("type") != "message":
            continue
        msg = obj.get("message", {})
        role = msg.get("role", "")

        # 从 assistant 消息里提取 toolCall 的输入参数，建立 id → arguments 映射
        if role == "assistant":
            for ci in (msg.get("content", []) or []):
                if isinstance(ci, dict) and ci.get("type") == "toolCall":
                    tc_id = ci.get("id", "")
                    if tc_id:
                        toolcall_args[tc_id] = {
                            "name": ci.get("name", ""),
                            "arguments": ci.get("arguments", {}),
                        }

        raw_messages.append({
            "role": role,
            "toolName": msg.get("toolName", ""),
            "toolCallId": msg.get("toolCallId", ""),
            "content": msg.get("content", []),
            "details": msg.get("details", {}),
        })

    if not raw_messages:
        return []

    def _extract_hint(tool_name: str, args: dict, details: dict) -> str:
        """从工具参数或 details 里提取可读的操作摘要。"""
        # 优先用 details 里已有的摘要字段
        if details:
            # exec/process 的 details.name 是命令摘要（OpenClaw 已格式化好）
            if tool_name in ("exec", "execute_command") and details.get("name"):
                return details["name"][:60]
            # process 的 details.name（轮询中存在，完成后消失——fallback 到 arguments）
            if tool_name == "process" and details.get("name"):
                return details["name"][:60]
            # sessions_spawn 的 details.childSessionKey
            if tool_name == "sessions_spawn" and details.get("childSessionKey"):
                key = details["childSessionKey"]
                parts = key.split(":")
                return parts[-1][:16] if parts else key[:20]

        # 从工具参数里提取
        if not args:
            return ""

        # read/view 工具：显示文件名
        if tool_name in ("read", "read_file", "view_code_item", "view_file_outline"):
            p = args.get("file_path", args.get("path", ""))
            return p.split("/")[-1] if p else ""

        # exec：显示命令前缀
        if tool_name in ("exec", "execute_command"):
            cmd = args.get("command", "")
            return cmd[:50].strip()

        # process：显示 sessionId（完成态 details 里没有 name）
        if tool_name == "process":
            sid = args.get("sessionId", "")
            action = args.get("action", "")
            if sid:
                return f"{action}:{sid}".strip() if action else sid
            return ""  # action=list 不显示（无意义）

        # sessions_spawn：fallback 显示 label（details 里没有 childSessionKey 时）
        if tool_name == "sessions_spawn":
            label = args.get("label", "")
            return label[:40] if label else ""

        # grep/search：显示查询词
        if tool_name in ("grep_search", "codebase_search", "search_file"):
            return args.get("query", args.get("regex", ""))[:40]

        # 写文件：显示文件名（write 工具有 path 或 file_path 两种字段名）
        if tool_name in ("write", "replace_in_file", "multi_replace_in_file", "write_to_file"):
            p = args.get("path", args.get("file_path", ""))
            return p.split("/")[-1] if p else ""

        # fetch_web：显示域名
        if tool_name in ("fetch_web", "browser_agent"):
            url = args.get("url", args.get("task", ""))
            m = _re.search(r"https?://([^/]+)", url)
            return m.group(1) if m else url[:40]

        return ""

    # 逐条计算字符数和估算 tokens
    steps = []
    for i, m in enumerate(raw_messages):
        role = m.get("role", "?")
        tool_name = m.get("toolName", "")
        tool_call_id = m.get("toolCallId", "")
        content_items = m.get("content", [])
        details = m.get("details", {}) or {}

        char_len = 0
        if isinstance(content_items, list):
            for ci in content_items:
                if isinstance(ci, dict):
                    char_len += len(ci.get("text", ""))
                elif isinstance(ci, str):
                    char_len += len(ci)
        elif isinstance(content_items, str):
            char_len = len(content_items)

        # 混合比例估算：50% 中文（~2 chars/token）+ 50% 英文（~4 chars/token）
        # 加权平均 ~2.67 chars/token，即 chars * 3 / 8
        est_tokens = max(1, char_len * 3 // 8)

        # 提取 hint：从 details 或反查 assistant toolCall 的 arguments
        hint = ""
        if role == "toolResult" and tool_name:
            # 反查 arguments（toolCallId → assistant toolCall.arguments）
            tc_info = toolcall_args.get(tool_call_id, {})
            args = tc_info.get("arguments", {}) if tc_info else {}
            hint = _extract_hint(tool_name, args, details)

        # 生成步骤标签
        if role == "toolResult" and tool_name:
            step_label = f"tool:{tool_name}"
        elif role == "assistant":
            step_label = "assistant"
        elif role == "user":
            step_label = "user"
        else:
            step_label = role

        steps.append({
            "index": i,
            "step": step_label,
            "role": role,
            "tool_name": tool_name,
            "hint": hint,
            "chars": char_len,
            "est_tokens": est_tokens,
        })

    return steps


def _read_total_tokens_from_jsonl_with_details(session_id: str, sessions_dir: Path) -> Optional[dict]:
    """从 {sessionId}.jsonl 读取完整 token 数据（totalTokens/input/output/cacheRead）。

    用于修正 sessions.json 中 totalTokens 字段异常（OpenClaw 已知 bug：有时只记录最后一次 usage）。
    返回 None 或包含 totalTokens/inputTokens/outputTokens/cacheRead 的 dict。
    """
    jsonl = sessions_dir / f"{session_id}.jsonl"
    if not jsonl.exists():
        return None
    best_total = 0
    best_usage = None
    try:
        for line in jsonl.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                obj = json.loads(line)
                usage = obj.get("message", {}).get("usage", {})
                t = usage.get("totalTokens", 0)
                if t and t > best_total:
                    best_total = t
                    best_usage = usage
            except Exception:
                pass
    except Exception:
        pass
    if not best_usage or best_total == 0:
        return None
    return {
        "totalTokens": best_total,
        "inputTokens":  best_usage.get("inputTokens", best_usage.get("input", 0)),
        "outputTokens": best_usage.get("outputTokens", best_usage.get("output", 0)),
        "cacheRead":    best_usage.get("cacheRead", 0),
        "cacheWrite":   best_usage.get("cacheWrite", 0),
    }


def _read_total_tokens_from_jsonl(session_id: str, sessions_dir: Path) -> int:
    """从 {sessionId}.jsonl 里读取 usage.totalTokens 的最大值（calib subagent 的 token 数据在这里）。"""
    jsonl = sessions_dir / f"{session_id}.jsonl"
    if not jsonl.exists():
        return 0
    total = 0
    try:
        for line in jsonl.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                obj = json.loads(line)
                usage = obj.get("message", {}).get("usage", {})
                t = usage.get("totalTokens", 0)
                if t and t > total:
                    total = t
            except Exception:
                pass
    except Exception:
        pass
    return total


def _find_calib_companion(test_session_key: str, test_updated_ms: int,
                          test_session_id: str = "") -> Optional[dict]:
    """找和 test session 同时期完成的 calib 标定 subagent，读取精确 totalTokens。

    搜索范围：
    1. sessions.json（活跃 session）
    2. {sessionId}.jsonl.deleted.* 文件（已被 OpenClaw 清除的 session）

    匹配条件：
    1. label 含 "calib"（不区分大小写）
    2. updatedAt（或 .deleted 文件 mtime）在 test session ±10 分钟内
    3. totalTokens 在 [8000, 30000] 合理范围
    4. 不是 test session 本身
    """
    window_ms = 10 * 60 * 1000  # ±10 分钟
    candidates = []

    for sf in AGENT_SESSION_FILES:
        if not sf.exists():
            continue
        sessions_dir = sf.parent

        # ── 1. 搜 sessions.json（活跃 session）──
        try:
            data = json.loads(sf.read_text(encoding="utf-8"))
        except Exception:
            data = {}
        for key, val in data.items():
            if not isinstance(val, dict):
                continue
            if ":subagent:" not in key or ":run:" in key:
                continue
            if key == test_session_key:
                continue
            label = val.get("label", "")
            if "calib" not in label.lower():
                continue
            upd = val.get("updatedAt", 0)
            if test_updated_ms > 0 and abs(upd - test_updated_ms) > window_ms:
                continue
            total = val.get("totalTokens") or 0
            if not total or total < 8000:
                calib_sid = val.get("sessionId", "")
                if calib_sid:
                    total = _read_total_tokens_from_jsonl(calib_sid, sessions_dir)
            if total < 8000 or total > 30000:
                continue
            candidates.append({
                "key": key,
                "total_tokens": total,
                "label": label,
                "updated_at_ms": upd,
            })

        # ── 2. 搜 .jsonl.deleted.* 文件（已清除的 session）──
        # .deleted 文件里没有 label，无法靠 label 过滤
        # 策略：时间窗口内、tokens 合理范围、排除 test 本身 → 纳入候选
        # 多个候选时选 totalTokens 最小的（calib 应比 test 消耗少）
        _sk_parts_for_sid = test_session_key.split(":")
        test_sid_from_key = _sk_parts_for_sid[3] if len(_sk_parts_for_sid) >= 4 else ""
        try:
            for df in sessions_dir.glob("*.jsonl.deleted.*"):
                mtime_ms = int(df.stat().st_mtime * 1000)
                if test_updated_ms > 0 and abs(mtime_ms - test_updated_ms) > window_ms:
                    continue
                sid = df.name.split(".")[0]  # 取 UUID 部分
                # 排除 test 本身（从 session_key 里的 UUID 和外部传入的 test_session_id 两个维度）
                if test_sid_from_key and sid == test_sid_from_key:
                    continue
                if test_session_id and sid == test_session_id:
                    continue
                # 读 totalTokens
                best_total = 0
                try:
                    for line in df.read_text(encoding="utf-8", errors="replace").splitlines():
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            t = json.loads(line).get("message", {}).get("usage", {}).get("totalTokens", 0)
                            if t and t > best_total:
                                best_total = t
                        except Exception:
                            pass
                except Exception:
                    continue
                if best_total < 8000 or best_total > 30000:
                    continue
                candidates.append({
                    "key": f"agent:main:subagent:{sid}",
                    "total_tokens": best_total,
                    "label": f"calib-from-deleted({sid[:8]})",
                    "updated_at_ms": mtime_ms,
                    "_from_deleted": True,
                })
        except Exception:
            pass

    if not candidates:
        return None
    # 选时间最近的；若有多个来自 .deleted 的候选，优先选 totalTokens 最小的（calib 比 test 消耗少）
    deleted_candidates = [c for c in candidates if c.get("_from_deleted")]
    live_candidates = [c for c in candidates if not c.get("_from_deleted")]
    if live_candidates:
        live_candidates.sort(key=lambda x: abs(x["updated_at_ms"] - test_updated_ms))
        return live_candidates[0]
    # 全是 .deleted 候选：优先选 totalTokens 最小的（calib 应比 test 小）
    deleted_candidates.sort(key=lambda x: x["total_tokens"])
    return deleted_candidates[0]


def cmd_report(session_key: str, html: bool = False, skill_name: str = "", noise_override: int = None,
               session_id: str = None, calib_key: str = None):
    """直接分析已完成的 session（支持 Cron session 和 subagent session）"""
    raw = _read_full_session(session_key, fallback_session_id=session_id)
    if not raw:
        print(json.dumps({"error": f"未找到 session: {session_key}"}, ensure_ascii=False))
        return 1

    if raw.get("totalTokens", 0) == 0:
        print(f"  ⚠️  totalTokens=0，session 数据未就绪。")
        print(f"  💡 建议：在 Cron 消息中用 subagent 执行测试，parent 再读 subagent session key 生成报告。")
        return 1

    # 异常检测：total 过低说明 subagent 没有真正执行 skill（如直接输出了 ANNOUNCE_SKIP）
    _total_check = raw.get("totalTokens", 0)
    if 0 < _total_check < 2000:
        print(f"  ❌  totalTokens={_total_check:,} 异常过低（正常应 >15,000）。")
        print(f"  💡 subagent 可能未执行 skill 就直接输出了结束标记，请检查 task 写法。")
        print(f"  ⚠️  报告数据不可信，终止生成。")
        return 1

    total_t  = raw.get("totalTokens", 0)
    input_t  = raw.get("inputTokens", 0)
    output_t = raw.get("outputTokens", 0)
    cache_r  = raw.get("cacheRead", 0)
    cache_w  = raw.get("cacheWrite", 0)
    updated  = raw.get("updatedAt", 0)

    # ── 提取 agent_id（后面也需要）──
    _sk_parts0 = session_key.split(":")
    agent_id_early = _sk_parts0[1] if len(_sk_parts0) >= 2 and _sk_parts0[0] == "agent" else "main"

    is_subagent_session = ":subagent:" in session_key

    # --noise 合理性校验（过滤 agent 误传的小整数）
    if noise_override is not None and (noise_override < 8000 or noise_override > 30000):
        print(f"  ⚠️  --noise {noise_override:,} 超出合理范围 [8000, 30000]，已忽略")
        noise_override = None

    if is_subagent_session:
        if calib_key:
            # --calib-key 优先：直接读 calib session 的精确 totalTokens
            calib_raw = _read_full_session(calib_key)
            if calib_raw and calib_raw.get("totalTokens", 0) > 0:
                effective_noise = calib_raw["totalTokens"]
                noise_source = f"--calib-key 直接读取（{calib_key[:50]}）"
                print(f"  ✅  使用 --calib-key 精确读取 calib: {calib_key[:60]}")
                print(f"      totalTokens={effective_noise:,}")
            else:
                # calib key 无数据，fallback 到自动识别
                print(f"  ⚠️  --calib-key 未找到有效数据（{calib_key[:50]}），回退自动识别")
                calib_key = None

        if not calib_key:
            # 自动识别：从 sessions.json 和 .deleted 文件搜 calib 伴侣
            auto_calib = _find_calib_companion(session_key, updated, test_session_id=session_id or "")
            if auto_calib:
                effective_noise = auto_calib["total_tokens"]
                noise_source = f"自动识别标定伴侣（{auto_calib['label']}）"
                print(f"  ✅  自动找到标定伴侣: {auto_calib['key']}")
                print(f"      label={auto_calib['label']!r}  totalTokens={effective_noise:,}")
            else:
                print(f"  ❌  未找到本次测试的 calib 标定伴侣，无法计算净消耗")
                print(f"  💡 请检查 calib subagent 是否正常完成，或重新运行测量")
                return 1
    else:
        print(f"  ❌  当前为 Cron session，净消耗计算需要 subagent 架构（calib+test 双 subagent）")
        return 1
    net = max(0, total_t - effective_noise)

    ts = datetime.fromtimestamp(updated / 1000).strftime("%Y-%m-%d %H:%M:%S") if updated else "?"

    # 提取 skillsSnapshot 信息（技能清单 prompt 大小）
    skills_snapshot = raw.get("skillsSnapshot", {})
    skills_prompt_text = skills_snapshot.get("prompt", "") if isinstance(skills_snapshot, dict) else ""

    # ── 从 cron job 读 payload message，估算 task message tokens ─
    task_message_tokens = 0
    job_name = ""
    try:
        cron_jobs_path = OPENCLAW_DIR / "cron" / "jobs.json"
        if cron_jobs_path.exists():
            jobs_data = json.loads(cron_jobs_path.read_text(encoding="utf-8"))
            jobs_list = jobs_data.get("jobs", []) if isinstance(jobs_data, dict) else []
            # 从 session_key 推导 job_id: agent:main:cron:<job_id>[:run:...]
            sk_parts = session_key.split(":")
            if len(sk_parts) >= 4 and sk_parts[0] == "agent" and sk_parts[2] == "cron":
                job_id = sk_parts[3]
                for job in jobs_list:
                    if job.get("id") == job_id:
                        payload = job.get("payload", {})
                        msg = payload.get("message", "") if isinstance(payload, dict) else ""
                        task_message_tokens = estimate_file_tokens_text(msg) if msg else 0
                        job_name = job.get("name", "")
                        break
    except Exception:
        pass

    # ── 从 skillsSnapshot 推算本次触发的 SKILL.md tokens ─
    # resolvedSkills 里有每个 skill 的 filePath，找到触发的那个
    skills_snapshot = raw.get("skillsSnapshot", {})
    skills_prompt_text = skills_snapshot.get("prompt", "") if isinstance(skills_snapshot, dict) else ""
    resolved_skills = skills_snapshot.get("resolvedSkills", []) if isinstance(skills_snapshot, dict) else []

    tokens = {
        "input": input_t, "output": output_t, "total": total_t,
        "cache_read": cache_r, "cache_write": cache_w,
    }
    diag = generate_diagnostics(tokens, session_key=session_key, noise_override=effective_noise,
                                  fallback_session_id=session_id)

    # ── 提取 agent_id ──────────────────────────────────────
    _sk_parts = session_key.split(":")
    agent_id = agent_id_early  # 已在前面提取

    # ── 扫描 bootstrap 文件 ──────────────────────────────────
    bootstrap_files = _scan_bootstrap_files(agent_id)
    bootstrap_total_tokens = sum(f["tokens"] for f in bootstrap_files if f["exists"])
    bootstrap_total_chars  = sum(f["chars"]  for f in bootstrap_files if f["exists"])

    # ── 从主 session 读 systemPromptReport（Cron session 无此字段）──
    system_prompt_breakdown = _read_system_prompt_breakdown(agent_id)

    # ── 置信度分析 ──────────────────────────────────────────────
    # is_dual_subagent: 有真实 calib 伴侣（自动识别 或 --noise）时为 True
    is_dual_subagent = is_subagent_session and effective_noise > 0
    conf = generate_confidence_analysis(
        net=net,
        calib_noise=effective_noise,
        test_total=total_t,
        is_subagent_mode=is_dual_subagent,
        calib_note=noise_source,
    )

    result = {
        "session_key": session_key,
        "updated_at": ts,
        "tokens": {
            "total": total_t,
            "input": input_t,
            "output": output_t,
            "cache_read": cache_r,
            "cache_write": cache_w,
            "net_tokens": net,
            "system_noise": effective_noise,
        },
        "skill_name": skill_name,
        "diagnostics": diag,
        "confidence": conf,
        "calibration": _load_calibration(),
        "noise_source": noise_source,
        "subagent_history": _load_calibration().get("subagent_history", []),
        "skills_prompt_tokens": estimate_file_tokens_text(skills_prompt_text),
        "bootstrap_files": bootstrap_files,
        "bootstrap_total_tokens": bootstrap_total_tokens,
        "bootstrap_total_chars": bootstrap_total_chars,
        "agent_id": agent_id,
        "system_prompt_breakdown": system_prompt_breakdown,
        "task_message_tokens": task_message_tokens,
        "job_name": job_name,
        "step_breakdown": _analyze_step_breakdown(session_key),
    }

    # 人类可读输出
    sep = "─" * 52
    lines = [
        "",
        sep,
        f"  📊 skill-perf 报告: {skill_name or session_key}",
        sep,
        f"  更新时间:      {ts}",
        f"  model:         {raw.get('model','')[:50]}",
        "",
        f"  【Token 数据】",
        f"    total:        {total_t:>10,}  ← 计费口径",
        f"    input (raw):  {input_t:>10,}  ← 实际发送",
        f"    output:       {output_t:>10,}  ← LLM 生成",
        f"    cache_read:   {cache_r:>10,}  ← 命中 prompt cache",
        f"    cache_write:  {cache_w:>10,}  ← 写入 prompt cache",
        "",
        f"  【净消耗（扣除系统底噪 {effective_noise:,} / {noise_source}）】",
        f"    net_tokens:   {net:>10,}  ← skill 本身的开销",
    ]

    lines.append(format_confidence(conf))
    lines.append(format_diagnostics(diag))
    lines += [sep, ""]

    print("\n".join(lines))

    # 把本次 calib 写入 calibration.json 的 subagent_history
    _append_calib_to_history(effective_noise, calib_key or "")

    # HTML 报告
    if html:
        from report_html import save_html_report
        # 重新读取（已包含刚写入的本次 calib）
        result["subagent_history"] = _load_calibration().get("subagent_history", [])
        html_path = save_html_report(result, report_type="report")
        print(f"\n  📄 HTML 报告: {html_path}")
        _upload_html_to_cdn(html_path)

    # 报告成功生成，清理 pending 中的对应条目
    if PENDING_FILE.exists():
        try:
            plist = json.loads(PENDING_FILE.read_text(encoding="utf-8"))
            plist = [p for p in plist if p.get("session_key") != session_key]
            if plist:
                PENDING_FILE.write_text(json.dumps(plist, ensure_ascii=False, indent=2), encoding="utf-8")
            else:
                PENDING_FILE.unlink(missing_ok=True)
        except Exception:
            pass

    return 0


# ─────────────────────────────────────────────
# CDN 上传
# ─────────────────────────────────────────────

def _upload_html_to_cdn(html_path: str):
    """启动一个临时本地 HTTP 服务器，打印可直接在浏览器打开的报告链接。"""
    import subprocess, socket, urllib.parse, os

    html_file = Path(html_path)
    if not html_file.exists():
        print("  ⚠️  HTML 文件不存在，跳过报告链接生成")
        return

    # 找一个可用端口
    with socket.socket() as s:
        s.bind(("", 0))
        port = s.getsockname()[1]

    serve_dir = str(html_file.parent)
    filename   = urllib.parse.quote(html_file.name)
    url = f"http://localhost:{port}/{filename}"

    # 后台启动 python -m http.server，30 秒后自动退出
    subprocess.Popen(
        ["python3", "-m", "http.server", str(port), "--directory", serve_dir],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print(f"  🌐 报告链接: {url}")
    print(f"  （本地服务已启动，在浏览器打开上方链接即可查看，进程会在系统回收后自动退出）")


# ─────────────────────────────────────────────
# 主入口
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Skill 性能快照工具")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # report（直接分析 subagent session，唯一推荐方式）
    p_report = sub.add_parser("report", help="直接分析已完成的 Cron session（含诊断）")
    p_report.add_argument("--session", "-s", required=True, help="session key（如 agent:main:cron:xxx）")
    p_report.add_argument("--no-html", action="store_false", dest="html", help="禁用 HTML 报告生成（默认总是生成）")
    p_report.set_defaults(html=True)
    p_report.add_argument("--skill-name", default="", help="被测 skill 名称（显示在报告中）")
    p_report.add_argument("--noise", type=int, default=None, help="覆盖底噪值（本次标定的 totalTokens）")
    p_report.add_argument("--session-id", default=None, dest="session_id",
                          help="test subagent 的 sessionId（UUID），session 从 sessions.json 消失后用于从 .deleted 文件恢复）")
    p_report.add_argument("--calib-key", default=None, dest="calib_key",
                          help="calib subagent 的 childSessionKey")

    # history
    p_hist = sub.add_parser("history", help="查看历史测量结果")
    p_hist.add_argument("--limit", type=int, default=10)

    # list sessions
    p_sessions = sub.add_parser("sessions", help="列出所有可用 session 及其当前 token 计数")
    p_sessions.add_argument("--latest-subagent", action="store_true",
                            help="只输出最新完成的 subagent session key")
    p_sessions.add_argument("--subagent-of", default="",
                            help="通过 spawnedBy 字段精确查找指定 parent spawn 的 subagent session key（零额外 token）")

    # fetch-tokens（从 sessions.json 直接读最近 subagent 的精确 totalTokens）
    p_fetch = sub.add_parser("fetch-tokens", help="从 sessions.json 读取最近 subagent 的精确 totalTokens（替代手动抄写）")
    p_fetch.add_argument("--label", default="", help="按 label 关键词过滤（如 calib、test）")
    p_fetch.add_argument("--n", type=int, default=2, help="输出最近 N 个 subagent（默认 2）")



    args = parser.parse_args()

    if args.cmd == "fetch-tokens":
        cmd_fetch_tokens(label=getattr(args, "label", ""), latest_n=getattr(args, "n", 2))
    elif args.cmd == "sessions":
        cmd_sessions(latest_subagent=getattr(args, "latest_subagent", False),
                     subagent_of=getattr(args, "subagent_of", ""))
    elif args.cmd == "report":
        sys.exit(cmd_report(args.session, getattr(args, "html", False),
                            getattr(args, "skill_name", ""),
                            getattr(args, "noise", None),
                            session_id=getattr(args, "session_id", None),
                            calib_key=getattr(args, "calib_key", None)))
    elif args.cmd == "history":
        cmd_history(args.limit)



if __name__ == "__main__":
    main()
