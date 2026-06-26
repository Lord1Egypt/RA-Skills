# -*- coding: utf-8 -*-
"""
SkillPilot - 智能技能路由引擎
用户偏好模块

让用户定义自己的优化目标和约束条件
"""

import os
import json
import yaml
from typing import Dict, List, Optional
from pathlib import Path


class UserPreference:
    """用户偏好配置"""
    
    def __init__(self, config_file: str = None):
        self.config_file = config_file or os.path.expanduser(
            "~/.openclaw/workspace/skills/skill-pilot/config/preference.yaml"
        )
        
        # 默认配置
        self.optimization_goal = "balanced"  # speed | cost | quality | balanced
        self.budget_limit = "free"  # free | low | medium | high
        self.quality_threshold = 0.8  # 最低质量要求 (0-1)
        self.timeout_preference = 30  # 秒
        self.region_preference = "no-preference"  # cn | global | no-preference
        self.preferred_skills: List[str] = []  # 用户明确偏好的技能
        self.avoided_skills: List[str] = []  # 用户明确避免的技能
        
        # 高级选项
        self.allow_parallel = False  # 允许并行执行
        self.max_fallback_depth = 3  # 最大降级深度
        self.cache_enabled = True  # 启用缓存
        self.cache_ttl = 300  # 缓存 TTL (秒)
        
        # 加载用户配置
        self.load()
    
    def load(self) -> bool:
        """加载用户配置"""
        if not os.path.exists(self.config_file):
            return False
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            if config:
                self._apply_config(config)
            return True
        except Exception as e:
            print(f"加载用户偏好配置失败：{e}")
            return False
    
    def save(self):
        """保存用户配置"""
        config = self.to_dict()
        
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
            return True
        except Exception as e:
            print(f"保存用户偏好配置失败：{e}")
            return False
    
    def _apply_config(self, config: Dict):
        """应用配置"""
        # 基础配置
        if 'optimization_goal' in config:
            self.optimization_goal = config['optimization_goal']
        if 'budget_limit' in config:
            self.budget_limit = config['budget_limit']
        if 'quality_threshold' in config:
            self.quality_threshold = config['quality_threshold']
        if 'timeout_preference' in config:
            self.timeout_preference = config['timeout_preference']
        if 'region_preference' in config:
            self.region_preference = config['region_preference']
        
        # 技能偏好
        if 'preferred_skills' in config:
            self.preferred_skills = config['preferred_skills']
        if 'avoided_skills' in config:
            self.avoided_skills = config['avoided_skills']
        
        # 高级选项
        advanced = config.get('advanced', {})
        if 'allow_parallel' in advanced:
            self.allow_parallel = advanced['allow_parallel']
        if 'max_fallback_depth' in advanced:
            self.max_fallback_depth = advanced['max_fallback_depth']
        if 'cache_enabled' in advanced:
            self.cache_enabled = advanced['cache_enabled']
        if 'cache_ttl' in advanced:
            self.cache_ttl = advanced['cache_ttl']
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'optimization_goal': self.optimization_goal,
            'budget_limit': self.budget_limit,
            'quality_threshold': self.quality_threshold,
            'timeout_preference': self.timeout_preference,
            'region_preference': self.region_preference,
            'preferred_skills': self.preferred_skills,
            'avoided_skills': self.avoided_skills,
            'advanced': {
                'allow_parallel': self.allow_parallel,
                'max_fallback_depth': self.max_fallback_depth,
                'cache_enabled': self.cache_enabled,
                'cache_ttl': self.cache_ttl,
            }
        }
    
    def to_weights(self) -> Dict[str, float]:
        """
        将优化目标转换为路由权重
        
        返回：{speed: 0.33, cost: 0.33, quality: 0.34}
        """
        weights = {
            'speed': 0.33,
            'cost': 0.33,
            'quality': 0.34,
        }
        
        if self.optimization_goal == 'speed':
            weights = {'speed': 0.5, 'cost': 0.2, 'quality': 0.3}
        elif self.optimization_goal == 'cost':
            weights = {'speed': 0.2, 'cost': 0.5, 'quality': 0.3}
        elif self.optimization_goal == 'quality':
            weights = {'speed': 0.2, 'cost': 0.2, 'quality': 0.6}
        elif self.optimization_goal == 'balanced':
            weights = {'speed': 0.33, 'cost': 0.33, 'quality': 0.34}
        
        # 区域偏好调整
        if self.region_preference == 'cn':
            weights['localization'] = 0.2
        elif self.region_preference == 'global':
            weights['global'] = 0.2
        
        return weights
    
    def apply_to_request(self, request) -> Dict:
        """
        将偏好应用到请求
        
        返回：额外的请求参数
        """
        extras = {
            'budget': self.budget_limit,
            'timeout': self.timeout_preference,
            'require_quality': self.quality_threshold,
        }
        
        # 根据优化目标添加额外要求
        if self.optimization_goal == 'speed':
            extras['requirements'] = ['fast']
        elif self.optimization_goal == 'quality':
            extras['requirements'] = ['accurate']
        elif self.optimization_goal == 'cost':
            extras['requirements'] = ['free']
        
        return extras
    
    def should_use_skill(self, skill_name: str) -> bool:
        """检查是否应该使用某技能"""
        if skill_name in self.avoided_skills:
            return False
        return True
    
    def get_skill_bonus(self, skill_name: str) -> float:
        """获取技能偏好加分"""
        if skill_name in self.preferred_skills:
            return 20.0  # 偏好技能加分
        if skill_name in self.avoided_skills:
            return -100.0  # 避免技能直接排除
        return 0.0
    
    def get_timeout(self, category: str) -> int:
        """获取某类别的超时时间"""
        base_timeout = self.timeout_preference
        
        # 根据类别调整
        timeouts = {
            'search': 1.0,
            'fetch': 1.5,
            'summarize': 1.0,
            'analyze': 2.0,
        }
        
        multiplier = timeouts.get(category, 1.0)
        return int(base_timeout * multiplier)
    
    def create_template(self, template_name: str = None) -> Dict:
        """
        创建预设模板
        
        模板：speed | cost | quality | balanced | cn-optimized | global-optimized
        """
        templates = {
            'speed': {
                'name': '极速模式',
                'description': '优先选择响应最快的技能',
                'optimization_goal': 'speed',
                'budget_limit': 'free',
                'timeout_preference': 20,
                'allow_parallel': True,
            },
            'cost': {
                'name': '经济模式',
                'description': '优先选择免费/低成本技能',
                'optimization_goal': 'cost',
                'budget_limit': 'free',
                'timeout_preference': 30,
                'allow_parallel': False,
            },
            'quality': {
                'name': '质量优先',
                'description': '优先选择质量最高的技能，不计成本',
                'optimization_goal': 'quality',
                'budget_limit': 'high',
                'timeout_preference': 60,
                'allow_parallel': False,
            },
            'balanced': {
                'name': '平衡模式',
                'description': '速度、成本、质量平衡',
                'optimization_goal': 'balanced',
                'budget_limit': 'free',
                'timeout_preference': 30,
                'allow_parallel': False,
            },
            'cn-optimized': {
                'name': '国内优化',
                'description': '针对中国大陆网络环境优化',
                'optimization_goal': 'balanced',
                'budget_limit': 'free',
                'region_preference': 'cn',
                'timeout_preference': 45,
                'preferred_capabilities': ['chinese'],
            },
            'global-optimized': {
                'name': '全球优化',
                'description': '针对海外网络环境优化',
                'optimization_goal': 'balanced',
                'budget_limit': 'free',
                'region_preference': 'global',
                'timeout_preference': 30,
                'preferred_capabilities': ['global'],
            },
        }
        
        if template_name:
            return templates.get(template_name, templates['balanced'])
        
        return templates[self.optimization_goal]


