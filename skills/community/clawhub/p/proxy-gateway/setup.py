from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="proxy-gateway",
    version="0.2.1",
    author="laoke",
    description="One-click internet access for AI agents with automatic crypto payment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/laoke/proxy-gateway",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.31.0",
        "web3>=7.0.0",
        "eth-account>=0.13.0",
    ],
    entry_points={
        "console_scripts": [
            "proxy-gateway=proxy_gateway.cli:main",
        ],
    },
)