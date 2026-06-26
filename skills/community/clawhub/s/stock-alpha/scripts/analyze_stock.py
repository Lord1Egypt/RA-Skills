#!/usr/bin/env python3
"""
股智Alpha - 个股六维分析报告
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import argparse
from src.collectors.ashare_collector import AshareCollector
from src.collectors.fund_flow_collector import FundFlowCollector
from src.collectors.futu_bridge import FutuBridge
from src.collectors.technical import add_technical_indicators
from src.analysis.stock_analyzer import StockAnalyzer
from src.dimension_explainer import DIMENSION_EXPLANATIONS as DE


_NAMES = {
    "600036":"招商银行","000001":"平安银行","000333":"美的集团",
    "600519":"贵州茅台","002594":"比亚迪","601318":"中国平安",
    "600900":"长江电力","601012":"隆基绿能","600276":"恒瑞医药",
    "000858":"五粮液","002415":"海康威视","300750":"宁德时代",
    "600030":"中信证券","601398":"工商银行","601939":"建设银行",
    "601166":"兴业银行","600585":"海螺水泥","600887":"伊利股份",
    "600690":"海尔智家","000651":"格力电器","600309":"万华化学",
    "603259":"药明康德","603288":"海天味业","600436":"片仔癀",
    "600809":"山西汾酒","000568":"泸州老窖","002304":"洋河股份",
    "601628":"中国人寿","601601":"中国太保","601336":"新华保险",
    "601688":"华泰证券","002230":"科大讯飞","000725":"京东方A",
    "600570":"恒生电子","600588":"用友网络","002475":"立讯精密",
    "300760":"迈瑞医疗","000538":"云南白药","600085":"同仁堂",
    "600584":"长电科技","002241":"歌尔股份","002049":"紫光国微",
    "603986":"兆易创新","603501":"韦尔股份","002371":"北方华创",
    "688981":"中芯国际","688012":"中微公司","600118":"中国卫星",
    "000066":"中国长城","600186":"莲花控股","002081":"金螳螂",
    "688037":"芯源微","688347":"华虹公司","002407":"多氟多",
    "002709":"天赐材料","002812":"恩捷股份",
}


def main():
    parser = argparse.ArgumentParser(description="股智Alpha - 个股六维分析")
    parser.add_argument("--code", type=str, required=True)
    args = parser.parse_args()
    code = args.code
    stock_name = _NAMES.get(code, code)

    print("[DATA] 正在采集行情...", flush=True)
    ac = AshareCollector()
    df = ac.get_daily_hist(code, count=60)
    if df.empty:
        print(f"[FAIL] 无法获取 {code} 行情")
        return
    df["stock_code"] = code
    tech_df = add_technical_indicators(df)

    fc = FundFlowCollector()
    flow_df = fc.get_fund_flow(code, price_df=tech_df)

    sentiment = None
    fb = FutuBridge()
    try:
        sentiment = fb.get_sentiment(code)
    except Exception:
        pass

    analyzer = StockAnalyzer()
    result = analyzer.analyze(code, stock_name, tech_df,
        flow_df if len(flow_df) > 0 else None, sentiment)

    sep = "=" * 58

    # === 头部 ===
    print(f"\n{sep}")
    print(f"  {stock_name} ({code})  六维分析报告")
    print(f"  最新价: {result['latest_price']:.2f}  |  "
          f"综评: {result['avg_score']:.2f}  |  研判: {result['verdict']}")
    print(sep)

    # === 数据源注释 ===
    print(f"\n  [数据源] 行情: Ashare ✅  资金流: {'价量估算' if len(flow_df)==0 else 'akshare'}  "
          f"情绪: {'Futu' if sentiment else '无'}")
    print(f"  {'='*56}")

    # === 各维度 ===
    for dim in ["behavior","technical","fund_flow","momentum","risk","volume","sentiment"]:
        d = result["dimensions"].get(dim)
        if not d:
            continue
        bar = chr(9608) * int(d.score * 20) + chr(9617) * (20 - int(d.score * 20))
        info = DE.get(dim, {})
        name_str = info.get("name", dim)
        src_str = info.get("source", "")
        print(f"\n  {name_str}  |  {bar}  {d.score:.2f}")
        print(f"  -> {d.detail}")
        if "interpret" in info:
            interp = info["interpret"]
            if d.score >= 0.65:
                reading = interp["high"]
            elif d.score >= 0.35:
                reading = interp["mid"]
            else:
                reading = interp["low"]
            print(f"  [解读] {reading}")

    # === 风险 ===
    if result["risk_warnings"]:
        print(f"\n  [风险提示]")
        for w in result["risk_warnings"]:
            print(f"    ! {w}")

    # === 尾部 ===
    print(f"\n  [综合研判] {result['verdict']}")
    print(sep)
    print("  [声明] 本报告仅供参考，不构成投资建议。")
    print(sep)


if __name__ == "__main__":
    main()
