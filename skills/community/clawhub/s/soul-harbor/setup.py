"""
Setup script for Soul Harbor
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="soul-harbor",
    version="1.0.0",
    description="Stop talking to a robot. Give your OpenClaw agent a soul that truly cares.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="SoulHarbor Team",
    url="https://github.com/openclaw/soul-harbor",
    packages=find_packages(exclude=["tests", "test_*"]),
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    install_requires=[
        # No external dependencies - uses standard library only
        # OpenClaw integration is handled at runtime
    ],
    entry_points={
        "console_scripts": [
            "soulharbor-cron=soulharbor.cron_trigger:main",
        ],
    },
)
