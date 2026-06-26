"""
Sum2Slides 主API接口
"""

import os
from typing import Optional, Dict, Any, List
from datetime import datetime

from .core.parser import TextParser
from .core.analyzer import ContentAnalyzer
from .core.generator import SlideGenerator
from .core.formatter import Formatter
from .core.validator import InputValidator
from .exporters.pptx import PowerPointExporter
from .models.document import Document
from .models.slide import Presentation
from .models.template import Template, Theme


class Sum2Slides:
    """Sum2Slides 主类"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化Sum2Slides转换器
        
        Args:
            config: 配置字典，包含以下可选参数：
                - template: 模板名称 (默认: "default")
                - theme: 主题名称 (默认: "light") 
                - max_slides: 最大幻灯片数量 (默认: 10)
                - font_size: 字体大小 (默认: 18)
                - language: 语言代码 (默认: "zh")
        """
        
        if config is None:
            config = {}
        
        self.config = {
            'template': config.get('template', 'default'),
            'theme': config.get('theme', 'light'),
            'max_slides': config.get('max_slides', 10),
            'font_size': config.get('font_size', 18),
            'language': config.get('language', 'zh'),
        }
        
        # 初始化组件
        self.parser = TextParser()
        self.analyzer = ContentAnalyzer(max_slides=self.config['max_slides'])
        self.generator = SlideGenerator()
        self.formatter = Formatter()
        self.validator = InputValidator()
        self.exporter = PowerPointExporter()
        
        # 初始化模板
        self.templates = self._load_default_templates()
    
    def convert(self, text: str, output_path: Optional[str] = None) -> Presentation:
        """
        将文本转换为幻灯片演示文稿
        
        Args:
            text: 输入文本
            output_path: 输出文件路径（可选）
            
        Returns:
            Presentation: 演示文稿对象
            
        Raises:
            ValueError: 如果输入验证失败
        """
        
        # 验证输入
        validation_result = self.validator.validate_text(text)
        if not validation_result.valid:
            raise ValueError(f"输入验证失败: {validation_result.message}")
        
        # 解析文本
        document = self.parser.parse(text, language=self.config['language'])
        
        # 分析内容
        structure = self.analyzer.analyze_structure(document)
        
        # 组织内容到幻灯片
        slide_contents = self.analyzer.organize_content(structure)
        
        # 获取模板
        template = self.templates.get(self.config['template'])
        
        # 生成幻灯片
        presentation = self.generator.generate(slide_contents, template)
        
        # 应用模板
        if template:
            presentation = self.generator.apply_template(presentation, template)
        
        # 优化布局
        presentation = self.generator.optimize_layout(presentation)
        
        # 添加幻灯片编号
        presentation = self.generator.add_slide_numbers(presentation)
        
        # 添加过渡备注
        presentation = self.generator.add_transition_notes(presentation)
        
        # 如果提供了输出路径，导出文件
        if output_path:
            self.export(presentation, output_path)
        
        return presentation
    
    def convert_from_file(self, input_file: str, output_file: str) -> None:
        """
        从文件转换
        
        Args:
            input_file: 输入文件路径
            output_file: 输出文件路径
            
        Raises:
            ValueError: 如果输入验证失败
            IOError: 如果文件操作失败
        """
        
        # 验证输入文件
        validation_result = self.validator.validate_file(input_file)
        if not validation_result.valid:
            raise ValueError(f"文件验证失败: {validation_result.message}")
        
        # 验证输出路径
        validation_result = self.validator.validate_output_path(output_file)
        if not validation_result.valid:
            raise ValueError(f"输出路径验证失败: {validation_result.message}")
        
        # 读取文件内容
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            raise IOError(f"无法读取文件 {input_file}: {str(e)}")
        
        # 转换文本
        presentation = self.convert(text)
        
        # 导出文件
        self.export(presentation, output_file)
    
    def convert_to_json(self, text: str) -> str:
        """
        转换为JSON格式
        
        Args:
            text: 输入文本
            
        Returns:
            str: JSON格式的演示文稿数据
            
        Raises:
            ValueError: 如果输入验证失败
        """
        
        # 验证输入
        validation_result = self.validator.validate_text(text)
        if not validation_result.valid:
            raise ValueError(f"输入验证失败: {validation_result.message}")
        
        # 解析文本
        document = self.parser.parse(text, language=self.config['language'])
        
        # 分析内容
        structure = self.analyzer.analyze_structure(document)
        
        # 组织内容到幻灯片
        slide_contents = self.analyzer.organize_content(structure)
        
        # 创建演示文稿对象
        presentation = Presentation(
            title=structure.title or "演示文稿",
            slides=[],
            author="Sum2Slides",
            created_at=datetime.now().isoformat(),
            template=self.config['template'],
            theme=self.config['theme']
        )
        
        # 添加幻灯片
        for i, content in enumerate(slide_contents):
            slide = self.generator._create_slide_from_content(content, i + 1)
            presentation.add_slide(slide)
        
        # 转换为JSON
        return presentation.to_json()
    
    def export(self, presentation: Presentation, output_path: str) -> None:
        """
        导出演示文稿
        
        Args:
            presentation: 演示文稿对象
            output_path: 输出文件路径
            
        Raises:
            ValueError: 如果输出路径验证失败
            IOError: 如果导出失败
        """
        
        # 验证输出路径
        validation_result = self.validator.validate_output_path(output_path)
        if not validation_result.valid:
            raise ValueError(f"输出路径验证失败: {validation_result.message}")
        
        # 准备导出选项
        export_options = {
            'template_path': None,  # 可以添加模板路径
            'font_size': self.config['font_size'],
            'theme': self.config['theme'],
        }
        
        # 导出文件
        try:
            self.exporter.export(presentation, output_path, export_options)
        except Exception as e:
            raise IOError(f"导出失败: {str(e)}")
    
    def batch_convert(self, input_files: List[str], output_dir: str) -> List[str]:
        """
        批量转换文件
        
        Args:
            input_files: 输入文件路径列表
            output_dir: 输出目录
            
        Returns:
            List[str]: 输出文件路径列表
            
        Raises:
            ValueError: 如果输入验证失败
            IOError: 如果文件操作失败
        """
        
        output_files = []
        
        # 确保输出目录存在
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        for input_file in input_files:
            # 生成输出文件名
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            output_file = os.path.join(output_dir, f"{base_name}.pptx")
            
            try:
                # 转换文件
                self.convert_from_file(input_file, output_file)
                output_files.append(output_file)
            except Exception as e:
                print(f"转换文件 {input_file} 失败: {str(e)}")
                continue
        
        return output_files
    
    def _load_default_templates(self) -> Dict[str, Template]:
        """加载默认模板"""
        
        # 创建默认主题
        light_theme = Theme(
            name="light",
            type="light",
            description="浅色主题"
        )
        
        dark_theme = Theme(
            name="dark", 
            type="dark",
            description="深色主题"
        )
        
        # 创建默认模板
        default_template = Template(
            name="default",
            path="",  # 使用python-pptx的默认模板
            theme=light_theme,
            description="默认模板"
        )
        
        business_template = Template(
            name="business",
            path="",
            theme=light_theme,
            description="商务模板"
        )
        
        academic_template = Template(
            name="academic",
            path="",
            theme=light_theme,
            description="学术模板"
        )
        
        return {
            'default': default_template,
            'business': business_template,
            'academic': academic_template,
        }
    
    def get_available_templates(self) -> List[str]:
        """获取可用模板列表"""
        
        return list(self.templates.keys())
    
    def get_config(self) -> Dict[str, Any]:
        """获取当前配置"""
        
        return self.config.copy()
    
    def update_config(self, new_config: Dict[str, Any]) -> None:
        """更新配置"""
        
        self.config.update(new_config)
        
        # 如果更新了max_slides，需要更新分析器
        if 'max_slides' in new_config:
            self.analyzer = ContentAnalyzer(max_slides=self.config['max_slides'])