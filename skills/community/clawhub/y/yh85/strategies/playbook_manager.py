#!/usr/bin/env python3
"""
Playbook Manager — YH8.5 策略参数进化管理器
=============================================
- 加载/保存 Playbook JSON
- 记录每笔交易复盘(reflection)
- 查询策略参数 + 进化边界
- 自动生成进化建议 (V3)
2026-07-10 v1: 基础Playbook + reflection存储
"""
import os, json, time
from datetime import datetime, timezone

DIR = os.path.dirname(os.path.abspath(__file__))
PLAYBOOK_PATH = os.path.join(DIR, 'playbook.json')


class PlaybookManager:
    """Playbook 管理器 — 单例模式, 热加载策略参数"""
    
    _instance = None
    _last_load = 0
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._loaded = None
            cls._instance._last_load = 0
        return cls._instance
    
    @property
    def data(self):
        """热加载: 每10秒检查文件更新"""
        now = time.time()
        if self._loaded is None or now - self._last_load > 10:
            try:
                with open(PLAYBOOK_PATH) as f:
                    self._loaded = json.load(f)
                self._apply_param_overrides(self._loaded)
                self._last_load = now
            except Exception:
                if self._loaded is None:
                    self._loaded = {'strategies': {}, 'coin_assignments': {}, 'trade_reflections': []}
        return self._loaded

    @staticmethod
    def _apply_param_overrides(data):
        """从 strategy_params.json 覆盖策略参数（付费订阅版提供回测调优的真实参数）"""
        p = os.path.join(os.path.dirname(DIR), 'strategy_params.json')
        if not os.path.exists(p):
            return
        try:
            with open(p) as f:
                overrides = json.load(f)
            for sid, params in overrides.items():
                if sid == 'engine':
                    continue
                if sid in data.get('strategies', {}):
                    data['strategies'][sid].setdefault('params', {}).update(params)
        except Exception:
            pass
    
    def _save(self):
        with open(PLAYBOOK_PATH, 'w') as f:
            json.dump(self._loaded, f, indent=2, ensure_ascii=False, default=str)
        self._last_load = time.time()
    
    # ═══ 策略查询 ═══
    def get_strategy(self, strategy_id):
        """获取策略定义"""
        return self.data.get('strategies', {}).get(strategy_id)
    
    def get_params(self, strategy_id):
        """获取策略参数"""
        s = self.get_strategy(strategy_id)
        return s.get('params', {}) if s else {}
    
    def get_evolution_bounds(self, strategy_id):
        """获取参数进化边界"""
        s = self.get_strategy(strategy_id)
        return s.get('evolution_bounds', {}) if s else {}
    
    def get_coin_strategy(self, symbol, market='trend'):
        """查询某币在某市场状态下的策略ID"""
        assignments = self.data.get('coin_assignments', {})
        coin = assignments.get(symbol, {})
        return coin.get(market)
    
    def is_coin_enabled(self, symbol):
        """检查币种是否在任何池中"""
        assignments = self.data.get('coin_assignments', {})
        if symbol not in assignments: return False
        coin = assignments[symbol]
        return coin.get('trend') is not None or coin.get('range') is not None
    
    # ═══ 策略池查询 ═══
    def get_trend_coins(self):
        """获取趋势池所有币种 (按策略分组)"""
        result = {}
        for sym, assign in self.data.get('coin_assignments', {}).items():
            sid = assign.get('trend')
            if sid:
                result.setdefault(sid, []).append(sym)
        return result
    
    def get_range_coins(self):
        """获取震荡池所有币种 (按策略分组)"""
        result = {}
        for sym, assign in self.data.get('coin_assignments', {}).items():
            sid = assign.get('range')
            if sid:
                result.setdefault(sid, []).append(sym)
        return result
    
    def get_all_active_coins(self):
        """获取所有激活币种"""
        return [sym for sym, a in self.data.get('coin_assignments', {}).items()
                if a.get('trend') or a.get('range')]
    
    # ═══ 性能追踪 ═══
    def get_performance(self, strategy_id=None):
        """查询策略性能"""
        perf = self.data.get('performance', {})
        return perf.get(strategy_id) if strategy_id else perf
    
    def update_performance(self, strategy_id, pnl, is_win):
        """实时更新性能统计"""
        d = self.data  # 触发加载
        if 'performance' not in d:
            d['performance'] = {}
        p = d['performance'].setdefault(strategy_id, {
            'trades': 0, 'wins': 0, 'losses': 0, 'total_pnl': 0.0, 'total_pnl_pct': 0.0
        })
        p['trades'] = p.get('trades', 0) + 1
        if is_win:
            p['wins'] = p.get('wins', 0) + 1
        else:
            p['losses'] = p.get('losses', 0) + 1
        p['total_pnl'] = round(p.get('total_pnl', 0) + pnl, 4)
        p['total_pnl_pct'] = round(p.get('total_pnl_pct', 0) + pnl, 4)  # pnl=百分比
        p['win_rate'] = round(p['wins'] / p['trades'] * 100, 1)
        self._save()
    
    # ═══ 交易复盘 ═══
    def record_reflection(self, **kwargs):
        """
        记录平仓复盘
        字段: symbol, side, entry, exit, pnl, pnl_pct, strategy_id,
              reason, open_time, exit_time, hold_hours, regime, auto_summary
        """
        entry = {
            'time': datetime.now(timezone.utc).isoformat(),
            'symbol': kwargs.get('symbol', '?'),
            'side': kwargs.get('side', '?'),
            'entry': kwargs.get('entry', 0),
            'exit': kwargs.get('exit', 0),
            'pnl': round(kwargs.get('pnl', 0), 4),
            'pnl_pct': round(kwargs.get('pnl_pct', 0), 4),
            'strategy_id': kwargs.get('strategy_id', 'unknown'),
            'reason': kwargs.get('reason', '?'),
            'open_time': kwargs.get('open_time', ''),
            'exit_time': kwargs.get('exit_time', ''),
            'hold_hours': round(kwargs.get('hold_hours', 0), 2),
            'regime': kwargs.get('regime', '?'),
            'outcome': 'win' if kwargs.get('pnl', 0) > 0 else 'loss',
            'tags': kwargs.get('tags', []),
        }
        
        # 自动生成经验总结
        summary = self._auto_summarize(entry)
        entry['auto_summary'] = summary
        
        d = self.data  # 确保加载
        if 'trade_reflections' not in d:
            d['trade_reflections'] = []
        d['trade_reflections'].insert(0, entry)
        # 保留最近500条
        d['trade_reflections'] = d['trade_reflections'][:500]
        
        # 更新性能
        self.update_performance(entry['strategy_id'], entry['pnl_pct'], entry['outcome'] == 'win')
        self._save()
        
        return entry
    
    def _auto_summarize(self, entry):
        """自动生成中文复盘摘要"""
        sym = entry['symbol'].replace('/USDT', '')
        side_cn = '做多' if entry['side'] == 'long' else '做空'
        pnl = entry['pnl']
        hold = entry['hold_hours']
        reason = entry['reason']
        
        if pnl > 0:
            return f"{sym} {side_cn} 获利{pnl:+.2f}U, 持{hold:.1f}h, {reason}离场"
        elif pnl < 0:
            return f"{sym} {side_cn} 亏损{pnl:+.2f}U, 持{hold:.1f}h, {reason}触发"
        else:
            return f"{sym} {side_cn} 保本平仓, 持{hold:.1f}h, {reason}"
    
    def get_recent_reflections(self, limit=20, strategy_id=None):
        """获取最近复盘记录"""
        reflections = self.data.get('trade_reflections', [])
        if strategy_id:
            reflections = [r for r in reflections if r.get('strategy_id') == strategy_id]
        return reflections[:limit]
    
    def get_coin_reflections(self, symbol, limit=20):
        """获取某币的复盘记录"""
        sym = symbol.replace('/USDT', '')
        reflections = self.data.get('trade_reflections', [])
        return [r for r in reflections if r.get('symbol','').replace('/USDT','') == sym][:limit]
    
    # ═══ 进化触发 ═══
    def should_evolve(self, strategy_id, min_trades=10, max_interval_hours=72):
        """判断是否触发进化: 交易数达标 或 时间到"""
        reflections = self.get_recent_reflections(strategy_id=strategy_id)
        trades_since = len([r for r in reflections if r.get('evolved', False) == False])
        
        if trades_since >= min_trades:
            return True, f"累计{trades_since}笔未进化交易"
        
        # 检查时间间隔
        evo_log = self.data.get('evolution_log', [])
        last_evo = None
        for e in reversed(evo_log):
            if e.get('strategy_id') == strategy_id:
                last_evo = e
                break
        
        if last_evo:
            try:
                last_time = datetime.fromisoformat(last_evo['time'].replace('+08',''))
                if (datetime.now(timezone.utc) - last_time.replace(tzinfo=timezone.utc)).total_seconds() / 3600 > max_interval_hours:
                    return True, f"距上次进化超{max_interval_hours}h"
            except: pass
        
        return False, f"仅{trades_since}笔, 未触发"
    
    def log_evolution(self, strategy_id, changes, based_on_trades):
        """记录进化事件"""
        evo = {
            'version': len(self.data.get('evolution_log', [])) + 1,
            'time': datetime.now(timezone.utc).isoformat(),
            'strategy_id': strategy_id,
            'trigger': 'auto' if based_on_trades >= 10 else 'manual',
            'changes': changes,
            'based_on_trades': based_on_trades,
        }
        d = self.data
        if 'evolution_log' not in d:
            d['evolution_log'] = []
        d['evolution_log'].append(evo)
        d['_meta']['version'] = evo['version']
        self._save()
        return evo
    
    # ═══ 统计面板 ═══
    def dashboard(self):
        """生成Playbook仪表板摘要"""
        lines = []
        lines.append("🎯 YH8.5 Playbook 仪表板 v{}".format(self.data.get('_meta', {}).get('version', 1)))
        lines.append("")
        
        for sid, strat in self.data.get('strategies', {}).items():
            perf = self.data.get('performance', {}).get(sid, {})
            lines.append(f"  {strat['name']}")
            lines.append(f"    参: {json.dumps(strat['params'], ensure_ascii=False)}")
            lines.append(f"    绩: {perf.get('trades',0)}笔 WR:{perf.get('win_rate',0)}% PnL:{perf.get('total_pnl',0)}U")
            
            coins = [s.replace('/USDT','') for s, a in self.data.get('coin_assignments',{}).items()
                    if a.get('trend')==sid or a.get('range')==sid]
            lines.append(f"    币: {', '.join(coins)}")
        
        # 最近复盘
        recent = self.data.get('trade_reflections', [])[:5]
        if recent:
            lines.append(f"\n  📝 最近复盘:")
            for r in recent:
                lines.append(f"    {r['symbol'].replace('/USDT','')} {r['side']} PnL:{r['pnl']:+.2f}U {r.get('auto_summary','')}")
        
        return '\n'.join(lines)


