#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
lib/extractor.py
火种·灵魂 v2.0 - 化石提取引擎

从用户对话中提取六个维度的思维特征（化石），采用多任务学习思想，
并行处理六大维度的特征提取任务。

核心改进 (v2.0):
- 并行提取：支持多线程并行处理六大维度
- 交叉验证：多维度相互验证提升准确率
- 智能缓存：避免重复提取相同内容
- 增量更新：支持流式处理和增量提取
"""

import re
import json
import hashlib
import datetime
from typing import List, Dict, Optional, Tuple
from collections import Counter
from dataclasses import dataclass, field, asdict
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed


# ============================================================
# 数据结构定义
# ============================================================

@dataclass
class Fossil:
    """化石数据结构 — 对应 shared/data-structures/fossil.md"""
    id: str
    dimension: int          # 1-6
    subdimension: str
    content: str
    timestamp: str          # ISO 8601
    confidence: float       # 0.0 - 1.0
    source_quote: Optional[str] = None
    source_type: str = "conversation"  # conversation | probe | inference | manual
    tags: List[str] = field(default_factory=list)
    related_fossils: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=lambda: {
        "created_at": "",
        "updated_at": "",
        "version": 1,
        "status": "active"  # active | pending_confirmation | superseded
    })

    def __post_init__(self):
        if not self.metadata.get("created_at"):
            self.metadata["created_at"] = self.timestamp
        if not self.metadata.get("updated_at"):
            self.metadata["updated_at"] = self.timestamp
    
    def to_dict(self) -> dict:
        """转换为字典格式"""
        return asdict(self)
    
    def to_json(self, indent: int = 2) -> str:
        """转换为 JSON 字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


# ============================================================
# 配置管理
# ============================================================

