#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
lib/distiller.py
火种·灵魂 v2.0 - 人格蒸馏器

从大量化石中蒸馏出结构化的人格模型，追踪人格演化轨迹。
"""

import json
import datetime
from typing import List, Dict, Optional
from collections import defaultdict
from dataclasses import dataclass, field, asdict

try:
    from .extractor import Fossil
except ImportError:
    from extractor import Fossil


@dataclass
class EvolutionRecord:
    """演化记录"""
    timestamp: str
    version: str
    changes: List[Dict] = field(default_factory=list)
    summary: str = ""
    
    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class PersonaModel:
    """人格模型"""
    user_id: str
    version: str
    dimensions: Dict[str, Dict] = field(default_factory=dict)
    evolution_timeline: List[EvolutionRecord] = field(default_factory=list)
    last_updated: str = ""
    fossil_count: int = 0
    
    def __post_init__(self):
        if not self.last_updated:
            self.last_updated = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


class FossilDistiller:
    """
    人格蒸馏器
    
    从化石集合中提炼出稳定的人格特征，构建六维度人格模型。
    
    使用示例:
        >>> distiller = FossilDistiller()
        >>> persona = distiller.distill(fossils)
        >>> print(persona['dimensions'])
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.current_persona: Optional[PersonaModel] = None
        self.fossil_cache: List[Fossil] = []
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """加载配置"""
        default_config = {
            "batch_size": 50,
            "frequency_hours": 24,
            "min_fossils_for_distill": 20,
        }
        
        if config_path:
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except FileNotFoundError:
                pass
        
        return default_config
    
    def distill(self, fossils: List[Fossil], user_id: str = "USR-DEFAULT") -> PersonaModel:
        """
        从化石列表中蒸馏人格模型
        
        参数:
            fossils: 化石列表
            user_id: 用户ID
            
        返回:
            人格模型
        """
        if len(fossils) < self.config["min_fossils_for_distill"]:
            print(f"警告: 化石数量不足（{len(fossils)} < {self.config['min_fossils_for_distill']}）")
        
        # 按维度分组
        dimension_groups = defaultdict(list)
        for fossil in fossils:
            dimension_groups[fossil.dimension].append(fossil)
        
        # 构建六维度人格向量
        dimensions = {
            "bio_physical": self._distill_dimension(dimension_groups.get(1, [])),
            "autobiographical": self._distill_dimension(dimension_groups.get(2, [])),
            "cognitive": self._distill_dimension(dimension_groups.get(3, [])),
            "affective": self._distill_dimension(dimension_groups.get(4, [])),
            "social": self._distill_dimension(dimension_groups.get(5, [])),
            "meta_cognitive": self._distill_dimension(dimension_groups.get(6, [])),
        }
        
        # 创建人格模型
        now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        persona = PersonaModel(
            user_id=user_id,
            version="2.0",
            dimensions=dimensions,
            last_updated=now,
            fossil_count=len(fossils)
        )
        
        # 如果有旧模型，记录演化
        if self.current_persona:
            evolution = self._compute_evolution(self.current_persona, persona)
            persona.evolution_timeline.append(evolution)
        
        self.current_persona = persona
        self.fossil_cache = fossils
        
        return persona
    
    def _distill_dimension(self, fossils: List[Fossil]) -> Dict:
        """
        蒸馏单个维度
        
        参数:
            fossils: 该维度的化石列表
            
        返回:
            该维度的人格特征字典
        """
        if not fossils:
            return {"confidence": 0.0, "features": [], "summary": "数据不足"}
        
        # 按子维度分组
        subdim_groups = defaultdict(list)
        for fossil in fossils:
            subdim_groups[fossil.subdimension].append(fossil)
        
        # 提取主要特征
        features = []
        for subdim, sub_fossils in subdim_groups.items():
            # 计算平均置信度
            avg_confidence = sum(f.confidence for f in sub_fossils) / len(sub_fossils)
            
            # 提取最常见的标签
            all_tags = [tag for f in sub_fossils for tag in f.tags]
            tag_counts = defaultdict(int)
            for tag in all_tags:
                tag_counts[tag] += 1
            
            top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:3]
            
            features.append({
                "subdimension": subdim,
                "confidence": round(avg_confidence, 2),
                "fossil_count": len(sub_fossils),
                "top_tags": [tag for tag, _ in top_tags],
                "representative_content": sub_fossils[0].content
            })
        
        # 生成摘要
        summary = f"基于{len(fossils)}个化石，识别出{len(features)}个主要特征"
        
        return {
            "confidence": round(sum(f.confidence for f in fossils) / len(fossils), 2),
            "features": features,
            "summary": summary
        }
    
    def _compute_evolution(self, old_persona: PersonaModel, 
                          new_persona: PersonaModel) -> EvolutionRecord:
        """计算两个版本间的演化"""
        changes = []
        
        for dim_name in old_persona.dimensions:
            old_dim = old_persona.dimensions[dim_name]
            new_dim = new_persona.dimensions[dim_name]
            
            old_conf = old_dim.get("confidence", 0)
            new_conf = new_dim.get("confidence", 0)
            
            if abs(new_conf - old_conf) > 0.1:  # 显著变化
                changes.append({
                    "dimension": dim_name,
                    "old_confidence": old_conf,
                    "new_confidence": new_conf,
                    "change": round(new_conf - old_conf, 2)
                })
        
        now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        summary = f"检测到{len(changes)}个显著变化" if changes else "无明显变化"
        
        return EvolutionRecord(
            timestamp=now,
            version=new_persona.version,
            changes=changes,
            summary=summary
        )
    
    def get_current_persona(self) -> Optional[PersonaModel]:
        """获取当前人格模型"""
        return self.current_persona
    
    def get_evolution(self, days: int = 30) -> List[EvolutionRecord]:
        """
        获取演化轨迹
        
        参数:
            days: 回溯天数
            
        返回:
            演化记录列表
        """
        if not self.current_persona:
            return []
        
        cutoff_date = datetime.datetime.utcnow() - datetime.timedelta(days=days)
        cutoff_str = cutoff_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        return [
            record for record in self.current_persona.evolution_timeline
            if record.timestamp >= cutoff_str
        ]
    
    def generate_evolution_report(self, days: int = 30) -> str:
        """
        生成演化报告（Markdown格式）
        
        参数:
            days: 回溯天数
            
        返回:
            Markdown格式的报告
        """
        if not self.current_persona:
            return "# 人格演化报告\n\n暂无数据，请先进行蒸馏。"
        
        evolution = self.get_evolution(days)
        
        report = f"""# 人格演化报告

**生成时间**: {datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}  
**回溯周期**: {days}天  
**当前版本**: {self.current_persona.version}  
**化石总数**: {self.current_persona.fossil_count}

---

## 人格概览

"""
        
        for dim_name, dim_data in self.current_persona.dimensions.items():
            confidence = dim_data.get("confidence", 0)
            summary = dim_data.get("summary", "")
            report += f"### {dim_name}\n\n"
            report += f"- **置信度**: {confidence}\n"
            report += f"- **摘要**: {summary}\n\n"
        
        report += "---\n\n## 演化记录\n\n"
        
        if not evolution:
            report += "近期无显著演化。\n"
        else:
            for record in evolution:
                report += f"### {record.timestamp}\n\n"
                report += f"{record.summary}\n\n"
                
                if record.changes:
                    report += "| 维度 | 旧值 | 新值 | 变化 |\n"
                    report += "|------|------|------|------|\n"
                    for change in record.changes:
                        report += (
                            f"| {change['dimension']} "
                            f"| {change['old_confidence']} "
                            f"| {change['new_confidence']} "
                            f"| {change['change']:+.2f} |\n"
                        )
                    report += "\n"
        
        return report
    
    def update_persona(self, new_fossils: List[Fossil]) -> PersonaModel:
        """
        增量更新人格模型
        
        参数:
            new_fossils: 新增的化石列表
            
        返回:
            更新后的人格模型
        """
        if not self.current_persona:
            return self.distill(new_fossils)
        
        # 合并新旧化石
        all_fossils = self.fossil_cache + new_fossils
        return self.distill(all_fossils, self.current_persona.user_id)
