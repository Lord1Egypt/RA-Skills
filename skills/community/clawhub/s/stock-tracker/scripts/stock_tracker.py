#!/usr/bin/env python3
"""东方财富自选股公告追踪 - 主脚本

每天定时运行，自动抓取自选股的最新公告，增量推送新公告。

支持两个数据来源:
  - eastmoney: 从东方财富获取公告列表（默认，支持 A 股+港股）
  - cninfo:    A 股从巨潮资讯网获取，港股从东方财富获取（推荐，PDF 更稳定）

用法:
    python stock_tracker.py                     # 正常运行（东方财富）
    python stock_tracker.py --source cninfo      # 从巨潮资讯网获取
    python stock_tracker.py --force              # 强制重新抓取所有公告
    python stock_tracker.py --days 14            # 抓取最近14天的公告
    python stock_tracker.py --dry-run            # 试运行（不更新状态）
    python stock_tracker.py --stats              # 查看数据库统计
    python stock_tracker.py --list               # 列出最近公告
    python stock_tracker.py --list --stock 600519 # 列出某只股票的历史公告
    python stock_tracker.py --fetch-content      # 补抓缺少全文的公告正文
    python stock_tracker.py --prune               # 清理无正文的空记录
    python stock_tracker.py --group 持仓 --fetch-content  # 抓取持仓分组公告并获取全文
"""

import argparse
import json
import logging
import logging.handlers
import os
import shutil
import sys
from datetime import datetime

import db
from ann_detail import fetch_all_contents
from cninfo_api import fetch_all_cninfo
from eastmoney_api import get_stocks, get_groups, fetch_all_announcements, load_cookie
from llm_judge import LLMJudge
from text_cleaner import clean_announcement_text

logger = logging.getLogger("stock_tracker")

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CONFIG = os.path.join(SKILL_DIR, "config.json")
DEFAULT_COOKIE = os.path.join(SKILL_DIR, "cookie.txt")
DEFAULT_LOG_DIR = os.path.join(SKILL_DIR, "logs")


_LOGGING_INITIALIZED = False


