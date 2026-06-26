"""
输入验证器
"""

import os
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """验证结果"""
    
    valid: bool
    message: str = ""
    errors: list = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
    
    @classmethod
    def success(cls, message: str = "验证通过") -> 'ValidationResult':
        """创建成功结果"""
        return cls(valid=True, message=message)
    
    @classmethod
    def error(cls, message: str, errors: list = None) -> 'ValidationResult':
        """创建错误结果"""
        if errors is None:
            errors = [message]
        return cls(valid=False, message=message, errors=errors)


class InputValidator:
    """输入验证器"""
    
    MAX_TEXT_LENGTH = 10000  # 最大文本长度
    MIN_TEXT_LENGTH = 10     # 最小文本长度
    SUPPORTED_FORMATS = ['txt', 'md', 'markdown']
    SUPPORTED_LANGUAGES = ['zh', 'en']
    
    def validate_text(self, text: str) -> ValidationResult:
        """验证文本输入"""
        
        errors = []
        
        # 检查文本是否为空
        if not text:
            errors.append("文本内容不能为空")
        
        # 检查文本长度
        if text:
            if len(text) < self.MIN_TEXT_LENGTH:
                errors.append(f"文本过短，至少需要{self.MIN_TEXT_LENGTH}个字符")
            
            if len(text) > self.MAX_TEXT_LENGTH:
                errors.append(f"文本过长，最多支持{self.MAX_TEXT_LENGTH}个字符")
        
        # 检查文本内容
        if text and text.strip() == "":
            errors.append("文本内容只包含空白字符")
        
        if errors:
            return ValidationResult.error("文本验证失败", errors)
        
        return ValidationResult.success("文本验证通过")
    
    def validate_file(self, file_path: str) -> ValidationResult:
        """验证文件输入"""
        
        errors = []
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            errors.append(f"文件不存在: {file_path}")
            return ValidationResult.error("文件验证失败", errors)
        
        # 检查是否为文件
        if not os.path.isfile(file_path):
            errors.append(f"路径不是文件: {file_path}")
        
        # 检查文件扩展名
        file_ext = os.path.splitext(file_path)[1].lower().lstrip('.')
        if file_ext not in self.SUPPORTED_FORMATS:
            errors.append(f"不支持的文件格式: {file_ext}，支持格式: {', '.join(self.SUPPORTED_FORMATS)}")
        
        # 检查文件大小
        try:
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                errors.append("文件为空")
            elif file_size > 1024 * 1024:  # 1MB
                errors.append("文件过大，最大支持1MB")
        except OSError as e:
            errors.append(f"无法读取文件大小: {str(e)}")
        
        if errors:
            return ValidationResult.error("文件验证失败", errors)
        
        return ValidationResult.success("文件验证通过")
    
    def validate_output_path(self, output_path: str) -> ValidationResult:
        """验证输出路径"""
        
        errors = []
        
        # 检查路径是否为空
        if not output_path:
            errors.append("输出路径不能为空")
            return ValidationResult.error("输出路径验证失败", errors)
        
        # 检查文件扩展名
        file_ext = os.path.splitext(output_path)[1].lower()
        if file_ext not in ['.pptx', '.ppt']:
            errors.append(f"不支持的输出格式: {file_ext}，只支持 .pptx 或 .ppt")
        
        # 检查目录是否可写
        output_dir = os.path.dirname(output_path) or '.'
        if output_dir:
            if not os.path.exists(output_dir):
                try:
                    os.makedirs(output_dir, exist_ok=True)
                except OSError as e:
                    errors.append(f"无法创建输出目录: {str(e)}")
            elif not os.path.isdir(output_dir):
                errors.append(f"输出目录不是目录: {output_dir}")
            elif not os.access(output_dir, os.W_OK):
                errors.append(f"输出目录不可写: {output_dir}")
        
        if errors:
            return ValidationResult.error("输出路径验证失败", errors)
        
        return ValidationResult.success("输出路径验证通过")
    
    def validate_template(self, template_name: str, 
                         available_templates: list) -> ValidationResult:
        """验证模板"""
        
        errors = []
        
        if not template_name:
            errors.append("模板名称不能为空")
        elif template_name not in available_templates:
            errors.append(f"模板不存在: {template_name}，可用模板: {', '.join(available_templates)}")
        
        if errors:
            return ValidationResult.error("模板验证失败", errors)
        
        return ValidationResult.success("模板验证通过")
    
    def validate_language(self, language: str) -> ValidationResult:
        """验证语言"""
        
        if language not in self.SUPPORTED_LANGUAGES:
            return ValidationResult.error(
                f"不支持的语言: {language}，支持语言: {', '.join(self.SUPPORTED_LANGUAGES)}"
            )
        
        return ValidationResult.success("语言验证通过")
    
    def validate_max_slides(self, max_slides: int) -> ValidationResult:
        """验证最大幻灯片数量"""
        
        errors = []
        
        if not isinstance(max_slides, int):
            errors.append("最大幻灯片数量必须是整数")
        elif max_slides < 1:
            errors.append("最大幻灯片数量必须大于0")
        elif max_slides > 50:
            errors.append("最大幻灯片数量不能超过50")
        
        if errors:
            return ValidationResult.error("最大幻灯片数量验证失败", errors)
        
        return ValidationResult.success("最大幻灯片数量验证通过")
    
    def validate_font_size(self, font_size: int) -> ValidationResult:
        """验证字体大小"""
        
        errors = []
        
        if not isinstance(font_size, int):
            errors.append("字体大小必须是整数")
        elif font_size < 8:
            errors.append("字体大小必须大于等于8")
        elif font_size > 72:
            errors.append("字体大小不能超过72")
        
        if errors:
            return ValidationResult.error("字体大小验证失败", errors)
        
        return ValidationResult.success("字体大小验证通过")
    
    def validate_theme(self, theme: str) -> ValidationResult:
        """验证主题"""
        
        valid_themes = ['light', 'dark', 'colorful', 'minimal', 'professional']
        
        if theme not in valid_themes:
            return ValidationResult.error(
                f"无效的主题: {theme}，有效主题: {', '.join(valid_themes)}"
            )
        
        return ValidationResult.success("主题验证通过")
    
    def validate_all(self, inputs: Dict[str, Any]) -> ValidationResult:
        """验证所有输入"""
        
        all_errors = []
        
        # 验证文本或文件
        if 'text' in inputs and inputs['text']:
            text_result = self.validate_text(inputs['text'])
            if not text_result.valid:
                all_errors.extend(text_result.errors)
        elif 'input_file' in inputs and inputs['input_file']:
            file_result = self.validate_file(inputs['input_file'])
            if not file_result.valid:
                all_errors.extend(file_result.errors)
        else:
            all_errors.append("必须提供文本内容或输入文件")
        
        # 验证输出路径
        if 'output_path' in inputs:
            output_result = self.validate_output_path(inputs['output_path'])
            if not output_result.valid:
                all_errors.extend(output_result.errors)
        
        # 验证可选参数
        if 'template' in inputs and inputs['template']:
            available = inputs.get('available_templates', ['default'])
            template_result = self.validate_template(inputs['template'], available)
            if not template_result.valid:
                all_errors.extend(template_result.errors)
        
        if 'language' in inputs and inputs['language']:
            language_result = self.validate_language(inputs['language'])
            if not language_result.valid:
                all_errors.extend(language_result.errors)
        
        if 'max_slides' in inputs and inputs['max_slides']:
            slides_result = self.validate_max_slides(inputs['max_slides'])
            if not slides_result.valid:
                all_errors.extend(slides_result.errors)
        
        if 'font_size' in inputs and inputs['font_size']:
            font_result = self.validate_font_size(inputs['font_size'])
            if not font_result.valid:
                all_errors.extend(font_result.errors)
        
        if 'theme' in inputs and inputs['theme']:
            theme_result = self.validate_theme(inputs['theme'])
            if not theme_result.valid:
                all_errors.extend(theme_result.errors)
        
        if all_errors:
            return ValidationResult.error("输入验证失败", all_errors)
        
        return ValidationResult.success("所有输入验证通过")