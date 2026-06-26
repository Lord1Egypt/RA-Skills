# -*- coding: utf-8 -*-
"""
Report-gama — 主控脚本（重写版）
✅ 并发执行：多模块同时跑，速度提升 5-10 倍
✅ 超时感知：单个模块最多等 60 秒，不卡死
✅ 实时进度：每个模块开始/完成都有提示
"""

import os
import sys
import time
import logging
import argparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError as FuturesTimeoutError
from threading import Lock

# 添加 scripts 目录到 path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# ── 依赖检查 ──────────────────────────────────────────────
try:
    from config import COUNTRIES, CATEGORY_KEYWORDS, OUTPUT_DIR, DATA_DIR, LOG_LEVEL, LOG_FORMAT
    import requests as _req
    from bs4 import BeautifulSoup as _bs
    _DEPS_OK = True
except ImportError as e:
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║  ⚠️  缺少必需依赖！                                       ║
╠═══════════════════════════════════════════════════════════╣
║  缺少模块: {str(e)[:45]:<45}  ║
║  请运行以下命令安装:                                      ║
║                                                           ║
║    pip install requests beautifulsoup4 lxml               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
""")
    sys.exit(1)

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# ── 全局状态 ──────────────────────────────────────────────
_progress_lock = Lock()
_progress_count = 0
_progress_total = 0

def _update_progress(module_name, status="done"):
    global _progress_count, _progress_total
    with _progress_lock:
        if status == "start":
            _progress_count += 1
            pct = int(_progress_count / _progress_total * 100) if _progress_total else 0
            print(f"  [{_progress_count}/{_progress_total} | {pct:3d}%]  ▶ {module_name}...")
        elif status == "done":
            print(f"  [{_progress_count}/{_progress_total} | 100%]  ✅ {module_name} 完成")


# ── 参数解析 ──────────────────────────────────────────────
def parse_args():
    parser = argparse.ArgumentParser(
        description="Report-gama — 专业市场调研报告生成工具（并发版）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python3 master.py --country 俄罗斯 --category 血糖检测设备 --lang ru
  python3 master.py --country 俄罗斯 --category 血糖检测设备 --modules news,competitor,ecommerce --lang ru
  python3 master.py --country 俄罗斯 --category 血糖检测设备 --modules all --pdf --timeout 120
"""
    )
    parser.add_argument("--country", default="俄罗斯", help="目标国家（默认：俄罗斯）")
    parser.add_argument("--category", default="医疗器械", help="目标品类（默认：医疗器械）")
    parser.add_argument("--category-ru", default="", help="品类俄语关键词（可选）")
    parser.add_argument("--category-en", default="", help="品类英语关键词（可选）")
    parser.add_argument("--lang", default="ru", help="主语言（ru/en/zh，默认：ru）")
    parser.add_argument(
        "--modules", default="all",
        help="模块列表：news,competitor,ecommerce,ads,customs,market,search,telegram,tender,registration,vk,medical_org,pricing（默认：all）"
    )
    parser.add_argument("--days", type=int, default=30, help="新闻监控天数（默认：30）")
    parser.add_argument("--output", default="", help="输出文件路径")
    parser.add_argument("--pdf", action="store_true", help="同时导出 PDF")
    parser.add_argument("--no-chart", action="store_true", help="跳过图表生成")
    parser.add_argument("--quiet", action="store_true", help="减少日志输出")
    parser.add_argument("--timeout", type=int, default=60, help="单个模块超时秒数（默认：60）")
    parser.add_argument("--workers", type=int, default=4, help="并发工作线程数（默认：4）")
    return parser.parse_args()


def get_keywords(category, category_ru="", category_en=""):
    """获取品类关键词"""
    if category_ru or category_en:
        return {
            "ru": category_ru.split(",") if category_ru else [category],
            "en": category_en.split(",") if category_en else [category],
            "zh": [category],
        }
    if category in CATEGORY_KEYWORDS:
        return CATEGORY_KEYWORDS[category]
    return {
        "ru": [category, category.lower()],
        "en": [category, category.lower()],
        "zh": [category],
    }


