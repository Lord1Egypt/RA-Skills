"""
宏观数据一键拉取脚本 — 三源混合策略版
用法: python fetch_macro.py [china|global|all]

数据源优先级：
  1. AKShare 国家统计局源（PPI/CPI/PMI/GDP/M2/社融/LPR/中美国债利率）
  2. AKShare 新浪源（全球指数/港股指数/期货主力/ETF）
  3. 东方财富EM源作为补充（网络不稳定时自动跳过）

已知不可用函数（勿用）：
  - macro_china_rmb() — TypeError (dtype错误)
  - stock_*_spot_em() — 频繁 RemoteDisconnected
  - stock_board_industry_name_em() — 同上
  - stock_sector_spot_indicator() — 函数不存在
  - stock_sector_fund_flow_rank() — KeyError
  - fund_qdii_spot_em() — 函数不存在
  - futures_foreign_commodity_realtime() — 需symbol参数
"""

import akshare as ak
import json
import sys
from datetime import datetime


def fetch_china_macro():
    """返回中国宏观指标字典（AKShare 国家统计局源，最稳定）"""
    result = {"fetch_time": datetime.now().isoformat(), "indicators": {}}

    try:
        # PPI
        df = ak.macro_china_ppi()
        latest = df.iloc[0]
        result["indicators"]["PPI"] = {
            "month": str(latest.iloc[0]),
            "current_value": float(latest.iloc[1]),
            "yoy_growth": float(latest.iloc[2]),
            "cumulative": float(latest.iloc[3]),
            "note": f"最新数据月：{latest.iloc[0]}，当月同比增长{latest.iloc[2]}%",
        }
        # 上月参考
        prev = df.iloc[1]
        result["indicators"]["PPI_prev"] = {
            "month": str(prev.iloc[0]),
            "yoy_growth": float(prev.iloc[2]),
        }
    except Exception as e:
        result["indicators"]["PPI"] = {"error": str(e)}

    try:
        # CPI
        df = ak.macro_china_cpi()
        latest = df.iloc[0]
        result["indicators"]["CPI"] = {
            "month": str(latest.iloc[0]),
            "current_value": float(latest.iloc[1]),
            "yoy_growth": float(latest.iloc[2]),
            "cumulative": float(latest.iloc[3]),
        }
    except Exception as e:
        result["indicators"]["CPI"] = {"error": str(e)}

    try:
        # PMI
        df = ak.macro_china_pmi()
        latest = df.iloc[0]
        result["indicators"]["PMI"] = {
            "month": str(latest.iloc[0]),
            "manufacturing": float(latest.iloc[1]),
            "non_manufacturing": float(latest.iloc[2]) if len(latest) > 2 else None,
        }
    except Exception as e:
        result["indicators"]["PMI"] = {"error": str(e)}

    try:
        # GDP
        df = ak.macro_china_gdp()
        result["indicators"]["GDP"] = {
            "latest_quarter": str(df.iloc[0, 0]),
            "gdp_yoy": float(df.iloc[0, 1]),
            "cumulative_yoy": float(df.iloc[0, 2]),
        }
    except Exception as e:
        result["indicators"]["GDP"] = {"error": str(e)}

    try:
        # M2
        df = ak.macro_china_money_supply()
        latest = df.iloc[0]
        result["indicators"]["M2"] = {
            "month": str(latest.iloc[0]),
            "m2_yoy": float(latest.iloc[2]) if len(latest) > 2 else float(latest.iloc[1]),
        }
    except Exception as e:
        result["indicators"]["M2"] = {"error": str(e)}

    try:
        # 社融
        df = ak.macro_china_shrzgm()
        result["indicators"]["SH_RZGM"] = {
            "month": str(df.iloc[-1, 0]),
            "value": float(df.iloc[-1, 1]),
        }
    except Exception as e:
        result["indicators"]["SH_RZGM"] = {"error": str(e)}

    try:
        # LPR
        df = ak.macro_china_lpr()
        result["indicators"]["LPR"] = {
            "date": str(df.iloc[0, 0]),
            "lpr_1y": float(df.iloc[0, 1]),
            "lpr_5y": float(df.iloc[0, 2]) if len(df.columns) > 2 else None,
        }
    except Exception as e:
        result["indicators"]["LPR"] = {"error": str(e)}

    # 人民币汇率 — macro_china_rmb() 已知 TypeError，需 WebSearch 兜底
    result["indicators"]["USDCNY"] = {
        "note": "macro_china_rmb() TypeError，需 WebSearch 兜底查 USD/CNY",
    }

    return result


