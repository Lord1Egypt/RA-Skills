#!/usr/bin/env python3
"""
测试 analyze_skill.py
"""
import unittest
import os
import sys
import tempfile

# 添加 scripts 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from analyze_skill import parse_skill_md, generate_report

class TestAnalyzeSkill(unittest.TestCase):
    
    def setUp(self):
        """创建测试用的 SKILL.md 文件."""
        self.test_skill_md = """---
name: test-skill
description: A test skill for unit testing
---

# Test Skill

## Features

- Feature 1: Test feature one
- Feature 2: Test feature two

## Usage

```bash
python3 test.py
```

## Configuration

- Config item 1
- Config item 2

## Notes

- Note 1
- Note 2
"""
        self.temp_dir = tempfile.mkdtemp()
        self.skill_file = os.path.join(self.temp_dir, 'SKILL.md')
        with open(self.skill_file, 'w') as f:
            f.write(self.test_skill_md)
    
    def tearDown(self):
        """清理测试文件."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_parse_skill_md(self):
        """测试解析 SKILL.md."""
        data = parse_skill_md(self.skill_file)
        
        self.assertIsNotNone(data)
        self.assertEqual(data['name'], 'test-skill')
        self.assertEqual(data['description'], 'A test skill for unit testing')
        self.assertEqual(len(data['features']), 2)
        self.assertEqual(len(data['examples']), 1)
        self.assertEqual(len(data['config']), 2)
        self.assertEqual(len(data['warnings']), 2)
    
    def test_generate_report_text(self):
        """测试生成文本报告."""
        data = parse_skill_md(self.skill_file)
        report = generate_report(data, 'text')
        
        self.assertIn('test-skill', report)
        self.assertIn('Feature 1', report)
        self.assertIn('python3 test.py', report)
    
    def test_generate_report_markdown(self):
        """测试生成 Markdown 报告."""
        data = parse_skill_md(self.skill_file)
        report = generate_report(data, 'markdown')
        
        self.assertIn('# 🔍 test-skill', report)
        self.assertIn('## 🎯 核心功能', report)
    
    def test_generate_report_json(self):
        """测试生成 JSON 报告."""
        data = parse_skill_md(self.skill_file)
        report = generate_report(data, 'json')
        
        import json
        parsed = json.loads(report)
        self.assertEqual(parsed['name'], 'test-skill')

if __name__ == '__main__':
    unittest.main()
