"""
习惯分析器 - 支持周期识别
"""
import statistics
from typing import Optional, List
from datetime import datetime, time as dt_time, timedelta
from src.models.habit import HabitReport


class HabitAnalyzer:
    """分析设备使用习惯 - 支持周期识别"""
    
    def __init__(self):
        self.min_confidence = 0.6
    
    def analyze(
        self, 
        entity_id: str, 
        state_history: List[dict]
    ) -> HabitReport:
        """分析单个设备的习惯"""
        
        if not state_history:
            return HabitReport(
                entity_id=entity_id,
                confidence=0.0,
                sample_count=0
            )
        
        # 提取开关时间 + 星期几
        on_data = []
        off_data = []
        
        for state in state_history:
            timestamp = state.get("last_changed")
            if not timestamp:
                continue
                
            try:
                dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                hour = dt.hour
                weekday = dt.weekday()  # 0=周一, 6=周日
                
                if state.get("state") == "on":
                    on_data.append({"hour": hour, "weekday": weekday, "dt": dt})
                else:
                    off_data.append({"hour": hour, "weekday": weekday, "dt": dt})
            except:
                continue
        
        # 计算典型时间
        typical_on = self._calculate_typical_time([d["hour"] for d in on_data]) if on_data else None
        typical_off = self._calculate_typical_time([d["hour"] for d in off_data]) if off_data else None
        
        # 计算置信度
        confidence = self._calculate_confidence(on_data, off_data)
        
        # 周期分析
        weekday_pattern = self._analyze_weekday_pattern(on_data, off_data)
        
        return HabitReport(
            entity_id=entity_id,
            typical_on_time=typical_on,
            typical_off_time=typical_off,
            weekday_pattern=weekday_pattern,
            confidence=confidence,
            sample_count=len(state_history)
        )
    
    def _calculate_typical_time(self, times: List[int]) -> Optional[str]:
        """计算典型时间"""
        if not times:
            return None
            
        if len(times) == 1:
            return f"{times[0]:02d}:00"
        
        median_val = statistics.median(times)
        hour = int(median_val)
        return f"{hour:02d}:00"
    
    def _calculate_confidence(
        self, 
        on_data: List[dict], 
        off_data: List[dict]
    ) -> float:
        """计算置信度"""
        total = len(on_data) + len(off_data)
        
        if total < 5:
            return 0.0
        if total < 10:
            return 0.5
        if total < 20:
            return 0.7
        
        # 考虑周期一致性
        weekday_consistency = self._calculate_weekday_consistency(on_data, off_data)
        
        return min(0.95, 0.6 + (total - 10) * 0.02 + weekday_consistency * 0.1)
    
    def _calculate_weekday_consistency(
        self, 
        on_data: List[dict], 
        off_data: List[dict]
    ) -> float:
        """计算周期一致性"""
        if len(on_data) < 7:
            return 0.0
        
        # 检查工作日和周末是否有区别
        weekday_hours = [d["hour"] for d in on_data if d["weekday"] < 5]
        weekend_hours = [d["hour"] for d in on_data if d["weekday"] >= 5]
        
        if not weekday_hours or not weekend_hours:
            return 0.5
        
        # 如果差异大，说明有周期
        weekday_avg = statistics.mean(weekday_hours)
        weekend_avg = statistics.mean(weekend_hours)
        
        diff = abs(weekday_avg - weekend_avg)
        
        if diff > 2:  # 差异大于2小时
            return 1.0
        elif diff > 1:
            return 0.7
        else:
            return 0.3
    
    def _analyze_weekday_pattern(
        self, 
        on_data: List[dict], 
        off_data: List[dict]
    ) -> str:
        """分析周期模式"""
        if len(on_data) < 7:
            return "daily"
        
        weekday_hours = [d["hour"] for d in on_data if d["weekday"] < 5]
        weekend_hours = [d["hour"] for d in on_data if d["weekday"] >= 5]
        
        if not weekday_hours or not weekend_hours:
            return "daily"
        
        weekday_avg = statistics.mean(weekday_hours)
        weekend_avg = statistics.mean(weekend_hours)
        
        diff = abs(weekday_avg - weekend_avg)
        
        if diff > 2:
            return "weekday_weekend"  # 工作日/周末不同
        else:
            return "daily"  # 每天都差不多
    
    def should_suggest(self, habit: HabitReport) -> bool:
        """是否应该生成建议"""
        return habit.confidence >= self.min_confidence
