#!/usr/bin/env python3
"""每日公告摘要脚本

为没有摘要的公告生成单条摘要，存入 DB 的 summary 字段。
--digest 可输出有价值公告的摘要列表（供 agent 读取 stdout 转发）。

用法:
    python scripts/daily_summary.py                  # 为未摘要的公告生成摘要
    python scripts/daily_summary.py --hours 12       # 只处理最近12小时入库的公告
    python scripts/daily_summary.py --group test     # 只处理 test 板块
    python scripts/daily_summary.py --digest         # 输出有价值公告摘要列表
"""

import argparse
import json
import logging
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from datetime import datetime, timedelta

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db
from llm_judge import _load_env_key

logger = logging.getLogger("daily_summary")
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH_SIZE = 1  # 每批处理的公告数


def load_config() -> dict:
    path = os.path.join(SKILL_DIR, "config.json")
    default = {"notify": {"type": "terminal"}}
    if os.path.exists(path):
        try:
            with open(path) as f:
                default.update(json.load(f))
        except (OSError, json.JSONDecodeError):
            pass
    return default


def get_unsummarized_announcements(hours: int = None, stock_codes: list[str] = None) -> list[dict]:
    """获取没有摘要的公告"""
    conn = db._get_conn()
    try:
        sql = (
            "SELECT ann_id, stock_code, stock_name, title, ann_date, clean_text, ann_type_tag, ann_type_category "
            "FROM announcements WHERE (summary IS NULL OR summary = '') "
            "AND clean_text IS NOT NULL AND clean_text != ''"
        )
        params = []

        if hours:
            since = (datetime.now() - timedelta(hours=hours)).strftime("%Y-%m-%d %H:%M:%S")
            sql += " AND first_seen_at >= ?"
            params.append(since)

        if stock_codes:
            placeholders = ",".join("?" for _ in stock_codes)
            sql += f" AND stock_code IN ({placeholders})"
            params.extend(stock_codes)

        sql += " ORDER BY ann_date DESC"
        rows = conn.execute(sql, params).fetchall()
        return [
            {
                "ann_id": r[0], "stock_code": r[1], "stock_name": r[2],
                "title": r[3], "ann_date": r[4], "clean_text": r[5],
                "ann_type_tag": r[6] if len(r) > 6 else "",
                "ann_type_category": r[7] if len(r) > 7 else "",
            }
            for r in rows
        ]
    finally:
        conn.close()


