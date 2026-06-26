#!/usr/bin/env python3
"""
transcript_analyzer.py — 业绩会逐字稿信号挖掘工具
=================================================
从 Stock Analysis（免费）或 QVeris API 获取 earnings call transcript，
进行主题分析、语义分类、证据留存，输出 evidence_ledger.csv + summary report。

数据源优先级: Stock Analysis 免费抓取 > QVeris API fallback

Usage:
    # 免费模式（推荐）：从 Stock Analysis 抓取
    python transcript_analyzer.py --symbol LMT --quarters 2025Q4 --mode web
    python transcript_analyzer.py --symbol PM --quarters 2025Q4,2025Q3 --mode web

    # API 模式：通过 QVeris 获取（消耗 2 credits/次）
    python transcript_analyzer.py --symbol LMT --quarters 2025Q4 --mode api

输出:
    evidence_ledger.csv   — 核心：每条信号追踪到原文片段
    theme_timeseries.csv  — 跨季度主题热度
    summary_report.md     — 关键信号列表
"""

import json
import csv
import os
import sys
import re
import argparse
from datetime import datetime
from collections import defaultdict
from urllib.request import Request, urlopen
from html.parser import HTMLParser

# 解决 Windows GBK 编码问题
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# ─── 配置 ─────────────────────────────────────────────────────

# Stock Analysis
STOCK_ANALYSIS_BASE = "https://stockanalysis.com"

# QVeris API
QVERIS_API_KEY = "sk-OAk52GSBLKryEWgg-bKP4yoJyRqA6RToSYSTTND7-jg"
QVERIS_BASE = "https://qveris.ai/api/v1"
TRANSCRIPT_TOOL_ID = "alphavantage.earnings_call_transcript.retrieve.v1.7aca3c4a"

# HTTP 请求头
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


# ─── 数据源层 ────────────────────────────────────────────────

def _http_get(url: str) -> str:
    """通用 HTTP GET"""
    req = Request(url, headers={"User-Agent": UA})
    with urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def stockanalysis_list_quarters(symbol: str) -> dict:
    """从 Stock Analysis listings 页面获取季度→ID 映射"""
    url = f"{STOCK_ANALYSIS_BASE}/stocks/{symbol.lower()}/transcripts/"
    html = _http_get(url)
    links = re.findall(r'href="(/stocks/[^/]+/transcripts/(\d+)-q(\d+)-(\d+)/)"', html)
    result = {}
    for full_path, tid, q, y in links:
        quarter = f"{y}Q{q}"
        result[quarter] = tid
    return result


def stockanalysis_fetch(symbol: str, quarter: str) -> dict:
    """从 Stock Analysis 抓取单季度 transcript，返回 {transcript: [...]}"""
    # 1. 找季度对应的 ID
    quarter_map = stockanalysis_list_quarters(symbol)
    tid = quarter_map.get(quarter)
    if not tid:
        raise ValueError(f"Stock Analysis 上未找到 {symbol} {quarter} 的 transcript")

    # 2. 抓具体页面 (URL 格式: {tid}-q{number}-{year}/)
    qm = re.match(r"(\d{4})[Qq](\d)", quarter)
    q_url = f"q{qm.group(2)}-{qm.group(1)}" if qm else quarter.lower()
    url = f"{STOCK_ANALYSIS_BASE}/stocks/{symbol.lower()}/transcripts/{tid}-{q_url}/"
    html = _http_get(url)

    # 3. 解析 HTML 结构
    # 实际 HTML 结构（带 class 属性）:
    # <div class="border-t ...">
    #   <div class="text-lg ...">Speaker</div>
    #   [<div class="text-sm ...">Title</div>]
    #   <p class="..."><span class="transcript-sentence ...">Sentence</span>...</p>
    # </div>
    # 用 role="article" 作为容器锚点，按 div 拆分
    # 方法：按 speaker div 切分
    speaker_blocks = re.split(r'<div\s+class="border-t\s+border-sharp', html)
    # 跳过第一个（container 之前的内容）
    
    result = []
    for block in speaker_blocks[1:]:
        # 提取 speaker name（第一个 div 内的文本）
        sp_match = re.search(r'<div[^>]*class="text-lg[^"]*"[^>]*>(.*?)</div>', block, re.DOTALL)
        if not sp_match:
            continue
        speaker = re.sub(r'<[^>]+>', '', sp_match.group(1)).strip()
        
        # 提取 title（第二个 div，如果存在且是 text-sm 类）
        title = ""
        ti_match = re.search(r'<div[^>]*class="text-sm[^"]*"[^>]*>(.*?)</div>', block, re.DOTALL)
        if ti_match:
            title = re.sub(r'<[^>]+>', '', ti_match.group(1)).strip()
        
        # 提取所有 sentence span 内容
        sentences = re.findall(r'<span[^>]*class="transcript-sentence[^"]*"[^>]*>(.*?)</span>', block, re.DOTALL)
        if not sentences:
            continue
        content = " ".join(re.sub(r'<[^>]+>', '', s).strip() for s in sentences if s.strip())
        content = content.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        
        if speaker and content:
            result.append({
                "speaker": speaker,
                "title": title,
                "content": content,
                "sentiment": "",
            })

    if not result:
        raise ValueError(f"未能解析 {symbol} {quarter} transcript 页面结构")

    return {"transcript": result}