def setup_logging(log_dir: str = DEFAULT_LOG_DIR):
    global _LOGGING_INITIALIZED
    if _LOGGING_INITIALIZED:
        return

    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(
        log_dir, f"stock_tracker_{datetime.now().strftime('%Y%m%d')}.log"
    )
    fmt = logging.Formatter(
        "[%(asctime)s] %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    console = logging.StreamHandler(sys.stderr)
    console.setFormatter(fmt)
    root.addHandler(console)

    fh = logging.handlers.TimedRotatingFileHandler(
        log_file, when="midnight", interval=1, backupCount=30, encoding="utf-8"
    )
    fh.setFormatter(fmt)
    root.addHandler(fh)

    _LOGGING_INITIALIZED = True


def load_config(path: str = DEFAULT_CONFIG) -> dict:
    default = {
        "notify": {"type": "terminal"},
        "fetch_interval_days": 7,
    }
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                cfg = json.load(f)
            default.update(cfg)
        except (json.JSONDecodeError, OSError) as e:
            logger.warning("配置文件加载失败: %s", e)
    return default


def send_notification(config: dict, new_anns: list[dict]):
    notify_type = config.get("notify", {}).get("type", "terminal")
    if notify_type == "terminal":
        _notify_terminal(new_anns)
    elif notify_type == "webhook":
        _notify_webhook(config["notify"], new_anns)
    else:
        _notify_terminal(new_anns)


def _notify_terminal(new_anns: list[dict]):
    if not new_anns:
        return
    logger.info("发现 %d 条新公告（已入库）", len(new_anns))


def _notify_webhook(notify_cfg: dict, new_anns: list[dict]):
    import requests as req

    url = notify_cfg.get("webhook_url", "")
    if not url:
        logger.warning("Webhook URL 未配置")
        return

    lines = [f"📢 自选股公告追踪报告 ({(datetime.now().strftime('%Y-%m-%d %H:%M'))})"]
    lines.append(f"共 {len(new_anns)} 条新公告\n")
    for ann in new_anns:
        lines.append(
            f"【{ann['stock_name']}({ann['stock_code']})】"
            f"{ann['title']} "
            f"[{ann['ann_date']}]"
        )

    text = "\n".join(lines)
    payload = {"msgtype": "text", "text": {"content": text[:4096]}}

    try:
        resp = req.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        logger.info("Webhook 通知发送成功")
    except (req.RequestException, OSError) as e:
        logger.warning("Webhook 通知发送失败: %s", e)


def run(args=None):
    parser = argparse.ArgumentParser(description="东方财富自选股公告追踪")
    parser.add_argument("--force", action="store_true", help="强制重新抓取所有公告")
    parser.add_argument("--days", type=int, default=None, help="抓取最近N天的公告")
    parser.add_argument("--dry-run", action="store_true", help="试运行（不更新状态）")
    parser.add_argument("--config", default=DEFAULT_CONFIG, help="配置文件路径")
    parser.add_argument("--group", "-g", default=None, help="只追踪指定分组（模糊匹配，如 持仓/hk/自选）")
    parser.add_argument("--list-groups", action="store_true", help="列出所有可用分组")
    parser.add_argument("--stats", action="store_true", help="查看数据库统计信息")
    parser.add_argument("--list", action="store_true", help="列出历史公告")
    parser.add_argument("--stock", default=None, help="配合 --list 使用，筛选指定股票代码")
    parser.add_argument("--fetch-content", action="store_true", help="获取公告全文并存入数据库")
    parser.add_argument("--clean", action="store_true", help="清洗已获取的公告正文（移除模板套话）")
    parser.add_argument("--prune", action="store_true", help="清理无正文的空记录")
    parser.add_argument("--source", choices=["eastmoney", "cninfo"], default="eastmoney",
                        help="数据来源: eastmoney（东方财富，A股+港股）或 cninfo（巨潮A股+东方财富港股，推荐）")
    parsed = parser.parse_args(args)

    setup_logging()

    # 自动备份数据库（保留上一次的快照）
    if os.path.exists(db.DB_PATH) and not parsed.stats and not parsed.list and not parsed.list_groups:
        bak_path = db.DB_PATH + ".bak"
        try:
            shutil.copy2(db.DB_PATH, bak_path)
            logger.debug("数据库已备份: %s", bak_path)
        except OSError as e:
            logger.warning("数据库备份失败: %s", e)

    if parsed.stats:
        stats = db.get_stats()
        print(f"\n数据库统计:")
        print(f"  总公告数: {stats['total']}")
        pct = (stats['with_content'] / stats['total'] * 100) if stats['total'] else 0
        print(f"  含正文: {stats['with_content']} ({pct:.1f}%)")
        print(f"  追踪股票数: {stats['stocks_tracked']}")
        print(f"  最后更新: {stats['latest_update']}")
        print(f"  数据库路径: {db.DB_PATH}")

        east_total = db._count_by_source("eastmoney")
        cninfo_total = db._count_by_source("cninfo")
        print(f"  来源: 东方财富 {east_total} 条 / 巨潮资讯 {cninfo_total} 条")

        need_clean = len(db.get_records_needing_clean())
        if need_clean:
            print(f"  待清洗: {need_clean} 条（运行 --clean 清洗）")
        need_content = len(db.get_pending_content())
        if need_content:
            print(f"  待采集全文: {need_content} 条（运行 --fetch-content 采集）")
        return

    if parsed.clean:
        pending = db.get_records_needing_clean()
        if not pending:
            logger.info("所有公告正文已清洗，无需处理")
        else:
            logger.info("正在清洗 %d 条公告正文...", len(pending))
            total_orig = 0
            total_clean = 0
            for ann in pending:
                raw_text = ann.get("full_text", "")
                if not raw_text:
                    continue
                cleaned = clean_announcement_text(raw_text)
                ann["clean_text"] = cleaned
                total_orig += len(raw_text)
                total_clean += len(cleaned)
            db.update_clean_text(pending)
            saved_pct = ((total_orig - total_clean) / total_orig * 100) if total_orig else 0
            logger.info("清洗完成: %d 条, %s → %s 字 (节省 %.1f%%)",
                        len(pending), f"{total_orig:,}", f"{total_clean:,}", saved_pct)
        return

    if parsed.prune:
        deleted = db.prune_empty()
        logger.info("清理完成，删除了 %d 条记录", deleted)
        return

    if parsed.list:
        days = parsed.days or 30
        # 如果指定了 --group，先获取该分组的股票代码列表用于过滤
        stock_codes = None
        if parsed.group:
            group_stocks = get_stocks(DEFAULT_COOKIE, group_name=parsed.group)
            if group_stocks:
                stock_codes = [s["code"] for s in group_stocks]
                logger.info("分组 [%s] 包含 %d 只股票", parsed.group, len(stock_codes))
            else:
                logger.warning("分组 [%s] 未获取到股票", parsed.group)
        anns = db.list_announcements(stock_code=parsed.stock, stock_codes=stock_codes, days=days)
        if not anns:
            print("暂无公告记录")
            return
        print(f"\n最近 {days} 天公告记录 ({len(anns)} 条):")
        print("-" * 80)
        for i, ann in enumerate(anns, 1):
            print(f"\n  {i}. {ann['stock_name']} ({ann['stock_code']})  [{ann['ann_date']}]")
            print(f"     {ann['title']}")
            print(f"     类型: {ann['ann_type']} | 首次发现: {ann['first_seen_at']}")
            print(f"     {ann['url']}")
        print("-" * 80)
        return

    if parsed.list_groups:
        cookie = load_cookie(DEFAULT_COOKIE)
        if not cookie:
            logger.error("需要 cookie.txt 才能获取分组列表")
            sys.exit(1)
        groups = get_groups(cookie)
        if groups:
            logger.info("可用分组:")
            for g in groups:
                logger.info("  gid=%s  gname=%s", g.get("gid"), g.get("gname"))
        else:
            logger.warning("未获取到分组列表")
        return

    config = load_config(parsed.config)
    llm_judge = LLMJudge.from_config(config)
    days = parsed.days or config.get("fetch_interval_days", 7)

    if parsed.fetch_content:
        pending = db.get_pending_content()
        if not pending:
            logger.info("数据库中没有待获取全文的公告")
        else:
            logger.info("正在补抓 %d 条缺少全文的公告（分批保存）...", len(pending))
            fetch_all_contents(pending, save_batch=db.update_content, batch_size=10, llm_judge=llm_judge)
            stats = db.get_stats()
            logger.info("全文获取完成（数据库共 %d 条，含正文 %d 条）",
                        stats["total"], stats["with_content"])
            if llm_judge.enabled:
                logger.info(llm_judge.report())
        db.prune_empty()
        if not parsed.group:
            return

    logger.info("=" * 50)
    logger.info("自选股公告追踪 - 开始运行")
    logger.info("=" * 50)
    logger.info("数据来源: %s", "巨潮+A股 / 东方财富+港股" if parsed.source == "cninfo" else "东方财富")
    logger.info("抓取窗口: 最近 %d 天", days)
    if parsed.group:
        logger.info("筛选分组: %s", parsed.group)

    cookie = load_cookie(DEFAULT_COOKIE)
    stocks = get_stocks(DEFAULT_COOKIE, group_name=parsed.group)
    if not stocks:
        logger.error("未获取到自选股列表，请检查 cookie.txt 或 config.json")
        sys.exit(1)

    logger.info("自选股共 %d 只:", len(stocks))
    for s in stocks:
        logger.info("  - %s (%s)", s["name"], s["code"])

    if parsed.source == "cninfo":
        a_stocks = [s for s in stocks if s.get("market") in ("0", "1")]
        hk_stocks = [s for s in stocks if s.get("market") == "116"]
        anns = []
        if a_stocks:
            logger.info("A 股 %d 只 -> 巨潮资讯网", len(a_stocks))
            anns.extend(fetch_all_cninfo(a_stocks, days_back=days))
        if hk_stocks:
            logger.info("港股 %d 只 -> 东方财富", len(hk_stocks))
            anns.extend(fetch_all_announcements(hk_stocks, cookie, days_back=days))
    else:
        anns = fetch_all_announcements(stocks, cookie, days_back=days)
    logger.info("共获取 %d 条公告", len(anns))

    seen_ids = db.get_seen_ids() if not parsed.force else set()

    new_anns = []
    for ann in anns:
        ann_id = db.make_ann_id(ann)
        if ann_id not in seen_ids:
            new_anns.append(ann)

    if new_anns:
        logger.info("发现 %d 条新公告！", len(new_anns))
        send_notification(config, new_anns)
    else:
        logger.info("暂无新公告")

    anns_to_save = anns if parsed.force else new_anns
    if not parsed.dry_run and anns_to_save:
        # 先获取全文（fetch_all_contents 会修改 ann 的 full_text）
        # 然后再根据 full_text 判断 status
        if parsed.fetch_content:
            logger.info("正在获取 %d 条新公告的全文...", len(anns_to_save))
            fetch_all_contents(anns_to_save, save_batch=db.update_content, batch_size=10, llm_judge=llm_judge)

        # 根据最终的 full_text 判断 status
        for ann in anns_to_save:
            ann["status"] = "valuable" if ann.get("full_text") else "filtered"
        valuable_count = sum(1 for a in anns_to_save if a["status"] == "valuable")
        filtered_count = len(anns_to_save) - valuable_count
        if filtered_count:
            logger.info("%d 条有价值 / %d 条已过滤", valuable_count, filtered_count)
        db.record_announcements(anns_to_save)
        stats = db.get_stats()
        logger.info("状态已保存（数据库共 %d 条，含正文 %d 条）",
                    stats["total"], stats["with_content"])
        if parsed.fetch_content and llm_judge.enabled:
            logger.info(llm_judge.report())
    elif not parsed.dry_run and not anns_to_save:
        stats = db.get_stats()
        logger.info("状态已保存（数据库共 %d 条，含正文 %d 条）",
                    stats["total"], stats["with_content"])

    logger.info("运行完成\n")


if __name__ == "__main__":
    run()