# 预设配置
PRESET_CONFIGS = {
    'default': {
        'optimization_goal': 'balanced',
        'budget_limit': 'free',
        'quality_threshold': 0.7,
        'timeout_preference': 30,
    },
    'developer': {
        'optimization_goal': 'quality',
        'budget_limit': 'medium',
        'quality_threshold': 0.9,
        'timeout_preference': 60,
        'preferred_skills': ['exa-web-search-free', 'github'],
    },
    'casual': {
        'optimization_goal': 'speed',
        'budget_limit': 'free',
        'quality_threshold': 0.6,
        'timeout_preference': 15,
    },
}


def create_config(template: str = 'default', output_file: str = None) -> str:
    """
    创建配置文件
    
    返回：配置文件路径
    """
    config = PRESET_CONFIGS.get(template, PRESET_CONFIGS['default'])
    
    output_file = output_file or os.path.expanduser(
        "~/.openclaw/workspace/skills/skill-pilot/config/preference.yaml"
    )
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
    
    return output_file


if __name__ == '__main__':
    # 命令行测试
    import sys
    
    if len(sys.argv) > 1:
        action = sys.argv[1]
        
        if action == 'init':
            template = sys.argv[2] if len(sys.argv) > 2 else 'default'
            path = create_config(template)
            print(f"✓ 配置文件已创建：{path}")
        
        elif action == 'show':
            pref = UserPreference()
            print("当前用户偏好配置:")
            print(json.dumps(pref.to_dict(), indent=2, ensure_ascii=False))
        
        elif action == 'template':
            template_name = sys.argv[2] if len(sys.argv) > 2 else 'balanced'
            pref = UserPreference()
            template = pref.create_template(template_name)
            print(f"模板：{template_name}")
            print(json.dumps(template, indent=2, ensure_ascii=False))
    else:
        # 默认：显示当前配置
        pref = UserPreference()
        print("当前用户偏好配置:")
        print(json.dumps(pref.to_dict(), indent=2, ensure_ascii=False))
        print(f"\n优化目标：{pref.optimization_goal}")
        print(f"权重：{pref.to_weights()}")