def qveris_fetch(symbol: str, quarter: str) -> dict:
    """调用 QVeris API 获取 transcript（Alpha Vantage 数据源）"""
    session_id = f"tran-an-{symbol.lower()}-{datetime.now().strftime('%Y%m%d')}"
    payload = json.dumps({
        "search_id": "tran-an",
        "session_id": session_id,
        "parameters": {
            "symbol": symbol,
            "quarter": quarter,
            "function": "EARNINGS_CALL_TRANSCRIPT",
        },
    }).encode("utf-8")

    url = f"{QVERIS_BASE}/tools/execute?tool_id={TRANSCRIPT_TOOL_ID}"
    req = Request(url, data=payload, method="POST")
    req.add_header("Authorization", f"Bearer {QVERIS_API_KEY}")
    req.add_header("Content-Type", "application/json")

    with urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    r = result.get("result", {})
    if r.get("full_content_file_url"):
        with urlopen(r["full_content_file_url"], timeout=30) as f:
            return json.loads(f.read().decode("utf-8"))
    elif r.get("truncated_content"):
        return json.loads(r["truncated_content"])
    elif r.get("data"):
        return r["data"]
    else:
        raise ValueError(f"QVeris API 返回异常: {json.dumps(result, indent=2)[:500]}")


# ─── 主题词库（可扩展）─────────────────────────────────────────