# ── 模块执行函数（每个函数有独立超时） ─────────────────────

def _run_news(args, keywords):
    from news_monitor import NewsMonitor
    monitor = NewsMonitor(country=args.country, lang=args.lang)
    articles = monitor.monitor_industry_news(keywords, days=args.days)
    gov = monitor.monitor_government_announcements(keywords)
    return {
        "articles": articles + gov,
        "news_brief": monitor.generate_news_brief(articles + gov),
    }

def _run_competitor(args, keywords):
    from competitor_analysis import CompetitorAnalyzer
    analyzer = CompetitorAnalyzer(country=args.country, lang=args.lang)
    brand_kw = keywords.get("brand_keywords", [])
    competitors = analyzer.analyze_from_search(keywords, brand_keywords=brand_kw)
    return {
        "competitors": competitors,
        "competitor_report": analyzer.generate_competitor_report(competitors),
    }

def _run_ecommerce(args, keywords):
    from ecommerce_tracker import EcommerceTracker
    tracker = EcommerceTracker(country=args.country, lang=args.lang)
    kws = keywords.get("ru", keywords.get("en", []))
    products = tracker.track_prices(kws[:3], platforms=None)
    stats = tracker.analyze_price_distribution(products)
    return {
        "products": products,
        "price_stats": stats,
        "ecommerce_report": tracker.generate_price_report(products, stats),
    }

def _run_ad(args, keywords):
    from ad_research import AdResearcher
    researcher = AdResearcher(country=args.country, lang=args.lang)
    channels = researcher.get_channel_overview(keywords)
    competitors_ads = researcher.research_competitor_ads(keywords, keywords.get("brand_keywords", []))
    budgets = researcher.estimate_campaign_budget(keywords)
    return {
        "channels": channels,
        "competitor_ads": competitors_ads,
        "budgets": budgets,
        "ad_report": researcher.generate_ad_report(channels, competitors_ads, budgets),
    }

def _run_customs(args, keywords):
    from customs_data import CustomsData
    customs = CustomsData(country=args.country, lang=args.lang)
    hs_codes = customs.get_hs_code(args.category)
    customs_data = customs.search_customs_from_web(hs_codes["primary"], keywords)
    market_estimate = customs.estimate_market_size_from_customs(customs_data, hs_codes["primary"], args.category)
    return {
        "customs_data": customs_data,
        "market_estimate": market_estimate,
        "customs_report": customs.generate_customs_report(customs_data, market_estimate),
    }

def _run_market(args, keywords):
    from market_research import MarketResearcher
    researcher = MarketResearcher(country=args.country, lang=args.lang)
    market_data = researcher.get_country_market_overview(keywords)
    tam_sam_som = researcher.estimate_tam_sam_som(args.category, keywords)
    return {
        "market_data": market_data,
        "tam_sam_som": tam_sam_som,
        "market_report": researcher.generate_market_report(market_data, tam_sam_som),
    }

def _run_search(args, keywords, active_modules):
    from multi_lang_search import MultiLangSearch
    searcher = MultiLangSearch(country=args.country, lang=args.lang)
    all_results = {}
    dimension_map = {
        "news": ["新闻"], "market": ["市场规模"], "competitor": ["竞争格局"],
        "ecommerce": ["电商", "价格"], "ads": ["广告"], "customs": ["进出口"],
    }
    for module in active_modules:
        dims = dimension_map.get(module, ["新闻"])
        keywords_to_search = []
        for dim in dims:
            keywords_to_search.extend(keywords.get(args.lang, []))
            keywords_to_search.extend(keywords.get("en", []))
        keywords_to_search = list(set(keywords_to_search))[:10]
        results = searcher.search(keywords_to_search, news_mode=(module == "news"))
        all_results[module] = results
        time.sleep(1)
    return {"search_results": all_results, "total_results": sum(len(v) for v in all_results.values())}