# 不同公告类型的摘要提取重点
TYPE_FOCUS = {
    # 回购类
    "回购股权": "累计回购金额、回购股数、占总股本比例、回购计划总额及完成进度",
    # 人事变动
    "人事变动": "具体人名、原职务、新职务、变动原因",
    # 业绩类
    "业绩预告": "预计营收/利润数字、同比增减幅度、业绩变动原因",
    "业绩快报": "实际营收/利润数字、同比增减、与前期预告的差异",
    # 资本运作
    "收购兼并": "交易标的名称、交易金额、交易对手、收购目的、标的公司主营业务及所在行业、标的估值及溢价率",
    "资产重组": "重组标的名称、交易金额、交易对手、重组方式、标的公司主营业务及所在行业、重组后对公司业务布局的影响",
    "重大合同": "合同金额、合同对手方、合同期限、合同内容、付款方式及条件、合同履行对当年营收/利润的影响、违约风险",
    "配股预案": "配股比例（几配几）、配股价格、募集资金总额、配股目的及资金用途、对每股收益的摊薄影响",
    "配股说明书": "配股比例、配股价格、募集资金用途、配股条件、对现有股东的影响",
    "配股获准": "获准日期、配股方案关键条款、后续时间安排",
    "配股发行": "实际发行股数、实际募集资金、发行结果、上市日期",
    "配股上市": "上市日期、配股价、对股价的影响",
    "增发预案": "增发原因及资金需求、增发股数及价格、募集资金总额及投向、发行对象（公开/定向）、对每股收益的摊薄影响",
    "增发说明书": "增发方案详情、募集资金用途、发行条件、风险因素",
    "增发获准": "获准日期、方案关键条款、后续安排",
    "增发发行": "实际发行股数、实际募集资金、发行价格、发行结果",
    "增发上市": "上市日期、对股价的影响",
    "利润分配": "每股分红金额、分红总额、股权登记日、除权除息日",
    # 股权激励
    "股权激励": "授予/行权价格、激励对象人数及构成、限售期及解锁条件、业绩考核目标、股权激励总量占股本比例",
    "员工持股": "持股计划规模、参与人数、股票来源、锁定期、业绩考核条件",
    # 关联交易
    "关联交易": "交易对方（关联方关系）、交易金额、定价依据及公允性、交易目的及必要性、对上市公司独立性的影响",
    # 股权变动
    "权益变动": "变动主体、变动前持股数量及比例、变动股数、变动后持股比例、变动方式（二级市场/协议转让等）",
    "股份增减持": "增减持主体、变动前持股数量及比例、增减持股数、增减持金额、变动后持股比例、增减持原因及后续计划",
    "质押冻结": "质押/冻结主体、质押股数、占持股比例、质权人、质押融资用途、平仓风险",
    # 诉讼/风险
    "法律纠纷": "原告被告、涉案金额、诉讼进展、判决结果、对公司财务的潜在影响",
    "风险提示": "风险类型、风险内容、可能影响、应对措施",
    "澄清公告": "澄清事项、市场传闻内容、事实情况、对股价影响",
    # 交易提示
    "停牌提示": "停牌原因、预计停牌时间、复牌条件",
    "交易异动": "异动类型（涨停/跌停/换手率）、异动原因、是否需核查",
    "特别处理": "ST/ST*原因、风险警示内容、可能后果",
    "终止上市": "终止原因、退市整理期、投资者保护措施",
    "恢复上市": "恢复上市原因、复牌后交易安排、公司当前经营状况",
    "暂停上市": "暂停上市原因、后续恢复条件、投资者风险提示",
    # 借贷/担保
    "借贷担保": "担保金额、担保对象、被担保方财务状况、担保期限、反担保措施",
    "委托理财": "理财金额、产品类型、预期收益率、期限、风险等级",
    # 股权股本
    "股本变动": "变动原因、变动前后股本结构、新增股份性质",
    "质押式回购": "回购主体、回购金额、质押标的、期限、到期安排",
    "约定购回": "购回主体、购回金额、标的证券、期限、购回价格",
    "股权分置改革": "改革方案概要、对价安排、流通股与非流通股比例变化",
    # 一般公告
    "机构调研公告": "调研机构名单、调研时间、公司回复要点、投资者关注的核心问题",
    "董事会公告": "议案内容、表决结果、重大决议",
    "资金投向": "投资项目、投资金额、预期收益、资金来源、项目实施周期",
    "违纪违规": "违规主体、违规事项、处罚措施、整改方案",
    "政策影响": "政策内容、对公司业务的具体影响、公司应对措施",
    "ESG报告": "环境/社会/治理关键指标、评级变化、重要披露事项",
    "产销经营快报": "主要产品产销量、同比变化、经营亮点、行业景气度",
    # 港股特有类型
    "供股": "供股比例（几供几）、供股价格、募集资金总额、供股目的及资金用途、对现有股东的影响",
    "发售以供认购": "发售价格、发售数量、集资额、认购安排、对股价影响",
    "公开招股": "招股价格区间、招股数量、集资额、上市日期、保荐人",
    "发售现有证券": "出售股东身份、发售股数、售价、较市价折让幅度、出售原因",
    "资本化发行": "发行方式、发行对象、对股本结构的影响、是否涉及大股东",
    "介绍上市": "介绍上市方式、不涉及公开发售的原因、上市日期、保荐人",
    "新上市": "新上市公司名称、主营业务及行业、发行规模及定价、集资用途、上市后表现预期",
    "须公布的交易": "交易性质（收购/出售/合营）、交易金额、交易对手、是否构成重大交易、对财务状况的影响",
    "交易安排": "关键日期（除净日、过户截止日、派息日）、每股派息金额",
    "翌日报表": "买入/卖出股数、成交价格、涉及股东名称及身份",
    "月报表": "月度股份变动汇总、各增减持主体及股数、变动后持股比例",
    "权证公告": "权证标的证券、行权价格、到期日、杠杆比率、实际杠杆",
    "权证上市": "权证条款（标的/行权价/到期日）、上市日期、初始价格",
    "债务证券公告": "债券规模、票面利率、期限、信用评级、担保情况、募集资金用途",
    "监管者公告": "监管机构名称、监管事项、处罚/警告措施、对公司经营的影响",
}


