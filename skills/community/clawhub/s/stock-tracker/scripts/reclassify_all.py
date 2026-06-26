#!/usr/bin/env python3
"""重新分类所有公告 - 清空旧 tag/category，用修复后的 Prompt 逐条重判

用法:
    python scripts/reclassify_all.py --dry-run   # 预览影响范围
    python scripts/reclassify_all.py              # 执行重分类
"""

import argparse
import logging
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db
from llm_judge import LLMJudge

logger = logging.getLogger("reclassify_all")


def _detect_market(stock_code: str, ann_type: str) -> str:
    import re
    if ann_type == "H":
        return "港股"
    if re.match(r"^(60\d{4}|00\d{4}|30\d{4}|688\d{3})$", stock_code):
        return "A股"
    if re.match(r"^\d{4,5}$", stock_code):
        return "港股"
    return "A股"


def get_all_records():
    conn = db._get_conn()
    try:
        rows = conn.execute(
            "SELECT ann_id, stock_code, stock_name, title, ann_type "
            "FROM announcements WHERE title IS NOT NULL AND title != ''"
        ).fetchall()
        return [
            {"ann_id": r[0], "stock_code": r[1], "stock_name": r[2], "title": r[3], "ann_type": r[4]}
            for r in rows
        ]
    finally:
        conn.close()


def clear_all_tags():
    conn = db._get_conn()
    try:
        conn.execute("UPDATE announcements SET ann_type_tag = '', ann_type_category = ''")
        conn.commit()
        logger.info("已清空所有 ann_type_tag 和 ann_type_category")
    finally:
        conn.close()


def update_single(conn, ann_id: str, tag: str, category: str):
    conn.execute(
        "UPDATE announcements SET ann_type_tag = ?, ann_type_category = ? WHERE ann_id = ?",
        (tag, category, ann_id),
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="只预览，不执行")
    parser.add_argument("--delay", type=float, default=0.5, help="每条请求间隔(秒)")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    records = get_all_records()
    total = len(records)
    logger.info("共 %d 条公告需要重新分类", total)

    if args.dry_run:
        logger.info("dry-run 模式，仅预览前 10 条:")
        for r in records[:10]:
            market = _detect_market(r["stock_code"], r["ann_type"] or "")
            logger.info("  [%s] %s - %s (%s)", market, r["stock_name"], r["title"][:50], r["ann_id"][:8])
        return

    # 加载 config.json 中的 LLM 配置（包含正确的 base_url）
    import json as _json
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = _json.load(f)
    else:
        config = {"llm": {"enabled": True}}
    judge = LLMJudge.from_config(config)
    if not judge.enabled:
        logger.error("LLM 未启用，请检查 .env 中的 LLM_API_KEY")
        sys.exit(1)

    # 清空旧标签
    clear_all_tags()

    conn = db._get_conn()
    try:
        updated = 0
        errors = 0
        for i, rec in enumerate(records, 1):
            market = _detect_market(rec["stock_code"], rec["ann_type"] or "")
            try:
                result = judge.judge(rec["title"], rec["stock_name"], market)
                tag = result.get("type", "个股其他公告")
                category = result.get("category", "")
                if not category:
                    from llm_judge import _get_category
                    category = _get_category(market, tag)

                update_single(conn, rec["ann_id"], tag, category)
                updated += 1

                if i % 10 == 0:
                    conn.commit()
                    logger.info("进度: %d/%d", i, total)

            except Exception as e:
                logger.warning("[%d/%d] 判断失败 %s: %s", i, total, rec["ann_id"][:8], e)
                errors += 1

            if i < total:
                time.sleep(args.delay)

        conn.commit()
        logger.info("=" * 50)
        logger.info("重分类完成: 成功 %d/%d, 失败 %d", updated, total, errors)
        logger.info("LLM 统计: %s", judge.report())
    finally:
        conn.close()


if __name__ == "__main__":
    main()
