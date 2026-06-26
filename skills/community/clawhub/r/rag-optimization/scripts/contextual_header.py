#!/usr/bin/env python3
"""
上下文头增强分块器（Contextual Chunk Headers）

为文档块添加元数据头部，补充全局背景信息，提升向量语义准确性

使用方法：
    python contextual_header.py --input documents/ --output enhanced/

核心功能：
    1. 头部内容生成：文档来源、主题标签、关键实体
    2. 多种格式支持：自然语言、结构化JSON、标签形式
    3. 分层头部设计：文档级 + 块级
    4. 向量化策略：整体编码 / 分离编码
"""

import os
import re
import json
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class ChunkHeader:
    """上下文头结构"""
    # 文档级信息（同一文档的所有块共享）
    document_title: str = ""           # 文档标题
    document_type: str = ""            # 文档类型（手册、论文、新闻等）
    document_source: str = ""          # 文档来源
    publish_date: str = ""             # 发布日期
    
    # 块级信息（每个块特有）
    section_path: str = ""             # 章节路径
    topic_tags: List[str] = field(default_factory=list)  # 主题标签
    key_entities: List[str] = field(default_factory=list)  # 关键实体
    summary: str = ""                  # 简短摘要
    
    # 元数据
    chunk_index: int = 0               # 块序号
    total_chunks: int = 0              # 总块数
    created_at: str = ""               # 创建时间
    
    def to_natural_language(self, max_length: int = 100) -> str:
        """转换为自然语言格式"""
        parts = []
        
        # 来源信息
        if self.document_title:
            source_part = f"【来源：{self.document_title}"
            if self.section_path:
                source_part += f" - {self.section_path}"
            source_part += "】"
            parts.append(source_part)
        
        # 主题信息
        if self.topic_tags:
            topic_part = f"【主题：{', '.join(self.topic_tags[:3])}】"
            parts.append(topic_part)
        
        # 实体信息（可选）
        if self.key_entities and len(parts) < 3:
            entity_part = f"【涉及：{', '.join(self.key_entities[:2])}】"
            parts.append(entity_part)
        
        result = ''.join(parts)
        
        # 长度限制
        if len(result) > max_length:
            result = result[:max_length - 1] + "】"
        
        return result
    
    def to_json(self) -> str:
        """转换为JSON格式"""
        return json.dumps({
            'document_title': self.document_title,
            'section_path': self.section_path,
            'topic_tags': self.topic_tags,
            'key_entities': self.key_entities,
            'chunk_index': self.chunk_index
        }, ensure_ascii=False)
    
    def to_tags(self) -> str:
        """转换为标签格式"""
        tags = []
        
        if self.document_title:
            tags.append(f"doc:{self.document_title}")
        if self.section_path:
            tags.append(f"section:{self.section_path}")
        for tag in self.topic_tags[:3]:
            tags.append(f"topic:{tag}")
        for entity in self.key_entities[:2]:
            tags.append(f"entity:{entity}")
        
        return ' '.join([f"[{t}]" for t in tags])


