#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

#!/usr/bin/env python3
"""
自选股监控预警工具 - OpenClaw集成版
支持 A股、ETF 及 国际现货黄金 (伦敦金)
"""

import requests
import json
import time
import os
import subprocess
from datetime import datetime
from pathlib import Path

# 导入操盘手分析器
try:
    from trader_analyzer import TraderAnalyzer
except ImportError:
    print("警告: 未找到操盘手分析器，将使用基础监控功能")
    TraderAnalyzer = None

# ============ 配置区 ============

# 监控列表 - 长期挂机通用配置
# 注意: 伦敦金使用新浪hf_XAU接口，价格为 人民币/克 (约4800元/克 = $2740/盎司)
# 
# 预警规则设计原则 (适合长期挂机):
# 1. 成本百分比预警: 基于持仓成本设置 ±10%/±15% 预警，比固定价格更合理
# 2. 单日涨跌幅预警: 
#    - 个股 ±3%~5% (波动大)
#    - ETF ±1.5%~2.5% (波动小)
#    - 黄金 ±2%~3% (24H特殊)
# 3. 防骚扰: 同类预警30分钟内只发一次

# 标的类型定义
STOCK_TYPE = {
    "INDIVIDUAL": "individual",  # 个股
    "ETF": "etf",                # ETF
    "GOLD": "gold"               # 黄金/贵金属
}

WATCHLIST = [
    # ===== 测试关注股票：光环新网 (300383) =====
    {
        "code": "300383", 
        "name": "光环新网", 
        "market": "sz",
        "type": "individual",
        "cost": None,  # 暂未持仓
        "focus": True,  # 重点关注
        "alerts": {
            "cost_pct_above": 15.0,    # 盈利15%提醒（持仓后启用）
            "cost_pct_below": -12.0,   # 亏损12%止损（持仓后启用）
            "change_pct_above": 4.0,   # 日内大涨4%预警
            "change_pct_below": -4.0,  # 日内大跌4%预警
            "volume_surge": 3.0        # 3倍放量预警（操盘手异动）
        }
    }
]

# 智能频率配置
SMART_SCHEDULE = {
    "market_open": {"hours": [(9, 30), (11, 30), (13, 0), (15, 0)], "interval": 300},  # 交易时间: 5分钟
    "after_hours": {"interval": 1800},  # 收盘后: 30分钟
    "night": {"hours": [(0, 0), (8, 0)], "interval": 3600},  # 凌晨: 1小时(仅伦敦金)
}

# ============ 核心代码 ============

