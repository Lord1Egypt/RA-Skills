from setuptools import setup, find_packages

setup(
    name="trading-agents",
    version="1.0.0",
    description="Trading Agent版的多智能体股票诊断系统",
    author="AI Assistant",
    packages=find_packages(),
    install_requires=[
        "agentscope>=0.0.5",
        "tushare>=1.2.89",
        "akshare>=1.12.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "requests>=2.31.0",
        "openai>=1.0.0",
        "fpdf2>=2.8.0",
        "python-dotenv",
    ],
    python_requires=">=3.8",
)
