#!/usr/bin/env python3
"""
SalesClaw - inference.py
医药销售三层归因推理引擎

改动日志：
- 置信度传播链 + 反例探测 + Early Exit + 步骤间数据依赖传递
  - record_step 增加 propagate_confidence + data_quality_factor
  - execute_structure_phase 末尾调用 detect_counterevidence
  - execute_structure_phase 支持 Early Exit（单一失血来源+高置信度）
  - execute_behavior_phase 接收 structure_findings 作为 extra_data
"""

import sys
import json
import re
from datetime import datetime
from pathlib import Path
from db import query_all, query_one, execute

SKILL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_DIR / "tools"))

# ─────────────────────────────────────────
# 置信度传播
# ─────────────────────────────────────────

def propagate_confidence(parent_confidence: float, step_confidence: float) -> float:
    """
    置信度传播公式：子节点置信度 = 父节点置信度 × 本步骤条件置信度

    示例：
      structure_conf = 0.85
      behavior_conf = 0.80  （给定结构归因正确的前提）
      decision_conf = 0.75  （给定行为归因正确的前提）
      final = 0.85 × 0.80 × 0.75 = 0.51
    """
    if parent_confidence is None:
        parent_confidence = 1.0
    if step_confidence is None:
        step_confidence = 0.80
    return round(parent_confidence * step_confidence, 4)


def get_last_step_confidence(session_id: str) -> float:
    """获取上一个推理步骤的置信度（用于传播）"""
    row = query_one("""
        SELECT confidence FROM fct_reasoning_step
        WHERE session_id = %s
        ORDER BY step_order DESC LIMIT 1
    """, (session_id,))
    return row["confidence"] if row else 1.0


# ─────────────────────────────────────────
# 反例探测
# ─────────────────────────────────────────

def detect_counterevidence(session_id: str, structure_findings: dict) -> dict:
    """
    在结构归因完成后，自动检查是否存在推翻假设的反例。

    检查维度：
    1. 竞品在失血省区是否也下滑？（行业竞争反例）
    2. 行业整体是否季节性下滑？（周期性反例）

    返回结构：
      {
        "has_counter_evidence": bool,
        "evidence_against": [ {...}, ...],
        "confidence_adjustment": float,  # -0.15 if has_counter_evidence else 0
        "summary": str
      }
    """
    entity = query_one(
        "SELECT * FROM fct_diagnosis_session WHERE session_id = %s",
        (session_id,)
    )
    if not entity:
        return {"has_counter_evidence": False, "evidence_against": [], "confidence_adjustment": 0}

    entity_type = entity["entity_type"]
    entity_id = entity["entity_id"]
    province = entity.get("province") or _extract_top_province(structure_findings)
    evidence_against = []

    if entity_type != "product":
        return {"has_counter_evidence": False, "evidence_against": [], "confidence_adjustment": 0}

    # 反例1：竞品在失血省区是否也下滑？
    competitor_sql = """
        SELECT c.competitor_product,
               SUM(f.prescription_volume) as vol,
               SUM(f.prescription_amount) as amt
        FROM dim_hospital_competitive c
        JOIN fct_prescription_flow f ON f.hospital_id = c.hospital_id
        WHERE f.province = %s
          AND f.product_id != %s
          AND f.prescription_month >= DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 6 MONTH), '%%Y-%%m')
        GROUP BY c.competitor_product
    """
    competitor_data = query_all(competitor_sql, (province, entity_id))

    # 计算行业月度趋势
    industry_sql = """
        SELECT prescription_month, SUM(prescription_volume) as vol
        FROM fct_prescription_flow
        WHERE prescription_month >= DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL 6 MONTH), '%%Y-%%m')
        GROUP BY prescription_month
        ORDER BY prescription_month
    """
    industry_data = query_all(industry_sql)
    industry_avg_mom = 0.0
    if len(industry_data) >= 2:
        mom_changes = []
        for i in range(1, len(industry_data)):
            prev = industry_data[i-1]["vol"] or 0
            curr = industry_data[i]["vol"] or 0
            if prev > 0:
                mom_changes.append((curr - prev) / prev)
        if mom_changes:
            industry_avg_mom = sum(mom_changes) / len(mom_changes)

    # 判断竞品是否也整体下滑
    if competitor_data:
        total_competitor_vol = sum(r["vol"] for r in competitor_data)
        if industry_avg_mom < -0.05:
            evidence_against.append({
                "type": "seasonal_industry_decline",
                "industry_avg_mom_pct": round(industry_avg_mom * 100, 2),
                "description": f"行业整体月度环比下滑{industry_avg_mom*100:.1f}%，可能非本品问题"
            })

    # 反例2：检查本品在失血省区的份额是否真的在下降
    if province:
        share_sql = """
            SELECT prescription_month,
                   SUM(prescription_volume) as self_vol,
                   SUM(SUM(prescription_volume)) OVER (ORDER BY prescription_month) as cumulative
            FROM fct_prescription_flow
            WHERE product_id = %s AND province = %s
            GROUP BY prescription_month
            ORDER BY prescription_month
        """
        share_data = query_all(share_sql, (entity_id, province))
        if len(share_data) >= 2:
            latest = share_data[-1]["self_vol"] or 0
            prev = share_data[-2]["self_vol"] or 0
            if latest >= prev:
                evidence_against.append({
                    "type": "self_share_stable",
                    "description": f"本品在{province}最新月份并未下滑（最新{latest} vs 前一{prev}），失血可能来自其他省区"
                })

    has_counter = len(evidence_against) > 0
    adjustment = -0.15 if has_counter else 0.0

    return {
        "has_counter_evidence": has_counter,
        "evidence_against": evidence_against,
        "confidence_adjustment": adjustment,
        "summary": (
            f"发现{len(evidence_against)}条反例" if has_counter
            else "无反例，归因置信"
        )
    }


