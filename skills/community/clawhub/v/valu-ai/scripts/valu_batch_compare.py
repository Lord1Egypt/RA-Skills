"""
批量股票对比分析模块
支持最多5只股票的横向对比分析
"""

import pandas as pd
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

# ====================== 股票对比分析器 ======================
class StockComparator:
    """股票对比分析器"""

    def __init__(self):
        self.comparison_result = {}

    def compare_stocks(self, stock_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        对多只股票进行横向对比分析

        参数:
            stock_results: 股票分析结果列表，每只股票包含:
                - symbol: 股票代码
                - name: 股票名称
                - price_data: 价格数据
                - financial_data: 财务数据
                - valuation: 估值结果（如有）

        返回:
            对比分析结果
        """
        if len(stock_results) < 2:
            return {"error": "对比分析至少需要2只股票"}

        if len(stock_results) > 5:
            return {"error": "对比分析最多支持5只股票"}

        comparison = {
            "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "stocks_count": len(stock_results),
            "stocks": [s.get('symbol', 'N/A') for s in stock_results],
            "comparison": {}
        }

        # 1. 价格指标对比
        comparison["price_comparison"] = self._compare_prices(stock_results)

        # 2. 估值指标对比
        comparison["valuation_comparison"] = self._compare_valuations(stock_results)

        # 3. 财务指标对比
        comparison["financial_comparison"] = self._compare_financials(stock_results)

        # 4. 风险指标对比
        comparison["risk_comparison"] = self._compare_risks(stock_results)

        # 5. 综合评分与排名
        comparison["rankings"] = self._generate_rankings(stock_results, comparison)

        # 6. 投资亮点
        comparison["highlights"] = self._generate_highlights(stock_results, comparison)

        # 7. 可视化数据（用于生成图表）
        comparison["chart_data"] = self._prepare_chart_data(stock_results, comparison)

        self.comparison_result = comparison
        return comparison

    def _compare_prices(self, stock_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """价格指标对比"""
        price_data = []

        for stock in stock_results:
            info = {
                "symbol": stock.get('symbol', 'N/A'),
                "name": stock.get('name', stock.get('symbol', 'N/A')),
            }

            # 从price_data提取价格信息
            if 'price_data' in stock and stock['price_data'] is not None:
                df = stock['price_data']
                if isinstance(df, pd.DataFrame) and not df.empty:
                    # 获取最新价格
                    if 'close' in df.columns:
                        info['current_price'] = float(df['close'].iloc[-1])
                    elif '收盘' in df.columns:
                        info['current_price'] = float(df['收盘'].iloc[-1])

                    # 计算涨跌幅
                    if 'pctChg' in df.columns:
                        info['daily_change'] = float(df['pctChg'].iloc[-1])
                    elif '涨跌幅' in df.columns:
                        info['daily_change'] = float(df['涨跌幅'].iloc[-1])

                    # 计算52周高低
                    if 'high' in df.columns:
                        info['52w_high'] = float(df['high'].max())
                        info['52w_low'] = float(df['low'].min())
                        if info.get('current_price'):
                            info['distance_from_high'] = round(
                                (info['current_price'] - info['52w_high']) / info['52w_high'] * 100, 2
                            )

            price_data.append(info)

        return {
            "metrics": ["current_price", "daily_change", "52w_high", "52w_low", "distance_from_high"],
            "data": price_data
        }

    def _compare_valuations(self, stock_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """估值指标对比"""
        valuation_data = []

        for stock in stock_results:
            info = {
                "symbol": stock.get('symbol', 'N/A'),
                "name": stock.get('name', stock.get('symbol', 'N/A')),
            }

            # 从basic_info或financial_data提取估值指标
            if 'basic_info' in stock:
                basic = stock['basic_info']
                if isinstance(basic, dict):
                    info['pe_ratio'] = basic.get('市盈率') or basic.get('pe', 'N/A')
                    info['pb_ratio'] = basic.get('市净率') or basic.get('pb', 'N/A')
                    info['ps_ratio'] = basic.get('市销率') or basic.get('ps', 'N/A')
                    info['pcf_ratio'] = basic.get('市现率') or basic.get('pcf', 'N/A')
                    info['market_cap'] = basic.get('总市值') or basic.get('market_cap', 'N/A')

            valuation_data.append(info)

        return {
            "metrics": ["pe_ratio", "pb_ratio", "ps_ratio", "pcf_ratio", "market_cap"],
            "data": valuation_data,
            "description": {
                "pe_ratio": "市盈率，越低越便宜（相对估值）",
                "pb_ratio": "市净率，适合金融股",
                "ps_ratio": "市销率，适合成长股",
                "market_cap": "总市值"
            }
        }

    def _compare_financials(self, stock_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """财务指标对比"""
        financial_data = []

        for stock in stock_results:
            info = {
                "symbol": stock.get('symbol', 'N/A'),
                "name": stock.get('name', stock.get('symbol', 'N/A')),
            }

            # 从financial_data提取关键指标
            if 'financial_data' in stock and stock['financial_data'] is not None:
                df = stock['financial_data']
                if isinstance(df, pd.DataFrame) and not df.empty:
                    # 这里需要根据实际列名调整
                    # 常见的财务指标列名
                    possible_cols = {
                        'roe': ['净资产收益率', 'ROE', 'return_on_equity'],
                        'gross_margin': ['毛利率', 'gross_profit_margin'],
                        'net_margin': ['净利率', 'net_profit_margin'],
                        'revenue_growth': ['营收增长率', 'revenue_growth'],
                        'profit_growth': ['利润增长率', 'profit_growth'],
                    }

                    for metric, col_names in possible_cols.items():
                        for col in col_names:
                            if col in df.columns:
                                try:
                                    info[metric] = float(df[col].iloc[0])
                                    break
                                except:
                                    pass

            financial_data.append(info)

        return {
            "metrics": ["roe", "gross_margin", "net_margin", "revenue_growth", "profit_growth"],
            "data": financial_data,
            "description": {
                "roe": "净资产收益率（%），越高越好",
                "gross_margin": "毛利率（%），越高越好",
                "net_margin": "净利率（%），越高越好",
                "revenue_growth": "营收增长率（%），越高越好",
                "profit_growth": "利润增长率（%），越高越好"
            }
        }

    def _compare_risks(self, stock_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """风险指标对比"""
        risk_data = []

        for stock in stock_results:
            info = {
                "symbol": stock.get('symbol', 'N/A'),
                "name": stock.get('name', stock.get('symbol', 'N/A')),
            }

            # 从price_data计算风险指标
            if 'price_data' in stock and stock['price_data'] is not None:
                df = stock['price_data']
                if isinstance(df, pd.DataFrame) and not df.empty:
                    price_col = 'close' if 'close' in df.columns else '收盘'

                    if price_col in df.columns:
                        # 计算波动率（标准差）
                        returns = df[price_col].pct_change().dropna()
                        info['volatility'] = round(returns.std() * 100, 2) if len(returns) > 0 else 0

                        # 计算最大回撤
                        cumulative = (1 + returns).cumprod()
                        running_max = cumulative.expanding().max()
                        drawdown = (cumulative - running_max) / running_max
                        info['max_drawdown'] = round(drawdown.min() * 100, 2) if len(drawdown) > 0 else 0

            risk_data.append(info)

        return {
            "metrics": ["volatility", "max_drawdown"],
            "data": risk_data,
            "description": {
                "volatility": "波动率（%），越低越稳定",
                "max_drawdown": "最大回撤（%），越小风险越低"
            }
        }

    def _generate_rankings(self, stock_results: List[Dict[str, Any]], comparison: Dict) -> Dict[str, Any]:
        """生成综合排名"""
        rankings = {}

        # 估值排名（PE，越低越好）
        val_data = comparison["valuation_comparison"]["data"]
        pe_ratios = []
        for stock in val_data:
            pe = stock.get('pe_ratio')
            if pe is not None and pe != 'N/A':
                try:
                    pe_ratios.append((stock['symbol'], float(pe)))
                except:
                    pass

        if pe_ratios:
            pe_ratios.sort(key=lambda x: x[1])
            rankings['cheapest_valuation'] = {
                metric: [{"symbol": s[0], "value": s[1]} for s in pe_ratios[:3]]
                for metric in ['pe', 'pb', 'ps']
            }

        # 成长性排名
        fin_data = comparison["financial_comparison"]["data"]
        growth_scores = []
        for stock in fin_data:
            score = 0
            count = 0
            if stock.get('revenue_growth') and stock['revenue_growth'] != 'N/A':
                score += float(stock['revenue_growth'])
                count += 1
            if stock.get('profit_growth') and stock['profit_growth'] != 'N/A':
                score += float(stock['profit_growth'])
                count += 1
            if count > 0:
                growth_scores.append((stock['symbol'], round(score / count, 2)))

        if growth_scores:
            growth_scores.sort(key=lambda x: x[1], reverse=True)
            rankings['growth_leaders'] = [
                {"symbol": s[0], "score": s[1]} for s in growth_scores[:3]
            ]

        # 盈利能力排名
        roe_scores = []
        for stock in fin_data:
            roe = stock.get('roe')
            if roe and roe != 'N/A':
                try:
                    roe_scores.append((stock['symbol'], float(roe)))
                except:
                    pass

        if roe_scores:
            roe_scores.sort(key=lambda x: x[1], reverse=True)
            rankings['most_profitable'] = [
                {"symbol": s[0], "roe": s[1]} for s in roe_scores[:3]
            ]

        # 风险最低排名
        risk_data = comparison["risk_comparison"]["data"]
        low_risk = []
        for stock in risk_data:
            vol = stock.get('volatility', 999)
            if vol != 'N/A':
                low_risk.append((stock['symbol'], vol))

        if low_risk:
            low_risk.sort(key=lambda x: x[1])
            rankings['lowest_risk'] = [
                {"symbol": s[0], "volatility": s[1]} for s in low_risk[:3]
            ]

        return rankings

    def _generate_highlights(self, stock_results: List[Dict[str, Any]], comparison: Dict) -> List[str]:
        """生成投资亮点"""
        highlights = []

        # 1. 估值洼地
        val_data = comparison["valuation_comparison"]["data"]
        for stock in val_data:
            pe = stock.get('pe_ratio')
            if pe and pe != 'N/A':
                try:
                    pe_val = float(pe)
                    if pe_val < 15:
                        highlights.append(f"💎 {stock['name']}({stock['symbol']})估值较低，PE={pe_val:.1f}")
                except:
                    pass

        # 2. 高成长
        fin_data = comparison["financial_comparison"]["data"]
        for stock in fin_data:
            growth = stock.get('revenue_growth') or stock.get('profit_growth')
            if growth and growth != 'N/A':
                try:
                    growth_val = float(growth)
                    if growth_val > 20:
                        highlights.append(f"📈 {stock['name']}({stock['symbol']})成长性强，增长率={growth_val:.1f}%")
                except:
                    pass

        # 3. 高ROE
        for stock in fin_data:
            roe = stock.get('roe')
            if roe and roe != 'N/A':
                try:
                    roe_val = float(roe)
                    if roe_val > 15:
                        highlights.append(f"💰 {stock['name']}({stock['symbol']})盈利能力强，ROE={roe_val:.1f}%")
                except:
                    pass

        return highlights[:10]  # 最多10条

    def _prepare_chart_data(self, stock_results: List[Dict[str, Any]], comparison: Dict) -> Dict[str, Any]:
        """准备图表数据"""
        chart_data = {
            "valuation_bar": {},
            "financial_radar": {},
            "price_trend": {},
            "risk_scatter": {}
        }

        # 估值对比柱状图数据
        val_data = comparison["valuation_comparison"]["data"]
        chart_data["valuation_bar"] = {
            "labels": [s['symbol'] for s in val_data],
            "pe": [s.get('pe_ratio', 'N/A') for s in val_data],
            "pb": [s.get('pb_ratio', 'N/A') for s in val_data]
        }

        return chart_data

    def generate_comparison_report(self) -> str:
        """生成对比分析报告（Markdown格式）"""
        if not self.comparison_result:
            return "请先执行对比分析"

        comp = self.comparison_result
        report = f"""# 📊 股票对比分析报告

**生成时间**: {comp['generated_at']}  
**对比股票数**: {comp['stocks_count']} 只

---

## 一、股票列表

| 股票代码 | 名称 |
|---------|------|
"""

        for stock in comp['stocks']:
            report += f"| {stock} | - |\n"

        # 估值对比
        report += f"""
---

## 二、估值指标对比

| 指标 | 说明 |
|------|------|
"""

        val_comp = comp['comparison']['valuation_comparison']
        for metric, desc in val_comp['description'].items():
            report += f"| {metric} | {desc} |\n"

        report += f"\n| 股票 | PE | PB | PS | 市值 |\n"
        report += f"|------|-----|-----|-----|------|\n"

        for stock in val_comp['data']:
            pe = stock.get('pe_ratio', 'N/A')
            pb = stock.get('pb_ratio', 'N/A')
            ps = stock.get('ps_ratio', 'N/A')
            mc = stock.get('market_cap', 'N/A')
            report += f"| {stock['symbol']} | {pe} | {pb} | {ps} | {mc} |\n"

        # 财务对比
        fin_comp = comp['comparison']['financial_comparison']
        if fin_comp['data'][0] and any(fin_comp['data'][0].get(m) for m in ['roe', 'gross_margin', 'net_margin']):
            report += f"""
---

## 三、财务指标对比

| 股票 | ROE(%) | 毛利率(%) | 净利率(%) | 营收增长(%) | 利润增长(%) |
|------|--------|-----------|-----------|------------|------------|
"""

            for stock in fin_comp['data']:
                roe = stock.get('roe', 'N/A')
                gm = stock.get('gross_margin', 'N/A')
                nm = stock.get('net_margin', 'N/A')
                rg = stock.get('revenue_growth', 'N/A')
                pg = stock.get('profit_growth', 'N/A')
                report += f"| {stock['symbol']} | {roe} | {gm} | {nm} | {rg} | {pg} |\n"

        # 风险对比
        risk_comp = comp['comparison']['risk_comparison']
        report += f"""
---

## 四、风险指标对比

| 股票 | 波动率(%) | 最大回撤(%) |
|------|----------|------------|
"""

        for stock in risk_comp['data']:
            vol = stock.get('volatility', 'N/A')
            dd = stock.get('max_drawdown', 'N/A')
            report += f"| {stock['symbol']} | {vol} | {dd} |\n"

        # 排名
        rankings = comp['comparison']['rankings']
        if rankings:
            report += f"""
---

## 五、排名榜单

"""

            if 'cheapest_valuation' in rankings:
                report += "### 💎 估值最低TOP3\n\n"
                for item in rankings['cheapest_valuation'].get('pe', []):
                    report += f"- {item['symbol']}: PE={item['value']}\n"

            if 'growth_leaders' in rankings:
                report += "\n### 📈 成长性最强TOP3\n\n"
                for item in rankings['growth_leaders']:
                    report += f"- {item['symbol']}: 增长={item['score']}%\n"

            if 'most_profitable' in rankings:
                report += "\n### 💰 盈利能力最强TOP3\n\n"
                for item in rankings['most_profitable']:
                    report += f"- {item['symbol']}: ROE={item['roe']}%\n"

            if 'lowest_risk' in rankings:
                report += "\n### 🛡️ 风险最低TOP3\n\n"
                for item in rankings['lowest_risk']:
                    report += f"- {item['symbol']}: 波动率={item['volatility']}%\n"

        # 投资亮点
        highlights = comp['comparison']['highlights']
        if highlights:
            report += f"""
---

## 六、投资亮点

"""
            for h in highlights:
                report += f"- {h}\n"

        # 免责声明
        report += f"""
---

## ⚠️ 免责声明

本报告仅供参考，不构成任何投资建议。股票投资有风险，入市需谨慎。过往业绩不代表未来表现。数据来源：AKShare/Baostock/DeepSeek AI。

"""

        return report


# ====================== 便捷函数 ======================
def compare_stocks(stock_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """快捷函数：对比多只股票"""
    comparator = StockComparator()
    return comparator.compare_stocks(stock_results)


if __name__ == "__main__":
    # 测试代码
    # 模拟两只股票的数据
    test_stocks = [
        {
            "symbol": "600519",
            "name": "贵州茅台",
            "price_data": pd.DataFrame({
                'close': [1850, 1860, 1870, 1880, 1890],
                'high': [1860, 1870, 1880, 1890, 1900],
                'low': [1840, 1850, 1860, 1870, 1880],
                'pctChg': [1.2, 0.5, 0.8, 0.3, 0.6]
            }),
            "basic_info": {
                "pe": 35.5,
                "pb": 12.3,
                "ps": 25.6,
                "market_cap": "2.5万亿"
            },
            "financial_data": pd.DataFrame({
                '净资产收益率': [30.5, 29.8, 31.2],
                '毛利率': [91.5, 90.8, 91.2],
                '净利率': [50.2, 49.5, 50.8]
            })
        },
        {
            "symbol": "000858",
            "name": "五粮液",
            "price_data": pd.DataFrame({
                'close': [145, 146, 147, 148, 149],
                'high': [146, 147, 148, 149, 150],
                'low': [144, 145, 146, 147, 148],
                'pctChg': [0.8, 0.7, 0.6, 0.5, 0.4]
            }),
            "basic_info": {
                "pe": 22.5,
                "pb": 6.8,
                "ps": 12.3,
                "market_cap": "6000亿"
            },
            "financial_data": pd.DataFrame({
                '净资产收益率': [22.5, 21.8, 23.2],
                '毛利率': [75.2, 74.5, 75.8],
                '净利率': [35.2, 34.5, 35.8]
            })
        }
    ]

    print("=" * 60)
    print("股票对比分析测试")
    print("=" * 60)

    comparator = StockComparator()
    result = comparator.compare_stocks(test_stocks)

    print("\n📊 对比结果:")
    print(f"  股票数: {result['stocks_count']}")
    print(f"  股票列表: {result['stocks']}")

    print("\n📈 估值对比:")
    for stock in result['comparison']['valuation_comparison']['data']:
        print(f"  {stock['symbol']}: PE={stock.get('pe_ratio')}, PB={stock.get('pb_ratio')}")

    print("\n💰 财务对比:")
    for stock in result['comparison']['financial_comparison']['data']:
        print(f"  {stock['symbol']}: ROE={stock.get('roe')}, 毛利率={stock.get('gross_margin')}")

    print("\n📋 排名:")
    rankings = result['comparison']['rankings']
    if rankings.get('cheapest_valuation'):
        print(f"  估值最低: {rankings['cheapest_valuation']['pe']}")

    print("\n✨ 投资亮点:")
    for h in result['comparison']['highlights']:
        print(f"  {h}")

    print("\n" + "=" * 60)
    print("生成报告预览:")
    print("=" * 60)
    print(comparator.generate_comparison_report()[:1000] + "...")
