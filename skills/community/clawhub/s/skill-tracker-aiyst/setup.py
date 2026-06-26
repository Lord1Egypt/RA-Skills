#!/usr/bin/env python3
"""
Skill Tracker - 技能使用统计追踪器

安装：
    pip install .

或直接复制：
    cp skill_tracker.py /path/to/your/project/
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取 README
this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text(encoding='utf-8')

# 读取版本
version = '1.2.0'

setup(
    name='skill-tracker',
    version=version,
    author='aiyst',
    author_email='aiyst@qq.com',
    description='通用技能使用统计追踪器 - 为 OpenClaw 技能提供使用情况统计',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/openclaw/skill-tracker',
    license='MIT',
    
    # 包信息
    py_modules=['skill_tracker'],
    packages=find_packages(),
    
    # Python 版本要求
    python_requires='>=3.6',
    
    # 依赖（无外部依赖，使用标准库）
    install_requires=[],
    
    # 开发依赖
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
        ]
    },
    
    # 入口点（命令行工具）
    entry_points={
        'console_scripts': [
            'skill-tracker=skill_tracker:main',
        ],
    },
    
    # 分类
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Logging',
    ],
    
    # 关键词
    keywords='skill tracking analytics statistics openclaw',
    
    # 包含的文件
    include_package_data=True,
    package_data={
        '': ['*.md', '*.json', '*.yaml'],
    },
    
    # 项目链接
    project_urls={
        'Bug Reports': 'https://github.com/openclaw/skill-tracker/issues',
        'Source': 'https://github.com/openclaw/skill-tracker',
        'Documentation': 'https://github.com/openclaw/skill-tracker#readme',
    },
)
