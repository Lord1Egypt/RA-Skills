"""
用户档案管理
管理用户基本信息、目标、健身数据
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional, List
from dataclasses import dataclass, asdict


@dataclass
class UserProfile:
    """用户档案"""
    user_id: str
    name: str = ""
    
    # 健身数据
    experience_years: float = 0  # 训练年限
    max_squat: float = 0  # 深蹲PR kg
    max_bench: float = 0  # 卧推PR kg
    max_deadlift: float = 0  # 硬拉PR kg
    body_weight: float = 0  # 体重 kg
    body_fat: float = 0  # 体脂%
    
    # 训练偏好
    days_per_week: int = 4  # 每周训练天数
    available_time: int = 60  # 每次可用时间 分钟
    equipment: List[str] = None  # 可用设备
    
    # 目标
    goal: str = "增肌"  # 增肌/减脂/保持/体能
    target_weight: float = 0  # 目标体重
    target_date: str = ""  # 目标日期
    
    # 弱点
    weak_points: List[str] = None  # 弱项列表
    
    # 时间
    created_at: str = ""
    updated_at: str = ""
    
    def __post_init__(self):
        if self.equipment is None:
            self.equipment = ["哑铃", "杠铃"]
        if self.weak_points is None:
            self.weak_points = []
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'UserProfile':
        return cls(**data)


class UserProfileManager:
    """用户档案管理器"""
    
    def __init__(self, data_dir: str = "data/profiles"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def _get_file_path(self, user_id: str) -> str:
        return os.path.join(self.data_dir, f"{user_id}.json")
    
    def save_profile(self, profile: UserProfile) -> bool:
        """保存用户档案"""
        profile.updated_at = datetime.now().isoformat()
        filepath = self._get_file_path(profile.user_id)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(profile.to_dict(), f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存档案失败: {e}")
            return False
    
    def load_profile(self, user_id: str) -> Optional[UserProfile]:
        """加载用户档案"""
        filepath = self._get_file_path(user_id)
        if not os.path.exists(filepath):
            return None
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return UserProfile.from_dict(data)
        except Exception as e:
            print(f"加载档案失败: {e}")
            return None
    
    def get_or_create(self, user_id: str, name: str = "") -> UserProfile:
        """获取或创建档案"""
        profile = self.load_profile(user_id)
        if profile is None:
            profile = UserProfile(user_id=user_id, name=name)
            self.save_profile(profile)
        return profile
    
    def delete_profile(self, user_id: str) -> bool:
        """删除档案"""
        filepath = self._get_file_path(user_id)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
    
    def list_profiles(self) -> List[str]:
        """列出所有用户ID"""
        try:
            files = os.listdir(self.data_dir)
            return [f.replace('.json', '') for f in files if f.endswith('.json')]
        except Exception:
            return []


# 全局实例
_profile_manager = None

def get_profile_manager() -> UserProfileManager:
    global _profile_manager
    if _profile_manager is None:
        _profile_manager = UserProfileManager()
    return _profile_manager

def get_user_profile(user_id: str) -> Optional[UserProfile]:
    return get_profile_manager().load_profile(user_id)

def save_user_profile(profile: UserProfile) -> bool:
    return get_profile_manager().save_profile(profile)
