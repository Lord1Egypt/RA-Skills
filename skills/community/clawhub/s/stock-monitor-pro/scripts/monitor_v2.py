#!/usr/bin/env python3
"""
自选股监控预警工具 V2 - 反爬虫优化版
支持 A股、ETF
优化: Session级UA绑定、完整请求头、3-10分钟随机延迟、多数据源冗余
"""

import requests
import json
import time
import os
import random
from datetime import datetime, timedelta
from pathlib import Path

# ============ 配置区 ============

WATCHLIST = [
    {
        "code": "159142", 
        "name": "科创创业人工智能ETF", 
        "market": "sz",
        "type": "etf",
        "cost": 1.158,
        "alerts": {
            "cost_pct_above": 10.0,
            "cost_pct_below": -15.0,
            "target_buy": 0.98,
            "change_pct_above": 3.0,
            "change_pct_below": -3.0,
            "volume_surge": 2.0,
            "ma_monitor": True,
            "rsi_monitor": True,
            "gap_monitor": True,
            "trailing_stop": False
        }
    },
    {
        "code": "159213", 
        "name": "机器人ETF汇添富", 
        "market": "sz",
        "type": "etf",
        "cost": 1.307,
        "alerts": {
            "cost_pct_above": 10.0,
            "cost_pct_below": -15.0,
            "target_buy": 1.11,
            "change_pct_above": 3.0,
            "change_pct_below": -3.0,
            "volume_surge": 2.0,
            "ma_monitor": True,
            "rsi_monitor": True,
            "gap_monitor": True,
            "trailing_stop": False
        }
    },
    {
        "code": "159828", 
        "name": "医疗ETF", 
        "market": "sz",
        "type": "etf",
        "cost": 0.469,
        "note": "策略：涨到¥0.45减仓50%，跌破¥0.40止损",
        "alerts": {
            "cost_pct_above": 10.0,
            "cost_pct_below": -14.7,
            "stop_loss": 0.40,
            "target_reduce": 0.45,
            "change_pct_above": 3.0,
            "change_pct_below": -3.0,
            "volume_surge": 2.0,
            "ma_monitor": True,
            "rsi_monitor": True,
            "gap_monitor": True,
            "trailing_stop": False
        }
    }
]

# UA池 - Session启动时随机选择一个
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Edg/119.0.0.0"
]

# ============ 核心代码 ============