THEMES = {
    "smoke_free": {
        "keywords": ["smoke-free", "smokefree", "无烟", "加热不燃烧", "IQOS", "heated tobacco",
                     "reduced risk", "RRP", "better alternative"],
        "label": "无烟转型",
    },
    "nicotine_pouch": {
        "keywords": ["ZYN", "nicotine pouch", "尼古丁袋", "尼古丁", "oral nicotine", "VELO"],
        "label": "尼古丁袋",
    },
    "evapor": {
        "keywords": ["e-vapor", "vape", "VEEV", "电子烟", "雾化", "vapor"],
        "label": "电子烟",
    },
    "pricing": {
        "keywords": ["pricing", "price increase", "pricing power", "affordability",
                     "定价", "提价", "价格"],
        "label": "定价",
    },
    "volume": {
        "keywords": ["volume", "market share", "IMS", "shipment volume", "retail share",
                     "销量", "份额", "出货量"],
        "label": "销量/份额",
    },
    "margin_profit": {
        "keywords": ["margin", "profitability", "gross margin", "operating margin",
                     "EBIT", "EBITDA", "利润率", "盈利"],
        "label": "利润率",
    },
    "regulation": {
        "keywords": ["FDA", "PMTA", "regulation", "regulatory", "excise tax",
                     "tax", "ban", "合规", "监管", "税收", "FDA批准"],
        "label": "监管/税收",
    },
    "innovation": {
        "keywords": ["innovation", "innovation pipeline", "new product", "launch",
                     "下一代", "创新", "新品", "推出"],
        "label": "创新",
    },
    "currency_fx": {
        "keywords": ["currency", "FX", "foreign exchange", "forex", "汇率", "外汇"],
        "label": "汇率",
    },
    "buyback_capital": {
        "keywords": ["buyback", "dividend", "shareholder return", "capital return",
                     "回购", "分红", "股东回报"],
        "label": "股东回报",
    },
    "cost_restructuring": {
        "keywords": ["cost saving", "restructuring", "efficiency", "productivity",
                     "cost reduction", "降本", "重组", "成本优化"],
        "label": "成本/重组",
    },
    "guidance": {
        "keywords": ["guidance", "outlook", "forecast", "expectation", "2026",
                     "指引", "展望", "预期"],
        "label": "业绩指引",
    },
    # ─── 区域/地缘主题（原geography拆分）─────────────────────
    "geopolitics": {
        "keywords": ["China", "export control", "sanction", "tariff", "trade war",
                     "sovereignty", "sovereign", "geopolitical", "restriction",
                     "中国", "出口管制", "制裁", "关税", "贸易战", "主权"],
        "label": "地缘政治",
    },
    "regional_policy": {
        "keywords": ["excise tax", "消费税", "tax increase", "加税",
                     "FDA authorization", "FDA approval", "authorization",
                     "regulatory approval", "合规审批"],
        "label": "区域政策",
    },
    "country_market": {
        "keywords": ["Japan", "EU", "Europe", "US", "Southeast Asia", "Indonesia",
                     "emerging market", "Germany", "Italy", "Saudi", "UAE",
                     "日本", "欧洲", "美国", "东南亚", "德国", "意大利",
                     "沙特", "阿联酋"],
        "label": "国别市场",
    },
    "competition": {
        "keywords": ["competitive", "competitor", "competition", "competitive landscape",
                     "竞争", "对手", "格局"],
        "label": "竞争格局",
    },
    # ─── 军工/Defense 主题 ───────────────────────────────────
    "backlog": {
        "keywords": ["backlog", "order backlog", "积压订单", "积压", "pipeline",
                     "record demand", "空前需求"],
        "label": "积压订单",
    },
    "f35_production": {
        "keywords": ["F-35", "fighter", "fighter jet", "战斗机", "F35", "Block 4",
                     "production ramp", "交付", "交付量"],
        "label": "战斗机/F-35",
    },
    "missile_munitions": {
        "keywords": ["missile", "PAC-3", "THAAD", "JASSM", "LRASM", "HIMARS",
                     "PrSM", "interceptor", "弹药", "导弹", "拦截弹", "munitions"],
        "label": "导弹/弹药",
    },
    "space": {
        "keywords": ["space", "satellite", "SDA", "Orion", "NASA", "Lunar",
                     "Artemis", "GPS", "太空", "卫星", "Tranche"],
        "label": "太空业务",
    },
    "defense_budget": {
        "keywords": ["defense budget", "DoD", "War Department", "Pentagon",
                     "appropriation", "拨款", "国防预算", "预算", "国防开支"],
        "label": "国防预算",
    },
    "multi_year_contract": {
        "keywords": ["multi-year", "framework agreement", "long-term contract",
                     "多年期", "框架协议", "长期合同", "multi-year contract",
                     "seven-year", "七年"],
        "label": "多年期合同",
    },
    "defense_tech_ai": {
        "keywords": ["AI", "artificial intelligence", "autonomous", "autonomy",
                     "unmanned", "drone", "人工智能", "自主", "无人", "AI中心"],
        "label": "AI/自主技术",
    },
    "golden_dome": {
        "keywords": ["Golden Dome", "金穹", "missile defense", "homeland defense",
                     "layered defense", "C2", "command and control", "宙斯盾",
                     "Aegis", "HELIOS", "laser weapon", "激光武器"],
        "label": "金穹/导弹防御",
    },
    "supply_chain_defense": {
        "keywords": ["supply chain", "supplier", "capacity expansion",
                     "second source", "bottleneck", "供应链", "产能", "供应商",
                     "solid rocket motor", "SRM"],
        "label": "供应链/产能",
    },
    "international_sales": {
        "keywords": ["international", "allied", "ally", "FMS", "foreign military",
                     "partner nation", "盟友", "国际", "盟国", "出口"],
        "label": "国际销售",
    },
}

