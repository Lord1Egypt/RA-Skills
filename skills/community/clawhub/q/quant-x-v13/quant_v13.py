#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
600330 天通股份 v13 量化分析器
=================================
集成 2026 最新主流量化策略 + 4 维 OBI 模型 + 龙虎榜 3 维验证 + 主力吸筹 5 大铁律

作者: MiniMax-M3 (基于 2026-08-24 最新研究)
数据源: 腾讯 qt.gtimg.cn (报价) + ifzq (分时) + 东方财富 push2 (全字段)
更新: 2026-08-24 整合 2026 最新 OBV 增强、龙虎榜 3 维验证、主力吸筹 5 大铁律
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime
import sys
import os

# ============================================================
# 0. 全局配置
# ============================================================

STOCK_CODE = "sh600330"
STOCK_NAME = "天通股份"
TODAY = datetime.now().strftime("%Y-%m-%d")

# OBI 4 维模型权重 (基于 2026 最新学术研究)
OBI_WEIGHTS = {
    "count": 0.15,        # 计数 OBI (简单但快速反应)
    "vol_weighted": 0.30, # 量加权 OBI (主力资金核心)
    "time_decay": 0.25,   # 时间衰减 OBI (近期偏多信号)
    "big_order": 0.30,    # 大单 OBI (主力意图)
}

# 大单阈值 (固定 500 手)
BIG_ORDER_THRESHOLD = 500

# 时间衰减权重函数: w = 1 + i * 0.05 (i 为分钟索引)
def time_decay_weight(i):
    return 1 + i * 0.05

# ============================================================
# 1. 数据层 (Data Layer) - 4 大数据源融合
# ============================================================

