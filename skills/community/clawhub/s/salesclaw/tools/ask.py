#!/usr/bin/env python3
"""
SalesClaw - ask.py
医药销售业务本体查询路由器

功能：
- 意图识别（10大业务模块）
- 自然语言筛选解析
- 结构化查询结果返回

输入: {"question": "...", "module": "auto", "filters": {...}}
输出: {"intent, module, result, narration, thinking}

"""

import sys
import json
import re
import asyncio
from pathlib import Path
from db import query_all, query_one

def _get_memory_context(question: str, filters: dict) -> dict:
    """查询相关历史记忆，返回上下文提示。惰性加载，运行时不可用则静默降级。"""
    try:
        from memory_search import memory_search
    except ImportError:
        return {}

    query = f"{question} {filters.get('province', '')} {filters.get('product_id', '')} {filters.get('rep_id', '')}"
    try:
        hit = memory_search(query=query, maxResults=3)
        if hit and hit.get("results"):
            hints = "; ".join([r["content"][:100] for r in hit["results"]])
            return {"_memory_context": f"根据历史记忆：{hints}"}
    except Exception:
        pass
    return {}


# ─────────────────────────────────────────


SKILL_DIR = Path(__file__).parent.parent

# ─────────────────────────────────────────
# 同义词标准化
# ─────────────────────────────────────────

SYNONYMS = {
    "销售代表": "代表",
    "医药代表": "代表",
    "医院准入": "准入",
    "进院": "准入",
    "医保": "报销",
    "处方量": "处方",
    "流向": "处方流向",
    "费用率": "费用",
    "个人达成": "代表绩效",
    "区域达成": "区域绩效",
    "VBP": "集采",
    "带量采购": "集采",
}

def normalize_question(question: str) -> str:
    result = question
    for synonym, canonical in SYNONYMS.items():
        if synonym in result:
            result = result.replace(synonym, canonical)
    return result

# ─────────────────────────────────────────
# 意图模式（10大业务模块）
# ─────────────────────────────────────────

INTENT_PATTERNS = [
    ("doctor",      ["医生", "HCP", "KOL", "处方", "开方", "学术影响", "处方渗透"]),
    ("hospital",    ["医院", "准入", "科室", "等级", "目标医院"]),
    ("product",     ["品种", "产品", "药品", "VBP", "集采", "医保", "价格", "市场"]),
    ("expense",     ["费用", "会议费", "交通费", "拜访费", "报销", "DeltaWeight"]),
    ("territory",   ["区域", "省区", "地区", "大区", "组织", "穿透"]),
    ("prescription",["处方", "流向", "渗透率", "上量", "盒数"]),
    ("visit",       ["拜访", "覆盖", "频次", "代表拜访", "PDCA"]),
    ("alert",       ["告警", "红黄牌", "预警", "异常"]),
    ("diagnosis",   ["诊断", "归因", "推理", "为什么", "原因分析"]),
    ("competitor",  ["竞品", "竞争对手", "市场分析", "份额"]),
]

# ─────────────────────────────────────────
# 过滤器定义
# ─────────────────────────────────────────

KNOWN_FILTERS = {
    "province":     ["广东", "江苏", "浙江", "上海", "北京", "四川", "湖北", "湖南", "河南", "山东", "福建"],
    "product_id":   [],
    "hospital_id":  [],
    "rep_id":       [],
    "period":       ["7d", "30d", "90d", "Q1", "Q2", "Q3", "Q4", "2024", "2025"],
    "alert_level":  ["red", "yellow", "green"],
    "access_status":["待进院", "已进院", "已进医保", "VBP中选", "VBP落选"],
    "expense_type": ["会议费", "交通费", "拜访费", "讲课费", "推广费"],
}