class HeaderGenerator:
    """上下文头生成器"""
    
    def __init__(self, llm_client=None, config: Dict = None):
        """
        初始化生成器
        
        Args:
            llm_client: LLM客户端
            config: 配置参数
        """
        self.llm = llm_client
        self.config = config or {}
        
        # 格式配置
        self.format = self.config.get('header_format', 'natural')  # natural / json / tags
        self.max_length = self.config.get('max_header_length', 100)
        self.enable_llm_extraction = self.config.get('enable_llm_extraction', True)
    
    def generate(self, chunk: str, document_metadata: Dict = None) -> ChunkHeader:
        """
        为文档块生成上下文头
        
        Args:
            chunk: 文档块文本
            document_metadata: 文档元数据
        
        Returns:
            ChunkHeader: 上下文头
        """
        metadata = document_metadata or {}
        
        # 创建基础头部
        header = ChunkHeader(
            document_title=metadata.get('title', ''),
            document_type=metadata.get('type', ''),
            document_source=metadata.get('source', ''),
            publish_date=metadata.get('publish_date', ''),
            section_path=metadata.get('section_path', ''),
            created_at=datetime.now().isoformat()
        )
        
        # LLM提取语义信息
        if self.enable_llm_extraction and self.llm:
            semantic_info = self._extract_semantic_info(chunk)
            header.topic_tags = semantic_info.get('topic_tags', [])
            header.key_entities = semantic_info.get('key_entities', [])
            header.summary = semantic_info.get('summary', '')
        else:
            # 规则提取
            header.topic_tags = self._rule_extract_topics(chunk)
            header.key_entities = self._rule_extract_entities(chunk)
        
        return header
    
    def _extract_semantic_info(self, text: str) -> Dict:
        """使用LLM提取语义信息"""
        if not self.llm:
            return {}
        
        try:
            prompt = f"""
分析以下文本片段，提取关键信息：

文本：{text[:500]}

请提取：
1. 主题标签（2-3个关键词，描述这段话讲什么）
2. 关键实体（人名/产品名/概念/术语等，最多5个）
3. 一句话摘要（10-20字）

输出JSON格式：
{{
    "topic_tags": ["标签1", "标签2"],
    "key_entities": ["实体1", "实体2"],
    "summary": "一句话摘要"
}}
"""
            
            response = self.llm.invoke(prompt) if hasattr(self.llm, 'invoke') else self.llm(prompt)
            response_text = response.strip() if isinstance(response, str) else str(response)
            
            # 尝试解析JSON
            # 提取JSON部分
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                return json.loads(json_match.group())
            
            return {}
            
        except Exception as e:
            logger.error(f"LLM提取失败: {e}")
            return {}
    
    def _rule_extract_topics(self, text: str) -> List[str]:
        """基于规则提取主题标签"""
        # 简单的关键词提取
        # 停用词
        stopwords = {'的', '了', '是', '在', '和', '与', '或', '等', '这', '那', '有', '为'}
        
        # 分词（简单按空格和标点）
        words = re.findall(r'[\w]+', text.lower())
        
        # 统计词频
        word_freq = {}
        for word in words:
            if word not in stopwords and len(word) > 1:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # 取高频词作为主题
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [w[0] for w in sorted_words[:3]]
    
    def _rule_extract_entities(self, text: str) -> List[str]:
        """基于规则提取实体"""
        entities = []
        
        # 匹配大写开头的英文词组（可能的专有名词）
        cap_words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        entities.extend(cap_words[:3])
        
        # 匹配中文专有名词（简化：匹配引号内的内容）
        quoted = re.findall(r'[""「]([^""「」]+)[""」]', text)
        entities.extend(quoted[:2])
        
        return list(set(entities))[:5]


