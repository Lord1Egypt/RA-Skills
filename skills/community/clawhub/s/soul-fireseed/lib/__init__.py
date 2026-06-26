#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
lib 包 — 火种·灵魂 v2.0 核心逻辑库

本包包含化石提取引擎、人格蒸馏器、隐空间映射器、置信度校验器等核心模块。
火种 v2.0 是完全独立的升级版，不再依赖其他技能。

核心能力：
- 六大维度化石提取（生物物理、自传记忆、认知架构、情感动力学、社会网络、元认知）
- 人格模型蒸馏与演化追踪
- 语义相似度计算与检索
- 贝叶斯置信度校准

使用方式:
    from lib import FossilExtractor, FossilDistiller
    
    extractor = FossilExtractor()
    fossils = extractor.extract("用户对话内容")
    
    distiller = FossilDistiller()
    persona = distiller.distill(fossils)

版本: 2.0.0
"""

# ============================================================
# 版本与元数据
# ============================================================

__version__ = "2.0.0"
__author__ = "FireSeed Team - Soul Module v2"
__description__ = "火种·灵魂 v2.0 - 人格建模与记忆沉淀引擎（完全独立版）"
__all__ = [
    # 主入口类
    "FossilExtractor",
    "FossilDistiller",
    "FossilEmbedder",
    "ConfidenceValidator",
    
    # 六大维度提取器
    "BioPhysicalExtractor",
    "AutobiographicalExtractor",
    "CognitiveExtractor",
    "AffectiveExtractor",
    "SocialNetworkExtractor",
    "MetaCognitiveExtractor",
    
    # 数据结构
    "Fossil",
    "PersonaModel",
    "EvolutionRecord",
    
    # 配置
    "ExtractorConfig",
    
    # 便捷函数
    "create_extractor",
    "create_distiller",
    "get_default_config",
]

# ============================================================
# 导入核心类 — 简化用户调用路径
# ============================================================

# 主入口类
from .extractor import FossilExtractor
from .distiller import FossilDistiller
from .embedder import FossilEmbedder
from .validator import ConfidenceValidator

# 六大维度提取器
from .extractor import (
    BioPhysicalExtractor,
    AutobiographicalExtractor,
    CognitiveExtractor,
    AffectiveExtractor,
    SocialNetworkExtractor,
    MetaCognitiveExtractor,
)

# 数据结构
from .extractor import Fossil
from .models.persona_model import PersonaModel, EvolutionRecord

# 配置
from .extractor import ExtractorConfig

# ============================================================
# 便捷函数
# ============================================================

def create_extractor(config_path: str = None, parallel: bool = False, 
                    workers: int = 4) -> FossilExtractor:
    """
    创建并返回一个配置好的 FossilExtractor 实例。
    
    这是最简启动方式，适合大多数使用场景。
    
    参数:
        config_path: 配置文件路径（可选），默认使用内置配置
        parallel: 是否启用并行提取（默认 False）
        workers: 并行工作线程数（默认 4）
        
    返回:
        配置好的 FossilExtractor 实例
        
    使用示例:
        >>> from lib import create_extractor
        >>> extractor = create_extractor("config/defaults.json", parallel=True)
        >>> fossils = extractor.extract("我最近很累")
    """
    return FossilExtractor(config_path=config_path, parallel=parallel, workers=workers)

def create_distiller(config_path: str = None) -> FossilDistiller:
    """
    创建并返回一个配置好的 FossilDistiller 实例。
    
    参数:
        config_path: 配置文件路径（可选）
        
    返回:
        配置好的 FossilDistiller 实例
        
    使用示例:
        >>> from lib import create_distiller
        >>> distiller = create_distiller()
        >>> persona = distiller.distill(fossils)
    """
    return FossilDistiller(config_path=config_path)

def get_default_config() -> dict:
    """
    获取默认配置的字典表示。
    
    用于查看当前默认配置项，或在创建提取器前调整配置。
    
    返回:
        包含默认配置的字典
        
    使用示例:
        >>> from lib import get_default_config
        >>> config = get_default_config()
        >>> print(config["extraction"]["max_fossils_per_dimension"])
        2
    """
    config = ExtractorConfig()
    return {
        "version": __version__,
        "extraction": {
            "max_fossils_per_dimension": config.max_fossils_per_dimension,
            "pending_confidence_threshold": config.pending_confidence_threshold,
            "high_confidence_threshold": config.high_confidence_threshold,
            "negation_decay_factor": config.negation_decay_factor,
            "min_confidence": config.min_confidence,
        },
        "dimensions": {
            str(dim): {
                "name": name,
                "weight": config.dimension_weights[dim],
            }
            for dim, name in {
                1: "生物物理基座",
                2: "自传体记忆",
                3: "认知架构",
                4: "情感动力学",
                5: "社会网络",
                6: "元认知自我",
            }.items()
        },
        "distillation": {
            "batch_size": 50,
            "frequency_hours": 24,
        },
        "embedding": {
            "model_name": "sentence-transformers/all-MiniLM-L6-v2",
        },
    }

# ============================================================
# 包级初始化（仅用于调试和日志）
# ============================================================

import logging

logger = logging.getLogger(__name__)

# 仅在显式开启调试日志时输出
logger.debug(
    f"FireSeed v2.0 lib v{__version__} 已加载。"
    f"可用导出项: {len(__all__)} 个"
)

# 检查依赖是否可用
try:
    import sentence_transformers
    logger.debug("✓ sentence-transformers 可用")
except ImportError:
    logger.warning("✗ sentence-transformers 未安装，嵌入功能将不可用")

try:
    import sklearn
    logger.debug("✓ scikit-learn 可用")
except ImportError:
    logger.warning("✗ scikit-learn 未安装，聚类功能将不可用")