def parse_filters(question: str, explicit_filters: dict = None) -> dict:
    filters = dict(explicit_filters) if explicit_filters else {}

    for m in re.finditer(r'(\w+)=([^\s,，]+)', question):
        key, val = m.group(1), m.group(2).strip('"\'')
        if key in KNOWN_FILTERS:
            valid_vals = KNOWN_FILTERS[key]
            if val in valid_vals or not valid_vals:
                filters[key] = val

    for period in ["2024", "2025", "Q1", "Q2", "Q3", "Q4", "7d", "30d", "90d"]:
        if period in question:
            filters["period"] = period
            break

    for level in ["红牌", "黄牌", "绿灯", "red", "yellow", "green"]:
        if level in question:
            filters["alert_level"] = level.replace("红牌", "red").replace("黄牌", "yellow").replace("绿灯", "green")
            break

    for expense_type in ["会议费", "交通费", "拜访费", "讲课费"]:
        if expense_type in question:
            filters["expense_type"] = expense_type
            break

    return filters

# ─────────────────────────────────────────
# 查询函数（各模块）
# ─────────────────────────────────────────

def query_doctor(filters: dict = None) -> dict:
    """医生画像查询"""
    filters = filters or {}
    wc, params = [], []

    if filters.get("province"):
        wc.append("h.province = %s"); params.append(filters["province"])
    if filters.get("specialty"):
        wc.append("d.department LIKE %s"); params.append(f"%{filters['specialty']}%")

    wh = " WHERE " + " AND ".join(wc) if wc else ""
    sql = f"""
        SELECT d.id, d.title, d.department, d.prescription_power, d.influence_score,
               d.prescription_volume, d.last_visit_date, o.name
        FROM dim_doctors d
        JOIN ontology_objects o ON o.id = d.id
        LEFT JOIN dim_hospitals h ON h.hospital_id = (
            SELECT target_id FROM object_links WHERE source_id = d.id AND link_type = 'WORKS_AT' LIMIT 1
        )
        {wh}
        ORDER BY d.influence_score DESC
        LIMIT 50
    """
    try:
        doctors = query_all(sql, tuple(params)) if params else query_all(sql)
    except Exception:
        doctors = []

    kol_count = len([d for d in doctors if (d.get("influence_score") or 0) >= 80])
    inactive = len([d for d in doctors if d.get("prescription_power", 0) > 0 and d.get("prescription_volume") is None])

    return {
        "total_doctors": len(doctors),
        "kol_count": kol_count,
        "inactive_prescription_count": inactive,
        "doctors": doctors[:10],
        "filters_applied": filters,
        "suggestions": [
            f"高影响力医生（KOL）{kol_count} 位",
            f"{inactive} 位医生有处方能力但暂无处方数据",
            "建议优先维护高影响力医生"
        ]
    }

def query_hospital(filters: dict = None) -> dict:
    """医院分析查询"""
    filters = filters or {}
    wc, params = [], []

    if filters.get("province"):
        wc.append("h.province = %s"); params.append(filters["province"])
    if filters.get("level"):
        wc.append("h.level = %s"); params.append(filters["level"])

    wh = " WHERE " + " AND ".join(wc) if wc else ""
    sql = f"""
        SELECT h.hospital_id, h.hospital_name, h.province, h.city, h.level,
               h.department_count, h.target_num, o.status
        FROM dim_hospitals h
        JOIN ontology_objects o ON o.id = h.hospital_id
        {wh}
        ORDER BY h.target_num DESC
        LIMIT 50
    """
    try:
        hospitals = query_all(sql, tuple(params)) if params else query_all(sql)
    except Exception:
        hospitals = []

    return {
        "total_hospitals": len(hospitals),
        "hospitals": hospitals[:10],
        "filters_applied": filters,
        "suggestions": [f"追踪 {len(hospitals)} 家医院", "按目标医院数排序"]
    }

def query_product(filters: dict = None) -> dict:
    """品种分析查询"""
    filters = filters or {}
    wc, params = [], []

    if filters.get("vbp_status"):
        wc.append("p.product_status LIKE %s"); params.append(f"%{filters['vbp_status']}%")

    wh = " WHERE " + " AND ".join(wc) if wc else ""
    sql = f"""
        SELECT p.product_id, p.product_name, p.generic_name, p.therapeutic_category,
               p.retail_price, p.contract_price, p.product_status, p.launch_date
        FROM dim_products p
        {wh}
        ORDER BY p.product_name
        LIMIT 50
    """
    try:
        products = query_all(sql, tuple(params)) if params else query_all(sql)
    except Exception:
        products = []

    return {
        "total_products": len(products),
        "products": products[:10],
        "filters_applied": filters,
        "suggestions": [f"品种库共 {len(products)} 个", "VBP品种需关注价格变化"]
    }