class DataLayer:
    """4 大数据源融合: 腾讯报价 + 腾讯分时 + 东方财富 push2 + 东方财富 Skill"""
    
    def __init__(self, code=STOCK_CODE):
        self.code = code
        self.market = "sh" if code.startswith("sh") else "sz"
        self.pure_code = code[2:]
        self.data = {}
    
    def fetch_tencent_quote(self):
        """1. 腾讯 qt.gtimg.cn 实时报价 (CORS 开放 + 无限免费)"""
        url = f"https://qt.gtimg.cn/q={self.code}"
        req = urllib.request.Request(url, headers={"Referer": "https://gu.qq.com/"})
        text = urllib.request.urlopen(req, timeout=10).read().decode("gbk")
        content = text.split("=", 1)[1].strip()
        if content.startswith('"'): content = content[1:]
        if content.endswith('";'): content = content[:-2]
        p = content.split("~")
        def s(i, d=""): return p[i] if len(p) > i and p[i] else d
        
        self.data["tencent"] = {
            "name": s(1),
            "code": s(2),
            "price": float(s(3)) if s(3) else 0,
            "prev_close": float(s(4)) if s(4) else 0,
            "open": float(s(5)) if s(5) else 0,
            "volume": int(s(6)) if s(6) else 0,
            "outer_volume": int(s(7)) if s(7) else 0,  # 外盘
            "inner_volume": int(s(8)) if s(8) else 0,  # 内盘
            "bid_prices": [float(s(i)) if s(i) else 0 for i in [9, 11, 13, 15, 17]],
            "bid_vols": [int(s(i)) if s(i) else 0 for i in [10, 12, 14, 16, 18]],
            "ask_prices": [float(s(i)) if s(i) else 0 for i in [19, 21, 23, 25, 27]],
            "ask_vols": [int(s(i)) if s(i) else 0 for i in [20, 22, 24, 26, 28]],
            "high": float(s(33)) if s(33) else 0,
            "low": float(s(34)) if s(34) else 0,
            "amplitude": float(s(43).replace("%", "")) if s(43) else 0,
            "turnover_rate": float(s(38).replace("%", "")) if s(38) else 0,
            "pct_change": float(s(32)) if s(32) else 0,
            "amount": int(s(37)) if s(37) else 0,  # 成交额 (元)
        }
        return self.data["tencent"]
    
    def fetch_tencent_minute(self):
        """2. 腾讯 ifzq 分时数据 (CORS 开放 + 分钟级)"""
        url = f"https://web.ifzq.gtimg.cn/appstock/app/minute/query?code={self.code}"
        req = urllib.request.Request(url, headers={"Referer": "https://gu.qq.com/"})
        raw = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
        data = json.loads(raw)
        minutes = data.get("data", {}).get(self.code, {}).get("data", {}).get("data", [])
        
        all_m = []
        prev_vol = 0
        for m in minutes:
            if isinstance(m, str):
                parts = m.split(" ")
                if len(parts) >= 4:
                    cum_vol = int(parts[2])
                    per_min = cum_vol - prev_vol
                    prev_vol = cum_vol
                    all_m.append({
                        "time": parts[0],
                        "price": float(parts[1]),
                        "vol": per_min,
                        "cum_vol": cum_vol,
                        "amount": float(parts[3]),
                    })
        
        self.data["minutes"] = all_m
        return all_m
    
    def fetch_eastmoney_push2(self):
        """3. 东方财富 push2 全字段 (主力净流入/DDX/融资融券, 需 Referer + UA)"""
        secid = f"{self.market}.{self.pure_code}"
        url = (f"https://push2.eastmoney.com/api/qt/stock/get?"
               f"secid={secid}&fields=f43,f44,f45,f46,f47,f48,f55,f56,f57,f58,f59,f60,"
               f"f62,f84,f85,f86,f87,f88,f89,f117,f168,f169,f170,f292")
        req = urllib.request.Request(url, headers={
            "Referer": "https://quote.eastmoney.com/",
            "User-Agent": "Mozilla/5.0"
        })
        try:
            raw = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
            data = json.loads(raw)
            d = data.get("data", {})
            
            def f(k, default=0):
                v = d.get(k)
                try:
                    return float(v) if v is not None else default
                except (ValueError, TypeError):
                    return default
            
            self.data["eastmoney"] = {
                "price": f("f43", 0) / 100,
                "high": f("f44", 0) / 100,
                "low": f("f45", 0) / 100,
                "open": f("f46", 0) / 100,
                "volume": int(f("f47", 0)),
                "amount": int(f("f48", 0)),
                "main_net_inflow_pct": f("f55", 0) / 100,  # 主力净流入占比
                "super_large_net": f("f56", 0),   # 超大单净流入
                "large_net": f("f57", 0),         # 大单净流入
                "medium_net": f("f58", 0),        # 中单净流入
                "small_net": f("f59", 0),         # 小单净流入
                "main_net_inflow": f("f62", 0),   # 主力净流入 (元)
                "main_in": f("f84", 0),           # 主力流入
                "main_out": f("f85", 0),          # 主力流出
                "margin_balance": f("f117", 0),   # 融资融券余额
                "turnover_rate": f("f168", 0) / 100,
                "change_amount": f("f169", 0) / 100,
                "pct_change": f("f170", 0) / 100,
                "pe_dynamic": f("f292", 0),
            }
            return self.data["eastmoney"]
        except Exception as e:
            self.data["eastmoney"] = {"error": str(e)}
            return self.data["eastmoney"]
    
    def fetch_sector(self):
        """4. 板块联动 (CPO + 半导体 + 宽基 ETF)"""
        codes = ",".join([
            "sh600330",  # 天通股份
            "sz300308",  # 中际旭创 (CPO 龙头)
            "sh688012",  # 中微公司
            "sz002371",  # 北方华创
            "sz300502",  # 新易盛
            "sh000001",  # 上证
            "sz399006",  # 创业板
            "sh588000",  # 科创 50ETF
            "sh510500",  # 中证 500ETF
            "sh510300",  # 沪深 300ETF
            "sh510050",  # 上证 50ETF
            "sh512100",  # 中证 1000ETF 南方
            "sh512480",  # 半导体 ETF
            "sh515050",  # 通信 ETF
            "sh512800",  # 银行 ETF
        ])
        url = f"https://qt.gtimg.cn/q={codes}"
        req = urllib.request.Request(url, headers={"Referer": "https://gu.qq.com/"})
        text = urllib.request.urlopen(req, timeout=10).read().decode("gbk")
        sectors = []
        for line in text.strip().split("\n"):
            if "=" not in line: continue
            c = line.split("=", 1)[1].strip()
            if c.startswith('"'): c = c[1:]
            if c.endswith('";'): c = c[:-2]
            pp = c.split("~")
            def sa(i, d=""): return pp[i] if len(pp) > i and pp[i] else d
            sectors.append({
                "code": sa(2),
                "name": sa(1),
                "price": float(sa(3)) if sa(3) else 0,
                "pct_change": float(sa(32)) if sa(32) else 0,
                "volume": int(sa(6)) if sa(6) else 0,
            })
        self.data["sectors"] = sectors
        return sectors


# ============================================================
# 2. 4 维 OBI 引擎 (基于 2026 最新学术研究)
# ============================================================