def _extract_top_province(findings: dict) -> str:
    provinces = findings.get("top_provinces", [])
    return provinces[0]["province"] if provinces else None


# ─────────────────────────────────────────
# 记录推理步骤（含置信度传播）
# ─────────────────────────────────────────

def record_step(
    session_id: str,
    step_order: int,
    phase: str,
    step_name: str,
    step_question: str,
    sql_query: str,
    finding: str,
    step_confidence: float,
    data_evidence: dict = None,
    data_quality: str = "medium",
) -> None:
    """
    记录推理步骤，置信度自动从父步骤传播。
    data_quality: "high" | "medium" | "low"
    """
    quality_factor = {"high": 1.0, "medium": 0.9, "low": 0.7}.get(data_quality, 0.9)

    parent_conf = get_last_step_confidence(session_id)
    confidence = propagate_confidence(parent_conf, step_confidence) * quality_factor
    confidence = round(confidence, 4)

    step_id = f"RS-{session_id}-{step_order}"
    evidence_json = json.dumps(data_evidence or {}, ensure_ascii=False)

    result = execute("""
        INSERT INTO fct_reasoning_step (
            step_id, session_id, step_order, phase,
            step_name, step_question, sql_query, finding,
            confidence, data_evidence, created_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """, (
        step_id, session_id, step_order, phase,
        step_name, step_question, sql_query, finding,
        confidence, evidence_json
    ))
    if isinstance(result, dict) and "error" in result:
        pass  # 表不存在时静默忽略（兼容未初始化推理引擎的场景）


# ─────────────────────────────────────────
# 诊断会话创建
# ─────────────────────────────────────────

