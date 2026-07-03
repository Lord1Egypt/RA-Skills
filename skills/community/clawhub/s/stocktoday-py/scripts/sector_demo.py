"""
板块 / 打板 / 情绪 demo
======================

教 LLM 怎么查板块表现 / 涨停梯队 / 资金流向.

注意: 指数代码 (000001.SH 上证 / 000300.SH 沪深300 / 399006.SZ 创业板指)
不要用 pro.daily(), 要用 pro.index_daily(). pro.daily() 对指数代码返空.
"""

import sys
import pandas as pd

try:
    from proxy_demo import get_client
except ImportError:
    from scripts.proxy_demo import get_client


def index_daily_safe(pro, ts_code: str, **kwargs):
    """
    拉指数日线 (注意: 指数代码 000001.SH 等不要用 daily, 用这个)
    """
    return pro.index_daily(ts_code=ts_code, **kwargs)


def main_index_snapshot(pro: "ts.pro_api", date: str = None) -> dict:
    """
    拉 4 大指数最近 1 日快照 (上证 / 深证 / 沪深300 / 创业板)
    """
    if date is None:
        import datetime
        date = datetime.date.today().strftime("%Y%m%d")
    indices = {
        "上证指数": "000001.SH",
        "深证成指": "399001.SZ",
        "沪深300": "000300.SH",
        "创业板指": "399006.SZ",
    }
    return {name: pro.index_daily(ts_code=code, trade_date=date)
            for name, code in indices.items()}


def limit_up_pool(pro: "ts.pro_api", date: str) -> pd.DataFrame:
    """
    涨停股票池 (limit_list_d, limit_type='U')
    """
    return pro.limit_list_d(trade_date=date, limit_type="U",
                            fields="ts_code,name,trade_date,close,pct_chg,amount,limit_amount,fd_amount")


def limit_step_pool(pro: "ts.pro_api", date: str, nums: str = "2,3,4") -> pd.DataFrame:
    """
    涨停连板天梯 (limit_step, nums='2,3,4' 表示 2-4 连板)
    """
    return pro.limit_step(trade_date=date, nums=nums,
                          fields="ts_code,name,trade_date,nums,limit_amount")


def moneyflow_ind_dc(pro: "ts.pro_api", date: str) -> pd.DataFrame:
    """
    板块资金流向 (东方财富)
    """
    return pro.moneyflow_ind_dc(trade_date=date,
                                 fields="ts_code,name,trade_date,pct_change,net_amount,net_amount_rate")


# ============================================================
# 主入口
# ============================================================

if __name__ == "__main__":
    pro = get_client()
    print(f"✅ 板块/打板 demo 启动")

    # 1) 4 大指数
    print(f"\n{'=' * 60}")
    print(f"📊 4 大指数快照")
    print(f"{'=' * 60}")
    snap = main_index_snapshot(pro, "20260618")
    for name, df in snap.items():
        if df is not None and len(df) > 0:
            row = df.iloc[0]
            print(f"  {name:8} ({row['ts_code']:10}) "
                  f"close={row.get('close', 'N/A'):>8} "
                  f"pct_chg={row.get('pct_chg', 'N/A'):>6}%")

    # 2) 涨停池
    print(f"\n{'=' * 60}")
    print(f"🔥 涨停股票池 (6/18)")
    print(f"{'=' * 60}")
    try:
        df = limit_up_pool(pro, "20260618")
        print(f"  共 {len(df)} 只涨停")
        print(df.head(10).to_string(index=False))
    except Exception as e:
        print(f"  ⚠️ {e}")

    # 3) 连板天梯
    print(f"\n{'=' * 60}")
    print(f"📈 连板天梯 (2-4 板, 6/18)")
    print(f"{'=' * 60}")
    try:
        df = limit_step_pool(pro, "20260618", "2,3,4")
        print(f"  共 {len(df)} 只连板")
        print(df.to_string(index=False))
    except Exception as e:
        print(f"  ⚠️ {e}")

    # 4) 板块资金流
    print(f"\n{'=' * 60}")
    print(f"💰 板块资金流 (东方财富, 6/18)")
    print(f"{'=' * 60}")
    try:
        df = moneyflow_ind_dc(pro, "20260618")
        print(f"  共 {len(df)} 个板块")
        print(df.head(10).to_string(index=False))
    except Exception as e:
        print(f"  ⚠️ {e}")