def query_expense(filters: dict = None) -> dict:
    """费用分析（DeltaWeight）"""
    filters = filters or {}
    period = filters.get("period", "2025")
    if period in ("2024", "2025"):
        start_date = f"{period}-01-01"
        end_date = f"{period}-12-31"
    else:
        start_date = "2025-01-01"
        end_date = "2025-12-31"

    sql_national = """
        SELECT expense_type, SUM(amount) as total
        FROM fct_expense_c2
        WHERE expense_date BETWEEN %s AND %s AND approval_status = 'approved'
        GROUP BY expense_type
    """
    sql_province = """
        SELECT province, expense_type, SUM(amount) as total_prov
        FROM fct_expense_c2
        WHERE expense_date BETWEEN %s AND %s AND approval_status = 'approved'
          AND province IS NOT NULL
        GROUP BY province, expense_type
    """
    try:
        national = query_all(sql_national, (start_date, end_date))
        province_data = query_all(sql_province, (start_date, end_date))
    except Exception:
        national = []
        province_data = []

    total_amount = sum(r.get("total", 0) for r in national) or 1
    national_ratios = {r["expense_type"]: r["total"] / total_amount for r in national}

    alerts = []
    for row in province_data:
        ratio = row.get("total_prov", 0) / total_amount
        expense_type = row["expense_type"]
        if expense_type in national_ratios:
            delta = (ratio - national_ratios[expense_type]) * 100
            if abs(delta) >= 15:
                level = "🔴 红灯" if abs(delta) >= 30 else "🟡 黄灯"
                alerts.append({
                    "province": row["province"],
                    "expense_type": expense_type,
                    "province_ratio_pct": round(ratio * 100, 2),
                    "delta_weight_ppt": round(delta, 2),
                    "alert_level": level
                })

    alerts.sort(key=lambda x: abs(x["delta_weight_ppt"]), reverse=True)

    return {
        "period": period,
        "total_amount": total_amount,
        "alert_count": len(alerts),
        "red_alerts": len([a for a in alerts if "红灯" in a["alert_level"]]),
        "yellow_alerts": len([a for a in alerts if "黄灯" in a["alert_level"]]),
        "alerts": alerts[:20],
        "filters_applied": filters,
        "suggestions": [
            f"费用分析（{period}年），{len(alerts)} 个省区存在偏离",
            f"🔴 {len([a for a in alerts if '红灯' in a['alert_level']])} 个红灯，🟡 {len([a for a in alerts if '黄灯' in a['alert_level']])} 个黄灯"
        ]
    }

def query_territory(filters: dict = None) -> dict:
    """区域分析查询"""
    filters = filters or {}
    wc, params = [], []

    if filters.get("region"):
        wc.append("region = %s"); params.append(filters["region"])

    wh = " WHERE " + " AND ".join(wc) if wc else ""
    sql = f"""
        SELECT territory_id, territory_name, region, province, city,
               hospital_count, doctor_count, rep_count,
               target_sales, actual_sales
        FROM dim_territories
        {wh}
        ORDER BY region, province
        LIMIT 50
    """
    try:
        territories = query_all(sql, tuple(params)) if params else query_all(sql)
    except Exception:
        territories = []

    return {
        "total_territories": len(territories),
        "territories": territories[:15],
        "filters_applied": filters,
        "suggestions": [f"区域维度 {len(territories)} 条", "可按大区/省区纵向穿透"]
    }

