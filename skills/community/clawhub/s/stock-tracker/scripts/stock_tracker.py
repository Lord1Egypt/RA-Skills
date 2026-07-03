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
from typing import Any, Optional

from dependencies import get_db, get_llm_judge, get_text_cleaner, get_ann_detail, get_eastmoney_api, get_cninfo_api
from error_handler import DatabaseError, APIError, ConfigError, CookieError, DataError, handle_error, safe_execute
from config_manager import ConfigManager, AppConfig, NotifyConfig

db = get_db()
LLMJudge = get_llm_judge()
clean_announcement_text = get_text_cleaner()
ann_detail = get_ann_detail()
eastmoney_api = get_eastmoney_api()
cninfo_api = get_cninfo_api()

fetch_all_contents = ann_detail.fetch_all_contents
fetch_all_cninfo = cninfo_api.fetch_all_cninfo
get_stocks = eastmoney_api.get_stocks
get_groups = eastmoney_api.get_groups
fetch_all_announcements = eastmoney_api.fetch_all_announcements
load_cookie = eastmoney_api.load_cookie

logger: logging.Logger = logging.getLogger("stock_tracker")

SKILL_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CONFIG: str = os.path.join(SKILL_DIR, "config.json")
DEFAULT_COOKIE: str = os.path.join(SKILL_DIR, "cookie.txt")
DEFAULT_LOG_DIR: str = os.path.join(SKILL_DIR, "logs")


_LOGGING_INITIALIZED: bool = False


def setup_logging(log_dir: str = DEFAULT_LOG_DIR) -> None:
    global _LOGGING_INITIALIZED
    if _LOGGING_INITIALIZED:
        return

    os.makedirs(log_dir, exist_ok=True)
    log_file: str = os.path.join(
        log_dir, f"stock_tracker_{datetime.now().strftime('%Y%m%d')}.log"
    )
    fmt: logging.Formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    root: logging.Logger = logging.getLogger()
    root.setLevel(logging.INFO)

    console: logging.StreamHandler = logging.StreamHandler(sys.stderr)
    console.setFormatter(fmt)
    root.addHandler(console)

    fh: logging.handlers.TimedRotatingFileHandler = logging.handlers.TimedRotatingFileHandler(
        log_file, when="midnight", interval=1, backupCount=30, encoding="utf-8"
    )
    fh.setFormatter(fmt)
    root.addHandler(fh)

    _LOGGING_INITIALIZED = True


def send_notification(config: AppConfig, new_anns: list[dict[str, Any]]) -> None:
    notify_type: str = config.notify.type
    if notify_type == "terminal":
        _notify_terminal(new_anns)
    elif notify_type == "webhook":
        _notify_webhook(config.notify, new_anns)
    else:
        _notify_terminal(new_anns)


def _notify_terminal(new_anns: list[dict[str, Any]]) -> None:
    if not new_anns:
        return
    logger.info("发现 %d 条新公告（已入库）", len(new_anns))


def _notify_webhook(notify_cfg: NotifyConfig, new_anns: list[dict[str, Any]]) -> None:
    import requests as req

    url: str = notify_cfg.webhook_url
    if not url:
        logger.warning("Webhook URL 未配置")
        return

    lines: list[str] = [f"📢 自选股公告追踪报告 ({(datetime.now().strftime('%Y-%m-%d %H:%M'))})"]
    lines.append(f"共 {len(new_anns)} 条新公告\n")
    for ann in new_anns:
        lines.append(
            f"【{ann['stock_name']}({ann['stock_code']})】"
            f"{ann['title']} "
            f"[{ann['ann_date']}]"
        )

    text: str = "\n".join(lines)
    payload: dict[str, Any] = {"msgtype": "text", "text": {"content": text[:4096]}}

    try:
        resp = req.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        logger.info("Webhook 通知发送成功")
    except (req.RequestException, OSError) as e:
        logger.warning("Webhook 通知发送失败: %s", e)


def _backup_database() -> None:
    bak_path: str = db.DB_PATH + ".bak"
    try:
        shutil.copy2(db.DB_PATH, bak_path)
        logger.debug("数据库已备份: %s", bak_path)
    except OSError as e:
        logger.warning("数据库备份失败: %s", e)


def handle_stats() -> None:
    """处理 --stats 子命令：查看数据库统计信息"""
    stats: dict[str, Any] = db.get_stats()
    print(f"\n数据库统计:")
    print(f"  总公告数: {stats['total']}")
    pct: float = (stats['with_content'] / stats['total'] * 100) if stats['total'] else 0
    print(f"  含正文: {stats['with_content']} ({pct:.1f}%)")
    print(f"  追踪股票数: {stats['stocks_tracked']}")
    print(f"  最后更新: {stats['latest_update']}")
    print(f"  数据库路径: {db.DB_PATH}")

    east_total: int = db._count_by_source("eastmoney")
    cninfo_total: int = db._count_by_source("cninfo")
    print(f"  来源: 东方财富 {east_total} 条 / 巨潮资讯 {cninfo_total} 条")

    need_clean: int = len(db.get_records_needing_clean())
    if need_clean:
        print(f"  待清洗: {need_clean} 条（运行 --clean 清洗）")
    need_content: int = len(db.get_pending_content())
    if need_content:
        print(f"  待采集全文: {need_content} 条（运行 --fetch-content 采集）")


