"""
文档数据模型
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator


class Section(BaseModel):
    """文档章节"""
    
    title: str = Field(..., description="章节标题")
    content: str = Field(..., description="章节内容")
    level: int = Field(1, description="章节级别 (1-3)")
    key_points: List[str] = Field(default_factory=list, description="关键点列表")
    
    class Config:
        frozen = True  # 不可变对象


class SlideContent(BaseModel):
    """幻灯片内容"""
    
    title: str = Field(..., description="幻灯片标题")
    bullet_points: List[str] = Field(default_factory=list, description="要点列表")
    notes: Optional[str] = Field(None, description="演讲者备注")
    layout: str = Field("title_and_content", description="布局类型")
    
    class Config:
        frozen = True


class DocumentStructure(BaseModel):
    """文档结构"""
    
    title: Optional[str] = Field(None, description="文档标题")
    sections: List[Section] = Field(default_factory=list, description="章节列表")
    total_sections: int = Field(0, description="总章节数")
    estimated_slides: int = Field(0, description="预计幻灯片数量")
    
    @validator("estimated_slides", always=True)
    def calculate_slides(cls, v, values):
        """计算预计幻灯片数量"""
        if "sections" in values:
            sections = values["sections"]
            # 简单规则：每2个章节或每5个关键点生成一张幻灯片
            total_points = sum(len(section.key_points) for section in sections)
            return max(3, len(sections) // 2 + total_points // 5)
        return v
    
    class Config:
        frozen = True


class Document(BaseModel):
    """文档模型"""
    
    raw_text: str = Field(..., description="原始文本")
    format: str = Field("plain", description="格式类型: plain/markdown/html")
    language: str = Field("zh", description="语言代码")
    created_at: datetime = Field(default_factory=datetime.now, description="创建时间")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")
    structure: Optional[DocumentStructure] = Field(None, description="文档结构")
    
    class Config:
        frozen = True
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return self.dict()
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        return self.json(indent=2, ensure_ascii=False)