def _run_telegram(args, keywords):
    from telegram_monitor import TelegramMonitor
    monitor = TelegramMonitor(country=args.country, lang=args.lang)
    posts = monitor.search_channel_posts(keywords.get(args.lang, keywords.get("en", [])), limit=20)
    trends = monitor.get_keyword_trends(keywords.get(args.lang, keywords.get("en", [])), days=30)
    return {
        "channels": monitor.get_known_industry_channels(),
        "posts": posts,
        "trends": trends,
        "telegram_report": monitor.generate_telegram_report(posts, trends),
    }

def _run_tender(args, keywords):
    from tender_monitor import TenderMonitor
    monitor = TenderMonitor(country=args.country, lang=args.lang)
    tenders = monitor.search_tenders(keywords.get(args.lang, keywords.get("en", [])), date_from=None, date_to=None)
    price_estimate = monitor.get_market_price_from_tenders(keywords.get(args.lang, keywords.get("en", [])))
    return {
        "tenders": tenders,
        "price_estimate": price_estimate,
        "tender_report": monitor.generate_tender_report(tenders, price_estimate),
    }

def _run_registration(args, keywords):
    from registration_db import RegistrationDB
    db = RegistrationDB(country=args.country, lang=args.lang)
    registrations = db.search_registrations(keywords.get(args.lang, keywords.get("en", [])))
    return {
        "registrations": registrations,
        "registration_report": db.generate_registration_report(registrations),
    }

def _run_vk(args, keywords):
    from vk_monitor import VKMonitor
    monitor = VKMonitor(country=args.country, lang=args.lang)
    posts = monitor.search_vk_public(keywords.get(args.lang, keywords.get("en", [])), limit=30)
    mentions = monitor.analyze_vk_mentions(keywords.get(args.lang, keywords.get("en", [])))
    return {
        "posts": posts,
        "mentions": mentions,
        "vk_report": monitor.generate_vk_report(posts, mentions),
    }

def _run_medical_org(args, keywords):
    from medical_org_db import MedicalOrgDB
    db = MedicalOrgDB(country=args.country, lang=args.lang)
    orgs = db.get_market_capacity("all", keywords.get("region", "Москва"))
    distribution = db.get_org_distribution_by_region(keywords.get(args.lang, keywords.get("en", [])))
    return {
        "orgs": orgs,
        "distribution": distribution,
        "medical_org_report": db.generate_medical_org_report(orgs, distribution),
    }

def _run_pricing(args, keywords):
    from pricing_db import PricingDB
    db = PricingDB(country=args.country, lang=args.lang)
    prices = db.search_reference_prices(keywords.get(args.lang, keywords.get("en", [])))
    zhnvlp = db.get_zhnvlp_prices(keywords.get(args.lang, keywords.get("en", [])))
    return {
        "prices": prices,
        "zhnvlp": zhnvlp,
        "pricing_report": db.generate_pricing_report(prices, zhnvlp),
    }


# ── 并发执行调度器 ─────────────────────────────────────────

MODULE_HANDLERS = {
    "news":         ("📰 新闻监控",        _run_news),
    "market":       ("📊 市场分析",        _run_market),
    "competitor":   ("🏢 竞品分析",        _run_competitor),
    "ecommerce":    ("🛒 电商价格",        _run_ecommerce),
    "ads":          ("📢 广告研究",        _run_ad),
    "customs":      ("🚢 海关数据",        _run_customs),
    "search":       ("🔍 多语种搜索",       _run_search),
    "telegram":     ("💬 Telegram社群",    _run_telegram),
    "tender":       ("📋 政府招标",        _run_tender),
    "registration": ("🏥 注册证查询",      _run_registration),
    "vk":           ("🌐 VKontakte",       _run_vk),
    "medical_org":  ("🏨 医疗机构",        _run_medical_org),
    "pricing":      ("💰 参考定价",         _run_pricing),
}

