# -*- coding: utf-8 -*-
"""
SkillPilot - 智能技能路由引擎
技能注册中心
"""

import os
import json
import re
import yaml
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path

from .models import SkillMetadata


class SkillRegistry:
    """技能注册中心"""
    
    def __init__(self, skills_dir: str = None):
        self.skills_dir = skills_dir or self._default_skills_dir()
        self.skills: Dict[str, SkillMetadata] = {}
        self.categories: Dict[str, List[str]] = {}  # category -> [skill_names]
        self.capability_index: Dict[str, List[str]] = {}  # capability -> [skill_names]
        
        # 自动发现并注册
        self.auto_discover()
    
    def _default_skills_dir(self) -> str:
        """默认技能目录"""
        workspace = os.path.expanduser("~/.openclaw/workspace")
        return os.path.join(workspace, "skills")
    
    def auto_discover(self) -> int:
        """
        自动扫描技能目录，注册所有技能
        返回：发现的技能数量
        """
        discovered = 0
        
        if not os.path.exists(self.skills_dir):
            print(f"技能目录不存在：{self.skills_dir}")
            return 0
        
        for skill_folder in os.listdir(self.skills_dir):
            skill_path = os.path.join(self.skills_dir, skill_folder)
            
            # 跳过非目录和特殊目录
            if not os.path.isdir(skill_path):
                continue
            if skill_folder.startswith(".") or skill_folder.startswith("_"):
                continue
            
            # 解析技能元数据
            skill_meta = self._parse_skill_meta(skill_path)
            if skill_meta:
                self.register(skill_meta)
                discovered += 1
                print(f"✓ 发现技能：{skill_meta.name}")
        
        print(f"共发现 {discovered} 个技能")
        return discovered
    
    def _parse_skill_meta(self, skill_path: str) -> Optional[SkillMetadata]:
        """解析技能元数据 (从 SKILL.md)"""
        skill_md_path = os.path.join(skill_path, "SKILL.md")
        
        if not os.path.exists(skill_md_path):
            print(f"  ⚠ 未找到 SKILL.md: {skill_path}")
            return None
        
        try:
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析 YAML front matter
            metadata = self._extract_yaml_frontmatter(content)
            if not metadata:
                return None
            
            # 提取技能信息
            openclaw_meta = metadata.get('metadata', {}).get('openclaw', {})
            
            return SkillMetadata(
                name=metadata.get('name', os.path.basename(skill_path)),
                category=openclaw_meta.get('category', self._infer_category(metadata.get('description', ''))),
                capabilities=openclaw_meta.get('capabilities', []),
                priority=openclaw_meta.get('priority', 5),
                timeout=openclaw_meta.get('timeout', 30.0),
                cost=openclaw_meta.get('cost', 0)
            )
            
        except Exception as e:
            print(f"  ✗ 解析失败 {skill_path}: {e}")
            return None
    
    def _extract_yaml_frontmatter(self, content: str) -> Optional[Dict]:
        """提取 YAML front matter"""
        if not content.startswith('---'):
            return None
        
        # 查找结束标记
        end_match = re.search(r'\n---\n', content[4:])
        if not end_match:
            return None
        
        yaml_content = content[4:end_match.start()+4]
        
        try:
            return yaml.safe_load(yaml_content)
        except Exception as e:
            print(f"  YAML 解析错误：{e}")
            return None
    
    def _infer_category(self, description: str) -> str:
        """从描述推断类别"""
        desc_lower = description.lower()
        
        if any(kw in desc_lower for kw in ['search', '搜索', '引擎']):
            return 'search'
        elif any(kw in desc_lower for kw in ['fetch', 'grab', '抓取', '爬取']):
            return 'fetch'
        elif any(kw in desc_lower for kw in ['summarize', 'summary', '总结', '摘要']):
            return 'summarize'
        elif any(kw in desc_lower for kw in ['analyze', 'analysis', '分析']):
            return 'analyze'
        else:
            return 'other'
    
    def register(self, meta: SkillMetadata):
        """注册技能"""
        self.skills[meta.name] = meta
        
        # 按类别索引
        if meta.category not in self.categories:
            self.categories[meta.category] = []
        if meta.name not in self.categories[meta.category]:
            self.categories[meta.category].append(meta.name)
        
        # 按能力标签索引
        for cap in meta.capabilities:
            if cap not in self.capability_index:
                self.capability_index[cap] = []
            if meta.name not in self.capability_index[cap]:
                self.capability_index[cap].append(meta.name)
    
    def unregister(self, skill_name: str):
        """注销技能"""
        if skill_name not in self.skills:
            return
        
        meta = self.skills[skill_name]
        
        # 从主字典移除
        del self.skills[skill_name]
        
        # 从类别索引移除
        if meta.category in self.categories:
            if skill_name in self.categories[meta.category]:
                self.categories[meta.category].remove(skill_name)
        
        # 从能力索引移除
        for cap in meta.capabilities:
            if cap in self.capability_index:
                if skill_name in self.capability_index[cap]:
                    self.capability_index[cap].remove(skill_name)
    
    def get_candidates(self, category: str, required_caps: List[str] = None) -> List[str]:
        """
        获取候选技能列表
        返回：按健康分数和优先级排序的技能名称列表
        """
        if category not in self.categories:
            return []
        
        candidates = self.categories[category].copy()
        
        # 过滤所需能力
        if required_caps:
            for cap in required_caps:
                if cap in self.capability_index:
                    candidates = [c for c in candidates if c in self.capability_index[cap]]
                else:
                    candidates = []  # 无此能力标签
                    break
        
        # 按健康分数和优先级排序
        candidates.sort(
            key=lambda name: (
                self.skills[name].health_score,
                self.skills[name].priority,
                -self.skills[name].avg_response_time
            ),
            reverse=True
        )
        
        return candidates
    
    def get_skill(self, skill_name: str) -> Optional[SkillMetadata]:
        """获取技能元数据"""
        return self.skills.get(skill_name)
    
    def list_skills(self, category: str = None) -> List[str]:
        """列出所有技能"""
        if category:
            return self.categories.get(category, [])
        return list(self.skills.keys())
    
    def get_status(self) -> Dict:
        """获取所有技能状态"""
        return {
            name: meta.to_dict()
            for name, meta in self.skills.items()
        }
    
    def save_state(self, state_file: str = None):
        """保存注册表状态"""
        if state_file is None:
            state_file = os.path.join(self.skills_dir, "skill-pilot-state.json")
        
        state = {
            "skills": {name: meta.to_dict() for name, meta in self.skills.items()},
            "updated_at": datetime.now().isoformat()
        }
        
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    
    def load_state(self, state_file: str = None):
        """加载注册表状态"""
        if state_file is None:
            state_file = os.path.join(self.skills_dir, "skill-pilot-state.json")
        
        if not os.path.exists(state_file):
            return
        
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
            
            for name, data in state.get('skills', {}).items():
                if name in self.skills:
                    # 更新动态指标
                    self.skills[name].health_score = data.get('health_score', 100)
                    self.skills[name].success_rate = data.get('success_rate', 1.0)
                    self.skills[name].avg_response_time = data.get('avg_response_time', 0)
                    self.skills[name].total_calls = data.get('total_calls', 0)
                    self.skills[name].failed_calls = data.get('failed_calls', 0)
        except Exception as e:
            print(f"加载状态失败：{e}")