class StockAlert:
    def __init__(self):
        self.prev_data = {}
        self.alert_log = []
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0"})
        
        # 初始化操盘手分析器
        if TraderAnalyzer:
            self.trader_analyzer = TraderAnalyzer()
        else:
            self.trader_analyzer = None
        
        # 添加全局配置到实例
        self.WATCHLIST = WATCHLIST
        
        self.feishu_target = os.getenv("FEISHU_TARGET", "ou_78f9e41a60baa905e5c2fe8178216ee6")  # 飞书用户 ID
        
    def should_run_now(self):
        """智能频率控制：判断当前是否应该执行监控 (基于北京时间)"""
        # 直接使用本地时间（已配置为北京时间）
        now = datetime.now()
        hour, minute = now.hour, now.minute
        time_val = hour * 100 + minute
        weekday = now.weekday()
        
        # 周末只监控伦敦金
        if weekday >= 5:  # 周六日
            return {"run": True, "mode": "weekend", "stocks": [s for s in WATCHLIST if s['market'] == 'fx']}
        
        # 交易时间 (9:30-11:30, 13:00-15:00)
        morning_session = 930 <= time_val <= 1130
        afternoon_session = 1300 <= time_val <= 1500
        
        if morning_session or afternoon_session:
            return {"run": True, "mode": "market", "stocks": WATCHLIST, "interval": 300}
        
        # 午休 (11:30-13:00)
        if 1130 < time_val < 1300:
            return {"run": True, "mode": "lunch", "stocks": WATCHLIST, "interval": 600}  # 10分钟
        
        # 收盘后 (15:00-24:00)
        if 1500 <= time_val <= 2359:
            return {"run": True, "mode": "after_hours", "stocks": WATCHLIST, "interval": 1800}  # 30分钟
        
        # 凌晨 (0:00-9:30)
        if 0 <= time_val < 930:
            return {"run": True, "mode": "night", "stocks": [s for s in WATCHLIST if s['market'] == 'fx'], "interval": 3600}  # 1小时
        
        return {"run": False}

    def fetch_eastmoney_kline(self, symbol, market):
        """获取最新日K线数据 (收盘后也能获取收盘价)"""
        secid = f"{market}.{symbol}"
        url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
        params = {
            'secid': secid,
            'fields1': 'f1,f2,f3,f4,f5,f6',
            'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
            'klt': '101',  # 日线
            'fqt': '0',
            'end': '20500101',
            'lmt': '2'  # 取最近2天，用于计算涨跌幅
        }
        try:
            resp = self.session.get(url, params=params, timeout=10)
            data = resp.json()
            klines = data.get('data', {}).get('klines', [])
            if len(klines) >= 1:
                # 格式: 日期,开盘,收盘,最高,最低,成交量,成交额,振幅,涨跌幅,涨跌额,换手率
                today = klines[-1].split(',')
                prev_close = float(today[2])  # 昨收
                if len(klines) >= 2:
                    prev_close = float(klines[-2].split(',')[2])  # 前一天收盘
                return {
                    'name': data.get('data', {}).get('name', symbol),
                    'price': float(today[2]),      # 收盘
                    'prev_close': prev_close,
                    'volume': int(float(today[5])),
                    'amount': float(today[6]),
                    'date': today[0],
                    'time': '15:00:00'
                }
        except Exception as e:
            print(f"东财K线获取失败 {symbol}: {e}")
        return None

    def fetch_volume_ma5(self, symbol, market):
        """获取5日平均成交量"""
        secid = f"{market}.{symbol}"
        url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
        params = {
            'secid': secid,
            'fields1': 'f1,f2,f3,f4,f5,f6',
            'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
            'klt': '101',
            'fqt': '0',
            'end': '20500101',
            'lmt': '6'  # 取最近6天(今天+前5天)
        }
        try:
            resp = self.session.get(url, params=params, timeout=10)
            data = resp.json()
            klines = data.get('data', {}).get('klines', [])
            if len(klines) >= 2:
                # 计算前5日平均成交量(不含今天)
                volumes = []
                for k in klines[:-1]:  # 排除最后一天(今天)
                    p = k.split(',')
                    volumes.append(float(p[5]))  # 成交量
                return sum(volumes) / len(volumes) if volumes else 0
        except Exception as e:
            print(f"获取均量失败 {symbol}: {e}")
        return 0

    def fetch_ma_data(self, symbol, market):
        """获取均线数据 (MA5, MA10, MA20) 和 RSI"""
        secid = f"{market}.{symbol}"
        url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
        params = {
            'secid': secid,
            'fields1': 'f1,f2,f3,f4,f5,f6',
            'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
            'klt': '101',
            'fqt': '0',
            'end': '20500101',
            'lmt': '30'  # 取最近30天计算MA20和RSI
        }
        try:
            resp = self.session.get(url, params=params, timeout=10)
            data = resp.json()
            klines = data.get('data', {}).get('klines', [])
            if len(klines) >= 20:
                closes = []
                for k in klines:
                    p = k.split(',')
                    closes.append(float(p[2]))  # 收盘价
                
                # 计算均线
                ma5 = sum(closes[-5:]) / 5
                ma10 = sum(closes[-10:]) / 10
                ma20 = sum(closes[-20:]) / 20
                
                # 判断均线趋势
                prev_ma5 = sum(closes[-6:-1]) / 5
                prev_ma10 = sum(closes[-11:-1]) / 10
                
                # 计算RSI(14)
                rsi = self._calculate_rsi(closes, 14)
                
                return {
                    'MA5': ma5,
                    'MA10': ma10,
                    'MA20': ma20,
                    'MA5_trend': 'up' if ma5 > prev_ma5 else 'down',
                    'MA10_trend': 'up' if ma10 > prev_ma10 else 'down',
                    'golden_cross': prev_ma5 <= prev_ma10 and ma5 > ma10,
                    'death_cross': prev_ma5 >= prev_ma10 and ma5 < ma10,
                    'RSI': rsi,
                    'RSI_overbought': rsi > 70 if rsi else False,
                    'RSI_oversold': rsi < 30 if rsi else False
                }
        except Exception as e:
            print(f"获取均线失败 {symbol}: {e}")
        return None
    
    def _calculate_rsi(self, closes, period=14):
        """计算RSI指标"""
        if len(closes) < period + 1:
            return None
        
        gains = []
        losses = []
        
        for i in range(1, period + 1):
            change = closes[-i] - closes[-i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        avg_gain = sum(gains) / period
        avg_loss = sum(losses) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return round(rsi, 2)

    def fetch_sina_realtime(self, stocks):
        """获取实时行情 (优先实时，收盘后用日K)"""
        stock_list = [s for s in stocks if s['market'] != 'fx']
        fx_list = [s for s in stocks if s['market'] == 'fx']
        results = {}
        
        # 1. A股/ETF - 尝试实时接口
        if stock_list:
            codes = [f"{s['market']}{s['code']}" for s in stock_list]
            url = f"https://hq.sinajs.cn/list={','.join(codes)}"
            try:
                resp = self.session.get(url, headers={'Referer': 'https://finance.sina.com.cn'}, timeout=10)
                resp.encoding = 'gb18030'
                for line in resp.text.strip().split(';'):
                    if 'hq_str_' not in line or '=' not in line: continue
                    key = line.split('=')[0].split('_')[-1]
                    if len(key) < 8: continue
                    data_str = line[line.index('"')+1 : line.rindex('"')]
                    p = data_str.split(',')
                    if len(p) > 30 and float(p[3]) > 0:
                        # 新浪数据格式: 名称,今日开盘,昨日收盘,当前价,今日最高,今日最低,竞买价,竞卖价,成交量,成交额...
                        # 保存昨日最高最低价用于跳空检测 (用昨日收盘近似，或用均线数据补充)
                        results[key[2:]] = {
                            'name': p[0], 
                            'price': float(p[3]), 
                            'prev_close': float(p[2]),
                            'open': float(p[1]),      # 今日开盘
                            'high': float(p[4]),      # 今日最高
                            'low': float(p[5]),       # 今日最低
                            'volume': int(p[8]), 
                            'amount': float(p[9]), 
                            'date': p[30], 
                            'time': p[31],
                            'prev_high': float(p[2]) * 1.02,  # 估算昨日最高 (昨收+2%)
                            'prev_low': float(p[2]) * 0.98    # 估算昨日最低 (昨收-2%)
                        }
            except Exception as e: 
                print(f"实时行情获取失败: {e}")
            
            # 2. 如果实时接口返回空或0，用日K线补数据
            for stock in stock_list:
                code = stock['code']
                if code not in results or results[code]['price'] <= 0:
                    kline_data = self.fetch_eastmoney_kline(code, 1 if stock['market'] == 'sh' else 0)
                    if kline_data:
                        results[code] = kline_data
                        print(f"  {stock['name']}: 使用日K收盘价 {kline_data['price']}")

        # 3. 伦敦金 (新浪hf_XAU接口，人民币/克)
        if fx_list:
            url = "https://hq.sinajs.cn/list=hf_XAU"
            try:
                resp = self.session.get(url, headers={'Referer': 'https://finance.sina.com.cn'}, timeout=10)
                line = resp.text.strip()
                if '"' in line:
                    data_str = line[line.index('"')+1 : line.rindex('"')]
                    p = data_str.split(',')
                    if len(p) >= 13:
                        # 新浪hf_XAU: 人民币/克 (约4800=2740美元/盎司)
                        price = float(p[0])
                        results['XAU'] = {
                            'name': '伦敦金', 
                            'price': price, 
                            'prev_close': float(p[7]),
                            'volume': 0, 'amount': 0, 
                            'date': p[11] if len(p) > 11 else datetime.now().strftime('%Y-%m-%d'), 
                            'time': p[6]
                        }
            except Exception as e: 
                print(f"伦敦金获取失败: {e}")
            
        return results
    
    def check_alerts(self, stock_config, data):
        """检查预警条件 (支持成本百分比、单日涨跌幅、分级预警)"""
        alerts = []
        alert_weights = []  # 用于计算预警级别
        code = stock_config['code']
        cfg = stock_config.get('alerts', {})
        cost = stock_config.get('cost', 0)
        stock_type = stock_config.get('type', 'individual')
        price, prev_close = data['price'], data['prev_close']
        change_pct = (price - prev_close) / prev_close * 100 if prev_close else 0
        
        # 1. 基于成本的百分比预警 (权重: 高)
        if cost and cost > 0:
            cost_change_pct = (price - cost) / cost * 100
            
            if 'cost_pct_above' in cfg and cost_change_pct >= cfg['cost_pct_above']:
                target_price = cost * (1 + cfg['cost_pct_above']/100)
                if not self._alerted_recently(code, 'cost_above'):
                    alerts.append(('cost_above', f"🎯 盈利 {cfg['cost_pct_above']:.0f}% (目标价 ¥{target_price:.2f})"))
                    alert_weights.append(3)  # 高权重
            
            if 'cost_pct_below' in cfg and cost_change_pct <= cfg['cost_pct_below']:
                target_price = cost * (1 + cfg['cost_pct_below']/100)
                if not self._alerted_recently(code, 'cost_below'):
                    alerts.append(('cost_below', f"🛑 亏损 {abs(cfg['cost_pct_below']):.0f}% (止损价 ¥{target_price:.2f})"))
                    alert_weights.append(3)  # 高权重
        
        # 2. 基于固定价格的预警 (权重: 中)
        if 'price_above' in cfg and price >= cfg['price_above'] and not self._alerted_recently(code, 'above'):
            alerts.append(('above', f"🚀 价格突破 ¥{cfg['price_above']}"))
            alert_weights.append(2)
        if 'price_below' in cfg and price <= cfg['price_below'] and not self._alerted_recently(code, 'below'):
            alerts.append(('below', f"📉 价格跌破 ¥{cfg['price_below']}"))
            alert_weights.append(2)
        
        # 3. 单日涨跌幅预警 (权重: 根据幅度)
        if 'change_pct_above' in cfg and change_pct >= cfg['change_pct_above'] and not self._alerted_recently(code, 'pct_up'):
            alerts.append(('pct_up', f"📈 日内大涨 {change_pct:+.2f}%"))
            # 异动越大权重越高
            if change_pct >= 7:
                alert_weights.append(3)  # 涨停附近
            elif change_pct >= 5:
                alert_weights.append(2)  # 大涨
            else:
                alert_weights.append(1)  # 一般异动
                
        if 'change_pct_below' in cfg and change_pct <= cfg['change_pct_below'] and not self._alerted_recently(code, 'pct_down'):
            alerts.append(('pct_down', f"📉 日内大跌 {change_pct:+.2f}%"))
            if change_pct <= -7:
                alert_weights.append(3)  # 跌停附近
            elif change_pct <= -5:
                alert_weights.append(2)  # 大跌
            else:
                alert_weights.append(1)  # 一般异动
        
        # 4. 成交量异动检测 (仅股票和ETF)
        if stock_type != 'gold' and 'volume_surge' in cfg:
            current_volume = data.get('volume', 0)
            if current_volume > 0:
                # 尝试获取5日均量
                ma5_volume = self.fetch_volume_ma5(code, 1 if stock_config['market'] == 'sh' else 0)
                if ma5_volume > 0:
                    volume_ratio = current_volume / ma5_volume
                    threshold = cfg['volume_surge']
                    
                    if volume_ratio >= threshold and not self._alerted_recently(code, 'volume_surge'):
                        alerts.append(('volume_surge', f"📊 放量 {volume_ratio:.1f}倍 (5日均量)"))
                        alert_weights.append(2)  # 中等权重
                    elif volume_ratio <= 0.5 and not self._alerted_recently(code, 'volume_shrink'):
                        alerts.append(('volume_shrink', f"📉 缩量 {volume_ratio:.1f}倍 (5日均量)"))
                        alert_weights.append(1)  # 低权重
        
        # 5. 均线系统 (MA金叉死叉)
        if stock_type != 'gold' and cfg.get('ma_monitor', True):
            ma_data = self.fetch_ma_data(code, 1 if stock_config['market'] == 'sh' else 0)
            if ma_data:
                # 金叉: MA5上穿MA10 (短期转强)
                if ma_data.get('golden_cross') and not self._alerted_recently(code, 'ma_golden'):
                    alerts.append(('ma_golden', f"🌟 均线金叉 (MA5¥{ma_data['MA5']:.2f}上穿MA10¥{ma_data['MA10']:.2f})"))
                    alert_weights.append(3)  # 高权重
                
                # 死叉: MA5下穿MA10 (短期转弱)
                if ma_data.get('death_cross') and not self._alerted_recently(code, 'ma_death'):
                    alerts.append(('ma_death', f"⚠️ 均线死叉 (MA5¥{ma_data['MA5']:.2f}下穿MA10¥{ma_data['MA10']:.2f})"))
                    alert_weights.append(3)  # 高权重
                
                # RSI超买超卖检测
                rsi = ma_data.get('RSI')
                if rsi:
                    if ma_data.get('RSI_overbought') and not self._alerted_recently(code, 'rsi_high'):
                        alerts.append(('rsi_high', f"🔥 RSI超买 ({rsi})，可能回调"))
                        alert_weights.append(2)
                    elif ma_data.get('RSI_oversold') and not self._alerted_recently(code, 'rsi_low'):
                        alerts.append(('rsi_low', f"❄️ RSI超卖 ({rsi})，可能反弹"))
                        alert_weights.append(2)
        
        # 5. 跳空缺口检测 (需要昨日数据)
        if stock_type != 'gold':
            prev_high = data.get('prev_high', 0)
            prev_low = data.get('prev_low', 0)
            current_open = data.get('open', price)  # 当前价近似开盘价
            
            # 向上跳空: 今日开盘 > 昨日最高
            if prev_high > 0 and current_open > prev_high * 1.01:  # 1%以上算跳空
                gap_pct = (current_open - prev_high) / prev_high * 100
                if not self._alerted_recently(code, 'gap_up'):
                    alerts.append(('gap_up', f"⬆️ 向上跳空 {gap_pct:.1f}%"))
                    alert_weights.append(2)
            
            # 向下跳空: 今日开盘 < 昨日最低
            elif prev_low > 0 and current_open < prev_low * 0.99:
                gap_pct = (prev_low - current_open) / prev_low * 100
                if not self._alerted_recently(code, 'gap_down'):
                    alerts.append(('gap_down', f"⬇️ 向下跳空 {gap_pct:.1f}%"))
                    alert_weights.append(2)
        
        # 6. 动态止盈/移动止损 (当盈利达到一定幅度后启动)
        if cost and cost > 0:
            profit_pct = (price - cost) / cost * 100
            
            # 当盈利 >= 10% 时，启动移动止盈
            if profit_pct >= 10:
                # 计算回撤幅度 (从最高点回撤)
                high_since_cost = data.get('high', price)
                drawdown = (high_since_cost - price) / high_since_cost * 100 if high_since_cost > cost else 0
                
                # 回撤5%提醒减仓
                if drawdown >= 5 and not self._alerted_recently(code, 'trailing_stop_5'):
                    alerts.append(('trailing_stop_5', f"📉 利润回撤 {drawdown:.1f}%，建议减仓保护利润"))
                    alert_weights.append(2)
                
                # 回撤10%提醒清仓
                elif drawdown >= 10 and not self._alerted_recently(code, 'trailing_stop_10'):
                    alerts.append(('trailing_stop_10', f"🚨 利润回撤 {drawdown:.1f}%，建议清仓止损"))
                    alert_weights.append(3)
        
        # 7. 操盘手习惯分析（只在异常时预警）
        if self.trader_analyzer:
            try:
                # 记录当前价格行为以供学习
                self.trader_analyzer.learn_from_price_action(code, data)
                
                # 检测操盘手异常行为（不是每天都报"符合习惯"）
                abnormal_behaviors = self.trader_analyzer.detect_abnormal_behavior(code, data)
                
                # 只在有异常行为时才预警
                for behavior in abnormal_behaviors:
                    alerts.append(('trader_abnormal', behavior))
                    alert_weights.append(3)  # 异常行为给予高权重
                
                # 检查价格是否接近已知的支撑阻力位（只在接近时预警）
                level_type, strength = self.trader_analyzer.identify_support_resistance(code, price)
                if level_type and strength >= 0.7:  # 只在高强度时预警
                    level_text = "支撑" if level_type == "support" else "阻力"
                    alerts.append(('support_resistance', f"🔄 接近{level_text}位 (强度{strength:.0%})"))
                    alert_weights.append(int(strength * 3))
            except Exception as e:
                print(f"操盘手分析出错 {code}: {e}")
        
        # 6. 计算预警级别
        level = self._calculate_alert_level(alerts, alert_weights, stock_type)
        
        return alerts, level
    
    def _calculate_alert_level(self, alerts, weights, stock_type):
        """计算预警级别: info(提醒) / warning(警告) / critical(紧急)"""
        if not alerts:
            return None
        
        total_weight = sum(weights)
        alert_count = len(alerts)
        
        # 紧急: 多条件共振 或 高权重单一条件
        if total_weight >= 5 or alert_count >= 3:
            return "critical"
        
        # 警告: 中等权重 或 2个条件
        if total_weight >= 3 or alert_count >= 2:
            return "warning"
        
        # 提醒: 单一低权重条件
        return "info"
    
    def _alerted_recently(self, code, atype):
        now = time.time()
        self.alert_log = [l for l in self.alert_log if now - l['t'] < 1800] # 30分钟有效期
        for l in self.alert_log:
            if l['c'] == code and l['a'] == atype: return True
        return False
    
    def record_alert(self, code, atype):
        self.alert_log.append({'c': code, 'a': atype, 't': time.time()})
    
    def send_feishu_alert(self, message: str):
        """通过 OpenClaw message 工具发送飞书消息"""
        try:
            # 直接使用 OpenClaw message 工具发送消息
            result = message(
                action="send",
                channel="feishu",
                target=f"user:{self.feishu_target}",
                message=message
            )
            if result and 'error' not in str(result).lower():
                print(f"[推送成功]")
                return True
            else:
                print(f"[推送失败] {result}")
                return False
        except Exception as e:
            print(f"[推送异常] {e}")
            return False

    def fetch_news(self, symbol):
        """抓取个股最近新闻 (新浪/东财聚合) - 简化版"""
        try:
            # 使用东财个股新闻API
            url = f"https://emweb.securities.eastmoney.com/PC_HSF10/CompanySurvey/CompanySurveyAjax"
            params = {"code": symbol}
            resp = self.session.get(url, params=params, timeout=5)
            return ["新闻模块已就绪 (市场收盘中)"]
        except:
            return []

    def run_once(self, smart_mode=True):
        """执行监控 (支持智能频率)"""
        if smart_mode:
            schedule = self.should_run_now()
            if not schedule.get("run"):
                return []
            
            stocks_to_check = schedule.get("stocks", WATCHLIST)
            mode = schedule.get("mode", "normal")
            
            # 只在特定模式打印日志
            if mode in ["market", "weekend"]:
                print(f"[{datetime.now().strftime('%H:%M')}] {mode}模式扫描 {len(stocks_to_check)} 只标的...")
        else:
            stocks_to_check = WATCHLIST
        
        data_map = self.fetch_sina_realtime(stocks_to_check)
        triggered = []
        
        for stock in stocks_to_check:
            code = stock['code']
            if code not in data_map: continue
            
            data = data_map[code]
            
            # 数据有效性检查
            if data['price'] <= 0 or data['prev_close'] <= 0:
                continue
            
            alerts, level = self.check_alerts(stock, data)
            
            if alerts:
                change_pct = (data['price'] - data['prev_close']) / data['prev_close'] * 100 if data['prev_close'] else 0
                
                # 中国习惯: 红色=上涨, 绿色=下跌
                if change_pct > 0:
                    color_emoji = "🔴"  # 红涨
                elif change_pct < 0:
                    color_emoji = "🟢"  # 绿跌
                else:
                    color_emoji = "⚪"
                
                # 预警级别标识
                level_icons = {
                    "critical": "🚨",  # 紧急
                    "warning": "⚠️",   # 警告
                    "info": "📢"       # 提醒
                }
                level_icon = level_icons.get(level, "📢")
                level_text = {"critical": "【紧急】", "warning": "【警告】", "info": "【提醒】"}.get(level, "")
                
                msg = f"{level_icon} {level_text}{color_emoji} {stock['name']} ({code})\n"
                msg += "━━━━━━━━━━━━━━━━━━━━\n"
                msg += f"💰 当前价格: <b>{data['price']:.2f}</b> ({change_pct:+.2f}%)\n"
                
                # 显示持仓盈亏
                cost = stock.get('cost', 0)
                if cost and cost > 0:
                    cost_change = (data['price'] - cost) / cost * 100
                    profit_icon = "🔴+" if cost_change > 0 else "🟢"
                    msg += f"📊 持仓成本: ¥{cost:.2f} | 盈亏: {profit_icon}{cost_change:.2f}%\n"
                
                msg += f"\n🎯 触发预警 ({len(alerts)}项):\n"
                for _, text in alerts: 
                    msg += f" • {text}\n"
                    self.record_alert(code, _)
                
                # 发送飞书推送（推送所有级别的预警，包括提醒级）
                # if level in ["critical", "warning", "info"]:  # 已注释，全部推送
                print("[飞书推送] " + msg.replace("<b>", "").replace("</b>", ""))
                
                triggered.append(msg)
        
        return triggered

if __name__ == '__main__':
    monitor = StockAlert()
    for alert in monitor.run_once():
        print(alert)

# ============ �����ܽṦ�� ============

def collect_pre_close_data():
    '''14:50 �ռ�����ǰ���ݲ�����'''
    print(f"[{datetime.now().strftime('%H:%M')}] ��ʼ�ռ�����ǰ����...")
    
    monitor = StockAlert()
    stocks_to_check = [s for s in WATCHLIST if s.get('focus', False)]
    
    if not stocks_to_check:
        print('[Ԥ�ռ�] û�й�ע�Ĺ�Ʊ������')
        return
    
    data_map = monitor.fetch_sina_realtime(stocks_to_check)
    
    # �ռ�ÿֻ��Ʊ����ϸ����
    collected_data = {}
    for stock in stocks_to_check:
        code = stock['code']
        if code in data_map:
            data = data_map[code]
            alerts, level = monitor.check_alerts(stock, data)
            
            collected_data[code] = {
                'stock': stock,
                'data': data,
                'alerts': alerts,
                'level': level,
                'collected_at': datetime.now().isoformat()
            }
    
    # ���浽�����ļ�
    cache_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'cache')
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, 'pre_close_data.json')
    
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(collected_data, f, ensure_ascii=False, indent=2)
    
    print(f'[Ԥ�ռ�] ��ɣ��ѻ��� {len(collected_data)} ֻ��Ʊ����')
    print(f'[Ԥ�ռ�] �����ļ���{cache_file}')
    return collected_data


