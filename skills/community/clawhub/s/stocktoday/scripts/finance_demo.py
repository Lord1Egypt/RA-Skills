"""
财务分析 demo
=============

教 LLM 怎么并行拉 3 表 + 财务指标, 给出完整财务快照.

LLM 调用方式:
    import sys
    sys.path.insert(0, "<skill_dir>/scripts")
    from proxy_demo import get_client
    from finance_demo import full_finance_snapshot
    pro = get_client("your_token")
    snapshot = full_finance_snapshot(pro, "600519.SH", "20251231")
"""

import sys
import os
import pandas as pd

# 允许从 scripts/ 目录 import
sys.path.insert(0, os.path.dirname(__file__) if "__file__" in dir() else ".")

try:
    from proxy_demo import get_client
except ImportError:
    from scripts.proxy_demo import get_client


def full_finance_snapshot(pro: "ts.pro_api", ts_code: str, period: str) -> dict:
    """
    拉 1 只股票最近 1 期完整财务快照 (3 表 + 指标)
    返回 dict 包含 income/balance/cashflow/ratios 4 个 DataFrame
    """
    return {
        "income": pro.income(ts_code=ts_code, period=period),
        "balance": pro.balancesheet(ts_code=ts_code, period=period),
        "cashflow": pro.cashflow(ts_code=ts_code, period=period),
        "ratios": pro.fina_indicator(ts_code=ts_code, period=period,
                                     fields="ts_code,period,roe,roa,grossprofit_margin,netprofit_margin,debt_to_assets,eps,bvps,total_revenue_ps,net_profit_ps"),
    }


def print_snapshot(snapshot: dict) -> None:
    """统一打印财务快照"""
    for key, df in snapshot.items():
        if df is None or len(df) == 0:
            print(f"\n⚠️ {key}: 空")
            continue
        print(f"\n{'=' * 60}")
        print(f"📊 {key.upper()} ({len(df)} 行)")
        print(f"{'=' * 60}")
        print(df.head(3).to_string(index=False))


def trend_8_quarters(pro: "ts.pro_api", ts_code: str) -> pd.DataFrame:
    """
    拉最近 8 个季度 ROE 趋势 (LLM 拿这个画趋势图 / 写摘要)

    注意: tushare 财务接口 period 是报告期末 (YYYYMMDD), 季度报告期是 0331/0630/0930/1231.
    """
    quarters = ["20231231", "20240331", "20240630", "20240930",
                "20241231", "20250331", "20250630", "20250930"]
    rows = []
    for q in quarters:
        df = pro.fina_indicator(ts_code=ts_code, period=q,
                                fields="ts_code,period,roe,revenue,yoy_net_profit")
        if df is not None and len(df) > 0:
            rows.append(df.iloc[0].to_dict())
    return pd.DataFrame(rows)


# ============================================================
# 主入口
# ============================================================

if __name__ == "__main__":
    pro = get_client()
    print(f"✅ 拉财务快照: 600519.SH / 20241231")

    snapshot = full_finance_snapshot(pro, "600519.SH", "20241231")
    print_snapshot(snapshot)

    print(f"\n\n{'=' * 60}")
    print(f"📈 ROE 8 季度趋势")
    print(f"{'=' * 60}")
    trend = trend_8_quarters(pro, "600519.SH")
    print(trend.to_string(index=False))