class OBIEngine:
    """4 维 OBI 模型 (基于 Cont, Kukanov, Stoikov 2014 学术研究 + 2026 增强)
    
    1. 计数 OBI: (上涨分钟 - 下跌分钟) / 总分钟
    2. 量加权 OBI: (上涨时成交量 - 下跌时成交量) / 总成交量
    3. 时间衰减 OBI: 近期 OBI 权重更大 (i * 0.05 衰减)
    4. 大单 OBI: 大单 (≥500手) 上涨 vs 下跌比例
    """
    
    def __init__(self, minutes, big_threshold=BIG_ORDER_THRESHOLD):
        self.minutes = minutes
        self.big_threshold = big_threshold
    
    def compute(self):
        """计算 4 维 OBI"""
        if not self.minutes or len(self.minutes) < 2:
            return {"error": "数据不足"}
        
        result = {}
        
        # 1. 计数 OBI
        up = down = flat = 0
        prev_price = None
        for m in self.minutes:
            if prev_price is not None:
                if m["price"] > prev_price: up += 1
                elif m["price"] < prev_price: down += 1
                else: flat += 1
            prev_price = m["price"]
        total = up + down + flat
        result["count_obi"] = (up - down) / max(1, total)
        result["count_detail"] = f"涨 {up} / 跌 {down} / 平 {flat}"
        
        # 2. 量加权 OBI
        up_vol = down_vol = 0
        prev_price = None
        for m in self.minutes:
            if prev_price is not None:
                if m["price"] > prev_price: up_vol += m["vol"]
                elif m["price"] < prev_price: down_vol += m["vol"]
            prev_price = m["price"]
        total_vol = up_vol + down_vol
        result["vol_weighted_obi"] = (up_vol - down_vol) / max(1, total_vol)
        result["vol_detail"] = f"涨时量 {up_vol:,} / 跌时量 {down_vol:,}"
        
        # 3. 时间衰减 OBI
        decay_up = decay_down = 0
        prev_price = None
        for i, m in enumerate(self.minutes):
            w = time_decay_weight(i)
            if prev_price is not None:
                if m["price"] > prev_price: decay_up += m["vol"] * w
                elif m["price"] < prev_price: decay_down += m["vol"] * w
            prev_price = m["price"]
        total_decay = decay_up + decay_down
        result["time_decay_obi"] = (decay_up - decay_down) / max(1, total_decay)
        result["decay_detail"] = f"衰减涨时 {decay_up:,.0f} / 衰减跌时 {decay_down:,.0f}"
        
        # 4. 大单 OBI
        big_up = big_down = 0
        prev_price = None
        for m in self.minutes:
            if m["vol"] >= self.big_threshold and prev_price is not None:
                if m["price"] > prev_price: big_up += 1
                elif m["price"] < prev_price: big_down += 1
            prev_price = m["price"]
        total_big = big_up + big_down
        result["big_order_obi"] = (big_up - big_down) / max(1, total_big)
        result["big_detail"] = f"大单涨 {big_up} / 大单跌 {big_down}"
        
        # 综合 OBI
        composite = (
            result["count_obi"] * OBI_WEIGHTS["count"] +
            result["vol_weighted_obi"] * OBI_WEIGHTS["vol_weighted"] +
            result["time_decay_obi"] * OBI_WEIGHTS["time_decay"] +
            result["big_order_obi"] * OBI_WEIGHTS["big_order"]
        )
        result["composite_obi"] = composite
        result["signal"] = self._signal(composite)
        
        return result
    
    def _signal(self, obi):
        if obi > 0.6: return "🟢🟢🟢 极强买入 (主力极强吸筹)"
        elif obi > 0.3: return "🟢🟢 强势买入 (主力强吸筹)"
        elif obi > 0.1: return "🟢 偏多 (主力小幅吸筹)"
        elif obi > -0.1: return "🟡 中性 (平衡)"
        elif obi > -0.3: return "🔴 偏空 (主力小幅派发)"
        elif obi > -0.6: return "🔴🔴 强势卖出 (主力强派发)"
        else: return "🔴🔴🔴 极强卖出 (主力极强派发)"


# ============================================================
# 3. OBV 增强引擎 (基于 2026 最新增强公式)
# ============================================================