class ContextualHeaderEnhancer:
    """上下文头增强器"""
    
    def __init__(self, llm_client=None, config: Dict = None):
        """
        初始化增强器
        
        Args:
            llm_client: LLM客户端
            config: 配置参数
        """
        self.config = config or {}
        self.generator = HeaderGenerator(llm_client, self.config)
        
        # 分块配置
        self.chunk_size = self.config.get('chunk_size', 500)
        self.overlap = self.config.get('overlap', 50)
        self.header_format = self.config.get('header_format', 'natural')
    
    def enhance(self, chunk: str, document_metadata: Dict = None) -> str:
        """
        为文档块添加上下文头
        
        Args:
            chunk: 文档块文本
            document_metadata: 文档元数据
        
        Returns:
            增强后的文本
        """
        # 生成头部
        header = self.generator.generate(chunk, document_metadata)
        
        # 格式化头部
        if self.header_format == 'json':
            header_text = header.to_json()
        elif self.header_format == 'tags':
            header_text = header.to_tags()
        else:  # natural
            header_text = header.to_natural_language(self.config.get('max_header_length', 100))
        
        # 拼接
        return f"{header_text}\n{chunk}"
    
    def enhance_document(self, document: str, metadata: Dict = None) -> List[Dict]:
        """
        处理整个文档
        
        Args:
            document: 完整文档
            metadata: 文档元数据
        
        Returns:
            增强后的块列表
        """
        # 切分文档
        chunks = self._split_document(document)
        
        enhanced_chunks = []
        for i, chunk in enumerate(chunks):
            # 生成头部
            header = self.generator.generate(chunk, metadata)
            header.chunk_index = i
            header.total_chunks = len(chunks)
            
            # 格式化
            header_text = header.to_natural_language(self.config.get('max_header_length', 100))
            enhanced_text = f"{header_text}\n{chunk}"
            
            enhanced_chunks.append({
                'id': f"chunk_{i}",
                'text': enhanced_text,
                'original_text': chunk,
                'header': {
                    'document_title': header.document_title,
                    'section_path': header.section_path,
                    'topic_tags': header.topic_tags,
                    'key_entities': header.key_entities
                }
            })
        
        return enhanced_chunks
    
    def _split_document(self, text: str) -> List[str]:
        """切分文档"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            
            # 尝试在句子边界结束
            if end < len(text):
                # 向后找最近的句子结束符
                while end < len(text) and text[end] not in '。！？.!?':
                    end += 1
                if end < len(text):
                    end += 1  # 包含结束符
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - self.overlap if end < len(text) else end
        
        return chunks


class HierarchicalHeaderBuilder:
    """分层头部构建器"""
    
    def __init__(self, config: Dict = None):
        """
        初始化分层头部构建器
        
        Args:
            config: 配置参数
        """
        self.config = config or {}
    
    def build_document_header(self, document: str, metadata: Dict = None) -> str:
        """
        构建文档级头部
        
        Args:
            document: 完整文档
            metadata: 文档元数据
        
        Returns:
            文档级头部文本
        """
        meta = metadata or {}
        
        parts = []
        
        if meta.get('title'):
            parts.append(f"【文档：{meta['title']}】")
        
        if meta.get('type'):
            parts.append(f"【类型：{meta['type']}】")
        
        if meta.get('author'):
            parts.append(f"【作者：{meta['author']}】")
        
        if meta.get('publish_date'):
            parts.append(f"【日期：{meta['publish_date']}】")
        
        return ''.join(parts)
    
    def build_section_header(self, section_title: str, section_path: str) -> str:
        """
        构建章节级头部
        
        Args:
            section_title: 章节标题
            section_path: 章节路径
        
        Returns:
            章节级头部文本
        """
        if section_path:
            return f"【章节：{section_path}】"
        elif section_title:
            return f"【章节：{section_title}】"
        return ""
    
    def build_chunk_header(self, chunk: str, topics: List[str] = None, 
                           entities: List[str] = None) -> str:
        """
        构建块级头部
        
        Args:
            chunk: 文档块
            topics: 主题标签
            entities: 关键实体
        
        Returns:
            块级头部文本
        """
        parts = []
        
        if topics:
            parts.append(f"【主题：{', '.join(topics[:3])}】")
        
        if entities:
            parts.append(f"【涉及：{', '.join(entities[:2])}】")
        
        return ''.join(parts)
    
    def build_full_header(self, document: str, chunk: str, 
                          document_metadata: Dict = None,
                          section_info: Dict = None,
                          chunk_info: Dict = None) -> str:
        """
        构建完整的分层头部
        
        Args:
            document: 完整文档
            chunk: 文档块
            document_metadata: 文档元数据
            section_info: 章节信息
            chunk_info: 块信息
        
        Returns:
            完整头部文本
        """
        headers = []
        
        # 文档级
        doc_header = self.build_document_header(document, document_metadata)
        if doc_header:
            headers.append(doc_header)
        
        # 章节级
        if section_info:
            section_header = self.build_section_header(
                section_info.get('title', ''),
                section_info.get('path', '')
            )
            if section_header:
                headers.append(section_header)
        
        # 块级
        if chunk_info:
            chunk_header = self.build_chunk_header(
                chunk,
                chunk_info.get('topics', []),
                chunk_info.get('entities', [])
            )
            if chunk_header:
                headers.append(chunk_header)
        
        return '\n'.join(headers)


# 使用示例
if __name__ == '__main__':
    # 示例配置
    config = {
        'header_format': 'natural',
        'max_header_length': 100,
        'enable_llm_extraction': False,  # 示例不使用LLM
        'chunk_size': 200
    }
    
    # 创建增强器
    enhancer = ContextualHeaderEnhancer(config=config)
    
    # 测试文档
    document = """
    产品使用手册
    
    第三章 充电参数
    
    本产品支持快充功能，充电时间为2小时。
    使用Type-C接口进行充电，支持PD协议。
    建议使用原装充电器以获得最佳充电效果。
    
    第四章 电池维护
    
    为延长电池寿命，建议避免在高温环境下充电。
    每月进行一次完整的充放电循环。
    """
    
    # 文档元数据
    metadata = {
        'title': '产品使用手册',
        'type': '手册',
        'source': '官方文档',
        'publish_date': '2024-01'
    }
    
    # 处理文档
    enhanced_chunks = enhancer.enhance_document(document, metadata)
    
    print("\n=== 上下文头增强结果 ===\n")
    
    for chunk in enhanced_chunks:
        print(f"--- 块 {chunk['id']} ---")
        print(f"头部: {chunk['header']}")
        print(f"增强后文本:\n{chunk['text']}")
        print()
    
    # 测试分层头部
    print("\n=== 分层头部构建 ===\n")
    
    builder = HierarchicalHeaderBuilder()
    
    full_header = builder.build_full_header(
        document=document,
        chunk="本产品支持快充功能，充电时间为2小时。",
        document_metadata=metadata,
        section_info={'title': '充电参数', 'path': '第三章 > 充电参数'},
        chunk_info={'topics': ['快充', '充电时间'], 'entities': ['Type-C', 'PD协议']}
    )
    
    print("完整分层头部：")
    print(full_header)