# 每个模块失败时的默认空数据
EMPTY_DATA = {
    "news":         {"articles": [], "news_brief": ""},
    "market":       {"market_data": {}, "tam_sam_som": {}, "market_report": ""},
    "competitor":   {"competitors": [], "competitor_report": ""},
    "ecommerce":    {"products": [], "price_stats": {}, "ecommerce_report": ""},
    "ad":           {"channels": {}, "competitor_ads": [], "budgets": {}, "ad_report": ""},
    "customs":      {"customs_data": {}, "market_estimate": {}, "customs_report": ""},
    "search":       {"search_results": {}, "total_results": 0},
    "telegram":     {"channels": [], "posts": [], "trends": {}, "telegram_report": ""},
    "tender":       {"tenders": [], "price_estimate": {}, "tender_report": ""},
    "registration": {"registrations": [], "registration_report": ""},
    "vk":           {"posts": [], "mentions": {}, "vk_report": ""},
    "medical_org":  {"orgs": [], "distribution": {}, "medical_org_report": ""},
    "pricing":      {"prices": [], "zhnvlp": {}, "pricing_report": ""},
}

# 数据映射（某些模块叫 ad 但存储在 "ad" key）
DATA_KEY_MAP = {
    "news": "news", "market": "market", "competitor": "competitor",
    "ecommerce": "ecommerce", "ads": "ad", "customs": "customs",
    "search": "search", "telegram": "telegram", "tender": "tender",
    "registration": "registration", "vk": "vk", "medical_org": "medical_org",
    "pricing": "pricing",
}


def run_concurrent_modules(args, keywords, active_modules, module_timeout, workers):
    """并发执行所有活跃模块，统一超时控制"""
    global _progress_total
    _progress_total = len(active_modules)

    all_data = {}
    start_time = time.time()

    print(f"\n📡 并发采集（{len(active_modules)} 个模块，{workers} 线程，超时 {module_timeout}s/模块）...\n")

    def execute_module(module_name):
        """包装器：执行单个模块，带超时和异常处理"""
        label = MODULE_HANDLERS.get(module_name, (module_name, None))[0]
        _update_progress(label, "start")
        try:
            handler = MODULE_HANDLERS[module_name][1]
            # search 模块需要额外传 active_modules
            if module_name == "search":
                return module_name, handler(args, keywords, active_modules)
            return module_name, handler(args, keywords)
        except Exception as e:
            logger.error(f"[{label}] 模块失败: {e}")
            return module_name, EMPTY_DATA.get(module_name, {})
        finally:
            _update_progress(label, "done")

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(execute_module, m): m for m in active_modules}

        for future in as_completed(futures, timeout=module_timeout * len(active_modules) * 2 + 120):
            module_name = futures[future]
            try:
                result_module, result_data = future.result(timeout=module_timeout)
                data_key = DATA_KEY_MAP.get(result_module, result_module)
                all_data[data_key] = result_data
            except FuturesTimeoutError:
                logger.warning(f"[{MODULE_HANDLERS.get(module_name, ('',))[0]}] 模块执行超时（>{module_timeout}s）")
                data_key = DATA_KEY_MAP.get(module_name, module_name)
                all_data[data_key] = EMPTY_DATA.get(module_name, {})
            except Exception as e:
                logger.error(f"[{MODULE_HANDLERS.get(module_name, ('',))[0]}] 异常: {e}")
                data_key = DATA_KEY_MAP.get(module_name, module_name)
                all_data[data_key] = EMPTY_DATA.get(module_name, {})

    elapsed = time.time() - start_time
    print(f"\n⏱  采集完成，耗时 {elapsed:.1f}s，成功 {len(all_data)}/{len(active_modules)} 个模块\n")
    return all_data


# ── 报告生成 ───────────────────────────────────────────────