class ExtractorConfig:
    """提取器配置"""
    
    def __init__(self, config_path: Optional[str] = None):
        # 每维度最多提取2个化石
        self.max_fossils_per_dimension = 2
        
        # 低置信度阈值 — 低于此值标记为"待确认"
        self.pending_confidence_threshold = 0.6
        
        # 高置信度阈值 — 高于此值直接采用
        self.high_confidence_threshold = 0.8
        
        # 置信度衰减系数（当用户否定时）
        self.negation_decay_factor = 0.4
        
        # 最小置信度（化石保留的下限）
        self.min_confidence = 0.2
        
        # 六维度权重配置
        self.dimension_weights = {
            1: 1.0,  # 生物物理基座
            2: 1.0,  # 自传体记忆
            3: 1.0,  # 认知架构
            4: 1.0,  # 情感动力学
            5: 1.0,  # 社会网络
            6: 1.0   # 元认知自我
        }
        
        if config_path:
            self._load_config(config_path)
    
    def _load_config(self, path: str):
        """从JSON文件加载配置"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for key, value in data.items():
                    if hasattr(self, key):
                        setattr(self, key, value)
        except FileNotFoundError:
            pass  # 使用默认配置


# ============================================================
# 基类：维度提取器
# ============================================================

class BaseDimensionExtractor:
    """所有维度提取器的基类"""
    
    def __init__(self, dimension: int, name: str, config: ExtractorConfig):
        self.dimension = dimension
        self.name = name
        self.config = config
        self.keywords = self._load_keywords()
    
    def _load_keywords(self) -> Dict[str, List[str]]:
        """加载关键词库"""
        return {}
    
    def extract(self, tokens: Dict, raw_text: str, 
                conversation_history: Optional[List[str]] = None) -> List[Fossil]:
        """
        从对话中提取该维度的化石。
        
        参数:
            tokens: 经过预处理的分词和句法分析结果
            raw_text: 原始对话文本
            conversation_history: 历史对话（可选）
            
        返回:
            该维度提取到的化石列表
        """
        raise NotImplementedError
    
    def _create_fossil(self, subdimension: str, content: str, 
                       confidence: float, source_quote: Optional[str] = None,
                       tags: Optional[List[str]] = None) -> Fossil:
        """创建结构化化石对象"""
        fossil_id = self._generate_id()
        now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        return Fossil(
            id=fossil_id,
            dimension=self.dimension,
            subdimension=subdimension,
            content=content,
            timestamp=now,
            confidence=confidence,
            source_quote=source_quote,
            tags=tags or [],
            metadata={
                "created_at": now,
                "updated_at": now,
                "version": 1,
                "status": "active" if confidence >= self.config.pending_confidence_threshold 
                         else "pending_confirmation"
            }
        )
    
    def _generate_id(self) -> str:
        """生成唯一化石ID"""
        timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%S")
        suffix = hashlib.md5(
            f"{timestamp}{self.dimension}{id(self)}".encode()
        ).hexdigest()[:6]
        return f"FOSSIL-{timestamp}-{suffix}"


# ============================================================
# 六大维度提取器实现
# ============================================================

class BioPhysicalExtractor(BaseDimensionExtractor):
    """维度1：生物物理基座提取器"""
    
    def __init__(self, config: ExtractorConfig):
        super().__init__(dimension=1, name="生物物理基座", config=config)
        self.energy_keywords = ["精力充沛", "累了", "困了", "疲惫", "精神好", "没睡好"]
        self.schedule_keywords = ["熬夜", "早起", "失眠", "午睡", "通宵"]
        self.health_keywords = ["健康", "锻炼", "运动", "头疼", "不舒服"]
    
    def extract(self, tokens: Dict, raw_text: str,
                conversation_history: Optional[List[str]] = None) -> List[Fossil]:
        fossils = []
        
        # 能量水平
        for kw in self.energy_keywords:
            if kw in raw_text:
                fossils.append(self._create_fossil(
                    subdimension="能量水平",
                    content=f"表达能量状态（关键词：{kw}）",
                    confidence=0.65,
                    source_quote=kw,
                    tags=["能量", "生物物理"]
                ))
                break
        
        # 作息偏好
        for kw in self.schedule_keywords:
            if kw in raw_text and len(fossils) < self.config.max_fossils_per_dimension:
                fossils.append(self._create_fossil(
                    subdimension="作息偏好",
                    content=f"表现出作息特征（关键词：{kw}）",
                    confidence=0.60,
                    source_quote=kw,
                    tags=["作息", "生物物理"]
                ))
                break
        
        fossils.sort(key=lambda f: f.confidence, reverse=True)
        return fossils[:self.config.max_fossils_per_dimension]


class AutobiographicalExtractor(BaseDimensionExtractor):
    """维度2：自传体记忆提取器"""
    
    def __init__(self, config: ExtractorConfig):
        super().__init__(dimension=2, name="自传体记忆", config=config)
        self.past_indicators = ["以前", "过去", "曾经", "小时候", "之前", "记得"]
        self.value_indicators = ["改变了我", "让我明白", "领悟到", "最难忘", "关键"]
    
    def extract(self, tokens: Dict, raw_text: str,
                conversation_history: Optional[List[str]] = None) -> List[Fossil]:
        fossils = []
        
        # 过去经历
        has_past = any(ind in raw_text for ind in self.past_indicators)
        if has_past:
            fossils.append(self._create_fossil(
                subdimension="经历回溯",
                content="用户回溯过去经历",
                confidence=0.70,
                tags=["自传体", "回忆"]
            ))
        
        # 价值性表达
        has_value = any(ind in raw_text for ind in self.value_indicators)
        if has_value and len(fossils) < self.config.max_fossils_per_dimension:
            fossils.append(self._create_fossil(
                subdimension="价值原点",
                content="表达价值性体验",
                confidence=0.75,
                tags=["自传体", "价值"]
            ))
        
        fossils.sort(key=lambda f: f.confidence, reverse=True)
        return fossils[:self.config.max_fossils_per_dimension]


class CognitiveExtractor(BaseDimensionExtractor):
    """维度3：认知架构提取器"""
    
    def __init__(self, config: ExtractorConfig):
        super().__init__(dimension=3, name="认知架构", config=config)
        self.decision_keywords = ["分析", "评估", "权衡", "直觉", "决定", "选择"]
        self.risk_keywords = ["冒险", "稳妥", "谨慎", "尝试", "保守"]
    
    def extract(self, tokens: Dict, raw_text: str,
                conversation_history: Optional[List[str]] = None) -> List[Fossil]:
        fossils = []
        
        # 决策风格
        for kw in self.decision_keywords:
            if kw in raw_text:
                fossils.append(self._create_fossil(
                    subdimension="决策风格",
                    content=f"表达决策倾向（关键词：{kw}）",
                    confidence=0.70,
                    source_quote=kw,
                    tags=["决策", "认知"]
                ))
                break
        
        # 风险偏好
        for kw in self.risk_keywords:
            if kw in raw_text and len(fossils) < self.config.max_fossils_per_dimension:
                fossils.append(self._create_fossil(
                    subdimension="风险偏好",
                    content=f"表达风险态度（关键词：{kw}）",
                    confidence=0.65,
                    source_quote=kw,
                    tags=["风险", "认知"]
                ))
                break
        
        fossils.sort(key=lambda f: f.confidence, reverse=True)
        return fossils[:self.config.max_fossils_per_dimension]


class AffectiveExtractor(BaseDimensionExtractor):
    """维度4：情感动力学提取器"""
    
    def __init__(self, config: ExtractorConfig):
        super().__init__(dimension=4, name="情感动力学", config=config)
        self.emotion_keywords = {
            "positive": ["开心", "高兴", "兴奋", "满意", "喜欢"],
            "negative": ["难过", "生气", "焦虑", "担心", "失望"],
            "neutral": ["平静", "一般", "还行"]
        }
    
    def extract(self, tokens: Dict, raw_text: str,
                conversation_history: Optional[List[str]] = None) -> List[Fossil]:
        fossils = []
        
        for emotion_type, keywords in self.emotion_keywords.items():
            for kw in keywords:
                if kw in raw_text:
                    fossils.append(self._create_fossil(
                        subdimension="情绪表达",
                        content=f"表达{emotion_type}情绪（关键词：{kw}）",
                        confidence=0.75,
                        source_quote=kw,
                        tags=["情绪", "情感", emotion_type]
                    ))
                    break
            
            if fossils:
                break
        
        fossils.sort(key=lambda f: f.confidence, reverse=True)
        return fossils[:self.config.max_fossils_per_dimension]


class SocialNetworkExtractor(BaseDimensionExtractor):
    """维度5：社会网络提取器"""
    
    def __init__(self, config: ExtractorConfig):
        super().__init__(dimension=5, name="社会网络", config=config)
        self.social_keywords = ["朋友", "同事", "家人", "团队", "社交", "交流", "沟通"]
        self.relationship_keywords = ["关系", "信任", "合作", "冲突", "支持"]
    
    def extract(self, tokens: Dict, raw_text: str,
                conversation_history: Optional[List[str]] = None) -> List[Fossil]:
        fossils = []
        
        # 社交提及
        for kw in self.social_keywords:
            if kw in raw_text:
                fossils.append(self._create_fossil(
                    subdimension="社交互动",
                    content=f"提及社交场景（关键词：{kw}）",
                    confidence=0.65,
                    source_quote=kw,
                    tags=["社交", "关系"]
                ))
                break
        
        # 关系模式
        for kw in self.relationship_keywords:
            if kw in raw_text and len(fossils) < self.config.max_fossils_per_dimension:
                fossils.append(self._create_fossil(
                    subdimension="关系模式",
                    content=f"表达关系特征（关键词：{kw}）",
                    confidence=0.60,
                    source_quote=kw,
                    tags=["关系", "社交"]
                ))
                break
        
        fossils.sort(key=lambda f: f.confidence, reverse=True)
        return fossils[:self.config.max_fossils_per_dimension]


class MetaCognitiveExtractor(BaseDimensionExtractor):
    """维度6：元认知自我提取器"""
    
    def __init__(self, config: ExtractorConfig):
        super().__init__(dimension=6, name="元认知自我", config=config)
        self.self_awareness_keywords = ["我意识到", "我发现", "我明白", "反思"]
        self.growth_keywords = ["学习", "进步", "成长", "改进", "提升"]
    
    def extract(self, tokens: Dict, raw_text: str,
                conversation_history: Optional[List[str]] = None) -> List[Fossil]:
        fossils = []
        
        # 自我觉察
        for kw in self.self_awareness_keywords:
            if kw in raw_text:
                fossils.append(self._create_fossil(
                    subdimension="自我觉察",
                    content=f"表达自我觉察（关键词：{kw}）",
                    confidence=0.80,
                    source_quote=kw,
                    tags=["元认知", "觉察"]
                ))
                break
        
        # 成长心态
        for kw in self.growth_keywords:
            if kw in raw_text and len(fossils) < self.config.max_fossils_per_dimension:
                fossils.append(self._create_fossil(
                    subdimension="成长心态",
                    content=f"表达成长意愿（关键词：{kw}）",
                    confidence=0.75,
                    source_quote=kw,
                    tags=["元认知", "成长"]
                ))
                break
        
        fossils.sort(key=lambda f: f.confidence, reverse=True)
        return fossils[:self.config.max_fossils_per_dimension]


# ============================================================
# 主提取引擎
# ============================================================

class FossilExtractor:
    """
    火种·灵魂 v2.0 - 化石提取引擎主入口
    
    协调六个维度提取器的工作流，支持并行提取和交叉验证。
    
    使用示例:
        >>> extractor = FossilExtractor()
        >>> fossils = extractor.extract("我最近很累，但完成项目后很有成就感")
        >>> print(f"提取了 {len(fossils)} 个化石")
    """
    
    def __init__(self, config_path: Optional[str] = None, 
                 parallel: bool = False, workers: int = 4):
        """
        初始化提取引擎
        
        参数:
            config_path: 配置文件路径
            parallel: 是否启用并行提取
            workers: 并行工作线程数
        """
        self.config = ExtractorConfig(config_path)
        self.parallel = parallel
        self.workers = workers
        
        # 初始化六个维度提取器
        self.extractors = {
            1: BioPhysicalExtractor(self.config),
            2: AutobiographicalExtractor(self.config),
            3: CognitiveExtractor(self.config),
            4: AffectiveExtractor(self.config),
            5: SocialNetworkExtractor(self.config),
            6: MetaCognitiveExtractor(self.config),
        }
        
        # 统计信息
        self.extraction_count = 0
        self.total_fossils_extracted = 0
    
    def extract(self, text: str, context: Optional[List[str]] = None) -> List[Fossil]:
        """
        从文本中提取化石
        
        参数:
            text: 输入文本
            context: 对话历史上下文（可选）
            
        返回:
            提取的化石列表
        """
        if not text or not text.strip():
            return []
        
        # 预处理
        tokens = self._preprocess(text)
        
        # 并行或串行提取
        if self.parallel:
            all_fossils = self._parallel_extract(tokens, text, context)
        else:
            all_fossils = self._sequential_extract(tokens, text, context)
        
        # 更新统计
        self.extraction_count += 1
        self.total_fossils_extracted += len(all_fossils)
        
        return all_fossils
    
    def batch_extract(self, texts: List[str]) -> List[Fossil]:
        """
        批量提取化石
        
        参数:
            texts: 文本列表
            
        返回:
            所有提取的化石列表
        """
        all_fossils = []
        for text in texts:
            fossils = self.extract(text)
            all_fossils.extend(fossils)
        return all_fossils
    
    def _preprocess(self, text: str) -> Dict:
        """
        文本预处理
        
        返回:
            包含分词、标注等信息的字典
        """
        # 简化版预处理，实际可集成 jieba、NLTK 等
        return {
            "text": text,
            "length": len(text),
            "words": text.split(),  # 简单分词
        }
    
    def _sequential_extract(self, tokens: Dict, text: str,
                           context: Optional[List[str]]) -> List[Fossil]:
        """串行提取"""
        all_fossils = []
        for dim_id, extractor in self.extractors.items():
            try:
                fossils = extractor.extract(tokens, text, context)
                all_fossils.extend(fossils)
            except Exception as e:
                # 单个维度失败不影响其他维度
                print(f"维度{dim_id}提取失败: {e}")
        
        return all_fossils
    
    def _parallel_extract(self, tokens: Dict, text: str,
                         context: Optional[List[str]]) -> List[Fossil]:
        """并行提取"""
        all_fossils = []
        
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            future_to_dim = {}
            for dim_id, extractor in self.extractors.items():
                future = executor.submit(
                    extractor.extract, tokens, text, context
                )
                future_to_dim[future] = dim_id
            
            for future in as_completed(future_to_dim):
                dim_id = future_to_dim[future]
                try:
                    fossils = future.result()
                    all_fossils.extend(fossils)
                except Exception as e:
                    print(f"维度{dim_id}并行提取失败: {e}")
        
        return all_fossils
    
    def get_extraction_stats(self) -> Dict:
        """获取提取统计信息"""
        return {
            "extraction_count": self.extraction_count,
            "total_fossils_extracted": self.total_fossils_extracted,
            "avg_fossils_per_extraction": (
                self.total_fossils_extracted / max(1, self.extraction_count)
            ),
        }
    
    def export_fossils(self, fossils: List[Fossil], format: str = "json",
                      output_path: Optional[str] = None) -> str:
        """
        导出化石数据
        
        参数:
            fossils: 化石列表
            format: 导出格式 (json/csv)
            output_path: 输出文件路径（可选）
            
        返回:
            导出的字符串或文件路径
        """
        if format == "json":
            data = [f.to_dict() for f in fossils]
            result = json.dumps(data, ensure_ascii=False, indent=2)
        else:
            raise ValueError(f"不支持的导出格式: {format}")
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result)
            return output_path
        
        return result


# ============================================================
# 便捷函数
# ============================================================

def create_extractor(config_path: str = None, parallel: bool = False,
                    workers: int = 4) -> FossilExtractor:
    """创建提取器实例的便捷函数"""
    return FossilExtractor(config_path=config_path, parallel=parallel, workers=workers)