def generate_close_summary():
    '''15:00 ���������ܽᲢ����'''
    print(f"[{datetime.now().strftime('%H:%M')}] ��ʼ���������ܽ�...")
    
    # ��ȡ��������
    cache_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'cache')
    cache_file = os.path.join(cache_dir, 'pre_close_data.json')
    
    if not os.path.exists(cache_file):
        print('[�����ܽ�] δ�ҵ��������ݣ�ִ�м�ʱɨ��')
        collect_pre_close_data()
    
    with open(cache_file, 'r', encoding='utf-8') as f:
        cached_data = json.load(f)
    
    # ����������ݣ����̼�ȷ�ϣ�
    monitor = StockAlert()
    summary_lines = []
    summary_lines.append('=' * 50)
    summary_lines.append(f'?? �����ܽ� ({datetime.now().strftime("%Y-%m-%d %H:%M")})')
    summary_lines.append('=' * 50)
    
    triggered_alerts = []
    
    for code, item in cached_data.items():
        stock = item['stock']
        data = item['data']
        alerts = item['alerts']
        level = item['level']
        
        # ��ȡ���¼۸�ȷ�����̼ۣ�
        latest = monitor.fetch_sina_realtime([stock])
        if code in latest:
            data = latest[code]
        
        change_pct = (data['price'] - data['prev_close']) / data['prev_close'] * 100 if data['prev_close'] else 0
        color_emoji = '??' if change_pct > 0 else '??' if change_pct < 0 else '?'
        
        summary_lines.append('')
        summary_lines.append(f'{color_emoji} {stock["name"]} ({code})')
        summary_lines.append(f'   ���̼ۣ�{data["price"]:.2f} Ԫ ({change_pct:+.2f}%)')
        summary_lines.append(f'   Ԥ������{level}')
        
        if alerts:
            summary_lines.append(f'   ����Ԥ�� ({len(alerts)}��):')
            for _, text in alerts:
                summary_lines.append(f'     ? {text}')
            triggered_alerts.append((stock, data, alerts, level))
        else:
            summary_lines.append(f'   ��Ԥ��')
    
    summary_lines.append('')
    summary_lines.append('=' * 50)
    summary_lines.append('?? ���չ�ע:')
    summary_lines.append('   - ������ע�ɽ����춯��Ʊ')
    summary_lines.append('   - ��ע������ϰ�߱仯')
    summary_lines.append('=' * 50)
    
    # ����ܽ�
    summary_text = '\n'.join(summary_lines)
    print(summary_text)
    
    # ���ͷ��飨ֻ������Ԥ���Ĺ�Ʊ��
    if triggered_alerts:
        push_msg = generate_push_message(triggered_alerts)
        print(f'\n[��������] {push_msg.replace("<b>", "").replace("</b>", "")}')
    
    return summary_text


