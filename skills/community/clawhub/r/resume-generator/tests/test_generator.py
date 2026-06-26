#!/usr/bin/env python3
"""
Resume Generator 单元测试
TDD模式：先写测试，验证核心功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generator import ResumeGenerator
import pytest


class TestResumeGeneratorInit:
    """测试简历生成器初始化"""
    
    def test_init_with_minimal_data(self):
        """最小数据初始化"""
        data = {'name': '张三', 'email': 'zhangsan@example.com'}
        gen = ResumeGenerator(data)
        assert gen.data['name'] == '张三'
        assert gen.data['email'] == 'zhangsan@example.com'
    
    def test_init_with_full_data(self):
        """完整数据初始化"""
        data = {
            'name': '李四',
            'email': 'lisi@example.com',
            'phone': '13900001111',
            'location': '北京',
            'education': [{'school': '北大', 'major': 'CS', 'degree': '硕士', 'year': '2020'}],
            'experience': [{'company': '阿里', 'title': '工程师', 'duration': '2020-至今', 'description': '后端开发'}],
            'projects': [{'name': 'X项目', 'role': '负责人', 'tech': 'Python', 'description': '开发', 'outcome': '提升50%'}],
            'skills': [{'category': '语言', 'items': ['Python']}]
        }
        gen = ResumeGenerator(data)
        assert gen.data['phone'] == '13900001111'
        assert gen.data['location'] == '北京'
        assert len(gen.data['education']) == 1
    
    def test_init_missing_name_raises(self):
        """缺少姓名应抛异常"""
        with pytest.raises(ValueError, match="必填字段"):
            ResumeGenerator({'email': 'test@example.com'})
    
    def test_init_missing_email_raises(self):
        """缺少邮箱应抛异常"""
        with pytest.raises(ValueError, match="必填字段"):
            ResumeGenerator({'name': '张三'})
    
    def test_default_values(self):
        """测试默认值填充"""
        data = {'name': '王五', 'email': 'wang@example.com'}
        gen = ResumeGenerator(data)
        assert gen.data['location'] == ''
        assert gen.data['education'] == []
        assert gen.data['experience'] == []


class TestMarkdownTemplates:
    """测试Markdown模板生成"""
    
    @pytest.fixture
    def sample_data(self):
        return {
            'name': '张三',
            'email': 'zhangsan@example.com',
            'phone': '13800138000',
            'location': '上海',
            'education': [{'school': '上海大学', 'major': '计算机', 'degree': '本科', 'year': '2020'}],
            'experience': [{'company': '字节', 'title': '测试工程师', 'duration': '2020.06-至今', 'description': '负责测试'}],
            'projects': [{'name': 'XX平台', 'role': '测试', 'tech': 'Python', 'description': '自动化', 'outcome': '提升30%'}],
            'skills': [{'category': '语言', 'items': ['Python', 'JavaScript']}]
        }
    
    def test_simple_template_basic(self, sample_data):
        """简约模板基本结构"""
        gen = ResumeGenerator(sample_data)
        md = gen.generate_markdown('simple')
        assert '# 张三' in md
        assert 'zhangsan@example.com' in md
        assert '13800138000' in md
        assert '上海' in md
    
    def test_simple_template_skills(self, sample_data):
        """简约模板技能部分"""
        gen = ResumeGenerator(sample_data)
        md = gen.generate_markdown('simple')
        assert 'Python' in md
        assert 'JavaScript' in md
        assert '## 教育经历' in md
        assert '上海大学' in md
    
    def test_simple_template_experience(self, sample_data):
        """简约模板工作经历"""
        gen = ResumeGenerator(sample_data)
        md = gen.generate_markdown('simple')
        assert '字节' in md
        assert '测试工程师' in md
        assert '2020.06-至今' in md
    
    def test_simple_template_projects(self, sample_data):
        """简约模板项目经历"""
        gen = ResumeGenerator(sample_data)
        md = gen.generate_markdown('simple')
        assert 'XX平台' in md
        assert 'Python' in md
        assert '自动化' in md
        assert '提升30%' in md
    
    def test_classic_template_basic(self, sample_data):
        """经典模板基本结构"""
        gen = ResumeGenerator(sample_data)
        md = gen.generate_markdown('classic')
        assert '# 张三' in md
        assert 'zhangsan@example.com' in md
    
    def test_modern_template_basic(self, sample_data):
        """现代模板基本结构"""
        gen = ResumeGenerator(sample_data)
        md = gen.generate_markdown('modern')
        assert '# 张三' in md
        assert 'zhangsan@example.com' in md
    
    def test_invalid_template_raises(self, sample_data):
        """无效模板应抛异常"""
        gen = ResumeGenerator(sample_data)
        with pytest.raises(ValueError, match="未知模板"):
            gen.generate_markdown('invalid')


class TestEdgeCases:
    """边界情况测试"""
    
    def test_empty_education(self):
        """空教育经历"""
        data = {'name': '测试', 'email': 'test@example.com', 'education': []}
        gen = ResumeGenerator(data)
        md = gen.generate_markdown('simple')
        assert '## 教育经历' not in md or '暂无' in md
    
    def test_empty_experience(self):
        """空工作经历"""
        data = {'name': '测试', 'email': 'test@example.com', 'experience': []}
        gen = ResumeGenerator(data)
        md = gen.generate_markdown('simple')
        assert '## 工作经历' not in md or '暂无' in md
    
    def test_empty_projects(self):
        """空项目经历"""
        data = {'name': '测试', 'email': 'test@example.com', 'projects': []}
        gen = ResumeGenerator(data)
        md = gen.generate_markdown('simple')
        assert '## 项目经历' not in md or '暂无' in md
    
    def test_self_intro(self):
        """自我介绍字段"""
        data = {
            'name': '测试', 'email': 'test@example.com',
            'self_intro': '5年经验测试工程师'
        }
        gen = ResumeGenerator(data)
        md = gen.generate_markdown('simple')
        assert '5年经验测试工程师' in md


class TestCLI:
    """测试CLI入口（通过subprocess）"""
    pass  # CLI测试已在quick_test.py中手动验证


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