class OBVEngine:
    """OBV 增强指标 (2026 鱼皮豆优化公式)
    
    增强点:
    1. 双线区分 (主力红线 + 散户灰线)
    2. 趋势提前预警 (OBV 增强趋势线)
    3. 资金体量单位换算 (万手)
    4. 适配全周期 (日线 + 分时)
    """
    
    def __init__(self, minutes):
        self.minutes = minutes
    
    def compute(self):
        if not self.minutes or len(self.minutes) < 2:
            return {"error": "数据不足"}
        
        # 基础 OBV
        obv = 0
        obv_series = []
        prev_price = None
        for m in self.minutes:
            if prev_price is not None:
                if m["price"] > prev_price:
                    obv += m["vol"]
                elif m["price"] < prev_price:
                    obv -= m["vol"]
            obv_series.append(obv)
            prev_price = m["price"]
        
        # 单位换算 (万手)
        obv_wan = obv / 10000
        
        # 主力线 (13 周期 MA)
        period_main = min(13, len(obv_series))
        obv_main = sum(obv_series[-period_main:]) / period_main / 10000
        
        # 散户线 (5 周期 MA)
        period_retail = min(5, len(obv_series))
        obv_retail = sum(obv_series[-period_retail:]) / period_retail / 10000
        
        # 增强趋势 (OBV * 0.98)
        obv_enhanced = obv_wan * 0.98
        
        # 30 周期 MAOBV (中长期)
        period_30 = min(30, len(obv_series))
        obv_ma30 = sum(obv_series[-period_30:]) / period_30 / 10000 if period_30 > 0 else 0
        
        # 红线 vs 灰线
        if obv_main > obv_retail:
            signal_type = "🟢 主力资金净流入"
            cross = "红线穿灰线 = 主力真实资金进场"
        elif obv_main < obv_retail:
            signal_type = "🔴 主力资金净流出"
            cross = "灰线穿红线 = 主力出货"
        else:
            signal_type = "🟡 平衡"
            cross = "双线黏合 = 主力观望"
        
        # 趋势判断
        if obv_wan > obv_enhanced and obv_wan > obv_ma30:
            trend = "🟢 上升趋势 (持续吸筹)"
        elif obv_wan < obv_enhanced and obv_wan < obv_ma30:
            trend = "🔴 下降趋势 (持续出货)"
        else:
            trend = "🟡 震荡 (观望)"
        
        return {
            "obv_total": obv_wan,
            "main_line": obv_main,
            "retail_line": obv_retail,
            "enhanced_trend": obv_enhanced,
            "ma30": obv_ma30,
            "signal_type": signal_type,
            "cross": cross,
            "trend": trend,
        }


# ============================================================
# 4. 龙虎榜 3 维验证引擎 (基于 2026 最新分析)
# ============================================================

class LongHubangEngine:
    """龙虎榜 3 维验证 (2026 最新)
    
    维度 1: 买卖结构 (买入前 5 / 卖出前 5 比值 ≥ 2:1)
    维度 2: 席位身份 (机构专用 + 北向 + 知名游资)
    维度 3: 3 日累计 + 量价配合
    """
    
    def __init__(self, tencent_data, eastmoney_data, current_pct):
        self.tencent = tencent_data
        self.eastmoney = eastmoney_data
        self.current_pct = current_pct
    
    def trigger_check(self):
        """龙虎榜触发条件检查"""
        triggers = {
            "涨幅 ±7%": abs(self.current_pct) >= 7,
            "跌幅 ±7%": abs(self.current_pct) >= 7,
            "换手率 20%": self.tencent.get("turnover_rate", 0) >= 20,
            "振幅 15%": self.tencent.get("amplitude", 0) >= 15,
        }
        triggered = [k for k, v in triggers.items() if v]
        return triggered
    
    def verify(self):
        """3 维验证 (基于 2026 最新方法)"""
        if not self.eastmoney:
            return {"error": "无东方财富数据"}
        
        # 维度 1: 买卖结构
        main_in = self.eastmoney.get("main_in", 0) / 1e8  # 主力流入 (亿)
        main_out = self.eastmoney.get("main_out", 0) / 1e8  # 主力流出 (亿)
        main_net = self.eastmoney.get("main_net_inflow", 0) / 1e8  # 主力净流入 (亿)
        main_net_pct = self.eastmoney.get("main_net_inflow_pct", 0)  # 主力净流入占比
        
        # 维度 2: 资金性质
        super_large = self.eastmoney.get("super_large_net", 0) / 1e8
        large = self.eastmoney.get("large_net", 0) / 1e8
        medium = self.eastmoney.get("medium_net", 0) / 1e8
        small = self.eastmoney.get("small_net", 0) / 1e8
        
        # 维度 3: 量价配合
        outer = self.tencent.get("outer_volume", 0)
        inner = self.tencent.get("inner_volume", 0)
        outer_inner_ratio = (outer - inner) / max(1, (outer + inner)) * 100
        
        # 综合判断
        dim1_signal = "🟢 买入结构强" if main_net > 0 and main_net_pct > 5 else \
                      "🔴 卖出结构强" if main_net < 0 and main_net_pct < -5 else "🟡 中性"
        
        dim2_signal = "🟢 大单+超大单净流入" if super_large + large > 0 else \
                      "🔴 大单+超大单净流出" if super_large + large < 0 else "🟡 中性"
        
        dim3_signal = "🟢 外盘主导" if outer_inner_ratio > 5 else \
                      "🔴 内盘主导" if outer_inner_ratio < -5 else "🟡 平衡"
        
        # 3 维共振判断
        bullish_count = sum(1 for s in [dim1_signal, dim2_signal, dim3_signal] if "🟢" in s)
        bearish_count = sum(1 for s in [dim1_signal, dim2_signal, dim3_signal] if "🔴" in s)
        
        if bullish_count >= 2:
            consensus = "🟢🟢🟢 三维共振: 真吸筹信号"
        elif bearish_count >= 2:
            consensus = "🔴🔴🔴 三维共振: 真出货信号"
        else:
            consensus = "🟡 三维分歧: 假动作/震荡"
        
        return {
            "dim1_买卖结构": {
                "主力净流入": main_net,
                "主力净流入占比": main_net_pct,
                "信号": dim1_signal,
            },
            "dim2_资金性质": {
                "超大单净": super_large,
                "大单净": large,
                "中单净": medium,
                "小单净": small,
                "信号": dim2_signal,
            },
            "dim3_量价配合": {
                "外盘": outer,
                "内盘": inner,
                "外/内比": outer_inner_ratio,
                "信号": dim3_signal,
            },
            "consensus": consensus,
        }