def build_summary_prompt(announcements: list[dict]) -> str:
    """构建批量摘要 prompt"""
    lines = [
        "你是专业的财经分析师。请为以下每条公告生成一段精炼但信息完整的摘要。",
        "",
        "摘要要求（按优先级严格执行）：",
        "1. 必须严格按照每条公告标注的'重点关注'列表逐条提取，不得省略任何一项",
        "2. 每个重点必须配合正文中的具体数字呈现（金额、比例、股数、日期等），禁止泛泛而谈",
        "3. 如果正文中没有某个重点的数据，明确标注'未披露'，不要跳过",
        "4. 在包含所有重点的前提下，语言尽量简练，但绝不以省略关键信息为代价",
        "",
        "请严格按照以下 JSON 格式返回，不要添加其他内容：",
        '[{"ann_id": "xxx", "summary": "摘要内容"}, ...]',
        "",
        "--- 公告列表 ---",
        "",
    ]

    for i, ann in enumerate(announcements):
        text = ann.get("clean_text", "")[:3000]
        tag = ann.get("ann_type_tag", "")
        category = ann.get("ann_type_category", "")
        type_display = f"{category}-{tag}" if category else tag
        focus = TYPE_FOCUS.get(tag, "公告核心内容和关键数字")
        lines.append(f"[{i+1}] ann_id={ann['ann_id']}")
        lines.append(f"    股票: {ann['stock_name']}({ann['stock_code']})")
        lines.append(f"    标题: {ann['title']}")
        lines.append(f"    类型: {type_display}（重点关注：{focus}）")
        if text:
            lines.append(f"    正文: {text}")
        lines.append("")

    return "\n".join(lines)


def call_llm(prompt: str, max_tokens: int = 10000, json_mode: bool = False, retries: int = 2) -> str:
    """调用 LLM"""
    api_key = _load_env_key("LLM_API_KEY")
    if not api_key:
        logger.warning("LLM_API_KEY 未配置")
        return ""

    config = load_config()
    llm_cfg = config.get("llm", {})
    base_url = llm_cfg.get("base_url", "https://opencode.ai/zen/go/v1")
    model = llm_cfg.get("model", "deepseek-v4-flash")
    timeout = llm_cfg.get("timeout", 60)

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": max_tokens,
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}

    for attempt in range(retries + 1):
        try:
            resp = requests.post(
                f"{base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=timeout,
            )
            resp.raise_for_status()
            msg = resp.json()["choices"][0]["message"]
            # 推理模型可能把输出放在 reasoning_content 而非 content
            content = msg.get("content") or msg.get("reasoning_content") or ""
            return content
        except (requests.RequestException, json.JSONDecodeError) as e:
            logger.warning("LLM 调用失败 (attempt %d/%d): %s", attempt + 1, retries + 1, e)
            if attempt < retries:
                time.sleep((attempt + 1) * 2)
            continue

    logger.error("LLM 调用全部失败")
    return ""


def _clean_llm_json(text: str) -> str:
    """清洗 LLM 返回的 JSON，修复常见污染"""
    text = re.sub(r"^```json\s*", "", text.strip(), flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text.strip())
    text = text.lstrip("\ufeff")
    text = re.sub(r"[\u200b-\u200f\ufeff]", "", text)
    return text


def parse_summaries(text: str) -> dict[str, str]:
    """从 LLM 响应中解析摘要 JSON"""
    text = _clean_llm_json(text)

    # 尝试 1：直接提取 JSON 数组
    try:
        start = text.find("[")
        end = text.rfind("]") + 1
        if start >= 0 and end > start:
            items = json.loads(text[start:end])
            return {item["ann_id"]: item["summary"] for item in items if "ann_id" in item and "summary" in item}
    except (json.JSONDecodeError, KeyError):
        pass

    # 尝试 2：修复 summary 字段中未转义的嵌套双引号后再解析
    try:
        start = text.find("[")
        end = text.rfind("]") + 1
        if start >= 0 and end > start:
            raw = text[start:end]
            fixed = re.sub(
                r'("summary"\s*:\s*"[^"]*)"([^"]*)"([^"]*")',
                lambda m: m.group(1) + '\u201c' + m.group(2) + '\u201d' + m.group(3),
                raw,
            )
            items = json.loads(fixed)
            return {item["ann_id"]: item["summary"] for item in items if "ann_id" in item and "summary" in item}
    except (json.JSONDecodeError, KeyError):
        pass

    # 回退：逐行匹配 ann_id=xxx 格式
    result = {}
    current_id = None
    for line in text.split("\n"):
        id_match = re.search(r'ann_id[=:]\s*["\']?([a-f0-9]+)', line)
        if id_match:
            current_id = id_match.group(1)
        summary_match = re.search(r'summary[=:]\s*["\'](.+?)["\']', line)
        if summary_match and current_id:
            result[current_id] = summary_match.group(1)
            current_id = None
    return result


# 需要跳过 LLM 的类型（定期报告/财报类，正文太长且内容标准化）
SKIP_LLM_TYPES = {"业绩预告", "业绩快报", "季度报告", "半年报告", "年度报告", "补充更正"}


