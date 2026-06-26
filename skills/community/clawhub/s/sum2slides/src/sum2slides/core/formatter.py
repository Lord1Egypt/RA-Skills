"""
格式转换器
"""

import re
from typing import List, Optional


class Formatter:
    """格式转换器 - 格式化内容和优化布局"""
    
    def __init__(self):
        self.max_bullet_points = 6  # 每张幻灯片最多6个要点
        self.max_line_length = 80   # 每行最多80个字符
    
    def format_content(self, content: str) -> str:
        """格式化内容"""
        
        # 清理文本
        cleaned = self._clean_text(content)
        
        # 标准化标点
        normalized = self._normalize_punctuation(cleaned)
        
        # 断行优化
        optimized = self._optimize_line_breaks(normalized)
        
        return optimized
    
    def optimize_layout(self, content_lines: List[str]) -> List[str]:
        """优化布局"""
        
        optimized = []
        
        for line in content_lines:
            # 分割长行
            if len(line) > self.max_line_length:
                split_lines = self._split_long_line(line)
                optimized.extend(split_lines)
            else:
                optimized.append(line)
        
        # 限制要点数量
        if len(optimized) > self.max_bullet_points:
            optimized = optimized[:self.max_bullet_points]
        
        return optimized
    
    def format_bullet_points(self, points: List[str]) -> List[str]:
        """格式化要点列表"""
        
        formatted = []
        
        for point in points:
            # 清理每个要点
            clean_point = self._clean_text(point)
            
            # 确保以项目符号或数字开头
            if not re.match(r'^(\d+[\.\)]|[-•*])\s+', clean_point):
                clean_point = f"• {clean_point}"
            
            # 优化长度
            if len(clean_point) > self.max_line_length:
                clean_point = self._split_long_line(clean_point)[0]
            
            formatted.append(clean_point)
        
        return formatted
    
    def create_title(self, text: str) -> str:
        """创建合适的标题"""
        
        # 提取可能作为标题的部分
        lines = text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if line:
                # 清理标题
                title = self._clean_text(line)
                
                # 移除常见的前缀
                title = re.sub(r'^[#\d\.\s\-*•]*', '', title)
                
                # 限制长度
                if len(title) > 50:
                    title = title[:47] + "..."
                
                if title:
                    return title
        
        return "演示文稿"
    
    def create_subtitle(self, text: str) -> Optional[str]:
        """创建合适的副标题"""
        
        # 尝试从文本中提取副标题
        lines = text.strip().split('\n')
        
        if len(lines) >= 2:
            for line in lines[1:]:  # 跳过第一行（可能是标题）
                line = line.strip()
                if line and len(line) <= 100:
                    # 清理副标题
                    subtitle = self._clean_text(line)
                    
                    # 移除常见的前缀
                    subtitle = re.sub(r'^[#\d\.\s\-*•]*', '', subtitle)
                    
                    if subtitle and subtitle != lines[0].strip():
                        # 限制长度
                        if len(subtitle) > 80:
                            subtitle = subtitle[:77] + "..."
                        
                        return subtitle
        
        return None
    
    def _clean_text(self, text: str) -> str:
        """清理文本"""
        
        if not text:
            return ""
        
        # 移除多余空白
        text = re.sub(r'\s+', ' ', text)
        
        # 移除首尾空白
        text = text.strip()
        
        return text
    
    def _normalize_punctuation(self, text: str) -> str:
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
    
    def _optimize_line_breaks(self, text: str) -> str:
        """优化断行"""
        
        # 分割句子
        sentences = re.split(r'([.!?])\s+', text)
        
        # 重组句子，每句一行
        optimized = []
        i = 0
        while i < len(sentences):
            sentence = sentences[i].strip()
            if i + 1 < len(sentences) and sentences[i+1] in '.!?':
                sentence += sentences[i+1]
                i += 1
            
            if sentence:
                optimized.append(sentence)
            i += 1
        
        return '\n'.join(optimized)
    
    def _split_long_line(self, line: str) -> List[str]:
        """分割长行"""
        
        if len(line) <= self.max_line_length:
            return [line]
        
        # 尝试在标点处分割
        split_points = [',', ';', ':', '，', '；', '：']
        
        for point in split_points:
            if point in line:
                parts = line.split(point, 1)
                if len(parts[0]) < self.max_line_length:
                    result = [parts[0] + point]
                    if parts[1].strip():
                        result.extend(self._split_long_line(parts[1].strip()))
                    return result
        
        # 尝试在空格处分割
        words = line.split()
        if len(words) > 1:
            # 找到最佳分割点
            best_split = 0
            for i in range(1, len(words)):
                current_length = len(' '.join(words[:i]))
                if current_length > self.max_line_length:
                    break
                best_split = i
            
            if best_split > 0:
                first_part = ' '.join(words[:best_split])
                rest = ' '.join(words[best_split:])
                result = [first_part]
                result.extend(self._split_long_line(rest))
                return result
        
        # 强制分割
        return [line[:self.max_line_length] + '...', line[self.max_line_length:]]