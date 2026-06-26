"""
幻灯片数据模型
"""

from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


class Layout(str, Enum):
    """幻灯片布局类型"""
    
    TITLE = "title"
    TITLE_AND_CONTENT = "title_and_content"
    SECTION_HEADER = "section_header"
    TWO_CONTENT = "two_content"
    COMPARISON = "comparison"
    TITLE_ONLY = "title_only"
    BLANK = "blank"
    CONTENT_WITH_CAPTION = "content_with_caption"
    PICTURE_WITH_CAPTION = "picture_with_caption"


class Slide(BaseModel):
    """幻灯片模型"""
    
    title: str = Field(..., description="幻灯片标题")
    content: List[str] = Field(default_factory=list, description="内容列表")
    layout: Layout = Field(Layout.TITLE_AND_CONTENT, description="布局类型")
    slide_number: int = Field(..., description="幻灯片编号")
    notes: Optional[str] = Field(None, description="演讲者备注")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")
    
    class Config:
        use_enum_values = True
        frozen = True
    
    def add_content(self, content: str) -> None:
        """添加内容"""
        self.content.append(content)
    
    def set_notes(self, notes: str) -> None:
        """设置备注"""
        self.notes = notes


class Presentation(BaseModel):
    """演示文稿模型"""
    
    title: str = Field(..., description="演示文稿标题")
    slides: List[Slide] = Field(default_factory=list, description="幻灯片列表")
    author: Optional[str] = Field(None, description="作者")
    created_at: str = Field(..., description="创建时间")
    template: str = Field("default", description="模板名称")
    theme: str = Field("light", description="主题名称")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")
    
    class Config:
        frozen = True
    
    def add_slide(self, slide: Slide) -> None:
        """添加幻灯片"""
        self.slides.append(slide)
    
    def get_slide(self, index: int) -> Optional[Slide]:
        """获取指定索引的幻灯片"""
        if 0 <= index < len(self.slides):
            return self.slides[index]
        return None
    
    def total_slides(self) -> int:
        """获取总幻灯片数"""
        return len(self.slides)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return self.dict()
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        return self.json(indent=2, ensure_ascii=False)