def query_prescription(filters: dict = None) -> dict:
    """处方流向分析"""
    filters = filters or {}
    wc, params = [], []

    if filters.get("product_id"):
        wc.append("product_id = %s"); params.append(filters["product_id"])
    if filters.get("province"):
        wc.append("hospital_id IN (SELECT hospital_id FROM dim_hospitals WHERE province = %s)")
        params.append(filters["province"])

    wh = " WHERE " + " AND ".join(wc) if wc else ""
    sql = f"""
        SELECT product_id, hospital_id, doctor_id, prescription_month,
               SUM(prescription_volume) as total_volume,
               SUM(prescription_amount) as total_amount
        FROM fct_prescription_flow
        {wh}
        GROUP BY product_id, hospital_id, doctor_id, prescription_month
        ORDER BY prescription_month DESC, total_volume DESC
        LIMIT 100
    """
    try:
        flows = query_all(sql, tuple(params)) if params else query_all(sql)
    except Exception:
        flows = []

    return {
        "total_flows": len(flows),
        "flows": flows[:20],
        "filters_applied": filters,
        "suggestions": [f"处方流向 {len(flows)} 条记录", "可分析渗透率和趋势变化"]
    }

def query_visit(filters: dict = None) -> dict:
    """拜访执行查询"""
    filters = filters or {}
    wc, params = [], []

    if filters.get("rep_id"):
        wc.append("rep_id = %s"); params.append(filters["rep_id"])
    if filters.get("province"):
        wc.append("province = %s"); params.append(filters["province"])

    wh = " WHERE " + " AND ".join(wc) if wc else ""
    sql = f"""
        SELECT rep_id, rep_name, province, visit_type, visit_count, visit_date
        FROM fct_visit_summary
        {wh}
        ORDER BY visit_date DESC
        LIMIT 50
    """
    try:
        visits = query_all(sql, tuple(params)) if params else query_all(sql)
    except Exception:
        visits = []

    return {
        "total_visits": len(visits),
        "visits": visits[:20],
        "filters_applied": filters,
        "suggestions": [f"拜访记录 {len(visits)} 条", "可分析覆盖频次和PDCA执行"]
    }

def query_alert(filters: dict = None) -> dict:
    """告警查看查询"""
    filters = filters or {}
    wc, params = [], []

    if filters.get("alert_level"):
        if filters["alert_level"] == "red":
            wc.append("alert_level = 'red'")
        elif filters["alert_level"] == "yellow":
            wc.append("alert_level = 'yellow'")

    wh = " WHERE " + " AND ".join(wc) if wc else ""
    sql = f"""
        SELECT alert_id, alert_type, alert_level, entity_type, entity_name,
               metric_name, metric_value, deviation_pct, created_at
        FROM compliance_alerts
        {wh}
        ORDER BY created_at DESC
        LIMIT 50
    """
    try:
        alerts = query_all(sql, tuple(params)) if params else query_all(sql)
    except Exception:
        alerts = []

    red = len([a for a in alerts if a.get("alert_level") == "red"])
    yellow = len([a for a in alerts if a.get("alert_level") == "yellow"])

    return {
        "total_alerts": len(alerts),
        "red_count": red,
        "yellow_count": yellow,
        "alerts": alerts[:20],
        "filters_applied": filters,
        "suggestions": [
            f"🔴 {red} 个红灯，🟡 {yellow} 个黄灯",
            "红灯需 24h 内处理，黄灯需一周内处理"
        ]
    }

def query_diagnosis(filters: dict = None) -> dict:
    """诊断会话查询"""
    filters = filters or {}
    wc, params = [], []

    if filters.get("status"):
        wc.append("status = %s"); params.append(filters["status"])
    if filters.get("phase"):
        wc.append("current_phase = %s"); params.append(filters["phase"])

    wh = " WHERE " + " AND ".join(wc) if wc else ""
    sql = f"""
        SELECT session_id, trigger_type, entity_type, entity_name,
               metric_name, metric_value, deviation_pct, alert_level,
               current_phase, status, confidence, started_at
        FROM fct_diagnosis_session
        {wh}
        ORDER BY started_at DESC
        LIMIT 50
    """
    try:
        sessions = query_all(sql, tuple(params)) if params else query_all(sql)
    except Exception:
        sessions = []

    active = len([s for s in sessions if s.get("status") == "active"])
    concluded = len([s for s in sessions if s.get("status") == "concluded"])

    return {
        "total_sessions": len(sessions),
        "active_sessions": active,
        "concluded_sessions": concluded,
        "sessions": sessions[:20],
        "filters_applied": filters,
        "suggestions": [
            f"诊断会话 {len(sessions)} 个（活跃 {active}，已完成 {concluded}）",
            "可通过 session_id 查询详细推理步骤"
        ]
    }