def generate_push_message(triggered_alerts):
    '''���ɷ���������Ϣ'''
    lines = []
    lines.append('?? �������ܽ᡿')
    lines.append('')
    
    for stock, data, alerts, level in triggered_alerts:
        code = stock['code']
        change_pct = (data['price'] - data['prev_close']) / data['prev_close'] * 100 if data['prev_close'] else 0
        color_emoji = '??' if change_pct > 0 else '??' if change_pct < 0 else '?'
        
        level_icon = '??' if level == 'critical' else '??' if level == 'warning' else '??'
        
        lines.append(f'{level_icon} {color_emoji} {stock["name"]} ({code})')
        lines.append(f'?? ���̼ۣ�{data["price"]:.2f} Ԫ ({change_pct:+.2f}%)')
        lines.append(f'?? Ԥ�� ({len(alerts)}��):')
        for _, text in alerts:
            lines.append(f'  ? {text}')
        lines.append('')
    
    return '\n'.join(lines)


# ============ ��������� ============

if __name__ == '__main__':
    import sys
    
    # ��������в���
    if len(sys.argv) > 1:
        mode = sys.argv[1]
        
        if mode == 'pre_close':
            # 14:50 Ԥ�ռ�ģʽ
            collect_pre_close_data()
        elif mode == 'close_summary':
            # 15:00 �����ܽ�ģʽ
            generate_close_summary()
        else:
            # ��ͨ���ģʽ
            monitor = StockAlert()
            for alert in monitor.run_once():
                print(alert)
    else:
        # �޲�������ͨ���ģʽ
        monitor = StockAlert()
        for alert in monitor.run_once():
            print(alert)
