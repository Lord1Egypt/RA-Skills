"""
文本解析器测试
"""

import pytest

from sum2slides.core.parser import TextParser
from sum2slides.models.document import Document


def test_parser_initialization(parser):
    """测试解析器初始化"""
    
    assert parser is not None
    assert hasattr(parser, 'section_patterns')
    assert hasattr(parser, 'key_point_patterns')


def test_parse_basic_text(parser, sample_text):
    """测试解析基本文本"""
    
    document = parser.parse(sample_text)
    
    assert isinstance(document, Document)
    assert document.raw_text == sample_text.strip()
    assert document.format == "plain"
    assert document.language == "zh"
    assert document.structure is not None
    assert len(document.structure.sections) > 0


def test_parse_markdown(parser, sample_markdown):
    """测试解析Markdown文本"""
    
    document = parser.parse(sample_markdown)
    
    assert isinstance(document, Document)
    assert document.format == "markdown"
    assert document.structure is not None


def test_detect_format(parser):
    """测试格式检测"""
    
    # 纯文本
    plain_text = "这是一个纯文本。"
    assert parser.detect_format(plain_text) == "plain"
    
    # Markdown文本
    markdown_text = "# 标题\n\n这是一个Markdown文本。"
    assert parser.detect_format(markdown_text) == "markdown"
    
    # 包含Markdown元素的文本
    bold_text = "这是一个**粗体**文本。"
    assert parser.detect_format(bold_text) == "markdown"


def test_extract_sections(parser, sample_text):
    """测试提取章节"""
    
    sections = parser.extract_sections(sample_text)
    
    assert isinstance(sections, list)
    assert len(sections) > 0
    
    for section in sections:
        assert section.title
        assert section.content
        assert isinstance(section.key_points, list)


def test_identify_key_points(parser, sample_text):
    """测试识别关键点"""
    
    key_points = parser.identify_key_points(sample_text)
    
    assert isinstance(key_points, list)
    assert len(key_points) > 0
    
    # 检查是否包含预期的关键点
    expected_points = ["完成核心架构设计", "实现基础功能模块", "通过测试验证"]
    for point in expected_points:
        assert any(point in kp for kp in key_points)


def test_clean_text(parser):
    """测试文本清理"""
    
    dirty_text = "  这 是  一个   测试  文本。  "
    cleaned = parser._clean_text(dirty_text)
    
    assert cleaned == "这 是 一个 测试 文本。"


def test_is_section_header(parser):
    """测试章节标题判断"""
    
    # Markdown标题
    assert parser._is_section_header("# 标题")[0] == True
    assert parser._is_section_header("## 子标题")[0] == True
    
    # 数字编号
    assert parser._is_section_header("1. 第一章")[0] == True
    assert parser._is_section_header("2) 第二章")[0] == True
    
    # 中文编号
    assert parser._is_section_header("一、第一章")[0] == True
    assert parser._is_section_header("二. 第二章")[0] == True
    
    # 普通文本
    assert parser._is_section_header("这是一个普通段落")[0] == False


def test_extract_key_points(parser):
    """测试提取关键点"""
    
    lines = [
        "关键：这是一个关键点",
        "重点：这是另一个重点",
        "这是一个普通句子",
        "1. 第一点",
        "- 项目符号点"
    ]
    
    key_points = parser._extract_key_points(lines)
    
    assert len(key_points) == 4
    assert "这是一个关键点" in key_points
    assert "这是另一个重点" in key_points
    assert "第一点" in key_points
    assert "项目符号点" in key_points


def test_parse_empty_text(parser):
    """测试解析空文本"""
    
    with pytest.raises(Exception):
        document = parser.parse("")
    
    with pytest.raises(Exception):
        document = parser.parse("   ")


def test_parse_short_text(parser, short_text):
    """测试解析短文本"""
    
    document = parser.parse(short_text)
    
    assert document is not None
    assert document.structure is not None
    assert len(document.structure.sections) == 1  # 应该只有一个章节


def test_parse_long_text(parser, long_text):
    """测试解析长文本"""
    
    document = parser.parse(long_text)
    
    assert document is not None
    assert len(document.raw_text) > 1000
    assert document.structure is not None