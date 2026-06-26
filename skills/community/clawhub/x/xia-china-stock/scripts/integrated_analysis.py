#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合分析报告生成器
整合：统一数据源管理器 + 技术指标 + 统一资讯搜索
"""

import sys
import os
import json
import time
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# 添加路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

# 导入本地模块
from technical_indicators import TechnicalAnalyzer
from analysis_scratchpad import AnalysisScratchpad

# 导入资讯搜索模块
try:
    from news_search import NewsSearchManager, search_stock_news
    NEWS_SEARCH_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ 资讯搜索模块导入失败: {e}")
    NEWS_SEARCH_AVAILABLE = False

# MX data is not required for the published version (free data sources only)
MX_DATA_AVAILABLE = False


# 默认监控标的
DEFAULT_STOCKS = [
    ('002475.SZ', '立讯精密', '消费电子'),
    ('002594.SZ', '比亚迪', '新能源汽车'),
    ('688180.SH', '君实生物', '生物医药'),
    ('603893.SH', '瑞芯微', '半导体'),
    ('600938.SH', '中国海油', '石油'),
    ('688981.SH', '中芯国际', '半导体'),
    ('600276.SH', '恒瑞医药', '创新药'),
]

# 行业板块分类
SECTORS = {
    '消费电子': ['立讯精密', '京东方A', '歌尔股份'],
    '新能源汽车': ['比亚迪', '宁德时代', '理想汽车'],
    '半导体': ['中芯国际', '瑞芯微', '韦尔股份'],
    '生物医药': ['恒瑞医药', '君实生物', '药明康德'],
    '石油': ['中国海油', '中国石油', '中国石化'],
}


class IntegratedAnalyzer:
    """综合分析器（使用统一数据源和资讯搜索）"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.mx_data = None
        self.news_manager = None
        self.scratchpad = AnalysisScratchpad()
        
        # Initialize news search manager
        if NEWS_SEARCH_AVAILABLE:
            try:
                self.news_manager = NewsSearchManager()
            except Exception as e:
                print(f"News search init failed: {e}")
    
    def get_sector(self, name: str) -> str:
        """获取股票所属板块"""
        for sector, stocks in SECTORS.items():
            if name in stocks:
                return sector
        return '其他'
    
    # ==================== 技术分析 (本地) ====================
    
    def analyze_technical(self, symbol: str, name: str) -> Dict:
        """技术指标分析"""
        t0 = time.time()
        try:
            analyzer = TechnicalAnalyzer(symbol, period="3mo")
            result = analyzer.run_analysis()
            duration = int((time.time() - t0) * 1000)
            
            if not result:
                self.scratchpad.record_step('technical', name, '技术分析', False,
                                           error='获取数据失败', duration_ms=duration)
                return {'error': '获取数据失败', 'symbol': symbol, 'name': name}
            
            ind = result['indicators']
            trend = result['trend']
            
            tech_result = {
                'symbol': symbol,
                'name': name,
                'price': result['price'],
                'source': result['source'],
                'volume': ind['VOLUME']['volume'],
                'vol_ratio': ind['VOLUME']['vol_ratio'],
                'ma_status': self._format_ma_status(ind['MA']['status']),
                'macd': {
                    'dif': ind['MACD']['DIF'],
                    'dea': ind['MACD']['DEA'],
                    'macd': ind['MACD']['MACD'],
                    'signal': '多头' if ind['MACD']['MACD'] > 0 else '空头'
                },
                'rsi': ind['RSI']['RSI14'],
                'rsi_signal': self._get_rsi_signal(ind['RSI']['RSI14']),
                'kdj': {
                    'k': ind['KDJ']['K'],
                    'd': ind['KDJ']['D'],
                    'j': ind['KDJ']['J'],
                    'signal': '金叉' if ind['KDJ']['K'] > ind['KDJ']['D'] else '死叉'
                },
                'boll': {
                    'upper': ind['BOLL']['upper'],
                    'mid': ind['BOLL']['mid'],
                    'lower': ind['BOLL']['lower'],
                    'position': ind['BOLL']['price_position']
                },
                'trend': trend,
                'signals': result['signals']
            }
            
            # 数据质量验证
            quality = self.scratchpad.validate_data_quality('technical', name, tech_result)
            self.scratchpad.record_step('technical', name, '技术分析', True,
                                       data=tech_result, duration_ms=duration)
            
            return tech_result
            
        except Exception as e:
            duration = int((time.time() - t0) * 1000)
            self.scratchpad.record_step('technical', name, '技术分析', False,
                                       error=str(e), duration_ms=duration)
            return {'error': str(e), 'symbol': symbol, 'name': name}
    
    def _format_ma_status(self, ma_status: dict) -> str:
        """格式化均线状态"""
        parts = []
        for ma in ['MA5', 'MA10', 'MA20']:
            if ma in ma_status:
                pos = ma_status[ma].get('position', '未知')
                parts.append(f"{ma}({pos})")
        return ' | '.join(parts)
    
    def _get_rsi_signal(self, rsi: float) -> str:
        """RSI信号判断"""
        if rsi > 80:
            return '严重超买'
        elif rsi > 70:
            return '超买'
        elif rsi < 20:
            return '严重超卖'
        elif rsi < 30:
            return '超卖'
        else:
            return '正常'
    
    # ==================== Financial Data (Sina + Akshare) ====================
    
    def get_financial_data(self, name: str, symbol: str = '') -> Dict:
        """Get financial data from free sources"""
        try:
            from sina_finance import fetch_realtime_quote
            
            code = symbol.replace('.SZ', '').replace('.SH', '').replace('.SS', '') if symbol else name
            quote = fetch_realtime_quote(code)
            
            if quote:
                return {
                    'name': quote['name'],
                    'price': quote['close'],
                    'change_pct': quote['change_pct'],
                    'volume': quote['volume'],
                    'amount': quote['amount'],
                    'high': quote['high'],
                    'low': quote['low'],
                    'open': quote['open']
                }
            else:
                return {'error': 'Failed to fetch financial data'}
                
        except Exception as e:
            return {'error': str(e)}
    
    # ==================== 资讯搜索（统一管理器） ====================
    
    def get_news(self, name: str, symbol: str = '') -> Dict:
        """获取相关资讯（使用统一资讯搜索）"""
        if not self.news_manager:
            return {'error': '资讯搜索未配置'}
        
        try:
            # 使用统一资讯搜索
            result = search_stock_news(symbol, name, max_results=3, api_key=self.api_key)
            
            if not result:
                return {'error': '未找到相关资讯'}
            
            # 格式化结果
            formatted = {}
            for item in result.get('items', []):
                title = item.get('title', '')
                if title:
                    content_lines = [f"**{title}**"]
                    
                    meta = []
                    if item.get('source'):
                        meta.append(item['source'])
                    if item.get('rating'):
                        meta.append(f"评级:{item['rating']}")
                    if item.get('date'):
                        meta.append(item['date'])
                    
                    if meta:
                        content_lines.append(' | '.join(meta))
                    
                    if item.get('content'):
                        content_lines.append(item['content'][:300])
                    
                    formatted[title] = '\n'.join(content_lines)
            
            return formatted
            
        except Exception as e:
            return {'error': str(e)}
    
    # ==================== 综合分析 ====================
    
    def analyze_stock(self, symbol: str, name: str, sector: str, 
                      include_financial: bool = True,
                      include_news: bool = True) -> Dict:
        """综合分析单只股票"""
        result = {
            'symbol': symbol,
            'name': name,
            'sector': sector,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 1. 技术分析（必须，使用统一数据源管理器）
        print(f"  📊 技术分析: {name}...")
        tech = self.analyze_technical(symbol, name)
        result['technical'] = tech
        
        # 2. 财务数据（可选）
        if include_financial and self.mx_data:
            print(f"  💰 财务数据: {name}...")
            t0 = time.time()
            result['financial'] = self.get_financial_data(name)
            duration = int((time.time() - t0) * 1000)
            quality = self.scratchpad.validate_data_quality('financial', name, result['financial'])
            self.scratchpad.record_step('financial', name, '财务数据',
                                       quality['passed'], data=result['financial'], duration_ms=duration)
        else:
            result['financial'] = {'skipped': True}
        
        # 3. 资讯背景（可选，使用统一资讯搜索）
        if include_news and self.news_manager:
            print(f"  📰 资讯搜索: {name}...")
            t0 = time.time()
            result['news'] = self.get_news(name, symbol)
            duration = int((time.time() - t0) * 1000)
            quality = self.scratchpad.validate_data_quality('news', name, result['news'])
            self.scratchpad.record_step('news', name, '资讯搜索',
                                       quality['passed'], data=result['news'], duration_ms=duration)
        else:
            result['news'] = {'skipped': True}
        
        # 4. 综合建议
        result['recommendation'] = self._generate_recommendation(result)
        
        return result
    
    def _generate_recommendation(self, result: Dict) -> Dict:
        """生成综合建议"""
        tech = result.get('technical', {})
        if 'error' in tech:
            return {'action': '无法判断', 'reason': '技术数据获取失败'}
        
        trend = tech.get('trend', {})
        score = trend.get('score', 0)
        signals = tech.get('signals', [])
        rsi = tech.get('rsi', 50)
        
        # 统计信号
        bullish = sum(1 for s in signals if '买入' in s[1] or '看涨' in s[1] or '偏多' in s[1])
        bearish = sum(1 for s in signals if '卖出' in s[1] or '看跌' in s[1] or '偏空' in s[1])
        
        # 综合判断
        reasons = []
        risks = []
        
        # 趋势判断
        if score >= 30:
            reasons.append(f"技术面偏多(分数{score})")
        elif score <= -30:
            reasons.append(f"技术面偏空(分数{score})")
        else:
            reasons.append(f"技术面震荡(分数{score})")
        
        # 信号判断
        if bullish >= 2:
            reasons.append(f"{bullish}个看多信号")
        elif bearish >= 2:
            reasons.append(f"{bearish}个看空信号")
        
        # RSI判断
        if rsi > 70:
            risks.append(f"RSI超买({rsi:.1f})")
        elif rsi < 30:
            risks.append(f"RSI超卖({rsi:.1f})")
        
        # MACD判断
        macd = tech.get('macd', {})
        if macd.get('macd', 0) < 0:
            risks.append("MACD空头排列")
        
        # 生成建议
        if score >= 30 and bullish >= 2:
            action = '买入'
            strategy = "可考虑分批建仓，止损设在近期支撑位"
        elif score <= -30 and bearish >= 2:
            action = '卖出'
            strategy = "建议减仓或观望，等待企稳信号"
        elif rsi > 70:
            action = '减仓'
            strategy = "可部分止盈，锁定收益"
        elif rsi < 30:
            action = '关注'
            strategy = "可小仓位试探，等待确认信号"
        else:
            action = '持有'
            strategy = "等待方向明确后再操作"
        
        return {
            'action': action,
            'reasons': reasons,
            'risks': risks,
            'strategy': strategy,
            'trend_score': score,
            'bullish_signals': bullish,
            'bearish_signals': bearish
        }


def generate_report(results: List[Dict], format: str = 'markdown',
                    scratchpad: Optional['AnalysisScratchpad'] = None) -> str:
    """生成综合分析报告"""
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    if format == 'json':
        return json.dumps({
            'date': date_str,
            'type': '综合分析报告',
            'stocks': results
        }, ensure_ascii=False, indent=2)
    
    # Markdown报告
    md = f"""# 📊 综合分析报告

**生成时间**: {date_str}  
**分析股票数**: {len(results)}  
**数据来源**: 本地技术分析 + 东方财富妙想API

---

## 📈 市场概览

| 股票 | 代码 | 板块 | 现价 | 趋势 | 建议 |
|------|------|------|------|------|------|
"""
    
    for r in results:
        tech = r.get('technical', {})
        rec = r.get('recommendation', {})
        
        if 'error' in tech:
            md += f"| {r['name']} | {r['symbol']} | {r['sector']} | - | ❌ | - |\n"
        else:
            trend = tech.get('trend', {})
            action = rec.get('action', '持有')
            action_emoji = {'买入': '🟢', '持有': '🟡', '卖出': '🔴', '减仓': '🟠', '关注': '🔵'}.get(action, '⚪')
            price = tech.get('price', '-')
            md += f"| {r['name']} | {r['symbol']} | {r['sector']} | {price} | {trend.get('emoji', '-')} | {action_emoji}{action} |\n"
    
    # 每只股票详细分析
    for r in results:
        tech = r.get('technical', {})
        rec = r.get('recommendation', {})
        fin = r.get('financial', {})
        news = r.get('news', {})
        
        if 'error' in tech:
            md += f"""
---

## ❌ {r['name']} ({r['symbol']})

**状态**: 技术数据获取失败

"""
            continue
        
        action_emoji = {'买入': '🟢', '持有': '🟡', '卖出': '🔴', '减仓': '🟠', '关注': '🔵'}.get(rec.get('action', '持有'), '⚪')
        
        md += f"""
---

## 📋 {r['name']} ({r['symbol']})

**所属板块**: {r['sector']}  
**当前价格**: {tech.get('price', '-')}  
**分析时间**: {r.get('timestamp', '-')}

### 📊 技术指标

| 指标 | 数值 | 信号 |
|------|------|------|
| **趋势分数** | {tech.get('trend', {}).get('score', 0)} | {tech.get('trend', {}).get('trend', '-')} |
| **均线状态** | {tech.get('ma_status', '-')} | - |
| **MACD** | DIF: {tech.get('macd', {}).get('dif', 0):.2f}, DEA: {tech.get('macd', {}).get('dea', 0):.2f} | {tech.get('macd', {}).get('signal', '-')} |
| **RSI(14)** | {tech.get('rsi', 0):.2f} | {tech.get('rsi_signal', '-')} |
| **KDJ** | K: {tech.get('kdj', {}).get('k', 0):.2f}, D: {tech.get('kdj', {}).get('d', 0):.2f} | {tech.get('kdj', {}).get('signal', '-')} |
| **布林带** | 位置: {tech.get('boll', {}).get('position', 0):.0f}% | - |

### 💡 综合建议

**建议**: {action_emoji} **{rec.get('action', '持有')}**

**判断依据**:
"""
        for reason in rec.get('reasons', []):
            md += f"- {reason}\n"
        
        if rec.get('risks'):
            md += "\n**风险提示**:\n"
            for risk in rec['risks']:
                md += f"- ⚠️ {risk}\n"
        
        md += f"\n**操作策略**: {rec.get('strategy', '-')}\n"
        
        # 财务数据摘要
        if not fin.get('error') and not fin.get('skipped'):
            md += "\n### 💰 财务数据\n\n"
            md += "*(详细数据见附件)*\n"
        
        # 资讯摘要
        if not news.get('error') and not news.get('skipped'):
            md += "\n### 📰 相关资讯\n\n"
            for query, content in news.items():
                if query != 'error' and content:
                    md += f"**{query}**:\n{content}\n\n"
    
    md += """
---

## ⚠️ 免责声明

本报告仅供参考，不构成投资建议。投资有风险，入市需谨慎。

---

*🦞 由虾总工综合分析系统生成*
*数据来源: 本地技术分析 + 东方财富妙想API*
"""
    
    # 追加数据质量报告页脚
    if scratchpad:
        md += scratchpad.get_report_footer()
    
    return md


def main():
    parser = argparse.ArgumentParser(description='综合分析报告生成器')
    parser.add_argument('--stocks', nargs='+', help='自定义股票 (格式: 代码.名称.板块)')
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--no-financial', action='store_true', help='跳过财务数据')
    parser.add_argument('--no-news', action='store_true', help='跳过资讯搜索')
    
    args = parser.parse_args()
    
    # 解析股票列表
    if args.stocks:
        stocks = []
        for s in args.stocks:
            if ',' in s:
                parts = s.split(',')
            else:
                parts = s.split('|')  # 用 | 分隔，避免与代码中的 . 冲突
            
            if len(parts) >= 2:
                code = parts[0].strip()  # 完整代码如 002475.SZ
                name = parts[1].strip()
                sector = parts[2].strip() if len(parts) > 2 else '其他'
                stocks.append((code, name, sector))
            else:
                stocks.append((s, s, '其他'))
    else:
        stocks = DEFAULT_STOCKS
    
    print(f"🔄 正在分析 {len(stocks)} 只股票...")
    print(f"   技术分析: ✅")
    print(f"   财务数据: {'❌' if args.no_financial else '✅'}")
    print(f"   资讯搜索: {'❌' if args.no_news else '✅'}")
    print()
    
    # 初始化分析器
    analyzer = IntegratedAnalyzer()
    
    # 分析每只股票
    results = []
    for symbol, name, sector in stocks:
        print(f"分析 {name} ({symbol})...")
        result = analyzer.analyze_stock(
            symbol, name, sector,
            include_financial=not args.no_financial,
            include_news=not args.no_news
        )
        results.append(result)
        print()
    
    # 生成报告
    report = generate_report(results, args.format, scratchpad=analyzer.scratchpad)
    
    # 保存分析日志
    log_path = analyzer.scratchpad.save_log()
    print(f"📋 分析日志: {log_path}")
    if analyzer.scratchpad.warnings:
        print(f"⚠️ {len(analyzer.scratchpad.warnings)}个警告")
    
    # 输出
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)  # 自动创建目录
        output_path.write_text(report, encoding='utf-8')
        print(f"\n✅ 报告已保存到: {args.output}")
    else:
        print("\n" + "="*60)
        print(report)


if __name__ == '__main__':
    main()
