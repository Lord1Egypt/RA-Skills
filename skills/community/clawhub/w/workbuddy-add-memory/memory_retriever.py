#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强记忆检索器 v3.0
作者: zcg007
日期: 2026-03-15

基于TF-IDF和语义相似度的混合检索系统
"""

import os
import re
import json
import pickle
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Set
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import logging

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib

logger = logging.getLogger(__name__)


class MemoryRetriever:
    """增强记忆检索器"""
    
    def __init__(self, config=None, cache_dir=None):
        """
        初始化记忆检索器
        
        Args:
            config: 配置字典
            cache_dir: 缓存目录路径
        """
        if config is None:
            from config_loader import config_loader
            self.config = config_loader.get_retrieval_config()
        else:
            self.config = config
        
        # 设置缓存目录
        if cache_dir is None:
            self.cache_dir = Path.home() / ".workbuddy" / "cache" / "memory_retriever"
        else:
            self.cache_dir = Path(cache_dir)
        
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # TF-IDF向量化器
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words=None,  # 中文需要自定义停用词
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.9,
        )
        
        # 记忆库数据
        self.memory_data = []  # 原始记忆数据
        self.memory_texts = []  # 文本内容
        self.memory_vectors = None  # TF-IDF向量
        self.memory_metadata = []  # 元数据
        
        # 索引状态
        self.is_indexed = False
        self.index_version = "1.0"
        self.last_index_time = None
        
        # 缓存管理器
        self.cache = {}
        self.cache_size = self.config.get("cache_size", 1000)
        self.cache_ttl = self.config.get("cache_ttl", 3600)
        
        # 统计信息
        self.stats = {
            "total_memories": 0,
            "indexed_memories": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "last_retrieval_time": None,
        }
        
        # 关键词权重
        self.keyword_weights = self._load_keyword_weights()
        
        # 重要性标签
        self.importance_tags = {
            "critical": 3.0,
            "important": 2.0,
            "normal": 1.0,
            "low": 0.5,
        }
        
        # 时间衰减因子
        self.time_decay_days = 30  # 30天衰减到50%
    
    def load_memories(self, memory_sources: List[str] = None) -> int:
        """
        从多个源加载记忆
        
        Args:
            memory_sources: 记忆源路径列表
            
        Returns:
            加载的记忆数量
        """
        if memory_sources is None:
            from config_loader import config_loader
            memory_sources = config_loader.get_memory_sources()
        
        logger.info(f"开始加载记忆源: {len(memory_sources)}个")
        
        # 清空现有数据
        self.memory_data = []
        self.memory_texts = []
        self.memory_metadata = []
        self.is_indexed = False
        
        # 从每个源加载记忆
        total_loaded = 0
        for source_path in memory_sources:
            try:
                source_path = os.path.expanduser(source_path)
                if not os.path.exists(source_path):
                    logger.warning(f"记忆源不存在: {source_path}")
                    continue
                
                loaded_count = self._load_from_source(source_path)
                total_loaded += loaded_count
                logger.info(f"从 {source_path} 加载了 {loaded_count} 个记忆")
            except Exception as e:
                logger.error(f"加载记忆源失败 {source_path}: {e}")
        
        self.stats["total_memories"] = total_loaded
        logger.info(f"总共加载了 {total_loaded} 个记忆")
        
        return total_loaded
    
    def _load_from_source(self, source_path: str) -> int:
        """从单个源加载记忆"""
        loaded_count = 0
        source_path = Path(source_path)
        
        # 支持的扩展名
        supported_extensions = {'.md', '.txt', '.json', '.yaml', '.yml'}
        
        if source_path.is_file():
            # 单个文件
            if source_path.suffix in supported_extensions:
                memory = self._parse_memory_file(source_path)
                if memory:
                    self._add_memory(memory)
                    loaded_count += 1
        elif source_path.is_dir():
            # 目录，递归加载
            for file_path in source_path.rglob("*"):
                if file_path.suffix in supported_extensions:
                    memory = self._parse_memory_file(file_path)
                    if memory:
                        self._add_memory(memory)
                        loaded_count += 1
        
        return loaded_count
    
    def _parse_memory_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """解析记忆文件"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            # 提取元数据
            metadata = {
                "source": str(file_path),
                "filename": file_path.name,
                "file_size": file_path.stat().st_size,
                "modified_time": datetime.fromtimestamp(file_path.stat().st_mtime),
                "created_time": datetime.fromtimestamp(file_path.stat().st_ctime),
            }
            
            # 尝试提取标题和重要性
            title = self._extract_title(content, file_path.name)
            importance = self._extract_importance(content)
            category = self._extract_category(content, file_path.name)
            
            # 提取关键词
            keywords = self._extract_keywords(content)
            
            # 清理文本内容（用于检索）
            clean_content = self._clean_text_for_indexing(content)
            
            memory = {
                "id": hashlib.md5(str(file_path).encode()).hexdigest()[:16],
                "title": title,
                "content": content,
                "clean_content": clean_content,
                "metadata": metadata,
                "importance": importance,
                "category": category,
                "keywords": keywords,
                "length": len(content),
                "word_count": len(content.split()),
            }
            
            return memory
            
        except Exception as e:
            logger.warning(f"解析记忆文件失败 {file_path}: {e}")
            return None
    
    def _extract_title(self, content: str, filename: str) -> str:
        """提取标题"""
        # 尝试从内容中提取标题
        lines = content.strip().split('\n')
        for line in lines[:5]:  # 检查前5行
            line = line.strip()
            if line and len(line) < 100 and not line.startswith(('#', '//', '/*', '*/', '"""')):
                # 移除Markdown标题标记
                if line.startswith('# '):
                    return line[2:].strip()
                elif line.startswith('## '):
                    return line[3:].strip()
                elif line.startswith('### '):
                    return line[4:].strip()
                else:
                    return line
        
        # 使用文件名作为标题
        name_without_ext = filename.rsplit('.', 1)[0]
        return name_without_ext.replace('_', ' ').replace('-', ' ')
    
    def _extract_importance(self, content: str) -> str:
        """提取重要性标签"""
        content_lower = content.lower()
        
        importance_keywords = {
            "critical": ["关键", "重要", "必须", "核心", "基础", "原则", "绝对"],
            "important": ["重要", "需要", "建议", "应该", "推荐", "最佳实践"],
            "normal": ["一般", "普通", "常规", "标准"],
            "low": ["低", "次要", "可选", "额外"],
        }
        
        for importance_level, keywords in importance_keywords.items():
            for keyword in keywords:
                if keyword in content_lower:
                    return importance_level
        
        return "normal"
    
    def _extract_category(self, content: str, filename: str) -> str:
        """提取类别 - 优化版：解决excel分类过于宽泛的问题"""
        content_lower = content.lower()
        filename_lower = filename.lower()
        
        # 优化后的分类逻辑，考虑关键词权重和上下文
        categories = {
            "skill": ["技能", "skill", "安装", "开发", "创建", "workbuddy", "add-memory"],
            "memory": ["记忆", "经验", "总结", "学习", "记录", "knowledge", "experience"],
            "excel": ["excel", "表格", "xlsx", "spreadsheet", "worksheet"],
            "workflow": ["工作流", "流程", "自动化", "任务", "workflow", "automation"],
            "analysis": ["分析", "统计", "报告", "评估", "研究", "analysis"],
            "error": ["错误", "问题", "故障", "bug", "修复", "解决", "error", "fix"],
            "principle": ["原则", "规则", "方法", "策略", "规范", "principle"],
            "document": ["文档", "文档", "报告", "总结", "说明", "document", "report"],
        }
        
        # 首先检查特定类别（优先级高）
        # 1. 检查技能相关
        skill_keywords = ["技能", "skill", "安装", "开发", "创建", "workbuddy"]
        for keyword in skill_keywords:
            if keyword in content_lower or keyword in filename_lower:
                # 如果是技能相关文件，检查是否真的包含excel内容
                excel_keywords = ["excel", "表格", "报表", "预算表", "财务报表"]
                has_excel_content = any(kw in content_lower for kw in excel_keywords)
                
                # 如果文件名或内容明确是技能相关，优先分类为skill
                skill_indicators = ["workbuddy-add-memory", "skill.md", "skill-", "skills"]
                has_skill_indicator = any(ind in filename_lower for ind in skill_indicators)
                
                if has_skill_indicator or not has_excel_content:
                    return "skill"
        
        # 2. 检查记忆相关
        memory_keywords = ["记忆", "经验", "总结", "学习", "记录"]
        for keyword in memory_keywords:
            if keyword in content_lower or keyword in filename_lower:
                return "memory"
        
        # 3. 检查excel相关 - 更严格的判断
        # 避免将包含"报表"、"数据"等通用词的文件都分类为excel
        excel_keywords = ["excel", "xlsx", "spreadsheet", "worksheet"]
        for keyword in excel_keywords:
            if keyword in content_lower or keyword in filename_lower:
                return "excel"
        
        # 4. 通用关键词匹配（原始逻辑）
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in content_lower or keyword in filename_lower:
                    return category
        
        # 根据文件名判断
        if any(ext in filename_lower for ext in [".md", ".txt", ".rst"]):
            return "document"
        
        return "general"
    
    def _extract_keywords(self, content: str) -> List[str]:
        """提取关键词"""
        # 简单关键词提取：长度2-5的中文词汇
        chinese_words = re.findall(r'[\u4e00-\u9fff]{2,5}', content)
        
        # 英文单词（小写）
        english_words = re.findall(r'\b[a-z]{3,15}\b', content.lower())
        
        keywords = list(set(chinese_words + english_words))
        
        # 限制关键词数量
        return keywords[:20]
    
    def _clean_text_for_indexing(self, content: str) -> str:
        """清理文本用于索引"""
        # 移除代码块
        content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        content = re.sub(r'`.*?`', '', content)
        
        # 移除HTML标签
        content = re.sub(r'<.*?>', '', content)
        
        # 移除特殊标记
        content = re.sub(r'[#*\-_=+~`]', ' ', content)
        
        # 移除多余空白
        content = re.sub(r'\s+', ' ', content)
        
        return content.strip()
    
    def _add_memory(self, memory: Dict[str, Any]) -> None:
        """添加记忆到库中"""
        self.memory_data.append(memory)
        self.memory_texts.append(memory["clean_content"])
        self.memory_metadata.append({
            "id": memory["id"],
            "title": memory["title"],
            "importance": memory["importance"],
            "category": memory["category"],
            "keywords": memory["keywords"],
            "metadata": memory["metadata"],
        })
    
    def build_index(self) -> bool:
        """构建检索索引"""
        if not self.memory_texts:
            logger.warning("没有记忆数据可供索引")
            return False
        
        try:
            logger.info(f"开始构建索引，记忆数量: {len(self.memory_texts)}")
            
            # 训练TF-IDF向量化器
            self.memory_vectors = self.vectorizer.fit_transform(self.memory_texts)
            
            # 保存向量化器
            vectorizer_path = self.cache_dir / "tfidf_vectorizer.pkl"
            joblib.dump(self.vectorizer, vectorizer_path)
            
            # 保存索引数据
            index_data = {
                "memory_vectors": self.memory_vectors,
                "memory_metadata": self.memory_metadata,
                "version": self.index_version,
                "build_time": datetime.now().isoformat(),
            }
            
            index_path = self.cache_dir / "memory_index.pkl"
            joblib.dump(index_data, index_path)
            
            self.is_indexed = True
            self.last_index_time = datetime.now()
            self.stats["indexed_memories"] = len(self.memory_texts)
            
            logger.info(f"索引构建完成，保存到: {index_path}")
            return True
            
        except Exception as e:
            logger.error(f"构建索引失败: {e}")
            return False
    
    def search(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        """
        搜索相关记忆
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            
        Returns:
            相关记忆列表
        """
        if top_k is None:
            top_k = self.config.get("max_results", 15)
        
        self.stats["last_retrieval_time"] = datetime.now()
        
        # 检查缓存
        cache_key = hashlib.md5(query.encode()).hexdigest()[:16]
        if cache_key in self.cache:
            cache_entry = self.cache[cache_key]
            cache_time = cache_entry.get("timestamp")
            
            # 检查缓存是否过期
            if cache_time and datetime.now() - cache_time < timedelta(seconds=self.cache_ttl):
                self.stats["cache_hits"] += 1
                logger.debug(f"缓存命中: {cache_key}")
                return cache_entry["results"][:top_k]
        
        self.stats["cache_misses"] += 1
        
        # 确保索引已构建
        if not self.is_indexed or self.memory_vectors is None:
            if not self.load_memories():
                return []
            if not self.build_index():
                return []
        
        try:
            # 1. TF-IDF相似度计算
            query_vector = self.vectorizer.transform([query])
            tfidf_scores = cosine_similarity(query_vector, self.memory_vectors).flatten()
            
            # 2. 关键词匹配分数
            keyword_scores = self._calculate_keyword_scores(query)
            
            # 3. 时间衰减分数
            time_scores = self._calculate_time_scores()
            
            # 4. 重要性分数
            importance_scores = self._calculate_importance_scores()
            
            # 5. 组合分数
            weight_keyword = self.config.get("weight_keyword", 0.6)
            weight_semantic = self.config.get("weight_semantic", 0.4)
            
            combined_scores = (
                tfidf_scores * weight_semantic +
                keyword_scores * weight_keyword +
                time_scores * self.config.get("boost_recent", 0.2) +
                importance_scores * self.config.get("boost_importance", 0.3)
            )
            
            # 6. 排序和过滤
            min_relevance = self.config.get("min_relevance", 0.3)
            valid_indices = np.where(combined_scores >= min_relevance)[0]
            
            if len(valid_indices) == 0:
                logger.info(f"没有找到相关记忆 (最小相关性: {min_relevance})")
                return []
            
            # 按分数排序
            sorted_indices = valid_indices[np.argsort(-combined_scores[valid_indices])]
            
            # 7. 组装结果
            results = []
            for idx in sorted_indices[:top_k]:
                memory = self.memory_data[idx]
                metadata = self.memory_metadata[idx]
                
                result = {
                    "id": memory["id"],
                    "title": memory["title"],
                    "content": memory["content"][:500],  # 截断内容
                    "relevance_score": float(combined_scores[idx]),
                    "tfidf_score": float(tfidf_scores[idx]),
                    "keyword_score": float(keyword_scores[idx]),
                    "metadata": metadata,
                    "importance": memory["importance"],
                    "category": memory["category"],
                    "keywords": memory["keywords"],
                    "source": memory["metadata"]["source"],
                    "modified_time": memory["metadata"]["modified_time"].isoformat(),
                }
                results.append(result)
            
            # 8. 缓存结果
            self.cache[cache_key] = {
                "results": results,
                "timestamp": datetime.now(),
                "query": query,
            }
            
            # 清理缓存
            self._clean_old_cache()
            
            logger.info(f"搜索完成: 查询='{query[:50]}...', 找到 {len(results)} 个结果")
            return results
            
        except Exception as e:
            logger.error(f"搜索失败: {e}")
            return []
    
    def _calculate_keyword_scores(self, query: str) -> np.ndarray:
        """计算关键词匹配分数"""
        scores = np.zeros(len(self.memory_data))
        
        # 提取查询中的关键词
        query_keywords = self._extract_keywords(query)
        
        for i, memory in enumerate(self.memory_data):
            memory_keywords = set(memory["keywords"])
            query_keyword_set = set(query_keywords)
            
            # 计算Jaccard相似度
            if memory_keywords and query_keyword_set:
                intersection = len(memory_keywords & query_keyword_set)
                union = len(memory_keywords | query_keyword_set)
                if union > 0:
                    scores[i] = intersection / union
        
        return scores
    
    def _calculate_time_scores(self) -> np.ndarray:
        """计算时间衰减分数"""
        scores = np.zeros(len(self.memory_data))
        now = datetime.now()
        
        for i, memory in enumerate(self.memory_data):
            modified_time = memory["metadata"]["modified_time"]
            days_diff = (now - modified_time).days
            
            # 指数衰减：30天衰减到50%
            if days_diff <= 0:
                scores[i] = 1.0
            else:
                decay_factor = 0.5 ** (days_diff / self.time_decay_days)
                scores[i] = max(0.1, decay_factor)  # 最小0.1
        
        return scores
    
    def _calculate_importance_scores(self) -> np.ndarray:
        """计算重要性分数"""
        scores = np.zeros(len(self.memory_data))
        
        for i, memory in enumerate(self.memory_data):
            importance = memory["importance"]
            scores[i] = self.importance_tags.get(importance, 1.0)
        
        # 归一化到0-1范围
        if scores.max() > 0:
            scores = scores / scores.max()
        
        return scores
    
    def _load_keyword_weights(self) -> Dict[str, float]:
        """加载关键词权重"""
        # 这里可以加载预定义的关键词权重
        # 暂时返回空字典
        return {}
    
    def _clean_old_cache(self) -> None:
        """清理旧缓存"""
        if len(self.cache) > self.cache_size:
            # 按时间排序，删除最旧的缓存
            sorted_entries = sorted(
                self.cache.items(),
                key=lambda x: x[1].get("timestamp", datetime.min)
            )
            
            entries_to_remove = sorted_entries[:len(self.cache) - self.cache_size]
            for key, _ in entries_to_remove:
                del self.cache[key]
            
            logger.debug(f"清理了 {len(entries_to_remove)} 个缓存条目")
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        stats = self.stats.copy()
        stats.update({
            "cache_size": len(self.cache),
            "is_indexed": self.is_indexed,
            "memory_count": len(self.memory_data),
            "indexed_count": self.stats["indexed_memories"],
            "cache_hit_rate": (
                stats["cache_hits"] / (stats["cache_hits"] + stats["cache_misses"])
                if (stats["cache_hits"] + stats["cache_misses"]) > 0
                else 0
            ),
        })
        return stats
    
    def clear_cache(self) -> None:
        """清除所有缓存"""
        self.cache.clear()
        logger.info("缓存已清除")
    
    def save_state(self) -> bool:
        """保存状态到文件"""
        try:
            state_path = self.cache_dir / "retriever_state.pkl"
            state = {
                "cache": self.cache,
                "stats": self.stats,
                "config": self.config,
                "last_index_time": self.last_index_time,
                "save_time": datetime.now(),
            }
            
            joblib.dump(state, state_path)
            logger.info(f"状态已保存到: {state_path}")
            return True
            
        except Exception as e:
            logger.error(f"保存状态失败: {e}")
            return False
    
    def load_state(self) -> bool:
        """从文件加载状态"""
        try:
            state_path = self.cache_dir / "retriever_state.pkl"
            if not state_path.exists():
                logger.info("状态文件不存在，使用默认状态")
                return False
            
            state = joblib.load(state_path)
            
            self.cache = state.get("cache", {})
            self.stats = state.get("stats", self.stats)
            self.config = state.get("config", self.config)
            self.last_index_time = state.get("last_index_time")
            
            logger.info(f"状态已从 {state_path} 加载")
            return True
            
        except Exception as e:
            logger.error(f"加载状态失败: {e}")
            return False


# 全局记忆检索器实例
memory_retriever = MemoryRetriever()


if __name__ == "__main__":
    # 测试记忆检索器
    import logging
    
    logging.basicConfig(level=logging.INFO)
    
    retriever = MemoryRetriever()
    
    # 加载测试记忆
    test_memories = [
        {
            "id": "test1",
            "title": "Excel处理关键经验",
            "content": "处理Excel文件时，必须保留公式，使用openpyxl的data_only=False参数。",
            "clean_content": "处理Excel文件时，必须保留公式，使用openpyxl的data_only=False参数。",
            "importance": "important",
            "category": "excel",
            "keywords": ["excel", "公式", "openpyxl", "处理"],
        },
        {
            "id": "test2",
            "title": "技能安装原则",
            "content": "所有skill都必须通过SkillHub下载，这是不可违反的核心技能管理原则。",
            "clean_content": "所有skill都必须通过SkillHub下载，这是不可违反的核心技能管理原则。",
            "importance": "critical",
            "category": "skill",
            "keywords": ["skill", "SkillHub", "安装", "原则"],
        },
    ]
    
    for memory in test_memories:
        retriever._add_memory(memory)
    
    # 构建索引
    retriever.build_index()
    
    # 测试搜索
    queries = [
        "如何安装Excel技能？",
        "Excel处理有什么经验？",
        "记忆管理原则",
    ]
    
    print("=== 记忆检索器测试 ===")
    for query in queries:
        results = retriever.search(query, top_k=3)
        print(f"\n查询: {query}")
        print(f"找到 {len(results)} 个结果:")
        
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result['title']} (相关性: {result['relevance_score']:.3f})")
            print(f"     类别: {result['category']}, 重要性: {result['importance']}")
    
    # 显示统计信息
    print("\n=== 统计信息 ===")
    stats = retriever.get_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")