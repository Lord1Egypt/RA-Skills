"""
TOC Trading System - 监控与推送
"""
import os
import sys
from datetime import datetime, time

# 添加 src 目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.toc_app import TOCTTrading
from src.tushare_client import TushareClient

class Monitor:
    """监控系统"""
    
    def __init__(self):
        self.toc = TOCTTrading()
        self.tushare = TushareClient()
        self.last_check = None
    
    def is_trading_time(self) -> bool:
        """检查是否在交易时间"""
        now = datetime.now()
        current_time = now.time()
        
        # 工作日
        if now.weekday() >= 5:
            return False
        
        # 交易时间段：9:30-11:30, 13:00-15:00
        morning_start = time(9, 30)
        morning_end = time(11, 30)
        afternoon_start = time(13, 0)
        afternoon_end = time(15, 0)
        
        if morning_start <= current_time <= morning_end:
            return True
        if afternoon_start <= current_time <= afternoon_end:
            return True
        
        return False
    
    def check_alerts(self) -> list:
        """检查异动"""
        alerts = []
        
        # 获取持仓异动
        positions = self.toc.position.get_positions(with_profit=True)
        for pos in positions:
            code = pos.get('stock_code', '')
            name = pos.get('stock_name', '')
            
            # 检查涨跌幅
            change_pct = pos.get('profit_rate', 0)
            if abs(change_pct) >= 5:
                direction = "🔥 涨停" if change_pct > 0 else "⚠️ 跌停"
                alerts.append({
                    'type': 'price_alert',
                    'stock': name,
                    'code': code,
                    'message': f"{direction} {name} 日内涨跌 {change_pct:+.2f}%"
                })
            
            # 检查止损线
            challenge = self.toc.challenge.get_challenge()
            if challenge.get('active'):
                stop_loss = challenge.get('stop_loss_pct', -7)
                if change_pct <= stop_loss:
                    alerts.append({
                        'type': 'stop_loss',
                        'stock': name,
                        'code': code,
                        'message': f"⚠️ 止损提醒 {name} 已亏损 {change_pct:.2f}%，触及止损线"
                    })
        
        return alerts
    
    def get_market_summary(self) -> str:
        """获取市场简报"""
        if not self.tushare.is_available():
            return "⚠️ 数据服务暂不可用"
        
        try:
            # 获取涨停股
            limit_stocks = self.recommendation.get_limit_stocks(5)
            
            # 获取北向资金
            hsgt_stocks = self.recommendation.get_hsgt_stocks('in', 3)
            
            lines = ["📊 市场简报"]
            
            if limit_stocks:
                lines.append(f"\n🔥 今日涨停：{len(limit_stocks)} 只")
                for s in limit_stocks[:3]:
                    lines.append(f"  - {s['name']} {s['pct_chg']:.2f}%")
            else:
                lines.append("\n暂无涨停信息")
            
            if hsgt_stocks:
                lines.append(f"\n🟢 北向资金净买入 Top3：")
                for s in hsgt_stocks:
                    lines.append(f"  - {s['name']} 净买入 {s['净买入']/10000:.0f}万")
            
            return '\n'.join(lines)
        except Exception as e:
            return f"📊 市场简报\n获取失败：{str(e)}"
    
    def get_morning_report(self) -> str:
        """早盘报告"""
        lines = ["🌅 早盘播报"]
        lines.append(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # 挑战状态
        challenge = self.toc.challenge.get_challenge()
        if challenge.get('active'):
            capital = challenge.get('current_capital', 50000)
            profit = capital - challenge.get('initial_capital', 50000)
            profit_rate = (profit / challenge.get('initial_capital', 50000)) * 100
            lines.append(f"\n🏆 挑战状态：进行中")
            lines.append(f"当前资金：{capital:,.0f} 元 ({profit_rate:+.2f}%)")
        else:
            lines.append("\n🏆 挑战状态：未开启")
        
        # 持仓概览
        positions = self.toc.position.get_positions(with_profit=True)
        if positions:
            lines.append(f"\n📊 持仓概览：共 {len(positions)} 只")
            for p in positions[:3]:
                lines.append(f"  - {p.get('stock_name')} {p.get('profit_rate', 0):+.2f}%")
        else:
            lines.append("\n📊 持仓概览：空仓")
        
        # 市场信号
        lines.append("\n📈 今日信号：")
        limit_stocks = self.toc.recommendation.get_limit_stocks(3)
        if limit_stocks:
            lines.append(f"  涨停 {len(self.toc.tushare.get_limit_list())} 只")
        
        return '\n'.join(lines)
    
    def get_closing_report(self) -> str:
        """收盘报告"""
        lines = ["🌙 收盘总结"]
        lines.append(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # 挑战状态
        challenge = self.toc.challenge.get_challenge()
        if challenge.get('active'):
            capital = challenge.get('current_capital', 50000)
            initial = challenge.get('initial_capital', 50000)
            profit = capital - initial
            profit_rate = (profit / initial) * 100
            trades = challenge.get('trades_count', 0)
            win_rate = challenge.get('win_rate', 0)
            
            lines.append(f"\n🏆 挑战月度报告：")
            lines.append(f"  资金：{capital:,.0f} 元 ({profit_rate:+.2f}%)")
            lines.append(f"  交易：{trades} 笔")
            lines.append(f"  胜率：{win_rate:.1f}%")
        
        # 持仓收益
        positions = self.toc.position.get_positions(with_profit=True)
        if positions:
            total_profit, total_rate = self.toc.position.get_total_profit()
            lines.append(f"\n💰 持仓收益：{total_profit:+,.0f} 元 ({total_rate:+.2f}%)")
            
            for p in positions:
                name = p.get('stock_name', '')
                profit = p.get('profit', 0)
                rate = p.get('profit_rate', 0)
                lines.append(f"  - {name} {profit:+,.0f} ({rate:+.2f}%)")
        
        return '\n'.join(lines)
    
    def format_alert(self, alerts: list) -> str:
        """格式化提醒"""
        if not alerts:
            return ""
        
        lines = ["🚨 异动提醒"]
        for alert in alerts:
            lines.append(f"\n{alert.get('message', '')}")
        
        return '\n'.join(lines)


def run_heartbeat():
    """心跳任务"""
    monitor = Monitor()
    
    now = datetime.now()
    current_time = now.time()
    
    reports = []
    
    # 定时推送
    morning_time = time(9, 30)
    noon_time = time(13, 0)
    evening_time = time(15, 30)
    
    # 早盘推送
    if abs((current_time.hour * 60 + current_time.minute) - (morning_time.hour * 60 + morning_time.minute)) <= 5:
        reports.append(monitor.get_morning_report())
    
    # 午盘推送
    if abs((current_time.hour * 60 + current_time.minute) - (noon_time.hour * 60 + noon_time.minute)) <= 5:
        reports.append(monitor.get_market_summary())
    
    # 收盘推送
    if abs((current_time.hour * 60 + current_time.minute) - (evening_time.hour * 60 + evening_time.minute)) <= 5:
        reports.append(monitor.get_closing_report())
    
    # 异动提醒
    if monitor.is_trading_time():
        alerts = monitor.check_alerts()
        if alerts:
            reports.append(monitor.format_alert(alerts))
    
    return '\n\n'.join(reports) if reports else None


if __name__ == '__main__':
    result = run_heartbeat()
    if result:
        print(result)
    else:
        print("HEARTBEAT_OK")