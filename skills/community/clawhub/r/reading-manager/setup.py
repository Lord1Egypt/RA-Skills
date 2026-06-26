from setuptools import setup, find_packages

setup(
    name="reading-manager",
    version="1.0.0",
    description="个人阅读管理系统 - 记录书籍、跟踪进度、管理笔记",
    author="",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click>=8.0.0",
        "rich>=13.0.0",
        "requests>=2.28.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "reading=reading_cli:main",
        ],
    },
)
