"""
stocktoday-data proxy demo
==========================

StockToday 数据研究技能 demo 脚本, 调用 235+ 个数据接口, 后端走 StockToday 自定义加速 (https://tushare.citydata.club/).

LLM 调用方式:
    import sys
    sys.path.insert(0, "<skill_dir>/scripts")
    from proxy_demo import get_client
    pro = get_client("your_token_here")
    df = pro.daily(ts_code="600519.SH", start_date="20240101", end_date="20241231")

或者用环境变量:
    export TUSHARE_TOKEN="your_token"
    python proxy_demo.py
"""

import os
import sys
import tushare as ts
import pandas as pd

# === 4 个 fallback gateway (主站挂了自动切) ===
DEFAULT_GATEWAY = "https://tushare.citydata.club/"
BACKUP_GATEWAY_1 = "http://111.229.164.2:8083/"
BACKUP_GATEWAY_2 = "http://124.223.112.152:6331/"
BACKUP_GATEWAY_3 = "http://110.42.211.9:9900/"


def get_client(token: str = None, gateway: str = None) -> "ts.pro_api":
    """
    获取走 StockToday gateway 的 tushare pro client

    优先顺序: 参数 > TUSHARE_TOKEN env > TUSHARE_GATEWAY env > 默认 gateway
    """
    token = token or os.getenv("TUSHARE_TOKEN") or "your_token_here"
    gateway = gateway or os.getenv("TUSHARE_GATEWAY") or DEFAULT_GATEWAY

    pro = ts.pro_api(token)
    # 指向 stocktoday gateway
    pro._DataApi__token = token
    pro._DataApi__http_url = gateway
    return pro


def print_section(title: str, df: pd.DataFrame, max_rows: int = 5) -> None:
    """统一打印格式: 标题 + 前 max_rows 行"""
    print(f"\n{'=' * 50}")
    print(f"📊 {title}")
    print(f"{'=' * 50}")
    print(f"  数据行数: {len(df)}")
    print(f"  字段: {list(df.columns)[:8]}{'...' if len(df.columns) > 8 else ''}")
    print(df.head(max_rows).to_string(index=False))


# ============================================================
# 5 个 demo case: 行情 / 财务 / 对比 / 资金 / 板块
# ============================================================

def demo_quote(pro: "ts.pro_api") -> None:
    """Demo 1: 单只股票最近 1 个月日线"""
    df = pro.daily(ts_code="600519.SH", start_date="20260601", end_date="20260618")
    print_section("Demo 1: 茅台 6 月日线", df)


def demo_finance(pro: "ts.pro_api") -> None:
    """Demo 2: 单只股票 2024 年报关键指标"""
    df = pro.fina_indicator(ts_code="600519.SH", period="20241231",
                            fields="ts_code,period,roe,grossprofit_margin,eps,debt_to_assets")
    print_section("Demo 2: 茅台 2024 年报 ROE/毛利率/EPS", df)


def demo_compare(pro: "ts.pro_api") -> None:
    """Demo 3: 多只股票对比 (用 daily 取最新一日收盘)"""
    df = pro.daily(ts_code="600519.SH,000858.SZ,000568.SZ",
                   trade_date="20260618",
                   fields="ts_code,close,pct_chg,vol,amount")
    print_section("Demo 3: 白酒 3 只对比 (6/18 收盘)", df)


def demo_moneyflow(pro: "ts.pro_api") -> None:
    """Demo 4: 单只股票资金流向 (主力净流入)"""
    df = pro.moneyflow(ts_code="600519.SH", trade_date="20260618",
                       fields="ts_code,trade_date,buy_sm_amount,sell_sm_amount,buy_md_amount,sell_md_amount,buy_lg_amount,sell_lg_amount,buy_elg_amount,sell_elg_amount,net_mf_amount")
    print_section("Demo 4: 茅台 6/18 资金流向 (小/中/大/特大单)", df)


def demo_sector(pro: "ts.pro_api") -> None:
    """Demo 5: 板块行情 (同花顺概念)"""
    df = pro.ths_index(ts_code="881101", exchange="A", type="N")  # 半导体
    print_section("Demo 5: 半导体板块 ths_index 列表", df.head(10))


# ============================================================
# 主入口: 跑全部 5 个 demo
# ============================================================

if __name__ == "__main__":
    pro = get_client()
    print(f"✅ StockToday client 已初始化, gateway: {pro._DataApi__http_url}")
    print(f"   token: {pro._DataApi__token[:6]}***")

    try:
        demo_quote(pro)
    except Exception as e:
        print(f"❌ Demo 1 失败: {e}")

    try:
        demo_finance(pro)
    except Exception as e:
        print(f"❌ Demo 2 失败: {e}")

    try:
        demo_compare(pro)
    except Exception as e:
        print(f"❌ Demo 3 失败: {e}")

    try:
        demo_moneyflow(pro)
    except Exception as e:
        print(f"❌ Demo 4 失败: {e}")

    try:
        demo_sector(pro)
    except Exception as e:
        print(f"❌ Demo 5 失败: {e}")
