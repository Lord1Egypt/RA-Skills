"""
Web Search Skill Setup

Installation with uv (recommended):
    uv pip install -e .

Installation with pip:
    pip install -e .
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="web-search-skill",
    version="1.2.0",
    author="yejinlei",
    author_email="",
    description="Web Search Skill - Multi-engine web search without API keys",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yejinlei/web-search-skill",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    keywords="web search baidu bing duckduckgo internet",
    project_urls={
        "Bug Reports": "https://github.com/yejinlei/web-search-skill/issues",
        "Source": "https://github.com/yejinlei/web-search-skill",
    },
)
