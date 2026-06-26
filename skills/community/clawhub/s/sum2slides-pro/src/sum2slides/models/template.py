"""
模板数据模型
"""

from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, validator
from enum import Enum


class ThemeType(str, Enum):
    """主题类型"""
    
    LIGHT = "light"
    DARK = "dark"
    COLORFUL = "colorful"
    MINIMAL = "minimal"
    PROFESSIONAL = "professional"


class ColorScheme(BaseModel):
    """颜色方案"""
    
    primary: str = Field("#2c3e50", description="主色")
    secondary: str = Field("#3498db", description="辅色")
    accent: str = Field("#e74c3c", description="强调色")
    background: str = Field("#ffffff", description="背景色")
    text: str = Field("#333333", description="文字色")
    
    class Config:
        frozen = True


class FontScheme(BaseModel):
    """字体方案"""
    
    title_font: str = Field("Arial", description="标题字体")
    body_font: str = Field("Arial", description="正文字体")
    title_size: int = Field(44, description="标题字号")
    body_size: int = Field(18, description="正文字号")
    
    class Config:
        frozen = True


class Theme(BaseModel):
    """主题模型"""
    
    name: str = Field(..., description="主题名称")
    type: ThemeType = Field(ThemeType.LIGHT, description="主题类型")
    color_scheme: ColorScheme = Field(default_factory=ColorScheme, description="颜色方案")
    font_scheme: FontScheme = Field(default_factory=FontScheme, description="字体方案")
    description: Optional[str] = Field(None, description="主题描述")
    
    class Config:
        use_enum_values = True
        frozen = True


class Template(BaseModel):
    """模板模型"""
    
    name: str = Field(..., description="模板名称")
    path: str = Field(..., description="模板文件路径")
    theme: Theme = Field(default_factory=lambda: Theme(name="default"), description="主题")
    default_layouts: List[str] = Field(
        default_factory=lambda: ["title", "title_and_content", "section_header"],
        description="默认布局列表"
    )
    description: Optional[str] = Field(None, description="模板描述")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")
    
    class Config:
        frozen = True
    
    @validator("path")
    def validate_path(cls, v):
        """验证路径"""
        if not v:
            raise ValueError("模板路径不能为空")
        # 这里可以添加更多路径验证
        return v
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return self.dict()
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        return self.json(indent=2, ensure_ascii=False)