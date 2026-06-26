from setuptools import setup, find_packages

setup(
    name="equipment-analyzer-skill",
    version="2.3.0",
    description="设备数据分析 Skill - 完整安全版",
    author="AI Assistant",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "cryptography>=3.4.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