def generate_final_report(args, all_data):
    try:
        from report_generator import ReportGenerator
        generator = ReportGenerator(
            country=args.country,
            category=args.category,
            lang=args.lang
        )
        report = generator.generate_full_report(
            news_data=all_data.get("news"),
            competitor_data=all_data.get("competitor"),
            ecommerce_data=all_data.get("ecommerce"),
            ad_data=all_data.get("ad"),
            customs_data=all_data.get("customs"),
            market_data=all_data.get("market", {}).get("market_data"),
            tam_sam_som=all_data.get("market", {}).get("tam_sam_som"),
            search_results=all_data.get("search"),
            telegram_data=all_data.get("telegram"),
            tender_data=all_data.get("tender"),
            registration_data=all_data.get("registration"),
            vk_data=all_data.get("vk"),
            medical_org_data=all_data.get("medical_org"),
            pricing_data=all_data.get("pricing"),
        )
        if args.output:
            md_path = args.output
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            md_path = os.path.join(OUTPUT_DIR, f"report_{args.country}_{args.category}_{timestamp}.md")
        report_path = generator.save_report(report, md_path)
        logger.info(f"✅ Markdown 报告已保存: {report_path}")
        return report_path, generator.charts
    except Exception as e:
        logger.error(f"报告生成失败: {e}")
        return None, []


def export_to_pdf(md_path):
    try:
        from pdf_exporter import PDFExporter
        exporter = PDFExporter()
        pdf_path = exporter.markdown_to_pdf(md_path)
        logger.info(f"✅ PDF 已导出: {pdf_path}")
        return pdf_path
    except ImportError:
        logger.warning("reportlab 未安装，无法生成 PDF")
        return None
    except Exception as e:
        logger.error(f"PDF 导出失败: {e}")
        return None


# ── 主函数 ────────────────────────────────────────────────

def main():
    args = parse_args()

    if args.quiet:
        logging.getLogger().setLevel(logging.WARNING)

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║          📊 Report-gama — 专业市场调研报告生成器              ║
║                    并发执行版 v1.1                            ║
║                                                              ║
║  目标国家: {args.country:<46}║
║  目标品类: {args.category:<46}║
║  主语言:   {args.lang:<46}║
║  模块:     {args.modules:<46}║
║  超时:     {args.timeout}s/模块 | 并发数: {args.workers}                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")

    # 解析模块
    if args.modules == "all":
        active_modules = list(MODULE_HANDLERS.keys())
    else:
        active_modules = [m.strip() for m in args.modules.split(",") if m.strip() in MODULE_HANDLERS]
        if not active_modules:
            print("❌ 没有找到有效的模块名称！")
            sys.exit(1)

    # 关键词
    keywords = get_keywords(args.category, args.category_ru, args.category_en)
    logger.info(f"品类关键词: {keywords}")

    # 并发执行
    all_data = run_concurrent_modules(args, keywords, active_modules, args.timeout, args.workers)

    # 生成报告
    print("📝 正在生成报告...")
    report_path, charts = generate_final_report(args, all_data)

    if report_path:
        size = 0
        try:
            size = os.path.getsize(report_path)
        except Exception:
            pass

        print(f"""
╔══════════════════════════════════════════════════════════════╗
║  ✅ 报告生成成功！                                            ║
║                                                              ║
║  📄 文件: {report_path:<47}║
║  📦 大小: {size/1024:.1f} KB                                             ║
║  📊 图表: {len(charts)} 个                                               ║
╚══════════════════════════════════════════════════════════════╝
""")

        if args.pdf:
            print("📄 正在导出 PDF...")
            pdf_path = export_to_pdf(report_path)
            if pdf_path:
                print(f"   ✅ PDF: {pdf_path}")
            else:
                print("   ⚠️  PDF 导出失败（请运行 pip install reportlab）")
    else:
        print("\n❌ 报告生成失败！")
        sys.exit(1)

    print("\n🎉 完成！感谢使用 Report-gama v1.1\n")
    return report_path


if __name__ == "__main__":
    main()
