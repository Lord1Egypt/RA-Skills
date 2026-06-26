#!/usr/bin/env python3
"""Skills Monitor — 安装脚本"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取 README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="skills-monitor",
    version="0.6.1",
    description="Skills 监控评估系统 — 安全加固、7因子评估、数据脱敏、GDPR合规、中心化服务器、跨模型基准评测",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Skills Monitor Team",
    python_requires=">=3.9",
    packages=find_packages(exclude=["tests", "tests.*", "reports", "report_data", "logs"]),
    py_modules=["skills_monitor_cli", "skills_monitor_web"],
    install_requires=[
        "flask>=2.3.0",
        "flask-sqlalchemy>=3.0.0",
        "requests>=2.28.0",
        "pandas>=1.5.0",
        "apscheduler>=3.10.0",
        "keyring>=25.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "skills-monitor=skills_monitor_cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "skills": ["**/SKILL.md", "**/_meta.json", "**/skill.json", "**/*.py"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Testing",
    ],
)