def generate_summaries(announcements: list[dict], max_workers: int = 5) -> int:
    """批量生成公告摘要并存入 DB，返回成功数量"""
    total = 0

    # Phase 1: 分离需要 LLM 的 和 可以直接写固定摘要的
    llm_anns = []
    for ann in announcements:
        tag = ann.get("ann_type_tag", "")
        if tag in SKIP_LLM_TYPES:
            fixed = f"【{tag}】{ann['title']}"
            db.update_summary(ann["ann_id"], fixed)
            total += 1
            logger.info("跳过 LLM: %s %s -> %s", ann["stock_name"], tag, ann["title"][:40])
        else:
            llm_anns.append(ann)

    if not llm_anns:
        return total

    # Phase 2: 并发调用 LLM 生成摘要
    batches = [llm_anns[i:i + BATCH_SIZE] for i in range(0, len(llm_anns), BATCH_SIZE)]
    logger.info("LLM 并发生成摘要: %d 条公告, %d 批 (workers=%d)", len(llm_anns), len(batches), max_workers)

    batch_results = []   # [(batch, summaries_dict), ...]

    def _process_batch(batch):
        prompt = build_summary_prompt(batch)
        response = call_llm(prompt, max_tokens=10000, json_mode=True)
        if not response:
            return batch, {}
        summaries = parse_summaries(response)
        if not summaries:
            logger.warning("解析失败，LLM 返回前 500 字: %s", response[:500])
        return batch, summaries

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_process_batch, b): b for b in batches}
        for future in as_completed(futures):
            batch, summaries = future.result()
            batch_results.append((batch, summaries))
            logger.info("  批次完成 (%d/%d)", len(batch_results), len(batches))

    # Phase 3: 顺序保存到数据库
    failed = []
    for batch, summaries in batch_results:
        for ann in batch:
            summary = summaries.get(ann["ann_id"], "")
            if summary:
                db.update_summary(ann["ann_id"], summary)
                total += 1
            else:
                failed.append(ann)

    if failed:
        logger.warning("--- 摘要生成失败 %d 条 ---", len(failed))
        for ann in failed:
            logger.warning("  %s(%s) %s", ann.get("stock_name", ""), ann.get("stock_code", ""), ann.get("title", ""))
            if ann.get("url"):
                logger.warning("    %s", ann["url"])

    return total


def format_digest(announcements: list[dict]) -> str:
    """将有摘要的公告格式化为编号列表，供 agent 读取 stdout 转发"""
    if not announcements:
        return ""

    lines = [f"DIGEST_TOTAL:{len(announcements)}"]
    for i, ann in enumerate(announcements, 1):
        code = ann["stock_code"]
        name = ann.get("stock_name", "")
        title = ann.get("title", "")
        summary = ann.get("summary", "")
        lines.append(f"{i}.")
        lines.append(f"【{code}{name}】-【{title}】")
        lines.append(summary)
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="每日公告摘要")
    parser.add_argument("--hours", type=int, default=None, help="回溯小时数（不指定则处理所有未摘要的公告）")
    parser.add_argument("--group", default=None, help="只处理指定分组")
    parser.add_argument("--digest", action="store_true", help="输出过去24小时有价值公告摘要列表")
    parser.add_argument("--workers", type=int, default=20, help="LLM 并发数（默认 20）")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 获取分组的股票代码
    stock_codes = None
    if args.group:
        from eastmoney_api import get_stocks
        cookie_path = os.path.join(SKILL_DIR, "cookie.txt")
        group_stocks = get_stocks(cookie_path, group_name=args.group)
        if group_stocks:
            stock_codes = [s["code"] for s in group_stocks]
            logger.info("分组 [%s]: %d 只股票", args.group, len(stock_codes))
        else:
            logger.warning("分组 [%s] 未获取到股票", args.group)

    # 第一步：为没有摘要的公告生成单条摘要
    unsummarized = get_unsummarized_announcements(hours=args.hours, stock_codes=stock_codes)
    if unsummarized:
        logger.info("发现 %d 条未摘要的公告，开始生成...", len(unsummarized))
        count = generate_summaries(unsummarized, max_workers=args.workers)
        logger.info("摘要生成完成：成功 %d/%d 条", count, len(unsummarized))
    else:
        logger.info("所有公告已有摘要，跳过生成")

    # 第二步（可选）：输出有价值公告摘要列表
    if args.digest:
        days = min(args.hours // 24 + 1, 7) if args.hours else 1
        anns = db.get_announcements_with_summary(stock_codes=stock_codes, days=days)

        if anns:
            digest = format_digest(anns)
            print(digest)
            logger.info("Digest: %d 条有价值公告", len(anns))
        else:
            group_hint = f"{args.group}板块" if args.group else ""
            print(f"DIGEST_EMPTY:最近{days}天{group_hint}无高价值公告")
            logger.info("Digest: 无有价值公告摘要")


if __name__ == "__main__":
    main()
