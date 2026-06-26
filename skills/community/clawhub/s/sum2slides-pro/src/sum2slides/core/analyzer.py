"""
内容分析器
"""

from typing import List, Dict, Any
import re

from ..models.document import Document, Section, DocumentStructure, SlideContent
from ..models.slide import Layout


class ContentAnalyzer:
    """内容分析器 - 分析文档结构和逻辑"""
    
    def __init__(self, max_slides: int = 10):
        self.max_slides = max_slides
    
    def analyze_structure(self, document: Document) -> DocumentStructure:
        """分析文档结构"""
        if document.structure:
            return document.structure
        
        # 如果没有结构信息，重新分析
        sections = self._extract_sections(document.raw_text)
        structure = DocumentStructure(
            title=self._extract_title(document.raw_text),
            sections=sections,
            total_sections=len(sections)
        )
        
        return structure
    
    def determine_slide_count(self, structure: DocumentStructure) -> int:
        """确定需要的幻灯片数量"""
        if not structure.sections:
            return 3  # 默认3张：标题、内容、总结
        
        total_points = sum(len(section.key_points) for section in structure.sections)
        
        # 计算基础幻灯片数量
        base_slides = 2  # 标题和总结页
        
        # 根据章节数量增加
        section_slides = min(len(structure.sections), self.max_slides - base_slides)
        
        # 根据关键点数量增加
        point_slides = min(total_points // 3, self.max_slides - base_slides - section_slides)
        
        total = base_slides + section_slides + point_slides
        
        # 确保在合理范围内
        return min(max(3, total), self.max_slides)
    
    def organize_content(self, structure: DocumentStructure) -> List[SlideContent]:
        """组织内容到幻灯片"""
        slide_contents = []
        
        # 1. 标题幻灯片
        title_slide = SlideContent(
            title=structure.title or "演示文稿",
            bullet_points=[],
            layout="title"
        )
        slide_contents.append(title_slide)
        
        # 2. 内容幻灯片
        content_slides = self._create_content_slides(structure.sections)
        slide_contents.extend(content_slides)
        
        # 3. 总结幻灯片
        summary_slide = self._create_summary_slide(structure.sections)
        slide_contents.append(summary_slide)
        
        return slide_contents
    
    def prioritize_content(self, content: List[str]) -> List[str]:
        """内容优先级排序"""
        if not content:
            return []
        
        # 简单优先级规则：
        # 1. 包含数字或项目符号的优先
        # 2. 包含关键字的优先
        # 3. 长度适中的优先
        
        prioritized = []
        
        for item in content:
            # 检查是否为重要内容
            importance = self._calculate_importance(item)
            prioritized.append((importance, item))
        
        # 按重要性排序
        prioritized.sort(key=lambda x: x[0], reverse=True)
        
        # 返回排序后的内容
        return [item for _, item in prioritized]
    
    def _extract_sections(self, text: str) -> List[Section]:
        """提取文档章节"""
        # 这里简化实现，实际可以使用更复杂的算法
        lines = text.strip().split('\n')
        sections = []
        current_section = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检查是否为章节标题
            if self._is_section_header(line):
                # 保存前一个章节
                if current_section is not None:
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
        if current_section is not None:
            section = Section(
                title=current_section,
                content='\n'.join(current_content),
                level=1,
                key_points=self._extract_key_points(current_content)
            )
            sections.append(section)
        
        return sections
    
    def _extract_title(self, text: str) -> str:
        """提取文档标题"""
        lines = text.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line and len(line) <= 100:
                # 清理标题
                clean_line = re.sub(r'^[#\d\.\s\-*•]*', '', line).strip()
                if clean_line:
                    return clean_line
        
        return "演示文稿"
    
    def _is_section_header(self, line: str) -> bool:
        """判断是否为章节标题"""
        # 检查常见标题格式
        patterns = [
            r'^#{1,3}\s+.+$',  # Markdown标题
            r'^\d+\.\s+.+$',   # 数字编号
            r'^[一二三四五六七八九十]+[、.]\s*.+$',  # 中文编号
            r'^[A-Z][.)]\s*.+$',  # 字母编号
            r'^[•\-*]\s*.+$',  # 项目符号
        ]
        
        for pattern in patterns:
            if re.match(pattern, line):
                return True
        
        # 检查是否包含冒号（常见于标题）
        if '：' in line or ':' in line:
            parts = line.split('：') if '：' in line else line.split(':')
            if len(parts[0].strip()) <= 30:  # 标题不会太长
                return True
        
        return False
    
    def _extract_key_points(self, lines: List[str]) -> List[str]:
        """从内容中提取关键点"""
        key_points = []
        key_patterns = [
            r'关键[：:]',
            r'重点[：:]', 
            r'要点[：:]',
            r'核心[：:]',
            r'主要[：:]',
        ]
        
        for line in lines:
            # 检查是否包含关键点标记
            for pattern in key_patterns:
                if re.search(pattern, line):
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
    
    def _create_content_slides(self, sections: List[Section]) -> List[SlideContent]:
        """创建内容幻灯片"""
        slides = []
        
        for i, section in enumerate(sections):
            # 章节标题幻灯片
            title_slide = SlideContent(
                title=section.title,
                bullet_points=[],
                layout="section_header"
            )
            slides.append(title_slide)
            
            # 关键点幻灯片
            if section.key_points:
                # 将关键点分组，每张幻灯片3-5个点
                for j in range(0, len(section.key_points), 4):
                    chunk = section.key_points[j:j+4]
                    content_slide = SlideContent(
                        title=f"{section.title} - 要点{j//4 + 1}",
                        bullet_points=chunk,
                        layout="title_and_content"
                    )
                    slides.append(content_slide)
        
        return slides
    
    def _create_summary_slide(self, sections: List[Section]) -> SlideContent:
        """创建总结幻灯片"""
        all_key_points = []
        for section in sections:
            all_key_points.extend(section.key_points)
        
        # 取最重要的几个点作为总结
        summary_points = all_key_points[:5] if all_key_points else ["感谢观看"]
        
        return SlideContent(
            title="总结",
            bullet_points=summary_points,
            layout="title_and_content"
        )
    
    def _calculate_importance(self, text: str) -> float:
        """计算内容重要性"""
        importance = 0.0
        
        # 包含数字或项目符号
        if re.match(r'^(\d+[\.\)]|[-•*])\s+', text):
            importance += 2.0
        
        # 包含重要关键词
        important_keywords = ['关键', '重点', '核心', '主要', '重要', '必须', '务必']
        for keyword in important_keywords:
            if keyword in text:
                importance += 1.0
        
        # 长度适中（20-100字符）
        length = len(text)
        if 20 <= length <= 100:
            importance += 0.5
        
        # 包含冒号或分号（表示定义或列表）
        if '：' in text or ':' in text:
            importance += 0.5
        
        return importance