"""
幻灯片生成器
"""

from typing import List, Optional, Dict, Any
from datetime import datetime

from ..models.document import SlideContent
from ..models.slide import Slide, Presentation, Layout
from ..models.template import Template


class SlideGenerator:
    """幻灯片生成器 - 创建幻灯片对象"""
    
    def __init__(self, template: Optional[Template] = None):
        self.template = template
    
    def generate(self, slide_contents: List[SlideContent], 
                 template: Optional[Template] = None) -> Presentation:
        """生成幻灯片演示文稿"""
        
        if template is None:
            template = self.template
        
        # 创建演示文稿
        presentation = Presentation(
            title=slide_contents[0].title if slide_contents else "演示文稿",
            author="Sum2Slides",
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            template=template.name if template else "default",
            theme=template.theme.name if template else "light"
        )
        
        # 为每个幻灯片内容创建幻灯片
        for i, content in enumerate(slide_contents):
            slide = self._create_slide_from_content(content, i + 1)
            presentation.add_slide(slide)
        
        return presentation
    
    def create_title_slide(self, title: str, subtitle: Optional[str] = None) -> Slide:
        """创建标题幻灯片"""
        
        content = []
        if subtitle:
            content.append(subtitle)
        
        return Slide(
            title=title,
            content=content,
            layout=Layout.TITLE,
            slide_number=1
        )
    
    def create_content_slide(self, title: str, 
                            content: List[str]) -> Slide:
        """创建内容幻灯片"""
        
        return Slide(
            title=title,
            content=content,
            layout=Layout.TITLE_AND_CONTENT,
            slide_number=0  # 将在后续设置
        )
    
    def create_summary_slide(self, key_points: List[str]) -> Slide:
        """创建总结幻灯片"""
        
        return Slide(
            title="总结",
            content=key_points,
            layout=Layout.TITLE_AND_CONTENT,
            slide_number=0
        )
    
    def create_section_header_slide(self, section_title: str) -> Slide:
        """创建章节标题幻灯片"""
        
        return Slide(
            title=section_title,
            content=[],
            layout=Layout.SECTION_HEADER,
            slide_number=0
        )
    
    def _create_slide_from_content(self, content: SlideContent, 
                                  slide_number: int) -> Slide:
        """从幻灯片内容创建幻灯片对象"""
        
        # 确定布局
        layout = self._determine_layout(content.layout)
        
        # 创建幻灯片
        slide = Slide(
            title=content.title,
            content=content.bullet_points,
            layout=layout,
            slide_number=slide_number,
            notes=content.notes
        )
        
        return slide
    
    def _determine_layout(self, layout_str: str) -> Layout:
        """确定布局类型"""
        
        layout_map = {
            "title": Layout.TITLE,
            "title_and_content": Layout.TITLE_AND_CONTENT,
            "section_header": Layout.SECTION_HEADER,
            "two_content": Layout.TWO_CONTENT,
            "comparison": Layout.COMPARISON,
            "title_only": Layout.TITLE_ONLY,
            "blank": Layout.BLANK,
            "content_with_caption": Layout.CONTENT_WITH_CAPTION,
            "picture_with_caption": Layout.PICTURE_WITH_CAPTION,
        }
        
        return layout_map.get(layout_str, Layout.TITLE_AND_CONTENT)
    
    def apply_template(self, presentation: Presentation, 
                      template: Template) -> Presentation:
        """应用模板到演示文稿"""
        
        # 更新演示文稿的模板信息
        presentation.template = template.name
        presentation.theme = template.theme.name
        
        # 这里可以添加更多模板应用逻辑
        # 例如：更新幻灯片的样式、颜色等
        
        return presentation
    
    def optimize_layout(self, presentation: Presentation) -> Presentation:
        """优化幻灯片布局"""
        
        # 这里可以添加布局优化逻辑
        # 例如：根据内容长度调整布局，避免内容过多或过少
        
        for i, slide in enumerate(presentation.slides):
            # 根据内容数量调整布局
            content_count = len(slide.content)
            
            if content_count == 0:
                # 无内容，使用标题布局
                slide.layout = Layout.TITLE_ONLY
            elif content_count <= 3:
                # 内容较少，使用标题和内容布局
                slide.layout = Layout.TITLE_AND_CONTENT
            elif content_count <= 6:
                # 内容适中，使用两列布局
                slide.layout = Layout.TWO_CONTENT
            else:
                # 内容较多，可能需要分页
                # 这里简化处理，仍然使用标题和内容布局
                slide.layout = Layout.TITLE_AND_CONTENT
        
        return presentation
    
    def add_slide_numbers(self, presentation: Presentation) -> Presentation:
        """添加幻灯片编号"""
        
        for i, slide in enumerate(presentation.slides):
            slide.slide_number = i + 1
        
        return presentation
    
    def add_transition_notes(self, presentation: Presentation) -> Presentation:
        """添加过渡备注"""
        
        for i, slide in enumerate(presentation.slides):
            if i == 0:
                # 第一张幻灯片
                if not slide.notes:
                    slide.notes = "欢迎开始演示"
            elif i == len(presentation.slides) - 1:
                # 最后一张幻灯片
                if not slide.notes:
                    slide.notes = "演示结束，感谢观看"
            else:
                # 中间幻灯片
                if not slide.notes:
                    next_slide = presentation.get_slide(i + 1)
                    if next_slide:
                        slide.notes = f"接下来：{next_slide.title}"
        
        return presentation