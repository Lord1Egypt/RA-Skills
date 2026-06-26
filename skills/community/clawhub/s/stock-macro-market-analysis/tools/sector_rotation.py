#!/usr/bin/env python3
"""
板块轮动追踪器
追踪行业板块强弱变化，识别轮动节奏，预判下一个热点方向
"""

import json
import argparse
from dataclasses import dataclass, asdict
import pandas as pd
import numpy as np


@dataclass
class SectorMetrics:
    name: str
    change_1d: float       # 今日涨跌幅
    change_5d: float       # 5日涨跌幅
    change_20d: float      # 20日涨跌幅
    volume_ratio: float    # 量比
    capital_flow: float    # 主力净流入(亿)
    north_flow: float      # 北向净流入(亿)
    limit_up_count: int    # 涨停数
    momentum_score: float  # 动量评分
    heat_rank: int         # 热度排名
    stage: str             # 启动期/主升期/高潮期/退潮期


class SectorRotationTracker:

    # 经典美林时钟板块轮动逻辑
    CYCLE_SECTORS = {
        "复苏期": {
            "受益": ["信息技术", "可选消费", "工业", "金融"],
            "规避": ["公用事业", "日常消费"],
        },
        "过热期": {
            "受益": ["能源", "材料", "工业"],
            "规避": ["信息技术", "金融"],
        },
        "滞胀期": {
            "受益": ["能源", "日常消费", "医疗保健", "公用事业"],
            "规避": ["信息技术", "可选消费", "金融"],
        },
        "衰退期": {
            "受益": ["公用事业", "日常消费", "医疗保健", "金融(降息预期)"],
            "规避": ["能源", "材料", "工业"],
        },
    }

    def __init__(self, sector_data: list[dict]):
        self.sectors = [SectorMetrics(**s) for s in sector_data]

    def rank_sectors(self) -> list[dict]:
        """综合排名：动量 + 资金 + 热度"""
        for s in self.sectors:
            # 综合评分 = 40%动量 + 30%资金 + 30%热度
            s.momentum_score = (
                s.change_1d * 0.2 +
                s.change_5d * 0.3 +
                s.change_20d * 0.5
            )

        # 按综合评分排序
        ranked = sorted(self.sectors, key=lambda x: x.momentum_score, reverse=True)
        for i, s in enumerate(ranked):
            s.heat_rank = i + 1
        return [asdict(s) for s in ranked]

    def identify_rotation_stage(self, sector: SectorMetrics) -> str:
        """
        判断板块所处阶段:
        - 启动期: 缩量→放量，小幅上涨，涨停股少
        - 主升期: 持续放量，连续上涨，涨停股增多
        - 高潮期: 巨量，涨停潮，全面开花
        - 退潮期: 量能萎缩，分化加剧，龙头补跌
        """
        if sector.change_20d > 15 and sector.volume_ratio > 2.0 and sector.limit_up_count > 10:
            return "高潮期（⚠️注意风险，不宜追高）"
        elif sector.change_20d > 8 and sector.change_5d > 3 and sector.volume_ratio > 1.3:
            return "主升期（可顺势参与龙头）"
        elif sector.change_5d > 2 and sector.volume_ratio > 1.0 and sector.change_20d < 8:
            return "启动期（🔔关注，可能是新一轮行情起点）"
        elif sector.change_5d < -2 and sector.change_20d > 5:
            return "退潮期（回避，等待下一轮机会）"
        else:
            return "蛰伏期（暂不活跃）"

    def detect_rotation_pattern(self) -> dict:
        """
        检测当前板块轮动模式
        """
        strong_sectors = [s for s in self.sectors if s.change_5d > 3]
        weak_sectors = [s for s in self.sectors if s.change_5d < -2]

        # 轮动速度
        if len(strong_sectors) > 5:
            rotation_speed = "普涨（市场做多热情高）"
        elif len(strong_sectors) >= 2:
            rotation_speed = "正常轮动（资金在板块间切换）"
        elif len(strong_sectors) == 1:
            rotation_speed = "集中（资金高度集中于单一方向）"
        else:
            rotation_speed = "冰冻（缺乏热点，市场低迷）"

        # 风格偏好
        growth_avg = np.mean([s.change_5d for s in self.sectors
                              if s.name in ["信息技术", "通信", "医疗保健"]])
        value_avg = np.mean([s.change_5d for s in self.sectors
                             if s.name in ["金融", "能源", "公用事业"]])

        if growth_avg > value_avg + 1:
            style = "偏成长（科技/医药领涨）"
        elif value_avg > growth_avg + 1:
            style = "偏价值（金融/周期领涨）"
        else:
            style = "均衡"

        return {
            "rotation_speed": rotation_speed,
            "style_preference": style,
            "strong_sectors": [s.name for s in strong_sectors],
            "weak_sectors": [s.name for s in weak_sectors],
            "recommendation": self._generate_recommendation(strong_sectors, weak_sectors),
        }

    def _generate_recommendation(self, strong, weak) -> str:
        strong_names = [s.name for s in strong[:3]]
        if not strong_names:
            return "当前市场缺乏持续热点，建议观望，等待明确方向"
        stages = {s.name: self.identify_rotation_stage(s) for s in strong[:3]}
        recs = []
        for name, stage in stages.items():
            if "启动期" in stage:
                recs.append(f"🔔 {name}处于启动期，可重点关注龙头标的")
            elif "主升期" in stage:
                recs.append(f"📈 {name}处于主升期，可顺势参与但注意止盈")
            elif "高潮期" in stage:
                recs.append(f"⚠️ {name}已进入高潮期，不宜追高")
        return " | ".join(recs) if recs else "当前热点板块需进一步确认持续性"