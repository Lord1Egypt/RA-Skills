"""
PPT生成器抽象基类
支持多PPT软件扩展：PowerPoint、WPS、Google Slides等
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
import os


class PPTSoftware(Enum):
    """支持的PPT软件类型"""
    POWERPOINT = "powerpoint"
    WPS_OFFICE = "wps_office"
    GOOGLE_SLIDES = "google_slides"
    KEYNOTE = "keynote"


class PPTTemplate(Enum):
    """PPT模板类型"""
    BUSINESS = "business"
    EDUCATION = "education"
    TECHNICAL = "technical"
    CREATIVE = "creative"
    MINIMALIST = "minimalist"


@dataclass
class SlideContent:
    """幻灯片内容定义"""
    title: str
    content: Optional[List[str]] = None
    type: str = "content"  # content, two_column, comparison, summary
    bullet_points: bool = True
    left_content: Optional[List[str]] = None
    right_content: Optional[List[str]] = None
    key_points: Optional[List[str]] = None
    conclusion: Optional[str] = None
    
    def __post_init__(self):
        """初始化后处理"""
        if self.content is None:
            self.content = []


@dataclass
class PPTStructure:
    """PPT结构定义"""
    title: str
    subtitle: Optional[str] = None
    author: Optional[str] = None
    date: Optional[str] = None
    slides: List[SlideContent] = None
    template: PPTTemplate = PPTTemplate.BUSINESS
    software: PPTSoftware = PPTSoftware.POWERPOINT
    
    def __post_init__(self):
        if self.slides is None:
            self.slides = []


class BasePPTGenerator(ABC):
    """PPT生成器抽象基类"""
    
    def __init__(self, software_type: PPTSoftware, template: PPTTemplate = PPTTemplate.BUSINESS):
        """
        初始化生成器
        
        Args:
            software_type: PPT软件类型
            template: 模板类型
        """
        self.software_type = software_type
        self.template = template
        self.slides = []
        
    @abstractmethod
    def create_cover(self, structure: PPTStructure) -> Any:
        """
        创建封面页
        
        Args:
            structure: PPT结构
            
        Returns:
            平台特定的表示或状态
        """
        pass
    
    @abstractmethod
    def create_content_slide(self, content: SlideContent) -> Any:
        """
        创建内容页
        
        Args:
            content: 幻灯片内容
            
        Returns:
            平台特定的表示或状态
        """
        pass
    
    @abstractmethod
    def create_two_column_slide(self, content: SlideContent) -> Any:
        """
        创建两栏内容页
        
        Args:
            content: 幻灯片内容
            
        Returns:
            平台特定的表示或状态
        """
        pass
    
    @abstractmethod
    def create_comparison_slide(self, content: SlideContent) -> Any:
        """
        创建比较页
        
        Args:
            content: 幻灯片内容
            
        Returns:
            平台特定的表示或状态
        """
        pass
    
    @abstractmethod
    def create_summary_slide(self, content: SlideContent) -> Any:
        """
        创建总结页
        
        Args:
            content: 幻灯片内容
            
        Returns:
            平台特定的表示或状态
        """
        pass
    
    @abstractmethod
    def save_ppt(self, file_path: str) -> str:
        """
        保存PPT文件
        
        Args:
            file_path: 保存路径
            
        Returns:
            保存的文件路径
        """
        pass
    
    def generate_from_structure(self, structure: PPTStructure) -> str:
        """
        根据结构生成完整PPT
        
        Args:
            structure: PPT结构定义
            
        Returns:
            生成的PPT文件路径
        """
        # 验证结构
        self._validate_structure(structure)
        
        # 创建封面
        self.create_cover(structure)
        
        # 创建内容页
        for slide_content in structure.slides:
            if slide_content.type == "content":
                self.create_content_slide(slide_content)
            elif slide_content.type == "two_column":
                self.create_two_column_slide(slide_content)
            elif slide_content.type == "comparison":
                self.create_comparison_slide(slide_content)
            elif slide_content.type == "summary":
                self.create_summary_slide(slide_content)
        
        # 生成文件名
        default_name = f"{structure.title}_{self.software_type.value}_{self.template.value}.pptx"
        file_name = self._generate_filename(structure, default_name)
        
        # 保存
        output_dir = os.path.expanduser("~/Desktop")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, file_name)
        
        return self.save_ppt(output_path)
    
    def _validate_structure(self, structure: PPTStructure) -> None:
        """
        验证PPT结构有效性
        
        Args:
            structure: 要验证的结构
            
        Raises:
            ValueError: 如果结构无效
        """
        if not structure.title:
            raise ValueError("PPT标题不能为空")
        
        if not structure.slides:
            raise ValueError("PPT必须包含至少一个幻灯片")
    
    def _generate_filename(self, structure: PPTStructure, default_name: str) -> str:
        """
        生成文件名
        
        Args:
            structure: PPT结构
            default_name: 默认文件名
            
        Returns:
            生成的文件名
        """
        # 移除特殊字符
        safe_title = "".join(c for c in structure.title if c.isalnum() or c in (' ', '-', '_')).strip()
        
        if not safe_title:
            return default_name
        
        # 添加扩展名
        if not safe_title.lower().endswith(('.pptx', '.ppt', '.dps')):
            ext = self._get_extension_for_software()
            return f"{safe_title}{ext}"
        
        return safe_title
    
    def _get_extension_for_software(self) -> str:
        """
        根据软件类型获取文件扩展名
        
        Returns:
            文件扩展名
        """
        extensions = {
            PPTSoftware.POWERPOINT: ".pptx",
            PPTSoftware.WPS_OFFICE: ".pptx",  # WPS也支持.pptx格式
            PPTSoftware.GOOGLE_SLIDES: ".pptx",  # 下载时使用.pptx
            PPTSoftware.KEYNOTE: ".pptx"  # 导出时使用.pptx
        }
        
        return extensions.get(self.software_type, ".pptx")


class GeneratorFactory:
    """PPT生成器工厂，支持多种PPT软件"""
    
    @staticmethod
    def create_generator(software_type: PPTSoftware = PPTSoftware.POWERPOINT,
                        template: PPTTemplate = PPTTemplate.BUSINESS):
        """
        创建PPT生成器实例
        
        Args:
            software_type: PPT软件类型
            template: 模板类型
            
        Returns:
            BasePPTGenerator实例
            
        Raises:
            ValueError: 如果软件类型不支持
        """
        if software_type == PPTSoftware.POWERPOINT:
            from .pptx_generator import PPTXGenerator
            return PPTXGenerator(template=template)
        
        elif software_type == PPTSoftware.WPS_OFFICE:
            from .wps_generator import WPSGenerator
            return WPSGenerator(template=template)
        
        # 其他软件类型的导入
        elif software_type == PPTSoftware.GOOGLE_SLIDES:
            # TODO: 实现Google Slides生成器
            raise ValueError(f"暂不支持 {software_type.value}")
        
        elif software_type == PPTSoftware.KEYNOTE:
            # TODO: 实现Keynote生成器

            raise ValueError(f"暂不支持 {software_type.value}")
        
        else:
            raise ValueError(f"不支持的PPT软件类型: {software_type}")