# ═══ 便捷函数 (供live_runner调用) ═══
_pb = None

def get_playbook():
    global _pb
    if _pb is None:
        _pb = PlaybookManager()
    return _pb

def record_trade_reflection(symbol, side, entry, exit_price, pnl, pnl_pct, reason,
                              strategy_id, open_time=None, exit_time=None, regime='?'):
    """便捷函数: 记录交易复盘"""
    pb = get_playbook()
    hold = 0
    if open_time and exit_time:
        if isinstance(open_time, str):
            open_time = datetime.fromisoformat(open_time.replace('Z',''))
        if isinstance(exit_time, str):
            exit_time = datetime.fromisoformat(exit_time.replace('Z',''))
        if hasattr(open_time, 'timestamp') and hasattr(exit_time, 'timestamp'):
            hold = (exit_time - open_time).total_seconds() / 3600
    
    return pb.record_reflection(
        symbol=symbol, side=side, entry=entry, exit=exit_price,
        pnl=pnl, pnl_pct=pnl_pct, reason=reason, strategy_id=strategy_id,
        open_time=open_time, exit_time=exit_time, hold_hours=hold, regime=regime,
    )


if __name__ == '__main__':
    pb = PlaybookManager()
    print(pb.dashboard())
    print("\n--- 趋势池 ---")
    for sid, coins in pb.get_trend_coins().items():
        print(f"  {sid}: {coins}")
    print("\n--- 震荡池 ---")
    for sid, coins in pb.get_range_coins().items():
        print(f"  {sid}: {coins}")