def handle_clean() -> None:
    """处理 --clean 子命令：清洗公告正文"""
    pending: list[dict[str, Any]] = db.get_records_needing_clean()
    if not pending:
        logger.info("所有公告正文已清洗，无需处理")
        return
    logger.info("正在清洗 %d 条公告正文...", len(pending))
    total_orig: int = 0
    total_clean: int = 0
    for ann in pending:
        raw_text: str = ann.get("full_text", "")
        if not raw_text:
            continue
        cleaned: str = clean_announcement_text(raw_text)
        ann["clean_text"] = cleaned
        total_orig += len(raw_text)
        total_clean += len(cleaned)
    db.update_clean_text(pending)
    saved_pct: float = ((total_orig - total_clean) / total_orig * 100) if total_orig else 0
    logger.info("清洗完成: %d 条, %s → %s 字 (节省 %.1f%%)",
                len(pending), f"{total_orig:,}", f"{total_clean:,}", saved_pct)


def handle_prune() -> None:
    """处理 --prune 子命令：清理无正文的空记录"""
    deleted: int = db.prune_empty()
    logger.info("清理完成，删除了 %d 条记录", deleted)


def handle_list(parsed: argparse.Namespace) -> None:
    """处理 --list 子命令：列出历史公告"""
    days: int = parsed.days or 30
    stock_codes: Optional[list[str]] = None
    if parsed.group:
        group_stocks: list[dict[str, Any]] = get_stocks(DEFAULT_COOKIE, group_name=parsed.group)
        if group_stocks:
            stock_codes = [s["code"] for s in group_stocks]
            logger.info("分组 [%s] 包含 %d 只股票", parsed.group, len(stock_codes))
        else:
            logger.warning("分组 [%s] 未获取到股票", parsed.group)
    anns: list[dict[str, Any]] = db.list_announcements(stock_code=parsed.stock, stock_codes=stock_codes, days=days)
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


def handle_list_groups() -> None:
    """处理 --list-groups 子命令：列出所有可用分组"""
    cookie: Optional[str] = load_cookie(DEFAULT_COOKIE)
    if not cookie:
        logger.error("需要 cookie.txt 才能获取分组列表")
        sys.exit(1)
    groups: list[dict[str, Any]] = get_groups(cookie)
    if groups:
        logger.info("可用分组:")
        for g in groups:
            logger.info("  gid=%s  gname=%s", g.get("gid"), g.get("gname"))
    else:
        logger.warning("未获取到分组列表")


def handle_fetch_content(parsed: argparse.Namespace, llm_judge: Any) -> None:
    """处理 --fetch-content 子命令：补抓缺少全文的公告"""
    pending: list[dict[str, Any]] = db.get_pending_content()
    if not pending:
        logger.info("数据库中没有待获取全文的公告")
    else:
        logger.info("正在补抓 %d 条缺少全文的公告（分批保存）...", len(pending))
        fetch_all_contents(pending, save_batch=db.update_content, batch_size=10, llm_judge=llm_judge)
        stats: dict[str, Any] = db.get_stats()
        logger.info("全文获取完成（数据库共 %d 条，含正文 %d 条）",
                     stats["total"], stats["with_content"])
        if llm_judge.enabled:
            logger.info(llm_judge.report())
    db.prune_empty()


def _fetch_announcements(parsed: argparse.Namespace, stocks: list[dict[str, Any]], cookie: Optional[str], days: int) -> list[dict[str, Any]]:
    """根据数据来源获取公告列表"""
    if parsed.source == "cninfo":
        a_stocks: list[dict[str, Any]] = [s for s in stocks if s.get("market") in ("0", "1")]
        hk_stocks: list[dict[str, Any]] = [s for s in stocks if s.get("market") == "116"]
        anns: list[dict[str, Any]] = []
        if a_stocks:
            logger.info("A 股 %d 只 -> 巨潮资讯网", len(a_stocks))
            anns.extend(fetch_all_cninfo(a_stocks, days_back=days))
        if hk_stocks:
            logger.info("港股 %d 只 -> 东方财富", len(hk_stocks))
            anns.extend(fetch_all_announcements(hk_stocks, cookie, days_back=days))
    else:
        anns = fetch_all_announcements(stocks, cookie, days_back=days)
    return anns