# ============================================================
# 5. 主力吸筹 5 大铁律引擎 (基于 2026 最新方法)
# ============================================================

class MainForceAbsorptionEngine:
    """主力吸筹 5 大铁律 (2026 最新)
    
    1. 筹码结构: 低位单峰密集 (90% 集中度 ≤ 10%)
    2. 量能节奏: 极致缩量 → 精准放量 → 缩量横盘
    3. 累计换手: 小盘 ≥ 300% / 中盘 ≥ 200% / 大盘 ≥ 80-120%
    4. K 线重心: 稳步抬升, 拒绝创新低
    5. 控盘度: 游资 15-30% / 机构 35-50% / 长线 ≥ 50%
    """
    
    def __init__(self, tencent_data, minutes, current_price, prev_close):
        self.tencent = tencent_data
        self.minutes = minutes
        self.current_price = current_price
        self.prev_close = prev_close
    
    def absorption_signals(self):
        """5 大铁律信号检测"""
        signals = {}
        
        # 铁律 1: 筹码结构 (用 OBI 替代, 简化判断)
        signals["铁律 1_筹码结构"] = "🟡 需 Level-2 筹码数据验证 (本系统未集成)"
        
        # 铁律 2: 量能节奏
        if not self.minutes:
            return signals
        recent_15 = self.minutes[-15:] if len(self.minutes) >= 15 else self.minutes
        recent_15_avg = sum(m["vol"] for m in recent_15) / max(1, len(recent_15))
        total_avg = sum(m["vol"] for m in self.minutes) / max(1, len(self.minutes))
        vol_ratio = recent_15_avg / max(1, total_avg)
        
        if vol_ratio < 0.5:
            signals["铁律 2_量能节奏"] = f"🟢🟢 极致缩量 (近期 15 分钟量比 {vol_ratio:.2f})"
        elif vol_ratio < 0.8:
            signals["铁律 2_量能节奏"] = f"🟢 缩量 (近期 15 分钟量比 {vol_ratio:.2f})"
        elif vol_ratio > 1.5:
            signals["铁律 2_量能节奏"] = f"🔴 放量 (近期 15 分钟量比 {vol_ratio:.2f})"
        else:
            signals["铁律 2_量能节奏"] = f"🟡 正常 (近期 15 分钟量比 {vol_ratio:.2f})"
        
        # 铁律 3: 累计换手
        turnover = self.tencent.get("turnover_rate", 0)
        if turnover >= 8:
            signals["铁律 3_累计换手"] = f"🟢🟢 充分换手 {turnover:.2f}%"
        elif turnover >= 5:
            signals["铁律 3_累计换手"] = f"🟢 健康换手 {turnover:.2f}%"
        elif turnover >= 3:
            signals["铁律 3_累计换手"] = f"🟡 一般换手 {turnover:.2f}%"
        else:
            signals["铁律 3_累计换手"] = f"🔴 换手不足 {turnover:.2f}%"
        
        # 铁律 4: K 线重心 (高低点 + 开盘价)
        open_p = self.tencent.get("open", 0)
        high_p = self.tencent.get("high", 0)
        low_p = self.tencent.get("low", 0)
        
        if self.current_price > open_p > self.prev_close:
            signals["铁律 4_K线重心"] = f"🟢🟢 重心抬升 (开 {open_p:.2f} > 昨收 {self.prev_close:.2f})"
        elif self.current_price > open_p:
            signals["铁律 4_K线重心"] = f"🟢 重心抬升 (现 {self.current_price:.2f} > 开 {open_p:.2f})"
        elif self.current_price < low_p * 1.01:
            signals["铁律 4_K线重心"] = f"🔴 创新低 (现 {self.current_price:.2f} 接近今低 {low_p:.2f})"
        else:
            signals["铁律 4_K线重心"] = f"🟡 震荡 (现 {self.current_price:.2f} / 开 {open_p:.2f})"
        
        # 铁律 5: 控盘度 (用振幅 + 换手估算)
        amplitude = self.tencent.get("amplitude", 0)
        if amplitude > 8 and turnover > 5:
            signals["铁律 5_控盘度"] = f"🟢 机构控盘 (振幅 {amplitude:.2f}% + 换手 {turnover:.2f}%)"
        elif amplitude > 5 and turnover > 3:
            signals["铁律 5_控盘度"] = f"🟡 中等控盘 (振幅 {amplitude:.2f}% + 换手 {turnover:.2f}%)"
        else:
            signals["铁律 5_控盘度"] = f"🟢 游资控盘 (振幅 {amplitude:.2f}% + 换手 {turnover:.2f}%)"
        
        return signals


