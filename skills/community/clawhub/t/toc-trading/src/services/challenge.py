"""
TOC Trading System - 挑战服务
"""
import uuid
from typing import Dict, List, Optional, Tuple
from datetime import datetime, date
from calendar import monthrange

class ChallengeService:
    """AI 股神挑战服务"""
    
    def __init__(self, storage):
        self.storage = storage
    
    def get_challenge(self) -> Dict:
        """获取当前挑战数据"""
        data = self.storage.load('challenge.json')
        if not data:
            return self._create_default_challenge()
        return data
    
    def _create_default_challenge(self) -> Dict:
        """创建默认挑战配置"""
        today = datetime.now()
        year = today.year
        month = today.month
        _, last_day = monthrange(year, month)
        
        return {
            'version': '1.0',
            'active': False,
            'period': f'{year}-{month:02d}',
            'start_date': f'{year}-{month:02d}-01',
            'end_date': f'{year}-{month:02d}-{last_day}',
            'initial_capital': 50000,
            'current_capital': 50000,
            'max_daily_trades': 3,
            'stop_loss_pct': -7,
            'trades_count': 0,
            'win_count': 0,
            'loss_count': 0,
            'win_rate': 0,
            'max_profit_trade': 0,
            'max_loss_trade': 0,
            'max_consecutive_wins': 0,
            'max_consecutive_losses': 0,
            'daily_trades': [],
            'equity_curve': [
                {'date': f'{year}-{month:02d}-01', 'capital': 50000}
            ],
            'created_at': datetime.now().isoformat()
        }
    
    def start_challenge(self) -> Tuple[bool, str]:
        """开启新一轮挑战"""
        today = datetime.now()
        year = today.year
        month = today.month
        _, last_day = monthrange(year, month)
        
        challenge = self._create_default_challenge()
        challenge['active'] = True
        challenge['period'] = f'{year}-{month:02d}'
        challenge['start_date'] = f'{year}-{month:02d}-01'
        challenge['end_date'] = f'{year}-{month:02d}-{last_day}'
        challenge['created_at'] = datetime.now().isoformat()
        
        self.storage.save('challenge.json', challenge)
        
        period_str = f'{year}年{month}月'
        return True, (
            f"🏆 AI股神挑战已开启！\n\n"
            f"初始资金：50,000 元\n"
            f"模拟周期：{period_str}\n"
            f"每日最大交易：3 笔\n"
            f"止损线：-7%\n\n"
            f"加油！期待你的表现 🎯"
        )
    
    def end_challenge(self) -> Tuple[bool, str]:
        """结束当前挑战"""
        challenge = self.get_challenge()
        if not challenge.get('active'):
            return False, "当前没有进行中的挑战"
        
        challenge['active'] = False
        
        # 计算最终收益
        initial = challenge.get('initial_capital', 50000)
        current = challenge.get('current_capital', 50000)
        profit = current - initial
        profit_rate = (profit / initial) * 100 if initial > 0 else 0
        
        # 统计
        trades_count = challenge.get('trades_count', 0)
        win_count = challenge.get('win_count', 0)
        win_rate = challenge.get('win_rate', 0)
        
        self.storage.save('challenge.json', challenge)
        
        return True, (
            f"🏆 挑战结束\n\n"
            f"最终资金：{current:,.0f} 元\n"
            f"总收益：{profit:+,.0f} 元 ({profit_rate:+.2f}%)\n\n"
            f"交易统计：\n"
            f"- 总交易次数：{trades_count}\n"
            f"- 盈利次数：{win_count}\n"
            f"- 胜率：{win_rate:.1f}%\n\n"
            f"🎉 感谢参与！"
        )
    
    def get_status(self) -> str:
        """获取挑战状态"""
        challenge = self.get_challenge()
        
        if not challenge.get('active'):
            return "🏆 AI股神挑战\n当前没有进行中的挑战\n\n输入「开启挑战」开始新一轮"
        
        initial = challenge.get('initial_capital', 50000)
        current = challenge.get('current_capital', 50000)
        profit = current - initial
        profit_rate = (profit / initial) * 100 if initial > 0 else 0
        
        period = challenge.get('period', '')
        trades_count = challenge.get('trades_count', 0)
        win_rate = challenge.get('win_rate', 0)
        max_daily = challenge.get('max_daily_trades', 3)
        
        # 检查今日交易次数
        today_str = datetime.now().strftime('%Y-%m-%d')
        today_trades = 0
        for daily in challenge.get('daily_trades', []):
            if daily.get('date') == today_str:
                today_trades = daily.get('count', 0)
        
        remaining_trades = max_daily - today_trades
        
        return (
            f"🏆 AI股神挑战\n"
            f"周期：{period}\n\n"
            f"💰 当前资金：{current:,.0f} 元\n"
            f"📊 总收益：{profit:+,.0f} 元 ({profit_rate:+.2f}%)\n\n"
            f"📈 交易统计：\n"
            f"- 总交易：{trades_count} 笔\n"
            f"- 胜率：{win_rate:.1f}%\n\n"
            f"📅 今日剩余交易：{remaining_trades}/{max_daily} 笔\n\n"
            f"止损线：-7%"
        )
    
    def get_stats(self) -> str:
        """获取详细统计"""
        challenge = self.get_challenge()
        
        initial = challenge.get('initial_capital', 50000)
        current = challenge.get('current_capital', 50000)
        profit = current - initial
        profit_rate = (profit / initial) * 100 if initial > 0 else 0
        
        trades_count = challenge.get('trades_count', 0)
        win_count = challenge.get('win_count', 0)
        loss_count = challenge.get('loss_count', 0)
        win_rate = challenge.get('win_rate', 0)
        max_profit = challenge.get('max_profit_trade', 0)
        max_loss = challenge.get('max_loss_trade', 0)
        max_wins = challenge.get('max_consecutive_wins', 0)
        max_losses = challenge.get('max_consecutive_losses', 0)
        
        return (
            f"📊 挑战详细统计\n\n"
            f"**资金情况**\n"
            f"- 初始资金：{initial:,.0f} 元\n"
            f"- 当前资金：{current:,.0f} 元\n"
            f"- 总收益：{profit:+,.0f} 元 ({profit_rate:+.2f}%)\n\n"
            f"**交易统计**\n"
            f"- 总交易：{trades_count} 笔\n"
            f"- 盈利：{win_count} 笔\n"
            f"- 亏损：{loss_count} 笔\n"
            f"- 胜率：{win_rate:.1f}%\n\n"
            f"**单笔记录**\n"
            f"- 最大盈利：{max_profit:+,.0f} 元\n"
            f"- 最大亏损：{max_loss:,.0f} 元\n\n"
            f"**连胜记录**\n"
            f"- 最大连盈：{max_wins} 天\n"
            f"- 最大连亏：{max_losses} 天"
        )
    
    def can_trade(self) -> Tuple[bool, str]:
        """检查是否可以交易"""
        challenge = self.get_challenge()
        
        if not challenge.get('active'):
            return False, "挑战未开启"
        
        today_str = datetime.now().strftime('%Y-%m-%d')
        max_daily = challenge.get('max_daily_trades', 3)
        
        today_trades = 0
        for daily in challenge.get('daily_trades', []):
            if daily.get('date') == today_str:
                today_trades = daily.get('count', 0)
        
        if today_trades >= max_daily:
            return False, f"今日交易次数已用完 ({max_daily}/{max_daily})"
        
        return True, f"今日剩余 {max_daily - today_trades}/{max_daily} 笔"
    
    def record_trade(self, trade: Dict) -> bool:
        """记录交易"""
        challenge = self.get_challenge()
        if not challenge.get('active'):
            return False
        
        today_str = datetime.now().strftime('%Y-%m-%d')
        
        # 更新每日交易计数
        daily_found = False
        for daily in challenge.get('daily_trades', []):
            if daily.get('date') == today_str:
                daily['count'] += 1
                daily['trades'].append(trade.get('id', ''))
                daily_found = True
                break
        
        if not daily_found:
            challenge.setdefault('daily_trades', []).append({
                'date': today_str,
                'count': 1,
                'trades': [trade.get('id', '')]
            })
        
        # 更新统计
        challenge['trades_count'] += 1
        
        # 更新资金曲线
        challenge.setdefault('equity_curve', []).append({
            'date': today_str,
            'capital': challenge.get('current_capital', 50000)
        })
        
        self.storage.save('challenge.json', challenge)
        return True
    
    def check_stop_loss(self, stock_code: str, current_price: float, buy_price: float) -> Tuple[bool, str]:
        """检查是否触发止损"""
        challenge = self.get_challenge()
        if not challenge.get('active'):
            return False, ""
        
        stop_loss_pct = challenge.get('stop_loss_pct', -7)
        loss_rate = ((current_price - buy_price) / buy_price) * 100
        
        if loss_rate <= stop_loss_pct:
            return True, (
                f"⚠️ 止损提醒【{stock_code}】\n"
                f"当前亏损：{loss_rate:.2f}%\n"
                f"已触及止损线：{stop_loss_pct}%\n"
                f"建议：考虑止损出场"
            )
        
        return False, ""
    
    def update_capital(self, amount: float) -> bool:
        """更新资金"""
        challenge = self.get_challenge()
        if not challenge.get('active'):
            return False
        
        current = challenge.get('current_capital', 50000)
        challenge['current_capital'] = current + amount
        
        self.storage.save('challenge.json', challenge)
        return True
    
    def format_equity_curve(self) -> str:
        """格式化资金曲线"""
        challenge = self.get_challenge()
        curve = challenge.get('equity_curve', [])
        
        if not curve:
            return "📈 资金曲线\n暂无数据"
        
        lines = ["📈 资金曲线"]
        
        for entry in curve[-10:]:  # 最近10条
            date_str = entry.get('date', '')
            capital = entry.get('capital', 0)
            lines.append(f"- {date_str}：{capital:,.0f} 元")
        
        return '\n'.join(lines)