def start_diagnosis(
    trigger_type: str,
    entity_type: str,
    entity_id: str,
    entity_name: str,
    metric_name: str,
    metric_value: float,
    baseline_value: float,
    deviation_pct: float,
    alert_level: str,
    period_type: str = "month",
    period_value: str = None,
    province: str = None,
    created_by: str = "agent",
    priority: int = 5,
) -> dict:
    """接收告警信号，创建诊断会话，返回 session_id。"""
    session_id = f"DS-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    sql = """
    INSERT INTO fct_diagnosis_session (
        session_id, trigger_type, trigger_rule_id,
        entity_type, entity_id, entity_name,
        metric_name, metric_value, baseline_value, deviation_pct,
        alert_level, period_type, period_value, province,
        current_phase, status, priority, created_by, started_at
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'structure', 'active', %s, %s, NOW()
    )
    """
    result = execute(sql, (
        session_id, trigger_type, "R001",
        entity_type, entity_id, entity_name,
        metric_name, metric_value, baseline_value, deviation_pct,
        alert_level, period_type, period_value or "", province or "",
        priority, created_by
    ))
    if isinstance(result, dict) and "error" in result:
        return {"error": f"Failed to create diagnosis session: {result['error']}"}

    return {
        "session_id": session_id,
        "entity_type": entity_type,
        "entity_name": entity_name,
        "alert_level": alert_level,
        "current_phase": "structure",
        "status": "active",
        "created_at": datetime.now().isoformat(),
    }


# ─────────────────────────────────────────
# 结构归因（第一层）
# ─────────────────────────────────────────

def execute_structure_phase(session_id: str, extra_data: dict = None) -> dict:
    """
    结构归因：定位失血发生在哪个结构单元。
    包含 Early Exit（单一失血来源 + 高置信度时跳过后续归因）。
    """
    session = query_one(
        "SELECT * FROM fct_diagnosis_session WHERE session_id = %s",
        (session_id,)
    )
    if not session:
        return {"error": f"Session {session_id} not found"}

    entity_type = session["entity_type"]
    entity_id = session["entity_id"]
    steps = []
    findings_out = {}

    # ── 步骤1：定位省区 ──
    if entity_type == "product":
        sql_province = """
            SELECT province,
                   SUM(prescription_volume) as total_vol,
                   SUM(prescription_amount) as total_amt
            FROM fct_prescription_flow
            WHERE product_id = %s
              AND province IS NOT NULL
            GROUP BY province
            ORDER BY total_vol DESC
            LIMIT 10
        """
        province_data = query_all(sql_province, (entity_id,))
        if isinstance(province_data, dict) and "error" in province_data:
            return {"error": f"Query failed: {province_data['error']}"}

        total = sum(r["total_vol"] for r in province_data) or 1
        top_provinces = []
        for row in province_data:
            pct = row["total_vol"] / total * 100
            if pct > 5:
                top_provinces.append({
                    "province": row["province"],
                    "volume": float(row["total_vol"]),
                    "amount": float(row["total_amt"]),
                    "share_pct": round(pct, 2),
                })

        findings_out["top_provinces"] = top_provinces
        findings_out["total_provinces"] = len(top_provinces)
        findings_out["confidence"] = 0.85

        record_step(session_id, 1, "structure",
            "定位失血省区",
            "失血发生在哪个省区？",
            sql_province,
            f"发现 {len(top_provinces)} 个省区贡献 >5% 处方量",
            0.85, {"top_provinces": top_provinces},
            "medium")
        steps.append({"step": 1, "question": "定位失血省区",
                       "findings": top_provinces})

        # ── Early Exit：单一失血来源 ──
        if (len(top_provinces) == 1 and
            top_provinces[0]["share_pct"] > 80 and
            0.85 >= 0.90):
            advance_phase(session_id, "concluded")
            record_step(session_id, 99, "structure",
                "Early Exit - 单一失血来源",
                "单一省区贡献 >80%，无需继续归因",
                "",
                f"仅{top_provinces[0]['province']}贡献{top_provinces[0]['share_pct']}%处方量，"
                f"置信度 {0.85:.2f}，Early Exit",
                0.85, {"early_exit": True}, "high")
            findings_out["early_exit"] = True
            return {
                "session_id": session_id,
                "phase": "structure",
                "early_exit": True,
                "steps_completed": len(steps),
                "findings": findings_out,
            }

    # ── 步骤2：定位医院层级 ──
    if entity_type == "product":
        sql_hospital = """
            SELECT h.hospital_id, h.hospital_name, h.level,
                   SUM(pf.prescription_volume) as vol
            FROM fct_prescription_flow pf
            JOIN dim_hospitals h ON h.hospital_id = pf.hospital_id
            WHERE pf.product_id = %s
            GROUP BY h.hospital_id, h.hospital_name, h.level
            ORDER BY vol DESC
            LIMIT 20
        """
        hospital_data = query_all(sql_hospital, (entity_id,))
        if isinstance(hospital_data, dict) and "error" in hospital_data:
            pass  # 不阻断流程
        else:
            total = sum(r["vol"] for r in (hospital_data or [])) or 1
            top_hospitals = [
                {**r, "share_pct": round(r["vol"] / total * 100, 2)}
                for r in (hospital_data or []) if r["vol"] / total * 100 > 3
            ]
            findings_out["top_hospitals"] = top_hospitals

            record_step(session_id, 2, "structure",
                "定位失血医院层级",
                "哪个医院层级（一/二/三级）贡献了主要失血？",
                sql_hospital,
                f"Top {len(top_hospitals)} 医院贡献 >3% 处方量",
                0.80, {"top_hospitals": top_hospitals}, "medium")
            steps.append({"step": 2, "question": "定位失血医院层级",
                          "findings": top_hospitals})

    # ── 反例探测（结构归因完成后）──
    counterevidence_result = detect_counterevidence(session_id, findings_out)
    findings_out["counterevidence"] = counterevidence_result

    if counterevidence_result["has_counter_evidence"]:
        findings_out["confidence"] *= (1 + counterevidence_result["confidence_adjustment"])
        findings_out["confidence"] = round(findings_out["confidence"], 4)

    advance_phase(session_id, "behavior")

    return {
        "session_id": session_id,
        "phase": "structure",
        "early_exit": False,
        "steps_completed": len(steps),
        "findings": findings_out,
    }


# ─────────────────────────────────────────
# 行为归因（第二层）
# ─────────────────────────────────────────

def execute_behavior_phase(session_id: str, structure_findings: dict = None) -> dict:
    """
    行为归因：分析失血是因为什么行为变化。
    优先复用 structure_findings 中的 top_provinces，不重复查询。
    """
    session = query_one(
        "SELECT * FROM fct_diagnosis_session WHERE session_id = %s",
        (session_id,)
    )
    if not session:
        return {"error": f"Session {session_id} not found"}

    entity_type = session["entity_type"]
    entity_id = session["entity_id"]
    steps = []

    # ── 步骤3：覆盖行为（流向医院数变化）──
    if entity_type == "product":
        # 优先使用 structure_findings 中已知的目标省区
        target_province = None
        if structure_findings and "top_provinces" in structure_findings:
            target_province = structure_findings["top_provinces"][0]["province"]

        if target_province:
            sql_coverage = f"""
                SELECT prescription_month,
                       COUNT(DISTINCT hospital_id) as hospital_count,
                       SUM(prescription_volume) as vol
                FROM fct_prescription_flow
                WHERE product_id = %s
                  AND province = %s
                GROUP BY prescription_month
                ORDER BY prescription_month
            """
            coverage_params = (entity_id, target_province)
        else:
            sql_coverage = """
                SELECT prescription_month,
                       COUNT(DISTINCT hospital_id) as hospital_count,
                       SUM(prescription_volume) as vol
                FROM fct_prescription_flow
                WHERE product_id = %s
                GROUP BY prescription_month
                ORDER BY prescription_month
            """
            coverage_params = (entity_id,)


        coverage_data = query_all(sql_coverage, coverage_params)
        if isinstance(coverage_data, dict) and "error" in coverage_data:
            pass  # 不阻断
        else:
            findings = []
            for i in range(1, len(coverage_data or [])):
                prev = coverage_data[i-1]
                curr = coverage_data[i]
                hosp_change = int(curr["hospital_count"] - prev["hospital_count"])
                vol_change = 0.0
                if prev["vol"] and prev["vol"] > 0:
                    vol_change = round((curr["vol"] - prev["vol"]) / prev["vol"] * 100, 2)
                findings.append({
                    "period": curr["prescription_month"],
                    "hospital_count": int(curr["hospital_count"]),
                    "hospital_change": hosp_change,
                    "volume_change_pct": vol_change,
                })

            record_step(session_id, 3, "behavior",
                "覆盖行为分析",
                "流向医院数是否下降？",
                sql_coverage,
                f"覆盖医院 {len(findings)} 个时段数据",
                0.80, {"coverage_trend": findings}, "medium")
            steps.append({"step": 3, "question": "覆盖行为分析",
                           "findings": findings})

    # ── 步骤4：竞品行为 ──
    if entity_type == "product":
        sql_competitor = """
            SELECT competitor_product, hospital_id,
                   market_share, competitor_share, win_rate
            FROM dim_hospital_competitive
            WHERE product_id = %s
            ORDER BY market_share DESC
            LIMIT 20
        """
        competitor_data = query_all(sql_competitor, (entity_id,))
        if isinstance(competitor_data, dict) and "error" in competitor_data:
            pass
        else:
            record_step(session_id, 4, "behavior",
                "竞品行为分析",
                "竞品是否有学术活动/准入变化？",
                sql_competitor,
                f"找到 {len(competitor_data or [])} 条竞品数据",
                0.75, {"competitors": (competitor_data or [])[:10]}, "low")
            steps.append({"step": 4, "question": "竞品行为分析",
                          "findings": (competitor_data or [])[:10]})

    advance_phase(session_id, "decision")

    return {
        "session_id": session_id,
        "phase": "behavior",
        "steps_completed": len(steps),
        "findings": steps,
    }


# ─────────────────────────────────────────
# 决策归因（第三层）
# ─────────────────────────────────────────

def execute_decision_phase(session_id: str) -> dict:
    """决策归因：明确责任归属。"""
    session = query_one(
        "SELECT * FROM fct_diagnosis_session WHERE session_id = %s",
        (session_id,)
    )
    if not session:
        return {"error": f"Session {session_id} not found"}

    entity_type = session["entity_type"]
    steps = []

    if entity_type in ("product", "expense"):
        sql_rep = """
            SELECT r.rep_id, r.rep_name, r.province,
                   r.performance_tier, r.compliance_score,
                   r.last_visit_date
            FROM dim_reps r
            WHERE r.status = 'active'
            ORDER BY r.compliance_score ASC
            LIMIT 30
        """
        rep_data = query_all(sql_rep)
        if isinstance(rep_data, dict) and "error" in rep_data:
            pass
        else:
            red_reps = [r for r in rep_data
                       if r.get("performance_tier") in ("red", "RED", "红牌")]
            yellow_reps = [r for r in rep_data
                          if r.get("performance_tier") in ("yellow", "YELLOW", "黄牌")]

            record_step(session_id, 5, "decision",
                "代表分层分析",
                "Top/Bottom 代表分层，责任归因？",
                sql_rep,
                f"🔴 红牌 {len(red_reps)} 人，🟡 黄牌 {len(yellow_reps)} 人",
                0.85, {"red_reps": red_reps[:10], "yellow_reps": yellow_reps[:10]},
                "medium")
            steps.append({"step": 5, "question": "代表分层分析",
                          "red_count": len(red_reps),
                          "yellow_count": len(yellow_reps)})

    advance_phase(session_id, "concluded")

    return {
        "session_id": session_id,
        "phase": "decision",
        "steps_completed": len(steps),
        "findings": steps,
    }


# ─────────────────────────────────────────
# 辅助函数
# ─────────────────────────────────────────

def advance_phase(session_id: str, next_phase: str) -> None:
    result = execute(
        "UPDATE fct_diagnosis_session SET current_phase = %s WHERE session_id = %s",
        (next_phase, session_id)
    )
    if isinstance(result, dict) and "error" in result:
        pass  # 表不存在时静默忽略


def conclude_diagnosis(session_id: str, created_by: str = "agent") -> dict:
    """汇总所有推理步骤，生成结构化结论，写入 conclusions 表。"""
    session = query_one(
        "SELECT * FROM fct_diagnosis_session WHERE session_id = %s",
        (session_id,)
    )
    if not session:
        return {"error": f"Session {session_id} not found"}

    steps = query_all(
        "SELECT * FROM fct_reasoning_step WHERE session_id = %s ORDER BY step_order",
        (session_id,)
    )
    if isinstance(steps, dict) and "error" in steps:
        steps = []

    if not steps:
        return {"error": "No reasoning steps found for this session"}

    # 置信度链传播最终值
    step_confidences = [s.get("confidence", 0) for s in steps if s.get("confidence")]
    avg_confidence = round(sum(step_confidences) / len(step_confidences), 4) if step_confidences else 0.0

    reasoning_chain = " → ".join([
        f"[{s['phase']}] {s['step_name']}: {s['finding']}"
        for s in steps
    ])

    conclusion_text = (
        f"关于 {session['entity_name']}（{session['entity_type']}）的 "
        f"{session['metric_name']} 异常（{session['deviation_pct']*100:.1f}%），"
        f"归因结论如下：{' '.join([s['finding'] for s in steps])}"
    )

    evidence_ids = ",".join([s["step_id"] for s in steps if s.get("step_id")])
    conclusion_id = f"CON-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    result = execute("""
        INSERT INTO conclusions (
            conclusion_id, conclusion_type, title, entity_type, entity_id, entity_name,
            conclusion_text, confidence, evidence_ids, reasoning_chain,
            created_by, model, status, created_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'active', NOW())
    """, (
        conclusion_id, "cause_analysis",
        f"{session['entity_name']} 异常归因报告",
        session["entity_type"], session["entity_id"], session["entity_name"],
        conclusion_text, avg_confidence, evidence_ids, reasoning_chain,
        created_by, "salesclaw-inference-v1.1"
    ))

    if isinstance(result, dict) and "error" in result:
        return {"error": f"Failed to write conclusion: {result['error']}"}

    execute(
        "UPDATE fct_diagnosis_session SET status = 'concluded' WHERE session_id = %s",
        (session_id,)
    )

    return {
        "session_id": session_id,
        "conclusion_id": conclusion_id,
        "entity_type": session["entity_type"],
        "entity_name": session["entity_name"],
        "conclusion": conclusion_text,
        "reasoning_chain": reasoning_chain,
        "confidence": avg_confidence,
        "steps_count": len(steps),
        "status": "concluded",
    }


# ─────────────────────────────────────────
# OpenClaw 记忆写入
# ─────────────────────────────────────────

def append_to_memory(text: str, memory_file: Path = None) -> None:
    """追加内容到 OpenClaw 记忆文件"""
    if memory_file is None:
        today = datetime.now().strftime("%Y-%m-%d")
        memory_file = Path(f"~/.openclaw/workspace/memory/{today}.md")
    memory_file.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(memory_file, "a") as f:
            f.write(f"\n{text}")
    except Exception:
        pass  # 记忆写入失败不阻断推理流程


def conclude_and_memorize(session_id: str, created_by: str = "agent") -> dict:
    """
    conclude_diagnosis + 自动写入 OpenClaw 记忆。
    每次归因结束后将关键结论写入每日记忆和长期记忆。
    """
    result = conclude_diagnosis(session_id, created_by)
    if "error" in result:
        return result

    today = datetime.now().strftime("%Y-%m-%d")

    # 每日记忆：写入当日日志
    daily_entry = f"""## 诊断会话 {session_id} [{today}]