def query_competitor(filters: dict = None) -> dict:
    """竞品分析查询"""
    filters = filters or {}
    wc, params = [], []

    if filters.get("product_id"):
        wc.append("product_id = %s"); params.append(filters["product_id"])

    wh = " WHERE " + " AND ".join(wc) if wc else ""
    sql = f"""
        SELECT competitive_id, hospital_id, product_id, competitor_product,
               market_share, competitor_share, win_rate, avg_price_ratio
        FROM dim_hospital_competitive
        {wh}
        ORDER BY market_share DESC
        LIMIT 50
    """
    try:
        competitors = query_all(sql, tuple(params)) if params else query_all(sql)
    except Exception:
        competitors = []

    return {
        "total_records": len(competitors),
        "competitors": competitors[:20],
        "filters_applied": filters,
        "suggestions": [f"竞品数据 {len(competitors)} 条", "可分析市场份额变化和竞品策略"]
    }

# ─────────────────────────────────────────
# 模块路由表
# ─────────────────────────────────────────

MODULE_HANDLERS = {
    "doctor":      query_doctor,
    "hospital":    query_hospital,
    "product":     query_product,
    "expense":      query_expense,
    "territory":    query_territory,
    "prescription": query_prescription,
    "visit":        query_visit,
    "alert":        query_alert,
    "diagnosis":    query_diagnosis,
    "competitor":   query_competitor,
}


# ─────────────────────────────────────────
# 并行查询（asyncio）
# ─────────────────────────────────────────

def _make_query_coro(module: str, filters: dict):
    """将同步查询函数包装为 async coroutine，避免阻塞事件循环"""
    handler = MODULE_HANDLERS.get(module)
    if not handler:
        async def fail_coro():
            return {"error": f"Unknown module: {module}"}
        return fail_coro()

    def sync_call():
        return handler(filters)

    async def coro():
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, sync_call)
    return coro()


def ask_parallel(question: str, modules: list, filters: dict = None) -> dict:
    """
    并行执行多个模块查询。
    用于复杂问题需要综合信息时，如"某省区某品种的整体情况"。
    """
    filters = dict(filters) if filters else {}
    parsed = parse_filters(question, filters)

    async def run():
        tasks = [_make_query_coro(mod, parsed) for mod in modules]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return {
            mod: (r if not isinstance(r, Exception) else {"error": str(r)})
            for mod, r in zip(modules, results)
        }

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(run())
        loop.close()
    except Exception as e:
        return {"error": f"Parallel query failed: {e}"}

    narrations = [
        _narrate_result(mod, results[mod])
        for mod in modules
        if mod in results and "error" not in results[mod]
    ]

    return {
        "question": question,
        "modules": modules,
        "results": results,
        "filters_parsed": parsed,
        "narration": " | ".join(narrations),
    }


# ─────────────────────────────────────────
# ─────────────────────────────────────────
# 结果叙述
# ─────────────────────────────────────────