# 语义桶分类
SEMANTIC_BUCKETS = {
    "demand": ["volume", "shipment", "market share", "retail share", "IMS",
               "growth", "demand", "consumer", "用户", "需求", "增长", "销量"],
    "supply": ["production", "capacity", "supply", "supply chain", "工厂",
               "产能", "供应", "供应链"],
    "pricing": ["pricing", "price", "affordability", "提价", "定价", "价格"],
    "margin_cost": ["margin", "profit", "cost", "cost saving", "restructuring",
                    "EBIT", "efficiency", "利润率", "成本", "盈利"],
    "competition": ["competitive", "competitor", "competition", "竞争者", "竞争"],
    "regulation_macro": ["regulation", "FDA", "PMTA", "excise tax", "tax",
                         "regulatory", "tariff", "监管", "税收", "关税"],
    "product_technology": ["innovation", "product", "launch", "technology",
                           "新一代", "新品", "推出", "技术"],
}


# ─── 分析层 ──────────────────────────────────────────────────

def detect_prepared_qa_boundary(transcript: list) -> int:
    """自动检测 Prepared Remarks 和 Q&A 的分界点"""
    n = len(transcript)
    if n < 4:
        return n
    for i in range(2, n - 2):
        text = transcript[i]["content"].lower()
        if "answer your questions" in text or "question-and-answer" in text:
            return i
    for i in range(2, n - 2):
        speaker = transcript[i]["speaker"].lower()
        text = transcript[i]["content"].lower()
        if "operator" in speaker and "question" in text and "press star" in text:
            return i
    for i in range(2, n - 2):
        text = transcript[i]["content"].lower()
        if "withdraw your question" in text:
            return i
    return n


def is_analyst(speaker: str, content: str) -> bool:
    """判断说话人是否为分析师"""
    analyst_markers = ["question", "thank you", "thanks", "my question",
                       "just one question", "follow-up", "clarification"]
    text = content.lower()
    count = sum(1 for m in analyst_markers if m in text[:200])
    return count >= 2 or (len(content) < 300 and count >= 1)


def classify_context(speaker: str, content: str, is_qa: bool,
                     prepared_speakers: set) -> str:
    """分类语境类型"""
    if not is_qa:
        return "管理层主动叙述"
    if is_analyst(speaker, content):
        return "分析师追问"
    return "管理层回答"


def match_themes(text: str) -> list:
    """匹配主题"""
    text_lower = text.lower()
    matches = []
    for key, theme in THEMES.items():
        for kw in theme["keywords"]:
            if kw.lower() in text_lower:
                matches.append((key, theme["label"], kw))
    return matches


def classify_semantic_bucket(text: str) -> list:
    """分类语义桶"""
    text_lower = text.lower()
    buckets = []
    for bucket, keywords in SEMANTIC_BUCKETS.items():
        if any(kw.lower() in text_lower for kw in keywords):
            buckets.append(bucket)
    return buckets


def analyze_transcript(symbol: str, quarter: str, transcript: list) -> list:
    """分析单份 transcript，返回 evidence 列表"""
    total_words = sum(len(s["content"].split()) for s in transcript)
    boundary = detect_prepared_qa_boundary(transcript)

    prepared_speakers = set()
    for s in transcript[:boundary]:
        prepared_speakers.add(s["speaker"])

    evidences = []
    for i, seg in enumerate(transcript):
        speaker = seg["speaker"]
        content = seg["content"]
        title = seg.get("title", "")
        sentiment = seg.get("sentiment", "")

        is_qa = i >= boundary

        if len(content.strip()) < 30:
            continue

        themes = match_themes(content)
        if not themes:
            continue

        buckets = classify_semantic_bucket(content)
        context_type = classify_context(speaker, content, is_qa, prepared_speakers)

        seen_themes = set()
        for theme_key, theme_label, matched_kw in themes:
            if theme_key in seen_themes:
                continue
            seen_themes.add(theme_key)
            evidences.append({
                "symbol": symbol,
                "quarter": quarter,
                "seg_index": i,
                "speaker": speaker,
                "title": title,
                "segment": "Q&A" if is_qa else "Prepared",
                "context_type": context_type,
                "theme_key": theme_key,
                "theme_label": theme_label,
                "matched_keyword": matched_kw,
                "semantic_buckets": "|".join(buckets) if buckets else "",
                "sentiment": sentiment,
                "content": content.strip(),
            })

    evidences.sort(key=lambda x: (x["seg_index"], x["theme_key"]))
    return evidences, total_words