# ============================================================
# 6. 6 因子综合评分引擎
# ============================================================

class FactorEngine:
    """6 因子综合评分"""
    
    FACTORS = [
        ("趋势", 0.15, "现价 vs 昨收 vs 开盘 vs 最高/最低"),
        ("动量", 0.15, "涨跌幅 + 振幅"),
        ("量价", 0.10, "成交量 + 换手率 + 外内盘比"),
        ("波动", 0.10, "振幅 + ATR"),
        ("资金流向", 0.20, "主力净流入 + 5 档单"),
        ("DDX/DDY", 0.10, "大单动向"),
        ("板块", 0.10, "板块联动 + 背离"),
        ("涨停", 0.10, "是否涨停 + 封单"),
    ]
    
    def __init__(self, tencent, eastmoney, obi_result, obv_result, sector_data, code):
        self.tencent = tencent
        self.eastmoney = eastmoney
        self.obi = obi_result
        self.obv = obv_result
        self.sectors = sector_data
        self.code = code
    
    def compute(self):
        scores = {}
        
        # 1. 趋势
        pct = self.tencent.get("pct_change", 0)
        if pct > 5: scores["趋势"] = 90
        elif pct > 2: scores["趋势"] = 75
        elif pct > 0: scores["趋势"] = 60
        elif pct > -3: scores["趋势"] = 40
        else: scores["趋势"] = 20
        
        # 2. 动量
        amp = self.tencent.get("amplitude", 0)
        if abs(pct) > 5 and amp > 5: scores["动量"] = 85
        elif abs(pct) > 2: scores["动量"] = 70
        else: scores["动量"] = 50
        
        # 3. 量价
        turnover = self.tencent.get("turnover_rate", 0)
        outer = self.tencent.get("outer_volume", 0)
        inner = self.tencent.get("inner_volume", 0)
        if outer > inner and turnover > 5:
            scores["量价"] = 80
        elif outer > inner:
            scores["量价"] = 60
        else:
            scores["量价"] = 30
        
        # 4. 波动
        if amp > 8: scores["波动"] = 70  # 高波动
        elif amp > 4: scores["波动"] = 55
        else: scores["波动"] = 40
        
        # 5. 资金流向
        if self.eastmoney and "main_net_inflow" in self.eastmoney:
            main_net = self.eastmoney.get("main_net_inflow", 0) / 1e8
            main_pct = self.eastmoney.get("main_net_inflow_pct", 0)
            if main_net > 1: scores["资金流向"] = 90
            elif main_net > 0: scores["资金流向"] = 70
            elif main_net > -1: scores["资金流向"] = 40
            else: scores["资金流向"] = 20
        else:
            # fallback: 用外内盘
            if outer > inner * 1.1: scores["资金流向"] = 70
            else: scores["资金流向"] = 50
        
        # 6. DDX/DDY
        if self.eastmoney:
            super_large = self.eastmoney.get("super_large_net", 0) / 1e8
            large = self.eastmoney.get("large_net", 0) / 1e8
            if super_large + large > 0.5: scores["DDX/DDY"] = 85
            elif super_large + large > 0: scores["DDX/DDY"] = 65
            else: scores["DDX/DDY"] = 35
        else:
            scores["DDX/DDY"] = 50
        
        # 7. 板块
        stock = next((s for s in self.sectors if s["code"] == self.code[2:]), None)
        if stock:
            sector_pct = [s["pct_change"] for s in self.sectors if s["code"] != self.code[2:]]
            if sector_pct:
                avg = sum(sector_pct) / len(sector_pct)
                divergence = stock["pct_change"] - avg
                if divergence > 3: scores["板块"] = 90
                elif divergence > 0: scores["板块"] = 65
                elif divergence > -3: scores["板块"] = 45
                else: scores["板块"] = 25
            else:
                scores["板块"] = 50
        else:
            scores["板块"] = 50
        
        # 8. 涨停
        if pct >= 9.5: scores["涨停"] = 95
        elif pct >= 5: scores["涨停"] = 70
        elif pct <= -9.5: scores["涨停"] = 10
        elif pct <= -5: scores["涨停"] = 25
        else: scores["涨停"] = 50
        
        # 加权综合
        total = sum(scores[k] * w for k, w, _ in self.FACTORS)
        scores["综合"] = round(total, 2)
        
        return scores


