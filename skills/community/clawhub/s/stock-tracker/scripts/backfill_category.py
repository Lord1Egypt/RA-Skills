#!/usr/bin/env python3
"""批量回填旧数据的 ann_type_category 字段

从现有 ann_type_tag 反查大类，更新数据库中 category 为空的记录。
"""

import logging
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db
from llm_judge import _get_category

logger = logging.getLogger("backfill_category")


def _detect_market(stock_code: str, ann_type: str) -> str:
    """根据股票代码判断市场类型"""
    if ann_type == "H":
        return "港股"
    # A股代码: 6位数字，以60/00/30/688开头
    if re.match(r"^(60\d{4}|00\d{4}|30\d{4}|688\d{3})$", stock_code):
        return "A股"
    # 港股代码: 4-5位数字
    if re.match(r"^\d{4,5}$", stock_code):
        return "港股"
    return "A股"  # 默认兜底


# 模糊关键词映射（处理 LLM 返回的简化标签）
A_KEYWORD_MAP = {
    "回购": "股权股本类",
    "担保": "重大事项类",
    "分红": "重大事项类",
    "利润分配": "重大事项类",
    "董事会决议": "一般公告类",
    "董事会公告": "一般公告类",
    "股份质押": "股权股本类",
    "提示": "交易提示类",
    "一般公告": "一般公告类",
    "债券": "一般公告类",
    "业绩": "财务报告类",
    "报告": "财务报告类",
    "预告": "财务报告类",
    "增发": "增发类",
    "配股": "配股类",
    "招股": "招股类",
    "上市": "上市文件",
    "权益变动": "股权股本类",
    "股本变动": "股权股本类",
    "股份增减持": "重大事项类",
    "资产重组": "重大事项类",
    "收购": "重大事项类",
    "重大合同": "重大事项类",
    "股权激励": "重大事项类",
    "关联交易": "重大事项类",
    "委托理财": "重大事项类",
    "人事变动": "重大事项类",
    "法律纠纷": "一般公告类",
    "机构调研": "一般公告类",
    "员工持股": "一般公告类",
    "产销经营": "一般公告类",
    "ESG": "一般公告类",
    "交易异动": "交易提示类",
    "澄清": "交易提示类",
    "停牌": "交易提示类",
    "终止上市": "交易提示类",
    "恢复上市": "交易提示类",
    "暂停上市": "交易提示类",
    "特别处理": "交易提示类",
    "月报表": "股权股本类",
    "翌日披露": "股权股本类",
}

HK_KEYWORD_MAP = {
    "月报表": "股权股本",
    "翌日披露": "股权股本",
    "权益变动": "股权股本",
    "交易披露": "股权股本",
    "证券": "股权股本",
    "股本": "股权股本",
    "业绩": "业绩快报",
    "报告": "财务报告",
    "预告": "业绩快报",
    "上市": "上市文件",
    "招股": "上市文件",
    "供股": "上市文件",
    "发售": "上市文件",
    "公开招股": "上市文件",
    "资本化": "上市文件",
    "介绍上市": "上市文件",
    "聆讯": "上市文件",
    "重大事项": "公告及通函",
    "新上市": "公告及通函",
    "会议": "公告及通函",
    "表决": "公告及通函",
    "关联交易": "公告及通函",
    "须公布的交易": "公告及通函",
    "公司变动": "公告及通函",
    "财务资料": "公告及通函",
    "交易安排": "一般公告",
    "监管者": "一般公告",
    "委任代表": "一般公告",
    "宪章": "一般公告",
    "权证": "债券及结构性产品",
    "债务证券": "债券及结构性产品",
}


def _fuzzy_get_category(market: str, tag: str) -> str:
    """模糊匹配大类，处理 LLM 返回的简化标签"""
    # 先尝试精确匹配
    exact = _get_category(market, tag)
    if exact not in ("一般公告类", "一般公告"):
        return exact

    # 模糊关键词匹配
    keyword_map = HK_KEYWORD_MAP if market == "港股" else A_KEYWORD_MAP
    for keyword, category in keyword_map.items():
        if keyword in tag:
            return category

    # 兜底：返回精确匹配结果（默认一般公告类）
    return exact


def backfill():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    conn = db._get_conn()
    try:
        cursor = conn.execute(
            "SELECT ann_id, stock_code, ann_type, ann_type_tag "
            "FROM announcements "
            "WHERE ann_type_tag IS NOT NULL AND ann_type_tag != ''"
        )
        rows = cursor.fetchall()
        if not rows:
            logger.info("没有需要回填的记录")
            return

        logger.info("发现 %d 条需要回填 category 的记录", len(rows))

        updated = 0
        skipped = 0
        for ann_id, stock_code, ann_type, tag in rows:
            market = _detect_market(stock_code, ann_type or "")
            category = _fuzzy_get_category(market, tag)
            if category:
                conn.execute(
                    "UPDATE announcements SET ann_type_category = ? WHERE ann_id = ?",
                    (category, ann_id),
                )
                updated += 1
            else:
                skipped += 1

        conn.commit()
        logger.info("回填完成: 更新 %d 条, 跳过 %d 条", updated, skipped)
    finally:
        conn.close()


if __name__ == "__main__":
    backfill()
