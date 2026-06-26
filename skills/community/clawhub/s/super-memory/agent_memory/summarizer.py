from __future__ import annotations
"""
summarizer.py - 自动摘要生成系统

功能：
1. 为长文档自动生成摘要
2. 支持不同长度的摘要生成
3. 支持不同类型文档的摘要
4. 提供基于LLM的摘要生成
5. 支持批处理多个文档

使用方式：
    from summarizer import Summarizer
    summarizer = Summarizer()
    
    # 生成摘要
    summary = summarizer.summarize("长文档内容")
    
    # 生成指定长度的摘要
    summary = summarizer.summarize("长文档内容", max_length=100)
"""

import os
import sys
import logging
import json
from typing import Dict, List, Optional, Union
from datetime import datetime

logger = logging.getLogger(__name__)


class Summarizer:
    """自动摘要生成器"""
    
    def __init__(self, model_name: str = "default"):
        """
        初始化摘要生成器
        
        Args:
            model_name: 模型名称
        """
        self.model_name = model_name
        self.llm_client = None
        self._initialize_llm()
    
    def _initialize_llm(self):
        """初始化LLM客户端"""
        try:
            # 尝试导入LLM客户端
            from llm_client import LLMClient
            self.llm_client = LLMClient()
            logger.info("LLM客户端初始化成功")
        except Exception as e:
            logger.warning("summarizer: %s", e)
            self.llm_client = None
    
    def summarize(self, text: str, max_length: int = 200, min_length: int = 50, 
                  summary_type: str = "general", language: str = "zh") -> str:
        """
        生成文本摘要
        
        Args:
            text: 要摘要的文本
            max_length: 摘要最大长度
            min_length: 摘要最小长度
            summary_type: 摘要类型 (general, technical, creative, etc.)
            language: 摘要语言
        
        Returns:
            str: 生成的摘要
        """
        try:
            # 检查文本长度
            if not text or len(text.strip()) < 100:
                return text.strip()
            
            # 使用LLM生成摘要
            if self.llm_client and self.llm_client.is_available():
                return self._generate_summary_with_llm(text, max_length, min_length, summary_type, language)
            else:
                # 使用简单的摘要算法
                return self._generate_summary_simple(text, max_length, min_length)
        except Exception as e:
            logger.error(f"生成摘要失败: {e}")
            return "摘要生成失败"
    
    def _generate_summary_with_llm(self, text: str, max_length: int, min_length: int, 
                                  summary_type: str, language: str) -> str:
        """
        使用LLM生成摘要
        
        Args:
            text: 要摘要的文本
            max_length: 摘要最大长度
            min_length: 摘要最小长度
            summary_type: 摘要类型
            language: 摘要语言
        
        Returns:
            str: 生成的摘要
        """
        try:
            # 构建提示词
            prompt = f"请为以下文本生成{summary_type}类型的摘要，长度在{min_length}到{max_length}字之间，使用{language}语言：\n\n{text}"
            
            # 调用LLM
            messages = [
                {"role": "system", "content": "你是一个专业的文本摘要生成器，能够准确理解文本内容并生成简洁明了的摘要。"},
                {"role": "user", "content": prompt}
            ]
            
            response = self.llm_client.chat(messages)
            
            # 处理响应
            if response and isinstance(response, str):
                # 确保摘要长度符合要求
                summary = response.strip()
                if len(summary) < min_length:
                    # 摘要太短，重新生成
                    prompt = f"请为以下文本生成更详细的{summary_type}类型摘要，长度至少{min_length}字，使用{language}语言：\n\n{text}"
                    messages = [
                        {"role": "system", "content": "你是一个专业的文本摘要生成器，能够准确理解文本内容并生成简洁明了的摘要。"},
                        {"role": "user", "content": prompt}
                    ]
                    response = self.llm_client.chat(messages)
                    summary = response.strip()
                elif len(summary) > max_length:
                    # 摘要太长，重新生成
                    prompt = f"请为以下文本生成更简洁的{summary_type}类型摘要，长度不超过{max_length}字，使用{language}语言：\n\n{text}"
                    messages = [
                        {"role": "system", "content": "你是一个专业的文本摘要生成器，能够准确理解文本内容并生成简洁明了的摘要。"},
                        {"role": "user", "content": prompt}
                    ]
                    response = self.llm_client.chat(messages)
                    summary = response.strip()
                return summary
            else:
                # LLM调用失败，使用简单算法
                return self._generate_summary_simple(text, max_length, min_length)
        except Exception as e:
            logger.error(f"使用LLM生成摘要失败: {e}")
            # 失败时使用简单算法
            return self._generate_summary_simple(text, max_length, min_length)
    
    def _generate_summary_simple(self, text: str, max_length: int, min_length: int) -> str:
        """
        使用简单算法生成摘要
        
        Args:
            text: 要摘要的文本
            max_length: 摘要最大长度
            min_length: 摘要最小长度
        
        Returns:
            str: 生成的摘要
        """
        try:
            # 分割句子
            sentences = self._split_sentences(text)
            if not sentences:
                return text[:max_length]
            
            # 计算句子得分（基于长度和位置）
            sentence_scores = {}
            for i, sentence in enumerate(sentences):
                # 位置得分：开头和结尾的句子得分更高
                position_score = 1.0
                if i == 0 or i == len(sentences) - 1:
                    position_score = 2.0
                elif i < len(sentences) * 0.2:
                    position_score = 1.5
                
                # 长度得分：中等长度的句子得分更高
                length = len(sentence)
                length_score = 1.0
                if 20 <= length <= 100:
                    length_score = 1.5
                elif length < 10:
                    length_score = 0.5
                
                # 总分
                sentence_scores[i] = position_score * length_score
            
            # 选择得分最高的句子
            sorted_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
            selected_indices = [idx for idx, _ in sorted_sentences[:5]]  # 最多选择5个句子
            selected_indices.sort()  # 保持原顺序
            
            # 构建摘要
            summary = "".join([sentences[idx] for idx in selected_indices])
            
            # 调整长度
            if len(summary) > max_length:
                summary = summary[:max_length]
                # 确保摘要以完整句子结束
                for i in range(len(summary) - 1, -1, -1):
                    if summary[i] in ["。", "！", "？", ".", "!", "?"]:
                        summary = summary[:i+1]
                        break
            elif len(summary) < min_length and len(sentences) > 5:
                # 摘要太短，添加更多句子
                additional_indices = [idx for idx in range(len(sentences)) if idx not in selected_indices][:3]
                additional_indices.sort()
                for idx in additional_indices:
                    if len(summary) + len(sentences[idx]) <= max_length:
                        summary += sentences[idx]
                    else:
                        break
            
            return summary.strip()
        except Exception as e:
            logger.error(f"使用简单算法生成摘要失败: {e}")
            return text[:max_length]
    
    def _split_sentences(self, text: str) -> List[str]:
        """
        分割句子
        
        Args:
            text: 文本
        
        Returns:
            List[str]: 句子列表
        """
        import re
        # 分割句子的正则表达式
        sentence_pattern = re.compile(r'[。！？.!?]+')
        sentences = sentence_pattern.split(text)
        # 过滤空句子
        sentences = [s.strip() for s in sentences if s.strip()]
        # 重新添加标点
        result = []
        for i, sentence in enumerate(sentences):
            if i < len(sentences) - 1:
                # 查找原始文本中的标点
                for punct in ["。", "！", "？", ".", "!", "?"]:
                    if punct in text[text.find(sentence) + len(sentence):]:
                        result.append(sentence + punct)
                        break
                else:
                    result.append(sentence + "。")
            else:
                result.append(sentence)
        return result
    
    def summarize_file(self, file_path: str, max_length: int = 200, min_length: int = 50, 
                      summary_type: str = "general", language: str = "zh") -> str:
        """
        为文件生成摘要
        
        Args:
            file_path: 文件路径
            max_length: 摘要最大长度
            min_length: 摘要最小长度
            summary_type: 摘要类型
            language: 摘要语言
        
        Returns:
            str: 生成的摘要
        """
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # 生成摘要
            return self.summarize(text, max_length, min_length, summary_type, language)
        except Exception as e:
            logger.error(f"为文件生成摘要失败: {e}")
            return "摘要生成失败"
    
    def summarize_batch(self, texts: List[str], max_length: int = 200, min_length: int = 50, 
                       summary_type: str = "general", language: str = "zh") -> List[str]:
        """
        批量生成摘要
        
        Args:
            texts: 文本列表
            max_length: 摘要最大长度
            min_length: 摘要最小长度
            summary_type: 摘要类型
            language: 摘要语言
        
        Returns:
            List[str]: 摘要列表
        """
        summaries = []
        for text in texts:
            summary = self.summarize(text, max_length, min_length, summary_type, language)
            summaries.append(summary)
        return summaries
    
    def get_summary_stats(self, text: str, summary: str) -> Dict:
        """
        获取摘要统计信息
        
        Args:
            text: 原始文本
            summary: 摘要文本
        
        Returns:
            Dict: 统计信息
        """
        try:
            original_length = len(text)
            summary_length = len(summary)
            compression_ratio = (1 - summary_length / original_length) * 100 if original_length > 0 else 0
            
            # 计算句子数量
            original_sentences = len(self._split_sentences(text))
            summary_sentences = len(self._split_sentences(summary))
            
            return {
                "original_length": original_length,
                "summary_length": summary_length,
                "compression_ratio": round(compression_ratio, 2),
                "original_sentences": original_sentences,
                "summary_sentences": summary_sentences,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"获取摘要统计信息失败: {e}")
            return {}
    
    def save_summary(self, text: str, summary: str, output_path: str) -> bool:
        """
        保存摘要到文件
        
        Args:
            text: 原始文本
            summary: 摘要文本
            output_path: 输出文件路径
        
        Returns:
            bool: 是否保存成功
        """
        try:
            # 获取统计信息
            stats = self.get_summary_stats(text, summary)
            
            # 构建输出内容
            output = {
                "original_text": text,
                "summary": summary,
                "stats": stats,
                "timestamp": datetime.now().isoformat()
            }
            
            # 保存到文件
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            logger.error(f"保存摘要失败: {e}")
            return False


# 全局摘要生成器实例
_summarizer = None

def get_summarizer() -> Summarizer:
    """
    获取全局摘要生成器实例
    
    Returns:
        Summarizer: 摘要生成器实例
    """
    global _summarizer
    if _summarizer is None:
        _summarizer = Summarizer()
    return _summarizer