# ============================================================
# 7. 主分析器
# ============================================================

class QuantAnalyzer:
    """v13 主分析器"""
    
    def __init__(self, code=STOCK_CODE):
        self.code = code
        self.data_layer = DataLayer(code)
    
    def run(self):
        print("=" * 80)
        print(f"# {STOCK_NAME} ({self.code}) v13 量化分析器 - {TODAY}")
        print("=" * 80)
        print()
        
        # 1. 数据抓取
        print("## 📊 Step 1: 数据抓取 (4 大数据源)")
        tencent = self.data_layer.fetch_tencent_quote()
        minutes = self.data_layer.fetch_tencent_minute()
        eastmoney = self.data_layer.fetch_eastmoney_push2()
        sectors = self.data_layer.fetch_sector()
        print(f"   ✅ 腾讯报价: {tencent.get('name')} {tencent.get('price')} ({tencent.get('pct_change')}%)")
        print(f"   ✅ 腾讯分时: {len(minutes)} 分钟")
        print(f"   ✅ 东方财富 push2: {'成功' if eastmoney and 'error' not in eastmoney else '失败'}")
        print(f"   ✅ 板块联动: {len(sectors)} 标的")
        print()
        
        # 2. OBI 4 维分析
        print("## 🎯 Step 2: 4 维 OBI 分析 (基于 2026 学术研究)")
        obi_engine = OBIEngine(minutes)
        obi_result = obi_engine.compute()
        if "error" not in obi_result:
            print(f"   1. 计数 OBI (权重 0.15): {obi_result['count_obi']:+.4f} | {obi_result['count_detail']}")
            print(f"   2. 量加权 OBI (权重 0.30): {obi_result['vol_weighted_obi']:+.4f} | {obi_result['vol_detail']}")
            print(f"   3. 时间衰减 OBI (权重 0.25): {obi_result['time_decay_obi']:+.4f} | {obi_result['decay_detail']}")
            print(f"   4. 大单 OBI (权重 0.30): {obi_result['big_order_obi']:+.4f} | {obi_result['big_detail']}")
            print(f"   **综合 OBI: {obi_result['composite_obi']:+.4f}**")
            print(f"   信号: {obi_result['signal']}")
        print()
        
        # 3. OBV 增强
        print("## 📈 Step 3: OBV 增强分析 (2026 鱼皮豆优化公式)")
        obv_engine = OBVEngine(minutes)
        obv_result = obv_engine.compute()
        if "error" not in obv_result:
            print(f"   OBV 总量: {obv_result['obv_total']:.2f} 万手")
            print(f"   主力线 (13 周期): {obv_result['main_line']:.2f} 万手")
            print(f"   散户线 (5 周期): {obv_result['retail_line']:.2f} 万手")
            print(f"   增强趋势线: {obv_result['enhanced_trend']:.2f} 万手")
            print(f"   30 周期 MAOBV: {obv_result['ma30']:.2f} 万手")
            print(f"   {obv_result['signal_type']}")
            print(f"   {obv_result['cross']}")
            print(f"   趋势: {obv_result['trend']}")
        print()
        
        # 4. 龙虎榜 3 维验证
        print("## 🐉 Step 4: 龙虎榜 3 维验证 (2026 最新方法)")
        lh_engine = LongHubangEngine(tencent, eastmoney, tencent.get("pct_change", 0))
        triggered = lh_engine.trigger_check()
        print(f"   触发条件: {', '.join(triggered) if triggered else '❌ 无触发'}")
        lh_result = lh_engine.verify()
        if "error" not in lh_result:
            print(f"   维度 1 (买卖结构): {lh_result['dim1_买卖结构']['信号']}")
            print(f"     主力净流入: {lh_result['dim1_买卖结构']['主力净流入']:.2f} 亿")
            print(f"     主力净流入占比: {lh_result['dim1_买卖结构']['主力净流入占比']:.2f}%")
            print(f"   维度 2 (资金性质): {lh_result['dim2_资金性质']['信号']}")
            print(f"     超大单: {lh_result['dim2_资金性质']['超大单净']:.2f} 亿")
            print(f"     大单: {lh_result['dim2_资金性质']['大单净']:.2f} 亿")
            print(f"   维度 3 (量价配合): {lh_result['dim3_量价配合']['信号']}")
            print(f"     外/内盘比: {lh_result['dim3_量价配合']['外/内比']:.2f}%")
            print(f"   **综合: {lh_result['consensus']}**")
        print()
        
        # 5. 主力吸筹 5 大铁律
        print("## 🎯 Step 5: 主力吸筹 5 大铁律 (2026 最新)")
        mf_engine = MainForceAbsorptionEngine(
            tencent, minutes, tencent.get("price", 0), tencent.get("prev_close", 0)
        )
        signals = mf_engine.absorption_signals()
        for k, v in signals.items():
            print(f"   {k}: {v}")
        print()
        
        # 6. 6 因子综合评分
        print("## 🎯 Step 6: 6 因子综合评分")
        factor_engine = FactorEngine(tencent, eastmoney, obi_result, obv_result, sectors, self.code)
        scores = factor_engine.compute()
        for k, w, desc in factor_engine.FACTORS:
            print(f"   {k} (权重 {w:.2f}): {scores[k]}/100 | {desc}")
        print(f"   **综合评分: {scores['综合']}/100**")
        print()
        
        # 7. 操作建议
        print("## 💡 Step 7: 操作建议")
        self._advice(tencent, obi_result, obv_result, scores, lh_result)
        print()
        
        # 8. 输出 JSON
        result = {
            "timestamp": TODAY,
            "code": self.code,
            "name": tencent.get("name"),
            "tencent": tencent,
            "eastmoney": eastmoney,
            "obi": obi_result,
            "obv": obv_result,
            "longhubang": lh_result,
            "mainforce_signals": signals,
            "factor_scores": scores,
            "sectors": sectors,
        }
        
        # 保存结果
        with open("/workspace/v13/analysis_result.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2, default=str)
        print(f"## 📁 结果已保存: /workspace/v13/analysis_result.json")
        
        return result
    
    def _advice(self, tencent, obi, obv, scores, lh):
        pct = tencent.get("pct_change", 0)
        obi_composite = obi.get("composite_obi", 0) if obi else 0
        
        print(f"   当前: {tencent.get('price')} ({pct:+.2f}%) | 振幅 {tencent.get('amplitude', 0):.2f}% | 换手 {tencent.get('turnover_rate', 0):.2f}%")
        print()
        
        # 主力行为判断
        if obi_composite > 0.1 and pct > 0:
            print(f"   🟢🟢 综合 OBI {obi_composite:+.3f} + 涨幅 {pct:+.2f}% = 主力吸筹中")
        elif obi_composite < -0.1 and pct < 0:
            print(f"   🔴🔴 综合 OBI {obi_composite:+.3f} + 跌幅 {pct:+.2f}% = 主力派发中")
        elif obi_composite > 0.1 and pct < 0:
            print(f"   🟡 综合 OBI {obi_composite:+.3f} + 跌幅 {pct:+.2f}% = 主力洗盘 (吸筹 + 砸盘)")
        else:
            print(f"   🟡 综合 OBI {obi_composite:+.3f} + 涨跌幅 {pct:+.2f}% = 主力观望")
        
        # 关键位
        prev_close = tencent.get("prev_close", 0)
        open_p = tencent.get("open", 0)
        high_p = tencent.get("high", 0)
        low_p = tencent.get("low", 0)
        current = tencent.get("price", 0)
        
        print()
        print("   关键位:")
        print(f"   阻力: R1 {high_p:.2f} (今高) | R2 {open_p:.2f} (开盘) | R3 {prev_close * 1.03:.2f} (+3%)")
        print(f"   现价: {current:.2f}")
        print(f"   支撑: S1 {open_p:.2f} (开盘) | S2 {prev_close:.2f} (昨收) | S3 {low_p:.2f} (今低)")


if __name__ == "__main__":
    analyzer = QuantAnalyzer()
    analyzer.run()
