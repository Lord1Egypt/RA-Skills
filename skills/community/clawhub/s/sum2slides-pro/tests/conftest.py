"""
测试配置
"""

import pytest
import tempfile
import os

from sum2slides import Sum2Slides
from sum2slides.core.parser import TextParser
from sum2slides.core.analyzer import ContentAnalyzer
from sum2slides.core.generator import SlideGenerator
from sum2slides.core.formatter import Formatter
from sum2slides.core.validator import InputValidator


@pytest.fixture
def sample_text():
    """示例文本"""
    
    return """
    项目总结报告
    
    一、项目概述
    本项目旨在开发一个智能助手系统，帮助用户提高工作效率。
    
    二、关键成果
    1. 完成核心架构设计
    2. 实现基础功能模块
    3. 通过测试验证
    
    三、下一步计划
    1. 性能优化
    2. 功能扩展
    3. 发布准备
    """


@pytest.fixture
def sample_markdown():
    """示例Markdown文本"""
    
    return """
    # 项目总结报告
    
    ## 项目概述
    本项目旨在开发一个智能助手系统，帮助用户提高工作效率。
    
    ## 关键成果
    - 完成核心架构设计
    - 实现基础功能模块
    - 通过测试验证
    
    ## 下一步计划
    1. 性能优化
    2. 功能扩展
    3. 发布准备
    """


@pytest.fixture
def short_text():
    """短文本"""
    
    return "这是一个简短的测试文本，用于验证基本功能。"


@pytest.fixture
def long_text():
    """长文本"""
    
    return "这是一个长文本，" * 1000


@pytest.fixture
def temp_dir():
    """临时目录"""
    
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def temp_file(temp_dir):
    """临时文件"""
    
    temp_file = os.path.join(temp_dir, "test.txt")
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write("测试文件内容")
    
    return temp_file


@pytest.fixture
def converter():
    """Sum2Slides转换器"""
    
    return Sum2Slides()


@pytest.fixture
def parser():
    """文本解析器"""
    
    return TextParser()


@pytest.fixture
def analyzer():
    """内容分析器"""
    
    return ContentAnalyzer()


@pytest.fixture
def generator():
    """幻灯片生成器"""
    
    return SlideGenerator()


@pytest.fixture
def formatter():
    """格式转换器"""
    
    return Formatter()


@pytest.fixture
def validator():
    """输入验证器"""
    
    return InputValidator()