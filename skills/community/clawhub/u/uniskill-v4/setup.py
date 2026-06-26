#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UniSkill V4 Setup Script
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="uniskill-v4",
    version="4.0.0",
    author="Timo Cao",
    author_email="miscdd@163.com",
    description="Minimalist AI Agent Framework - The 3% Solution",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/timo/uniskill-v4",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "typing-extensions>=4.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    keywords="ai agent framework minimal socratic debate",
    project_urls={
        "Bug Reports": "https://github.com/timo/uniskill-v4/issues",
        "Source": "https://github.com/timo/uniskill-v4",
        "Documentation": "https://github.com/timo/uniskill-v4#readme",
    },
)