"""
训练计划生成器
基于LLM生成个性化的训练计划

支持：
- 16周训练计划
- 每日训练计划
- 跑步比赛计划（马拉松/10km/5km）
- 恢复计划
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional

# 导入LLM模块
from lib.llm import LLMClient, get_llm_client

# 数据路径
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(SKILL_DIR, "data", "processed", "latest.json")
USER_DATA_DIR = os.path.join(SKILL_DIR, "data", "profiles")


class TrainingPlanGenerator:
    """
    训练计划生成器
    
    使用LLM根据用户具体情况生成个性化训练计划
    """
    
    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        self.llm_generator = LLMClient(user_id)
        self.whoop_data = self._load_whoop_data()
        self.user_data = self._load_user_data()
    
    def _load_whoop_data(self) -> Dict:
        """加载WHOOP数据"""
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}
    
    def _load_user_data(self) -> Dict:
        """加载用户数据"""
        user_file = os.path.join(USER_DATA_DIR, f"{self.user_id}.json")
        try:
            if os.path.exists(user_file):
                with open(user_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return self._get_default_user_data()
    
    def _get_default_user_data(self) -> Dict:
        """获取默认用户数据"""
        return {
            "goal": "增肌",
            "experience_years": 2,
            "days_per_week": 4,
            "body_weight": 75,
            "equipment": ["健身房全套"]
        }
    
    def generate_16week_plan(self) -> str:
        """
        生成16周训练计划
        
        Returns:
            16周训练计划文本（由LLM生成）
        """
        return self.llm_generator.generate_16week_plan(
            user_data=self.user_data,
            whoop_data=self.whoop_data
        )
    
    def generate_daily_plan(self, recovery_override: Optional[int] = None) -> str:
        """
        生成今日训练计划
        
        Args:
            recovery_override: 可选的恢复评分覆盖值
        
        Returns:
            每日训练计划（由LLM生成）
        """
        user_data = self.user_data.copy()
        if recovery_override:
            # 临时修改恢复数据
            pass
        
        return self.llm_generator.generate_daily_plan(
            user_data=user_data,
            whoop_data=self.whoop_data
        )
    
    def generate_recovery_plan(self) -> str:
        """
        生成恢复计划
        
        Returns:
            恢复计划（由LLM生成）
        """
        return self.llm_generator.generate_recovery_plan(
            user_data=self.user_data,
            whoop_data=self.whoop_data
        )
    
    def generate_race_plan(
        self,
        race_type: str,  # marathon / 10km / 5km
        target_date: str,
        current_fitness: str
    ) -> str:
        """
        生成跑步比赛训练计划
        
        Args:
            race_type: 比赛类型
            target_date: 目标日期 (YYYY-MM-DD)
            current_fitness: 当前体能水平描述
        
        Returns:
            比赛训练计划（由LLM生成）
        """
        return self.llm_generator.generate_race_plan(
            user_data=self.user_data,
            race_type=race_type,
            target_date=target_date,
            current_fitness=current_fitness
        )
    
    def analyze_and_recommend(self) -> str:
        """
        分析数据并给出建议
        
        Returns:
            分析报告和建议（由LLM生成）
        """
        return self.llm_generator.analyze_and_recommend(
            user_data=self.user_data,
            whoop_data=self.whoop_data
        )
    
    def get_user_data(self) -> Dict:
        """获取用户数据"""
        return self.user_data.copy()
    
    def update_user_data(self, key: str, value: any) -> bool:
        """更新用户数据"""
        self.user_data[key] = value
        user_file = os.path.join(USER_DATA_DIR, f"{self.user_id}.json")
        os.makedirs(USER_DATA_DIR, exist_ok=True)
        try:
            with open(user_file, 'w') as f:
                json.dump(self.user_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False


class RacePlanGenerator:
    """
    跑步比赛计划生成器
    
    专门用于生成马拉松、10公里、5公里等跑步比赛训练计划
    """
    
    RACE_TYPES = {
        "marathon": {
            "name": "马拉松",
            "distance": "42.195km",
            "min_weeks": 16,
            "max_weeks": 24
        },
        "half_marathon": {
            "name": "半程马拉松",
            "distance": "21.0975km",
            "min_weeks": 12,
            "max_weeks": 20
        },
        "10km": {
            "name": "10公里",
            "distance": "10km",
            "min_weeks": 8,
            "max_weeks": 16
        },
        "5km": {
            "name": "5公里",
            "distance": "5km",
            "min_weeks": 6,
            "max_weeks": 12
        }
    }
    
    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        self.llm_generator = LLMClient(user_id)
        self.user_data = self._load_user_data()
    
    def _load_user_data(self) -> Dict:
        """加载用户数据"""
        user_file = os.path.join(USER_DATA_DIR, f"{self.user_id}.json")
        try:
            if os.path.exists(user_file):
                with open(user_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}
    
    def generate_plan(
        self,
        race_type: str,
        target_date: str,
        current_fitness: str
    ) -> str:
        """
        生成跑步训练计划
        
        Args:
            race_type: 比赛类型 (marathon/half_marathon/10km/5km)
            target_date: 目标日期 (YYYY-MM-DD)
            current_fitness: 当前体能水平描述
        
        Returns:
            训练计划文本
        """
        race_info = self.RACE_TYPES.get(race_type, self.RACE_TYPES["10km"])
        
        # 构建用户数据
        user_data = {
            **self.user_data,
            "goal": f"完成{race_info['name']}",
            "race_type": race_type,
            "target_date": target_date,
            "current_fitness": current_fitness,
            "race_distance": race_info["distance"]
        }
        
        return self.llm_generator.generate_race_plan(
            user_data=user_data,
            race_type=race_type,
            target_date=target_date,
            current_fitness=current_fitness
        )
    
    def estimate_duration(self, target_date: str) -> int:
        """估算训练周期周数"""
        try:
            target = datetime.strptime(target_date, "%Y-%m-%d")
            now = datetime.now()
            weeks = (target - now).days // 7
            return max(1, weeks)
        except Exception:
            return 12


# 便捷函数
def get_plan_generator(user_id: str = "default") -> TrainingPlanGenerator:
    """获取训练计划生成器"""
    return TrainingPlanGenerator(user_id)


def generate_16week(user_id: str = "default") -> str:
    """生成16周训练计划"""
    generator = TrainingPlanGenerator(user_id)
    return generator.generate_16week_plan()


def generate_daily(user_id: str = "default") -> str:
    """生成每日训练计划"""
    generator = TrainingPlanGenerator(user_id)
    return generator.generate_daily_plan()


def generate_recovery(user_id: str = "default") -> str:
    """生成恢复计划"""
    generator = TrainingPlanGenerator(user_id)
    return generator.generate_recovery_plan()


def generate_race_plan(
    user_id: str,
    race_type: str,
    target_date: str,
    current_fitness: str
) -> str:
    """生成跑步比赛计划"""
    generator = RacePlanGenerator(user_id)
    return generator.generate_plan(race_type, target_date, current_fitness)


if __name__ == "__main__":
    print("=== Training Plan Generator (LLM) ===")
    
    # 检查API配置
    client = get_llm_client("test")
    info = client.get_provider_info()
    print(f"LLM Provider: {info}")
    
    if info.get("has_key"):
        print("\n=== Testing 16 Week Plan Generation ===")
        generator = TrainingPlanGenerator("test")
        
        # 测试生成
        result = generator.generate_16week_plan()
        print(result[:500] if len(result) > 500 else result)
    else:
        print("\n请先配置LLM API Key")
        print("使用方法:")
        print("  client = get_llm_client('user_id')")
        print("  client.set_user_api('your-api-key')")