class StockAlert:
    def __init__(self):
        self.prev_data = {}
        self.alert_log = []
        self.failed_sources = {}  # 记录各数据源失败次数
        self.source_cooldown = {}  # 数据源冷却时间
        self.error_notifications = {}  # 错误通知记录（防重复）
        self.NOTIFICATION_COOLDOWN = 1800  # 错误通知冷却30分钟
        
        # 日报相关
        self.daily_report_sent = False  # 今日日报是否已发送
        self.daily_data = {}  # 存储当日数据用于日报
        self.today_date = datetime.now().strftime('%Y-%m-%d')
        
        # Session级UA绑定 - 整个生命周期使用同一个UA
        self.user_agent = random.choice(USER_AGENTS)
        print(f"[初始化] 使用UA: {self.user_agent[:60]}...")
        
        # 创建带完整请求头的session
        self.session = requests.Session()
        self._setup_session_headers()
        
    def _setup_session_headers(self):
        """设置完整的浏览器指纹请求头"""
        self.session.headers.update({
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Cache-Control": "max-age=0"
        })
        
    def _random_delay(self, min_sec=0.5, max_sec=3.0):
        """请求前随机延迟，模拟真人操作间隔"""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)
        return delay
        
    def _is_source_available(self, source_name):
        """检查数据源是否可用（冷却期已过）"""
        if source_name in self.source_cooldown:
            if time.time() < self.source_cooldown[source_name]:
                return False
        return True
        
    def _mark_source_failed(self, source_name, cooldown_minutes=5):
        """标记数据源失败，进入冷却期"""
        self.failed_sources[source_name] = self.failed_sources.get(source_name, 0) + 1
        # 连续失败3次以上，冷却30分钟
        if self.failed_sources[source_name] >= 3:
            cooldown_minutes = 30
        self.source_cooldown[source_name] = time.time() + cooldown_minutes * 60
        print(f"[数据源] {source_name} 标记为失败，冷却{cooldown_minutes}分钟")
        
    def _mark_source_success(self, source_name):
        """标记数据源成功，重置失败计数"""
        if source_name in self.failed_sources:
            del self.failed_sources[source_name]

    def should_run_now(self):
        """智能频率控制: 3-10分钟随机"""
        now = datetime.now() + timedelta(hours=13)  # 北京时间
        hour, minute = now.hour, now.minute
        time_val = hour * 100 + minute
        weekday = now.weekday()
        
        # 周末低频
        if weekday >= 5:
            return {"run": True, "mode": "weekend", "stocks": WATCHLIST, "interval": random.randint(600, 1800)}
        
        # 交易时间 (9:30-11:30, 13:00-15:00)
        morning_session = 930 <= time_val <= 1130
        afternoon_session = 1300 <= time_val <= 1500
        
        if morning_session or afternoon_session:
            # 交易活跃时段：3-6分钟随机
            return {"run": True, "mode": "market", "stocks": WATCHLIST, "interval": random.randint(180, 360)}
        
        # 午休 (11:30-13:00)
        if 1130 < time_val < 1300:
            return {"run": True, "mode": "lunch", "stocks": WATCHLIST, "interval": random.randint(300, 600)}
        
        # 收盘后 (15:00-24:00)
        if 1500 <= time_val <= 2359:
            return {"run": True, "mode": "after_hours", "stocks": WATCHLIST, "interval": random.randint(900, 1800)}
        
        # 凌晨 (0:00-9:30)
        if 0 <= time_val < 930:
            return {"run": True, "mode": "night", "stocks": WATCHLIST, "interval": random.randint(1800, 3600)}
        
        return {"run": False}

    # ============ 多数据源获取 ============
    
    def fetch_sina_realtime(self, stocks):
        """数据源1: 新浪财经实时行情"""
        source_name = "sina"
        if not self._is_source_available(source_name):
            return None, "冷却中"
            
        stock_list = [s for s in stocks if s['market'] != 'fx']
        if not stock_list:
            return {}, None
            
        codes = [f"{s['market']}{s['code']}" for s in stock_list]
        url = f"https://hq.sinajs.cn/list={','.join(codes)}"
        
        try:
            self._random_delay(0.3, 1.0)
            resp = self.session.get(url, headers={'Referer': 'https://finance.sina.com.cn'}, timeout=10)
            resp.encoding = 'gb18030'
            
            results = {}
            for line in resp.text.strip().split(';'):
                if 'hq_str_' not in line or '=' not in line: 
                    continue
                key = line.split('=')[0].split('_')[-1]
                if len(key) < 8: 
                    continue
                data_str = line[line.index('"')+1 : line.rindex('"')]
                p = data_str.split(',')
                if len(p) > 30 and float(p[3]) > 0:
                    results[key[2:]] = {
                        'name': p[0], 
                        'price': float(p[3]), 
                        'prev_close': float(p[2]),
                        'open': float(p[1]),
                        'high': float(p[4]),
                        'low': float(p[5]),
                        'volume': int(p[8]), 
                        'amount': float(p[9]), 
                        'date': p[30], 
                        'time': p[31],
                        'source': 'sina'
                    }
            
            if results:
                self._mark_source_success(source_name)
                return results, None
            return None, "返回数据为空"
            
        except Exception as e:
            self._mark_source_failed(source_name)
            return None, str(e)

    def fetch_tencent_realtime(self, stocks):
        """数据源2: 腾讯财经实时行情 (备用)"""
        source_name = "tencent"
        if not self._is_source_available(source_name):
            return None, "冷却中"
            
        stock_list = [s for s in stocks if s['market'] != 'fx']
        if not stock_list:
            return {}, None
            
        codes = [f"{s['market']}{s['code']}" for s in stock_list]
        url = f"https://qt.gtimg.cn/q={','.join(codes)}"
        
        try:
            self._random_delay(0.3, 1.0)
            resp = self.session.get(url, timeout=10)
            resp.encoding = 'gb18030'
            
            results = {}
            for line in resp.text.strip().split(';'):
                if 'v_' not in line or '=' not in line:
                    continue
                key = line.split('=')[0].split('_')[-1]
                data_str = line[line.index('"')+1 : line.rindex('"')]
                p = data_str.split('~')
                if len(p) > 40:
                    # 腾讯格式: 股票名称~股票代码~当前价格~昨收~今开...
                    results[key[2:]] = {
                        'name': p[1],
                        'price': float(p[3]),
                        'prev_close': float(p[4]),
                        'open': float(p[5]),
                        'high': float(p[33]),
                        'low': p[34],
                        'volume': int(p[36]),
                        'amount': float(p[37]),
                        'source': 'tencent'
                    }
            
            if results:
                self._mark_source_success(source_name)
                return results, None
            return None, "返回数据为空"
            
        except Exception as e:
            self._mark_source_failed(source_name)
            return None, str(e)

    def fetch_eastmoney_kline(self, symbol, market):
        """数据源3: 东方财富K线数据 (均线/RSI/成交量)"""
        source_name = "eastmoney"
        if not self._is_source_available(source_name):
            return None, "冷却中"
            
        secid = f"{market}.{symbol}"
        url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
        params = {
            'secid': secid,
            'fields1': 'f1,f2,f3,f4,f5,f6',
            'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
            'klt': '101',
            'fqt': '0',
            'end': '20500101',
            'lmt': '30'
        }
        
        try:
            self._random_delay(0.5, 1.5)
            resp = self.session.get(url, params=params, timeout=10)
            data = resp.json()
            klines = data.get('data', {}).get('klines', [])
            
            if len(klines) >= 20:
                self._mark_source_success(source_name)
                return klines, None
            return None, "数据不足"
            
        except Exception as e:
            self._mark_source_failed(source_name)
            return None, str(e)

    def fetch_ths_kline(self, symbol, market):
        """数据源4: 同花顺K线数据 (备用)"""
        source_name = "ths"
        if not self._is_source_available(source_name):
            return None, "冷却中"
            
        # 同花顺代码格式
        ths_code = f"{market}{symbol}"
        url = f"http://d.10jqka.com.cn/v6/line/{ths_code}/01/all.js"
        
        try:
            self._random_delay(0.5, 1.5)
            headers = {
                'Referer': f'http://stockpage.10jqka.com.cn/{symbol}/',
                'User-Agent': self.user_agent
            }
            resp = self.session.get(url, headers=headers, timeout=10)
            
            # 同花顺返回的是JSONP格式，需要解析
            text = resp.text
            if '(' in text and ')' in text:
                json_str = text[text.index('(')+1:text.rindex(')')]
                data = json.loads(json_str)
                
                # 解析K线数据
                klines = data.get('data', '').split(';')
                if len(klines) >= 20:
                    self._mark_source_success(source_name)
                    return klines, None
            return None, "解析失败"
            
        except Exception as e:
            self._mark_source_failed(source_name)
            return None, str(e)

    # ============ 技术指标计算 ============
    
    def calculate_indicators(self, klines):
        """从K线计算技术指标"""
        if not klines or len(klines) < 20:
            return None
            
        closes = []
        volumes = []
        
        for k in klines:
            if isinstance(k, str):
                p = k.split(',')
                if len(p) >= 6:
                    closes.append(float(p[2]))  # 收盘价
                    volumes.append(float(p[5]))  # 成交量
            elif isinstance(k, dict):
                closes.append(float(k.get('close', 0)))
                volumes.append(float(k.get('volume', 0)))
        
        if len(closes) < 20:
            return None
            
        # 计算均线
        ma5 = sum(closes[-5:]) / 5
        ma10 = sum(closes[-10:]) / 10
        ma20 = sum(closes[-20:]) / 20
        
        prev_ma5 = sum(closes[-6:-1]) / 5
        prev_ma10 = sum(closes[-11:-1]) / 10
        
        # 计算5日均量
        volume_ma5 = sum(volumes[-6:-1]) / 5 if len(volumes) >= 6 else 0
        today_volume = volumes[-1] if volumes else 0
        
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
            'RSI_oversold': rsi < 30 if rsi else False,
            'volume_ma5': volume_ma5,
            'volume_ratio': today_volume / volume_ma5 if volume_ma5 > 0 else 0
        }
    
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

    # ============ 主监控逻辑 ============
    
    def get_stock_data(self, stock):
        """获取单只股票的完整数据（多源降级）"""
        code = stock['code']
        market = 0 if stock['market'] == 'sh' else 1  # 东财用的市场代码
        
        result = {
            'code': code,
            'name': stock['name'],
            'price': 0,
            'prev_close': 0,
            'change_pct': 0,
            'volume': 0,
            'indicators': None,
            'sources_used': [],
            'errors': []
        }
        
        # Step 1: 获取实时价格（优先级: 新浪 → 腾讯）
        realtime_data = None
        
        # 尝试新浪
        sina_data, sina_err = self.fetch_sina_realtime([stock])
        if sina_data and code in sina_data:
            realtime_data = sina_data[code]
            result['sources_used'].append('sina')
        else:
            if sina_err:
                result['errors'].append(f"新浪: {sina_err}")
        
        # 新浪失败，尝试腾讯
        if not realtime_data:
            tencent_data, tencent_err = self.fetch_tencent_realtime([stock])
            if tencent_data and code in tencent_data:
                realtime_data = tencent_data[code]
                result['sources_used'].append('tencent')
            else:
                if tencent_err:
                    result['errors'].append(f"腾讯: {tencent_err}")
        
        if realtime_data:
            result['price'] = realtime_data['price']
            result['prev_close'] = realtime_data.get('prev_close', realtime_data['price'])
            result['volume'] = realtime_data.get('volume', 0)
            result['change_pct'] = round((result['price'] - result['prev_close']) / result['prev_close'] * 100, 2)
        else:
            result['errors'].append("无法获取实时价格")
            return result
        
        # Step 2: 获取技术指标（优先级: 东财 → 同花顺）
        klines = None
        
        # 尝试东财
        em_klines, em_err = self.fetch_eastmoney_kline(code, market)
        if em_klines:
            klines = em_klines
            result['sources_used'].append('eastmoney')
        else:
            if em_err:
                result['errors'].append(f"东财: {em_err}")
        
        # 东财失败，尝试同花顺
        if not klines:
            ths_klines, ths_err = self.fetch_ths_kline(code, stock['market'])
            if ths_klines:
                klines = ths_klines
                result['sources_used'].append('ths')
            else:
                if ths_err:
                    result['errors'].append(f"同花顺: {ths_err}")
        
        # 计算技术指标
        if klines:
            result['indicators'] = self.calculate_indicators(klines)
        else:
            result['errors'].append("无法获取技术指标")
        
        return result

    def check_alerts(self, stock, data):
        """检查预警条件"""
        alerts = []
        config = stock['alerts']
        price = data['price']
        cost = stock['cost']
        change_pct = data['change_pct']
        indicators = data.get('indicators')
        
        if price <= 0:
            return alerts
        
        # 1. 成本百分比预警
        cost_change_pct = round((price - cost) / cost * 100, 2)
        if config.get('cost_pct_above') and cost_change_pct >= config['cost_pct_above']:
            alerts.append({
                'level': 'warning',
                'type': 'cost_profit',
                'message': f"盈利 {cost_change_pct}% (目标 {config['cost_pct_above']}%)"
            })
        if config.get('cost_pct_below') and cost_change_pct <= config['cost_pct_below']:
            alerts.append({
                'level': 'warning', 
                'type': 'cost_loss',
                'message': f"亏损 {abs(cost_change_pct)}% (阈值 {abs(config['cost_pct_below'])}%)"
            })
        
        # 2. 日内涨跌幅预警
        if config.get('change_pct_above') and change_pct >= config['change_pct_above']:
            alerts.append({
                'level': 'info',
                'type': 'rise',
                'message': f"日内大涨 {change_pct}%"
            })
        if config.get('change_pct_below') and change_pct <= config['change_pct_below']:
            alerts.append({
                'level': 'info',
                'type': 'fall',
                'message': f"日内大跌 {abs(change_pct)}%"
            })
        
        # 3. 技术指标预警（如果有数据）
        if indicators:
            # 成交量异动
            if config.get('volume_surge') and indicators.get('volume_ratio', 0) >= config['volume_surge']:
                alerts.append({
                    'level': 'info',
                    'type': 'volume',
                    'message': f"放量 {indicators['volume_ratio']:.1f}倍"
                })
            
            # 均线金叉死叉
            if config.get('ma_monitor'):
                if indicators.get('golden_cross'):
                    alerts.append({
                        'level': 'warning',
                        'type': 'golden_cross',
                        'message': f"均线金叉 (MA5:{indicators['MA5']:.2f} > MA10:{indicators['MA10']:.2f})"
                    })
                if indicators.get('death_cross'):
                    alerts.append({
                        'level': 'warning',
                        'type': 'death_cross',
                        'message': f"均线死叉 (MA5:{indicators['MA5']:.2f} < MA10:{indicators['MA10']:.2f})"
                    })
            
            # RSI超买超卖
            if config.get('rsi_monitor'):
                if indicators.get('RSI_overbought'):
                    alerts.append({
                        'level': 'info',
                        'type': 'rsi_high',
                        'message': f"RSI超买 {indicators['RSI']}"
                    })
                if indicators.get('RSI_oversold'):
                    alerts.append({
                        'level': 'info',
                        'type': 'rsi_low',
                        'message': f"RSI超卖 {indicators['RSI']}"
                    })
        
        return alerts

    def format_message(self, stock, data, alerts):
        """格式化预警消息"""
        if not alerts:
            return None
        
        price = data['price']
        cost = stock['cost']
        change_pct = data['change_pct']
        cost_change_pct = round((price - cost) / cost * 100, 2) if cost > 0 else 0
        
        # 确定级别
        high_priority = [a for a in alerts if a['level'] == 'warning']
        level_icon = "🚨" if len(high_priority) >= 2 else ("⚠️" if high_priority else "📢")
        level_text = "紧急" if len(high_priority) >= 2 else ("警告" if high_priority else "提醒")
        
        # 颜色标识
        color_icon = "🔴" if change_pct >= 0 else "🟢"
        profit_icon = "🔴" if cost_change_pct >= 0 else "🟢"
        
        msg_lines = [
            f"{level_icon}【{level_text}】{color_icon} {stock['name']} ({stock['code']})",
            "━━━━━━━━━━━━━━━━━━━━",
            f"💰 当前价格: ¥{price:.3f} ({change_pct:+.2f}%)",
            f"📊 持仓成本: ¥{cost:.3f} | 盈亏: {profit_icon}{cost_change_pct:+.1f}%"
        ]
        
        # 预警详情
        if alerts:
            msg_lines.append("")
            msg_lines.append(f"🎯 触发预警 ({len(alerts)}项):")
            for alert in alerts:
                icon = {"cost_profit": "🎯", "cost_loss": "🛑", "rise": "📈", "fall": "📉",
                       "volume": "📊", "golden_cross": "🌟", "death_cross": "⚡",
                       "rsi_high": "🔥", "rsi_low": "❄️"}.get(alert['type'], "•")
                msg_lines.append(f"  {icon} {alert['message']}")
        
        # 数据源信息
        msg_lines.append("")
        msg_lines.append(f"📡 数据来源: {' → '.join(data.get('sources_used', ['未知']))}")
        
        return "\n".join(msg_lines)

    def run_once(self):
        """执行一次监控循环"""
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始扫描...")
        
        messages = []
        
        for stock in WATCHLIST:
            print(f"  检查 {stock['name']}...")
            
            # 获取数据
            data = self.get_stock_data(stock)
            
            if data['errors'] and not data['sources_used']:
                print(f"    ❌ 完全失败: {'; '.join(data['errors'])}")
                continue
            
            print(f"    ✅ 价格: ¥{data['price']:.3f} (来源: {'→'.join(data['sources_used'])})")
            
            # 检查预警
            alerts = self.check_alerts(stock, data)
            
            if alerts:
                msg = self.format_message(stock, data, alerts)
                if msg:
                    messages.append(msg)
                    print(f"    🔔 触发 {len(alerts)} 个预警")
                # 记录预警次数用于日报
                data['alert_count'] = len(alerts)
            else:
                data['alert_count'] = 0
            
            # 保存数据用于日报
            self.daily_data[stock['code']] = data
            
            # 错误提示（但不影响功能）
            if data['errors'] and data['sources_used']:
                print(f"    ⚠️ 部分失败: {'; '.join(data['errors'])}")
        
        return messages

    def check_and_notify_errors(self):
        """检查数据源错误并发送通知"""
        notifications = []
        now = time.time()
        
        for source, fail_count in self.failed_sources.items():
            # 连续失败3次以上，或刚进入30分钟冷却
            if fail_count >= 3:
                # 避免重复通知：每小时只通知一次
                last_notify_key = f"error_notified_{source}"
                last_notify = getattr(self, last_notify_key, 0)
                
                if now - last_notify > 1800:  # 30分钟冷却
                    cooldown_end = self.source_cooldown.get(source, 0)
                    remaining = int((cooldown_end - now) / 60) if cooldown_end > now else 0
                    
                    notifications.append({
                        'source': source,
                        'fail_count': fail_count,
                        'cooldown_minutes': remaining
                    })
                    setattr(self, last_notify_key, now)
        
        return notifications
    
    def format_error_notification(self, errors):
        """格式化错误通知消息"""
        if not errors:
            return None
        
        lines = [
            "⚠️【数据源异常提醒】",
            "━━━━━━━━━━━━━━━━━━━━",
            "以下数据源连续失败，已进入冷却期：",
            ""
        ]
        
        source_names = {
            'sina': '新浪财经',
            'tencent': '腾讯财经', 
            'eastmoney': '东方财富',
            'ths': '同花顺'
        }
        
        for err in errors:
            name = source_names.get(err['source'], err['source'])
            lines.append(f"• {name}: 失败{err['fail_count']}次，冷却{err['cooldown_minutes']}分钟")
        
        lines.extend([
            "",
            "📊 当前状态：",
            "• 实时价格监控：正常（新浪/腾讯备用）",
            "• 技术指标监控：可能受限（均线/RSI/成交量）",
            "",
            "💡 建议：",
            "如持续失败，可考虑部署WARP代理或调整请求频率"
        ])
        
        return "\n".join(lines)

    def _reset_daily_report_flag(self):
        """重置日报发送标志（新的一天）"""
        current_date = datetime.now().strftime('%Y-%m-%d')
        if current_date != self.today_date:
            self.today_date = current_date
            self.daily_report_sent = False
            self.daily_data = {}
            print(f"[日报] 日期已切换至 {current_date}，重置日报标志")

    def _check_and_send_daily_report(self, mode):
        """检查并发送收盘日报"""
        # 重置日期标志
        self._reset_daily_report_flag()
        
        # 只在收盘后模式且未发送过日报时发送
        if mode != 'after_hours' or self.daily_report_sent:
            return
        
        # 检查当前时间是否在15:00-15:30之间（北京时间）
        now = datetime.now() + timedelta(hours=13)  # 转换为北京时间
        hour, minute = now.hour, now.minute
        time_val = hour * 100 + minute
        
        if not (1500 <= time_val <= 1530):
            return
        
        # 生成并发送日报
        report = self._generate_daily_report()
        if report:
            print("\n" + report)
            # TODO: 调用OpenClaw发送日报
            self.daily_report_sent = True
            print(f"[日报] 收盘日报已发送 ({now.strftime('%H:%M')})")

    def _generate_daily_report(self):
        """生成收盘日报"""
        if not self.daily_data:
            return None
        
        now = datetime.now() + timedelta(hours=13)  # 北京时间
        date_str = now.strftime('%Y-%m-%d')
        
        lines = [
            f"📊【收盘日报】{date_str}",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            ""
        ]
        
        total_cost_value = 0
        total_current_value = 0
        total_day_change = 0
        alert_count = 0
        
        for stock in WATCHLIST:
            code = stock['code']
            data = self.daily_data.get(code)
            if not data:
                continue
            
            price = data['price']
            cost = stock['cost']
            change_pct = data.get('change_pct', 0)
            cost_change_pct = round((price - cost) / cost * 100, 2) if cost > 0 else 0
            
            # 计算市值（假设持仓1万份）
            position = 10000  # 默认持仓数量
            cost_value = cost * position
            current_value = price * position
            
            total_cost_value += cost_value
            total_current_value += current_value
            total_day_change += change_pct
            
            # 颜色标识
            profit_icon = "🔴" if cost_change_pct >= 0 else "🟢"
            day_icon = "🔴" if change_pct >= 0 else "🟢"
            
            lines.append(f"📈 {stock['name']} ({code})")
            lines.append(f"   成本: ¥{cost:.3f} → 收盘: ¥{price:.3f}")
            lines.append(f"   持仓盈亏: {profit_icon}{cost_change_pct:+.2f}% | 日内涨跌: {day_icon}{change_pct:+.2f}%")
            lines.append("")
            
            # 统计预警次数
            alert_count += data.get('alert_count', 0)
        
        # 总体统计
        if total_cost_value > 0:
            total_profit_pct = round((total_current_value - total_cost_value) / total_cost_value * 100, 2)
            avg_day_change = round(total_day_change / len(WATCHLIST), 2)
            profit_icon = "🔴" if total_profit_pct >= 0 else "🟢"
            day_icon = "🔴" if avg_day_change >= 0 else "🟢"
            
            lines.append("📋 今日汇总")
            lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            lines.append(f"💰 总持仓盈亏: {profit_icon}{total_profit_pct:+.2f}%")
            lines.append(f"📊 平均日内涨跌: {day_icon}{avg_day_change:+.2f}%")
            lines.append(f"🔔 预警触发次数: {alert_count}")
            lines.append("")
        
        # 市场点评
        if avg_day_change >= 2:
            comment = "🚀 今日市场表现强势，多只个股大涨"
        elif avg_day_change >= 0.5:
            comment = "📈 今日市场整体向好，稳步上涨"
        elif avg_day_change > -0.5:
            comment = "➡️ 今日市场震荡整理，波动较小"
        elif avg_day_change > -2:
            comment = "📉 今日市场小幅回调，注意风险"
        else:
            comment = "🛑 今日市场大幅下跌，谨慎操作"
        
        lines.append(f"💡 {comment}")
        lines.append("")
        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        lines.append("📌 数据来源: 新浪财经/腾讯财经")
        lines.append("⏰ 下次日报: 下一交易日收盘后")
        
        return "\n".join(lines)

    def run_forever(self):
        """持续运行"""
        print("="*50)
        print("股票监控启动 (V2反爬虫优化版)")
        print(f"监控标的: {len(WATCHLIST)} 只")
        print(f"UA: {self.user_agent[:50]}...")
        print("="*50)
        
        while True:
            schedule = self.should_run_now()
            if not schedule['run']:
                time.sleep(60)
                continue
            
            # 执行监控
            messages = self.run_once()
            
            # 发送消息（这里可以接入OpenClaw消息发送）
            for msg in messages:
                print("\n" + msg)
                # TODO: 调用OpenClaw发送消息
            
            # 检查并发送错误通知
            error_notifications = self.check_and_notify_errors()
            if error_notifications:
                error_msg = self.format_error_notification(error_notifications)
                if error_msg:
                    print("\n" + error_msg)
                    # TODO: 调用OpenClaw发送错误通知
            
            # 检查是否需要发送收盘日报（15:00-15:30之间，且未发送过）
            self._check_and_send_daily_report(schedule['mode'])
            
            # 等待下次扫描（3-10分钟随机）
            interval = schedule.get('interval', random.randint(180, 600))
            next_time = datetime.now() + timedelta(seconds=interval)
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 下次扫描: {next_time.strftime('%H:%M:%S')} (间隔{interval//60}分{interval%60}秒)")
            time.sleep(interval)


if __name__ == "__main__":
    monitor = StockAlert()
    monitor.run_forever()
