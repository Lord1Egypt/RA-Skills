#!/usr/bin/env python3
"""
智能排期算法
基于内容类型、目标受众和历史数据推荐最佳发布时间
"""

from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from dataclasses import dataclass
import random


@dataclass
class TimeSlot:
    """时间段数据结构"""
    hour: int
    score: float  # 推荐分数 0-100
    reason: str   # 推荐理由
    audience_type: str  # 受众类型


class SmartScheduler:
    """智能排期器"""
    
    # 小红书用户活跃时段数据（基于行业研究）
    # 分数越高表示该时段发布效果越好
    PEAK_HOURS = {
        # 早晨通勤时段
        7: {'score': 65, 'audience': '早起上班族', 'reason': '通勤刷手机高峰'},
        8: {'score': 75, 'audience': '上班族', 'reason': '上班前碎片时间'},
        
        # 上午工作时段
        9: {'score': 55, 'audience': '摸鱼党', 'reason': '工作间隙短暂休息'},
        10: {'score': 60, 'audience': '学生/自由职业', 'reason': '上午活跃时段'},
        11: {'score': 50, 'audience': '一般用户', 'reason': '午饭前准备'},
        
        # 午休时段 - 黄金时段
        12: {'score': 85, 'audience': '全量用户', 'reason': '午休刷手机高峰'},
        13: {'score': 80, 'audience': '全量用户', 'reason': '午休延续时段'},
        
        # 下午工作时段
        14: {'score': 55, 'audience': '摸鱼党', 'reason': '下午茶时间'},
        15: {'score': 60, 'audience': '学生党', 'reason': '下午课间'},
        16: {'score': 65, 'audience': '下班前', 'reason': '准备下班摸鱼'},
        
        # 晚高峰 - 最黄金时段
        17: {'score': 70, 'audience': '下班族', 'reason': '下班通勤开始'},
        18: {'score': 85, 'audience': '下班族', 'reason': '下班通勤高峰'},
        19: {'score': 90, 'audience': '全量用户', 'reason': '晚饭后休闲时光'},
        20: {'score': 95, 'audience': '全量用户', 'reason': '晚间黄金时段'},
        21: {'score': 90, 'audience': '夜猫子', 'reason': '睡前刷手机高峰'},
        22: {'score': 80, 'audience': '夜猫子', 'reason': '深夜活跃时段'},
        
        # 深夜时段
        23: {'score': 60, 'audience': '夜猫子', 'reason': '深夜党专属'},
        0: {'score': 40, 'audience': '极少数', 'reason': '深夜流量低'},
    }
    
    # 内容类型权重调整
    CONTENT_TYPE_WEIGHTS = {
        'fashion': {  # 时尚穿搭
            'boost_hours': [12, 13, 19, 20, 21],
            'boost_factor': 1.2,
            'desc': '时尚穿搭类'
        },
        'beauty': {  # 美妆护肤
            'boost_hours': [12, 13, 20, 21, 22],
            'boost_factor': 1.15,
            'desc': '美妆护肤类'
        },
        'food': {  # 美食
            'boost_hours': [11, 12, 17, 18, 19],
            'boost_factor': 1.25,
            'desc': '美食类'
        },
        'travel': {  # 旅行
            'boost_hours': [19, 20, 21, 22],
            'boost_factor': 1.1,
            'desc': '旅行类'
        },
        'tech': {  # 数码科技
            'boost_hours': [12, 13, 20, 21],
            'boost_factor': 1.05,
            'desc': '数码科技类'
        },
        'lifestyle': {  # 生活方式
            'boost_hours': [12, 13, 19, 20, 21],
            'boost_factor': 1.1,
            'desc': '生活方式类'
        },
        'education': {  # 教育学习
            'boost_hours': [9, 10, 14, 15, 20],
            'boost_factor': 1.15,
            'desc': '教育学习类'
        },
        'default': {
            'boost_hours': [12, 13, 19, 20, 21],
            'boost_factor': 1.0,
            'desc': '通用类型'
        }
    }
    
    def __init__(self):
        self.time_slots = self._init_time_slots()
    
    def _init_time_slots(self) -> Dict[int, TimeSlot]:
        """初始化时间段数据"""
        slots = {}
        for hour, data in self.PEAK_HOURS.items():
            slots[hour] = TimeSlot(
                hour=hour,
                score=data['score'],
                reason=data['reason'],
                audience_type=data['audience']
            )
        return slots
    
    def get_best_times(self, content_type: str = 'default', 
                      count: int = 3,
                      days_ahead: int = 1) -> List[Dict]:
        """
        获取推荐的最佳发布时间
        
        Args:
            content_type: 内容类型 (fashion/beauty/food/travel/tech/lifestyle/education)
            count: 推荐数量
            days_ahead: 提前天数（1=明天，2=后天）
            
        Returns:
            推荐时间段列表
        """
        # 获取内容类型权重
        weights = self.CONTENT_TYPE_WEIGHTS.get(content_type, self.CONTENT_TYPE_WEIGHTS['default'])
        
        # 计算加权分数
        scored_slots = []
        for hour, slot in self.time_slots.items():
            score = slot.score
            
            # 应用内容类型权重
            if hour in weights['boost_hours']:
                score *= weights['boost_factor']
            
            scored_slots.append({
                'hour': hour,
                'score': min(score, 100),  # 最高100分
                'original_score': slot.score,
                'reason': slot.reason,
                'audience': slot.audience_type,
                'content_type': weights['desc']
            })
        
        # 按分数排序
        scored_slots.sort(key=lambda x: x['score'], reverse=True)
        
        # 生成推荐时间（未来几天）
        recommendations = []
        base_date = datetime.now() + timedelta(days=days_ahead)
        
        for i, slot in enumerate(scored_slots[:count]):
            # 分散到不同日期，避免同一天发布过多
            target_date = base_date + timedelta(days=i // 2)
            
            recommended_time = target_date.replace(
                hour=slot['hour'],
                minute=random.choice([0, 15, 30, 45]),  # 随机分钟，避免整点
                second=0,
                microsecond=0
            )
            
            recommendations.append({
                'rank': i + 1,
                'datetime': recommended_time,
                'score': round(slot['score'], 1),
                'hour': slot['hour'],
                'reason': slot['reason'],
                'audience': slot['audience'],
                'content_type': slot['content_type'],
                'confidence': self._get_confidence_level(slot['score'])
            })
        
        return recommendations
    
    def _get_confidence_level(self, score: float) -> str:
        """根据分数返回置信度等级"""
        if score >= 85:
            return '[极高]'
        elif score >= 75:
            return '[高]'
        elif score >= 65:
            return '[中等]'
        else:
            return '[一般]'
    
    def schedule_batch(self, task_count: int, 
                      content_type: str = 'default',
                      start_date: datetime = None) -> List[datetime]:
        """
        为批量内容生成排期表
        
        Args:
            task_count: 内容数量
            content_type: 内容类型
            start_date: 开始日期
            
        Returns:
            发布时间列表
        """
        if start_date is None:
            start_date = datetime.now() + timedelta(days=1)
        
        # 获取最佳时段
        best_times = self.get_best_times(content_type, count=10)
        
        # 分配发布时间
        schedule = []
        for i in range(task_count):
            # 循环使用最佳时段，但分散到不同天
            time_slot = best_times[i % len(best_times)]
            
            # 每2篇内容推迟一天
            day_offset = i // 2
            publish_time = time_slot['datetime'] + timedelta(days=day_offset)
            
            # 确保不早于开始日期
            if publish_time.date() < start_date.date():
                publish_time = start_date.replace(
                    hour=publish_time.hour,
                    minute=publish_time.minute
                )
            
            schedule.append(publish_time)
        
        return sorted(schedule)
    
    def analyze_optimal_window(self, historical_data: List[Dict] = None) -> Dict:
        """
        分析最佳发布窗口（可接入历史数据优化）
        
        Args:
            historical_data: 历史发布数据（可选）
            
        Returns:
            分析报告
        """
        # 基础分析
        daily_slots = []
        for hour in range(7, 24):
            slot = self.time_slots.get(hour)
            if slot:
                daily_slots.append({
                    'hour': hour,
                    'score': slot.score,
                    'label': f"{hour}:00",
                    'recommendation': '推荐' if slot.score >= 75 else ('可考虑' if slot.score >= 60 else '不推荐')
                })
        
        # 找出黄金时段
        golden_hours = [s for s in daily_slots if s['score'] >= 80]
        good_hours = [s for s in daily_slots if 65 <= s['score'] < 80]
        
        return {
            'golden_hours': golden_hours,
            'good_hours': good_hours,
            'daily_timeline': daily_slots,
            'summary': {
                'best_periods': ['12:00-13:00', '19:00-22:00'],
                'avoid_periods': ['00:00-06:00', '09:00-11:00'],
                'peak_days': ['周二', '周四', '周六', '周日']
            }
        }
    
    def get_avoid_times(self) -> List[str]:
        """获取应该避免的发布时间"""
        return [
            '00:00-06:00 - 深夜流量极低',
            '09:00-11:00 - 工作时间，用户活跃度低',
            '14:00-16:00 - 下午工作时段，效果一般'
        ]


# CLI接口
if __name__ == '__main__':
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description='小红书智能排期算法')
    parser.add_argument('--type', default='default', 
                       choices=['fashion', 'beauty', 'food', 'travel', 'tech', 'lifestyle', 'education', 'default'],
                       help='内容类型')
    parser.add_argument('--count', type=int, default=3, help='推荐数量')
    parser.add_argument('--batch', type=int, help='批量排期数量')
    parser.add_argument('--format', choices=['json', 'table'], default='table', help='输出格式')
    
    args = parser.parse_args()
    
    scheduler = SmartScheduler()
    
    if args.batch:
        # 批量排期
        schedule = scheduler.schedule_batch(args.batch, args.type)
        print(f"\n批量排期表 ({args.batch}篇内容)\n")
        type_info = scheduler.CONTENT_TYPE_WEIGHTS.get(args.type, scheduler.CONTENT_TYPE_WEIGHTS['default'])
        print(f"内容类型: {type_info['desc']}")
        print()
        for i, time in enumerate(schedule, 1):
            print(f"第{i}篇: {time.strftime('%Y-%m-%d %H:%M')}")
    
    else:
        # 获取推荐时间
        recommendations = scheduler.get_best_times(args.type, args.count)
        
        if args.format == 'json':
            print(json.dumps(recommendations, indent=2, default=str))
        else:
            print("\n最佳发布时间推荐\n")
            print(f"内容类型: {recommendations[0]['content_type']}")
            print()
            
            for rec in recommendations:
                print(f"#{rec['rank']} {rec['confidence']}")
                print(f"   时间: {rec['datetime'].strftime('%Y-%m-%d %H:%M')}")
                print(f"   评分: {rec['score']}/100")
                print(f"   受众: {rec['audience']}")
                print(f"   理由: {rec['reason']}")
                print()
            
            # 显示分析
            analysis = scheduler.analyze_optimal_window()
            print("黄金时段窗口")
            print(f"   最佳: {', '.join(analysis['summary']['best_periods'])}")
            print(f"   避开: {', '.join(analysis['summary']['avoid_periods'])}")
            print(f"   推荐发布日: {', '.join(analysis['summary']['peak_days'])}")