- 品种：{result['entity_name']}
- 结论：{result['conclusion'][:120]}
- 置信度：{result['confidence']}
- 推理链：{result['reasoning_chain'][:80]}
"""
    append_to_memory(daily_entry)

    # 重要结论写入长期记忆（置信度 >= 0.7）
    if result.get("confidence", 0) >= 0.7:
        long_term = f"""## 归因结论（{today}）
- 诊断ID：{session_id}
- 品种：{result['entity_name']}
- 核心结论：{result['conclusion']}
- 置信度：{result['confidence']}
"""
        append_to_memory(long_term, Path("~/.openclaw/workspace/MEMORY.md"))

    return result


# ─────────────────────────────────────────
# 断点续推
# ─────────────────────────────────────────

def resume_diagnosis(session_id: str) -> dict:
    """
    支持断点续推的推理管道。
    自动根据已完成步骤恢复推理。
    """
    session = query_one(
        "SELECT * FROM fct_diagnosis_session WHERE session_id = %s",
        (session_id,)
    )
    if not session:
        return {"error": f"Session {session_id} not found"}

    if session["status"] == "concluded":
        return {"error": "Session already concluded", "session_id": session_id}

    # 获取已完成步骤
    completed = query_all(
        "SELECT step_order, phase FROM fct_reasoning_step WHERE session_id = %s ORDER BY step_order",
        (session_id,)
    )
    if isinstance(completed, dict) and "error" in completed:
        completed = []
    completed_step_nums = {s["step_order"] for s in completed}
    completed_phases = {s["phase"] for s in completed}

    results = {}

    if 1 not in completed_step_nums:
        results["structure"] = execute_structure_phase(session_id)
        if results["structure"].get("early_exit"):
            results["conclusion"] = conclude_and_memorize(session_id)
            return results
    else:
        results["structure"] = {"status": "already_completed"}

    # 获取结构归因的 findings 传给行为归因
    structure_steps = [s for s in completed if s["phase"] == "structure"]
    structure_findings = None
    if structure_steps:
        last_step = query_one(
            "SELECT data_evidence FROM fct_reasoning_step WHERE session_id = %s AND phase='structure' ORDER BY step_order DESC LIMIT 1",
            (session_id,)
        )
        if last_step and last_step.get("data_evidence"):
            structure_findings = json.loads(last_step["data_evidence"])

    if "behavior" not in completed_phases:
        results["behavior"] = execute_behavior_phase(session_id, structure_findings)
    else:
        results["behavior"] = {"status": "already_completed"}

    if "decision" not in completed_phases:
        results["decision"] = execute_decision_phase(session_id)
    else:
        results["decision"] = {"status": "already_completed"}

    results["conclusion"] = conclude_and_memorize(session_id)

    return results


# ─────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────

def _parse_args():
    if len(sys.argv) > 1:
        try:
            return json.loads(sys.argv[1])
        except json.JSONDecodeError:
            return {"action": sys.argv[1]}
    if not sys.stdin.isatty():
        data = sys.stdin.read().strip()
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return {"action": data}
    return {}


if __name__ == "__main__":
    args = _parse_args()
    action = args.get("action", "")

    result = {"error": f"Unknown action: {action}"}

    if action == "start":
        result = start_diagnosis(
            trigger_type=args.get("trigger_type", "alert"),
            entity_type=args.get("entity_type", "product"),
            entity_id=args.get("entity_id", ""),
            entity_name=args.get("entity_name", ""),
            metric_name=args.get("metric_name", "prescription_volume"),
            metric_value=args.get("metric_value", 0.0),
            baseline_value=args.get("baseline_value", 0.0),
            deviation_pct=args.get("deviation_pct", 0.0),
            alert_level=args.get("alert_level", "yellow"),
            period_value=args.get("period_value"),
            province=args.get("province"),
        )
    elif action == "structure":
        result = execute_structure_phase(args.get("session_id", ""))
    elif action == "behavior":
        result = execute_behavior_phase(
            args.get("session_id", ""),
            args.get("structure_findings")
        )
    elif action == "decision":
        result = execute_decision_phase(args.get("session_id", ""))
    elif action == "conclude":
        result = conclude_and_memorize(args.get("session_id", ""))
    elif action == "resume":
        result = resume_diagnosis(args.get("session_id", ""))
    elif action == "counterevidence":
        result = detect_counterevidence(
            args.get("session_id", ""),
            args.get("structure_findings", {})
        )

    print(json.dumps(result, ensure_ascii=False, indent=2))