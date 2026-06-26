"""
文本处理工具
"""

import re
from typing import List


def clean_text(text: str) -> str:
    """清理文本"""
    
    if not text:
        return ""
    
    # 移除多余空白
    text = re.sub(r'\s+', ' ', text)
    
    # 移除首尾空白
    text = text.strip()
    
    return text


def normalize_punctuation(text: str) -> str:
    """标准化标点"""
    
    # 中文标点转英文标点（某些情况下）
    replacements = {
        '，': ', ',
        '。': '. ',
        '；': '; ',
        '：': ': ',
        '！': '! ',
        '？': '? ',
        '（': '(',
        '）': ')',
        '【': '[',
        '】': ']',
        '《': '<',
        '》': '>',
    }
    
    for chinese, english in replacements.items():
        text = text.replace(chinese, english)
    
    # 确保标点后有一个空格（英文标点）
    text = re.sub(r'([,.!?;:])(\w)', r'\1 \2', text)
    
    return text


def split_into_sentences(text: str) -> List[str]:
    """分割成句子"""
    
    # 使用标点分割句子
    sentences = re.split(r'([.!?。！？])\s*', text)
    
    # 重组句子
    result = []
    i = 0
    while i < len(sentences):
        sentence = sentences[i].strip()
        if i + 1 < len(sentences) and sentences[i+1] in '.!?。！？':
            sentence += sentences[i+1]
            i += 1
        
        if sentence:
            result.append(sentence)
        i += 1
    
    return result


def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """提取关键词"""
    
    # 简单实现：按空格分割，取出现频率高的词
    words = re.findall(r'\b\w+\b', text.lower())
    
    # 统计词频
    word_count = {}
    for word in words:
        if len(word) > 1:  # 忽略单字符词
            word_count[word] = word_count.get(word, 0) + 1
    
    # 按频率排序
    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    
    # 取前N个关键词
    keywords = [word for word, count in sorted_words[:max_keywords]]
    
    return keywords


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """截断文本"""
    
    if len(text) <= max_length:
        return text
    
    # 在单词边界处截断
    truncated = text[:max_length]
    last_space = truncated.rfind(' ')
    
    if last_space > max_length * 0.7:  # 如果截断位置在合理范围内
        truncated = truncated[:last_space]
    
    return truncated + suffix


def count_words(text: str) -> int:
    """统计单词数"""
    
    # 简单实现：按空白分割
    words = text.split()
    return len(words)


def count_characters(text: str) -> int:
    """统计字符数"""
    
    return len(text)


def is_chinese(text: str) -> bool:
    """判断是否为中文文本"""
    
    # 检查是否包含中文字符
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    chinese_ratio = len(chinese_chars) / max(len(text), 1)
    
    return chinese_ratio > 0.3  # 如果超过30%是中文字符，认为是中文文本