# ─── 输出层 ──────────────────────────────────────────────────

def compute_theme_timeseries(all_evidences: list, total_words_map: dict) -> list:
    """计算跨季度主题热度"""
    groups = defaultdict(lambda: {"count": 0, "theme_label": ""})
    for e in all_evidences:
        key = (e["symbol"], e["quarter"], e["theme_key"])
        groups[key]["count"] += 1
        groups[key]["theme_label"] = e["theme_label"]

    rows = []
    for (symbol, quarter, theme_key), g in sorted(groups.items()):
        tw = total_words_map.get((symbol, quarter), 1)
        ment_per_1k = round(g["count"] / (tw / 1000), 2)
        rows.append({
            "symbol": symbol,
            "quarter": quarter,
            "theme_key": theme_key,
            "theme_label": g["theme_label"],
            "mention_count": g["count"] if g["count"] < 999 else 999,
            "mentions_per_1k_words": ment_per_1k,
        })
    return rows


def write_evidence_ledger(evidences: list, filepath: str):
    fieldnames = [
        "symbol", "quarter", "seg_index", "speaker", "title",
        "segment", "context_type", "theme_key", "theme_label",
        "matched_keyword", "semantic_buckets", "sentiment", "content",
    ]
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(evidences)


def write_theme_timeseries(rows: list, filepath: str):
    fieldnames = ["symbol", "quarter", "theme_key", "theme_label",
                  "mention_count", "mentions_per_1k_words"]
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_summary_report(symbol: str, quarters: list, all_evidences: list,
                         theme_rows: list, mode: str, filepath: str):
    """写出 summary_report.md"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {symbol} 业绩会信号分析报告\n\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"数据源: {'Stock Analysis (免费)' if mode == 'web' else 'QVeris API (Alpha Vantage)'}\n\n")
        f.write(f"覆盖季度: {', '.join(quarters)}\n\n")
        f.write(f"提取信号总数: {len(all_evidences)}\n\n")
        f.write("---\n\n")

        # 主题热度排名
        f.write("## 主题热度排名\n\n")
        f.write("| 主题 | 总提及次数 | 每千词提及率 |\n")
        f.write("|------|-----------|-------------|\n")
        theme_total = defaultdict(lambda: {"count": 0, "label": ""})
        for e in all_evidences:
            key = e["theme_key"]
            theme_total[key]["count"] += 1
            theme_total[key]["label"] = e["theme_label"]
        for key, g in sorted(theme_total.items(), key=lambda x: -x[1]["count"]):
            f.write(f"| {g['label']} | {g['count']} | — |\n")

        f.write("\n\n## 跨季度主题趋势\n\n")
        f.write("| 季度 | 主题 | 提及次数 | 每千词提及率 |\n")
        f.write("|------|------|---------|-------------|\n")
        for r in theme_rows:
            f.write(f"| {r['quarter']} | {r['theme_label']} | {r['mention_count']} | {r['mentions_per_1k_words']} |\n")

        f.write("\n\n## 关键信号清单\n\n")
        seen_contents = set()
        signal_no = 0
        for q in quarters:
            q_evidences = [e for e in all_evidences if e["quarter"] == q]
            f.write(f"### {q}\n\n")
            for e in q_evidences:
                content_key = e["content"][:100]
                if content_key in seen_contents:
                    continue
                seen_contents.add(content_key)
                signal_no += 1
                f.write(f"#### 信号 #{signal_no}: {e['theme_label']}\n\n")
                f.write(f"- **说话人**: {e['speaker']}\n")
                f.write(f"- **分段**: {e['segment']}\n")
                f.write(f"- **语境**: {e['context_type']}\n")
                f.write(f"- **匹配关键词**: `{e['matched_keyword']}`\n")
                f.write(f"- **语义桶**: {e['semantic_buckets']}\n\n")
                if e.get("sentiment") and e["sentiment"] != "0.0":
                    f.write(f"- **情感分数**: {e['sentiment']}\n\n")
                f.write(f"> {e['content'][:500]}\n\n")
                if len(e['content']) > 500:
                    f.write(f"> *(内容过长已截断，全文 {len(e['content'])} 字符)*\n\n")

        f.write("\n---\n\n")
        f.write("*本报告由 transcript_analyzer.py 自动生成。每条信号均可追溯至原文。*\n")


# ─── 主入口 ──────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="业绩会逐字稿信号挖掘工具")
    parser.add_argument("--symbol", required=True, help="股票代码，如 PM, LMT")
    parser.add_argument("--quarters", required=True,
                        help="季度列表，逗号分隔，如 2025Q4,2025Q3")
    parser.add_argument("--mode", default="web", choices=["web", "api"],
                        help="数据源: web=Stock Analysis(推荐/免费), api=QVeris(2credits/次)")
    parser.add_argument("--output-dir", default=".",
                        help="输出目录（默认当前目录）")
    args = parser.parse_args()

    symbol = args.symbol.upper()
    quarters = [q.strip() for q in args.quarters.split(",")]
    outdir = args.output_dir
    os.makedirs(outdir, exist_ok=True)

    mode_name = "Stock Analysis (免费)" if args.mode == "web" else "QVeris API"
    print(f"=> 开始分析 {symbol} ...")
    print(f"   数据源: {mode_name}")
    print(f"   覆盖季度: {quarters}")
    print(f"   输出目录: {os.path.abspath(outdir)}")

    # 按模式选择 fetch 函数
    fetch_fn = stockanalysis_fetch if args.mode == "web" else qveris_fetch

    all_evidences = []
    total_words_map = {}

    for q in quarters:
        print(f"\n  [获取] {q} transcript ...")
        try:
            data = fetch_fn(symbol, q)
        except Exception as e:
            print(f"  [失败] {q}: {e}")
            print(f"  [提示] 试试 --mode api 用 QVeris API 获取")
            continue

        transcript = data.get("transcript", [])
        if not transcript:
            print(f"  [警告] {q} 无 transcript 数据")
            continue

        print(f"     -> 获取成功: {len(transcript)} 段说话内容")
        evidences, total_words = analyze_transcript(symbol, q, transcript)
        total_words_map[(symbol, q)] = total_words
        all_evidences.extend(evidences)
        print(f"     -> 提取 {len(evidences)} 条信号")

    if not all_evidences:
        print("\n[错误] 未提取到任何信号，请检查数据")
        return

    # 生成输出
    print(f"\n  [生成] 分析报告 ...")

    ledger_path = os.path.join(outdir, f"{symbol}_evidence_ledger.csv")
    write_evidence_ledger(all_evidences, ledger_path)
    print(f"     -> evidence_ledger.csv ({len(all_evidences)} 行)")

    theme_rows = compute_theme_timeseries(all_evidences, total_words_map)
    ts_path = os.path.join(outdir, f"{symbol}_theme_timeseries.csv")
    write_theme_timeseries(theme_rows, ts_path)
    print(f"     -> theme_timeseries.csv ({len(theme_rows)} 行)")

    report_path = os.path.join(outdir, f"{symbol}_summary_report.md")
    write_summary_report(symbol, quarters, all_evidences, theme_rows, args.mode, report_path)
    print(f"     -> summary_report.md")

    print(f"\n[完成] 共提取 {len(all_evidences)} 条信号，覆盖 {len(quarters)} 个季度。")
    print(f"   输出文件:")
    print(f"     {ledger_path}")
    print(f"     {ts_path}")
    print(f"     {report_path}")


if __name__ == "__main__":
    main()