def _save_announcements(anns_to_save: list[dict[str, Any]], parsed: argparse.Namespace, llm_judge: Any) -> None:
    """保存公告到数据库，并生成摘要"""
    if parsed.fetch_content:
        logger.info("正在获取 %d 条新公告的全文...", len(anns_to_save))
        fetch_all_contents(anns_to_save, save_batch=db.update_content, batch_size=10, llm_judge=llm_judge)

    for ann in anns_to_save:
        ann["status"] = "valuable" if ann.get("full_text") else "filtered"
    valuable_count: int = sum(1 for a in anns_to_save if a["status"] == "valuable")
    filtered_count: int = len(anns_to_save) - valuable_count
    if filtered_count:
        logger.info("%d 条有价值 / %d 条已过滤", valuable_count, filtered_count)
    db.record_announcements(anns_to_save)
    stats: dict[str, Any] = db.get_stats()
    logger.info("状态已保存（数据库共 %d 条，含正文 %d 条）",
                stats["total"], stats["with_content"])
    if parsed.fetch_content and llm_judge.enabled:
        logger.info(llm_judge.report())

    # 自动生成摘要（对有 clean_text 的有价值公告）
    try:
        from daily_summary import get_unsummarized_announcements, generate_summaries
        stock_codes = list({a["stock_code"] for a in anns_to_save if a.get("stock_code")})
        unsummarized = get_unsummarized_announcements(stock_codes=stock_codes)
        if unsummarized:
            summaries = generate_summaries(unsummarized)
            logger.info("已为 %d 条公告生成摘要", summaries)
    except Exception as e:
        logger.warning("摘要生成失败（不影响主流程）: %s", e)


def handle_main_flow(parsed: argparse.Namespace) -> None:
    """处理主流程：获取公告、过滤、入库"""
    config_manager: ConfigManager = ConfigManager(parsed.config)
    config: AppConfig = config_manager.load()
    
    # 初始化LLM判断器（使用统一的 from_config 工厂方法）
    llm_judge: Any = LLMJudge.from_config(config)
    
    days: int = parsed.days or config.fetch_interval_days

    if parsed.fetch_content:
        handle_fetch_content(parsed, llm_judge)
        if not parsed.group:
            return

    logger.info("=" * 50)
    logger.info("自选股公告追踪 - 开始运行")
    logger.info("=" * 50)
    logger.info("数据来源: %s", "巨潮+A股 / 东方财富+港股" if parsed.source == "cninfo" else "东方财富")
    logger.info("抓取窗口: 最近 %d 天", days)
    if parsed.group:
        logger.info("筛选分组: %s", parsed.group)

    cookie: Optional[str] = load_cookie(DEFAULT_COOKIE)
    stocks: list[dict[str, Any]] = get_stocks(DEFAULT_COOKIE, group_name=parsed.group)
    if not stocks:
        raise DataError("未获取到自选股列表，请检查 cookie.txt 或 config.json")

    logger.info("自选股共 %d 只:", len(stocks))
    for s in stocks:
        logger.info("  - %s (%s)", s["name"], s["code"])

    anns: list[dict[str, Any]] = _fetch_announcements(parsed, stocks, cookie, days)
    logger.info("共获取 %d 条公告", len(anns))

    seen_ids: set[str] = db.get_seen_ids() if not parsed.force else set()

    new_anns: list[dict[str, Any]] = [ann for ann in anns if db.make_ann_id(ann) not in seen_ids]

    if new_anns:
        logger.info("发现 %d 条新公告！", len(new_anns))
        send_notification(config, new_anns)
    else:
        logger.info("暂无新公告")

    anns_to_save: list[dict[str, Any]] = anns if parsed.force else new_anns
    if not parsed.dry_run and anns_to_save:
        _save_announcements(anns_to_save, parsed, llm_judge)
    elif not parsed.dry_run and not anns_to_save:
        stats: dict[str, Any] = db.get_stats()
        logger.info("状态已保存（数据库共 %d 条，含正文 %d 条）",
                    stats["total"], stats["with_content"])

    logger.info("运行完成\n")


def run(args: Optional[list[str]] = None) -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="东方财富自选股公告追踪")
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
    parsed: argparse.Namespace = parser.parse_args(args)

    setup_logging()

    if os.path.exists(db.DB_PATH) and not parsed.stats and not parsed.list and not parsed.list_groups:
        _backup_database()

    # 子命令分发
    if parsed.stats:
        handle_stats()
        return
    if parsed.clean:
        handle_clean()
        return
    if parsed.prune:
        handle_prune()
        return
    if parsed.list:
        handle_list(parsed)
        return
    if parsed.list_groups:
        handle_list_groups()
        return

    handle_main_flow(parsed)


if __name__ == "__main__":
    run()
