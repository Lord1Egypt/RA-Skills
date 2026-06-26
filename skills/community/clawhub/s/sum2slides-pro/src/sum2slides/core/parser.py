"""
文本解析器
"""

import re
from typing import List, Optional, Tuple
import markdown

from ..models.document import Document, Section, DocumentStructure


class TextParser:
    """文本解析器 - 将原始文本转换为结构化数据"""
    
    def __init__(self):
        self.section_patterns = [
            (r'^(#{1,3})\s+(.+)$', 'markdown'),  # Markdown标题
            (r'^(\d+\.\s*.+)$', 'numbered'),     # 数字编号
            (r'^([一二三四五六七八九十]+[、.]\s*.+)$', 'chinese'),  # 中文编号
            (r'^([A-Z][.)]\s*.+)$', 'letter'),   # 字母编号
            (r'^([•\-*]\s*.+)$', 'bullet'),      # 项目符号
        ]
        
        self.key_point_patterns = [
            r'关键[：:]',
            r'重点[：:]',
            r'要点[：:]',
            r'核心[：:]',
            r'主要[：:]',
        ]
    
    def parse(self, text: str, language: str = "zh") -> Document:
        """解析文本，返回文档对象"""
        
        # 清理文本
        cleaned_text = self._clean_text(text)
        
        # 检测格式
        format_type = self.detect_format(cleaned_text)
        
        # 创建文档对象
        document = Document(
            raw_text=cleaned_text,
            format=format_type,
            language=language
        )
        
        # 解析内容
        if format_type == "markdown":
            sections = self._parse_markdown(cleaned_text)
        else:
            sections = self._parse_plain_text(cleaned_text)
        
        # 创建文档结构
        structure = DocumentStructure(
            title=self._extract_title(cleaned_text, sections),
            sections=sections,
            total_sections=len(sections)
        )
        
        document.structure = structure
        return document
    
    def detect_format(self, text: str) -> str:
        """检测输入格式"""
        # 检查是否包含Markdown标记
        markdown_patterns = [
            r'^#\s+',  # 标题
            r'\*\*.+\*\*',  # 粗体
            r'\[.+\]\(.+\)',  # 链接
        ]
        
        for pattern in markdown_patterns:
            if re.search(pattern, text, re.MULTILINE):
                return "markdown"
        
        return "plain"
    
    def extract_sections(self, text: str) -> List[Section]:
        """提取文档章节"""
        lines = text.strip().split('\n')
        sections = []
        current_section = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检查是否为章节标题
            is_section, level = self._is_section_header(line)
            
            if is_section:
                # 保存前一个章节
                if current_section is not None and current_content:
                    section = Section(
                        title=current_section,
                        content='\n'.join(current_content),
                        level=1,
                        key_points=self._extract_key_points(current_content)
                    )
                    sections.append(section)
                
                # 开始新章节
                current_section = line
                current_content = []
            else:
                current_content.append(line)
        
        # 保存最后一个章节
        if current_section is not None and current_content:
            section = Section(
                title=current_section,
                content='\n'.join(current_content),
                level=1,
                key_points=self._extract_key_points(current_content)
            )
            sections.append(section)
        
        # 如果没有检测到章节，将整个文本作为一个章节
        if not sections and text.strip():
            sections.append(Section(
                title="内容",
                content=text.strip(),
                level=1,
                key_points=self._extract_key_points([text.strip()])
            ))
        
        return sections
    
    def identify_key_points(self, text: str) -> List[str]:
        """识别关键点"""
        key_points = []
        
        # 从文本中提取关键点
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检查是否为关键点
            if self._is_key_point(line):
                key_points.append(line)
            
            # 提取数字或项目符号列表
            elif re.match(r'^(\d+[\.\)]|[-•*])\s+', line):
                key_points.append(re.sub(r'^(\d+[\.\)]|[-•*])\s+', '', line))
        
        # 如果没有显式关键点，从整个文本中提取重要句子
        if not key_points:
            sentences = re.split(r'[。！？\.\!\?]+', text)
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) > 10:  # 过滤短句子
                    key_points.append(sentence)
        
        return key_points[:20]  # 限制关键点数量
    
    def _clean_text(self, text: str) -> str:
        """清理文本"""
        # 移除多余空白
        text = re.sub(r'\s+', ' ', text)
        # 移除首尾空白
        text = text.strip()
        return text
    
    def _parse_markdown(self, text: str) -> List[Section]:
        """解析Markdown文本"""
        # 将Markdown转换为HTML以更好地解析结构
        html = markdown.markdown(text)
        
        # 提取标题和内容
        # 这里简化处理，实际可以更复杂
        lines = text.split('\n')
        return self.extract_sections(text)
    
    def _parse_plain_text(self, text: str) -> List[Section]:
        """解析纯文本"""
        return self.extract_sections(text)
    
    def _extract_title(self, text: str, sections: List[Section]) -> Optional[str]:
        """提取文档标题"""
        if sections and sections[0].title:
            # 使用第一个章节标题作为文档标题
            first_title = sections[0].title
            
            # 清理标题（移除标记符号）
            clean_title = re.sub(r'^[#\d\.\s\-*•]*', '', first_title).strip()
            
            if clean_title and len(clean_title) > 2:
                return clean_title
        
        # 从文本第一行提取
        first_line = text.split('\n')[0].strip()
        if first_line and len(first_line) <= 100:  # 限制标题长度
            return first_line
        
        return "演示文稿"
    
    def _is_section_header(self, line: str) -> Tuple[bool, int]:
        """判断是否为章节标题"""
        # 检查Markdown标题
        match = re.match(r'^(#{1,3})\s+(.+)$', line)
        if match:
            level = len(match.group(1))
            return True, level
        
        # 检查其他格式的标题
        for pattern, _ in self.section_patterns:
            if re.match(pattern, line):
                return True, 1
        
        return False, 0
    
    def _extract_key_points(self, lines: List[str]) -> List[str]:
        """从内容中提取关键点"""
        key_points = []
        
        for line in lines:
            # 检查是否包含关键点标记
            for pattern in self.key_point_patterns:
                if re.search(pattern, line):
                    # 提取关键点内容
                    parts = re.split(pattern, line, maxsplit=1)
                    if len(parts) > 1:
                        content = parts[1].strip()
                        if content:
                            key_points.append(content)
            
            # 提取列表项
            if re.match(r'^(\d+[\.\)]|[-•*])\s+', line):
                content = re.sub(r'^(\d+[\.\)]|[-•*])\s+', '', line).strip()
                if content:
                    key_points.append(content)
        
        return key_points
    
    def _is_key_point(self, line: str) -> bool:
        """判断是否为关键点"""
        # 检查是否包含关键点标记
        for pattern in self.key_point_patterns:
            if re.search(pattern, line):
                return True
        
        return False