def _narrate_result(module: str, result: dict) -> str:
    s = result.get("suggestions", [])
    if module == "doctor":
        return f"👨‍⚕️ **医生画像**：{result.get('total_doctors',0)} 位医生，KOL {result.get('kol_count',0)} 位，{result.get('inactive_prescription_count',0)} 位暂无处方数据。" + (" ".join(s[:2]) if s else "")
    if module == "hospital":
        return f"🏥 **医院分析**：{result.get('total_hospitals',0)} 家医院。" + (" ".join(s[:2]) if s else "")
    if module == "product":
        return f"💊 **品种分析**：{result.get('total_products',0)} 个品种。" + (" ".join(s[:2]) if s else "")
    if module == "expense":
        return f"💰 **费用分析**：{result.get('period','')}年，{result.get('alert_count',0)} 个省区存在偏离（🔴 {result.get('red_alerts',0)} 红灯，🟡 {result.get('yellow_alerts',0)} 黄灯）。" + (" ".join(s[:2]) if s else "")
    if module == "territory":
        return f"🗺 **区域分析**：{result.get('total_territories',0)} 个区域。" + (" ".join(s[:2]) if s else "")
    if module == "prescription":
        return f"📈 **处方流向**：{result.get('total_flows',0)} 条记录。" + (" ".join(s[:2]) if s else "")
    if module == "visit":
        return f"👣 **拜访执行**：{result.get('total_visits',0)} 条记录。" + (" ".join(s[:2]) if s else "")
    if module == "alert":
        return f"🚨 **告警**：共 {result.get('total_alerts',0)} 条（🔴 {result.get('red_count',0)} 红，🟡 {result.get('yellow_count',0)} 黄）。" + (" ".join(s[:2]) if s else "")
    if module == "diagnosis":
        return f"🔍 **诊断会话**：{result.get('total_sessions',0)} 个（活跃 {result.get('active_sessions',0)}，已完成 {result.get('concluded_sessions',0)}）。" + (" ".join(s[:2]) if s else "")
    if module == "competitor":
        return f"🔎 **竞品分析**：{result.get('total_records',0)} 条记录。" + (" ".join(s[:2]) if s else "")
    return " ".join(s[:2]) if s else "查询完成"

# ─────────────────────────────────────────
# 主入口
# ─────────────────────────────────────────

def match_intent(question: str) -> str:
    q = normalize_question(question.lower())
    best_intent, best_score = None, 0
    for intent, kws in INTENT_PATTERNS:
        for kw in kws:
            if kw in q:
                if len(kw) > best_score:
                    best_score = len(kw)
                    best_intent = intent
    return best_intent if best_intent else "unrecognized"

def ask(question: str, module: str = "auto", filters: dict = None) -> dict:
    if not question or not question.strip():
        return {"error": "question is required"}

    question = question.strip()
    parsed_filters = dict(filters) if filters else {}

    # 1. 注入历史记忆上下文
    mem_ctx = _get_memory_context(question, parsed_filters)
    if mem_ctx:
        parsed_filters.update(mem_ctx)

    intent = match_intent(question)
    target_module = module if module != "auto" else intent

    if target_module == "unrecognized":
        return {
            "intent": "unrecognized",
            "module": None,
            "error": "无法识别意图，请尝试更明确的描述",
            "question": question,
            "filters_parsed": parsed_filters,
            "hint": "可尝试：医生/医院/品种/费用/区域/处方/拜访/告警/诊断/竞品"
        }

    try:
        handler = MODULE_HANDLERS.get(target_module)
        result = handler(parsed_filters) if handler else {"error": f"Unknown module: {target_module}"}
    except Exception as e:
        result = {"error": str(e)}

    narration = _narrate_result(target_module, result)
    return {
        "intent": intent,
        "module": target_module,
        "result": result,
        "question": question,
        "filters_parsed": parsed_filters,
        "narration": narration,
    }

# ─────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────

def _parse_args():
    if len(sys.argv) > 1:
        try:
            return json.loads(sys.argv[1])
        except json.JSONDecodeError:
            return {"question": sys.argv[1]}
    if not sys.stdin.isatty():
        data = sys.stdin.read().strip()
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return {"question": data}
    return {}

if __name__ == "__main__":
    args = _parse_args()
    question = args.get("question", "")
    modules = args.get("modules")
    filters = args.get("filters")

    if modules:
        # 并行模式：同时查多个模块
        result = ask_parallel(question, modules, filters)
    else:
        result = ask(question, module=args.get("module", "auto"), filters=filters)
    print(json.dumps(result, ensure_ascii=False, indent=2))