def fetch_global_macro():
    """返回全球宏观指标（新浪源为主 + 中美国债利率）"""
    result = {"fetch_time": datetime.now().isoformat(), "indicators": {}}

    # ---- 新浪源：全球指数 ----
    try:
        df_global = ak.stock_info_global_sina()  # 20行，含道琼斯/标普/纳斯达克等
        for _, row in df_global.iterrows():
            name = str(row.iloc[0]) if len(row) > 0 else ""
            price = row.iloc[1] if len(row) > 1 else None
            change = row.iloc[2] if len(row) > 2 else None
            if name and price is not None:
                result["indicators"][f"SINA_{name}"] = {
                    "price": str(price),
                    "change": str(change) if change is not None else None,
                }
    except Exception as e:
        result["indicators"]["SINA_global_indices"] = {"error": str(e)}

    # ---- 新浪源：港股指数 ----
    try:
        df_hk = ak.stock_hk_index_spot_sina()  # 38行
        for _, row in df_hk.iterrows():
            name = str(row.iloc[0]) if len(row) > 0 else ""
            price = row.iloc[1] if len(row) > 1 else None
            if "恒生" in name and price is not None:
                result["indicators"]["HSI"] = {
                    "price": str(price),
                    "source": "sina",
                }
    except Exception as e:
        result["indicators"]["HSI"] = {"error": str(e)}

    # ---- 中美国债利率（AKShare 稳定） ----
    try:
        df_bond = ak.bond_zh_us_rate()
        last = df_bond.iloc[-1]
        result["indicators"]["BOND_SPREAD"] = {
            "date": str(last.iloc[0]),
            "cn_10y": float(last.iloc[1]) if len(last) > 1 and str(last.iloc[1]) != "nan" else None,
            "us_10y": float(last.iloc[2]) if len(last) > 2 and str(last.iloc[2]) != "nan" else None,
        }
    except Exception as e:
        result["indicators"]["BOND_SPREAD"] = {"error": str(e)}

    # ---- 新浪源：A股指数行情 ----
    try:
        df_a = ak.stock_zh_index_spot_sina()  # 562行，含上证/深证/创业板
        for _, row in df_a.iterrows():
            name = str(row.iloc[0]) if len(row) > 0 else ""
            price = row.iloc[1] if len(row) > 1 else None
            if name in ("上证指数", "深证成指", "创业板指") and price is not None:
                result["indicators"][f"A_{name}"] = {
                    "price": str(price),
                    "source": "sina",
                }
    except Exception as e:
        result["indicators"]["A_indices"] = {"error": str(e)}

    # ---- 期货主力品种列表（新浪源） ----
    try:
        df_futures = ak.futures_display_main_sina()  # 82行
        # 提取关键品种
        key_symbols = ["AU", "AG", "CU", "AL", "RB", "I", "J", "JM", "AP", "CF", "SR", "TA", "MA", "OI", "M", "Y", "P"]
        for _, row in df_futures.iterrows():
            symbol = str(row.iloc[0]) if len(row) > 0 else ""
            if symbol in key_symbols:
                name = str(row.iloc[1]) if len(row) > 1 else ""
                result["indicators"][f"FUTURES_{symbol}"] = {
                    "symbol": symbol,
                    "name": name,
                    "source": "sina",
                }
    except Exception as e:
        result["indicators"]["FUTURES_list"] = {"error": str(e)}

    # ---- ETF分类行情（新浪源） ----
    try:
        df_etf = ak.fund_etf_category_sina()  # 382行
        result["indicators"]["ETF_COUNT"] = len(df_etf)
    except Exception as e:
        result["indicators"]["ETF"] = {"error": str(e)}

    return result


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode == "china":
        data = fetch_china_macro()
    elif mode == "global":
        data = fetch_global_macro()
    else:
        data = {
            "china": fetch_china_macro(),
            "global": fetch_global_macro(),
        }

    print(json.dumps(data, ensure_ascii=False, indent=2))
