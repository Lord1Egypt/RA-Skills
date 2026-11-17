from pathlib import Path

from setuptools import find_packages, setup


setup(
    name="qshare",
    version="0.4.3",
    description="Share local files via CNB uploads by default, or an optional TryCloudflare tunnel.",
    long_description=Path(__file__).with_name("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="steinvenic",
    author_email="761701732@qq.com",
    url="https://github.com/steinvenic/qshare",
    project_urls={
        "Documentation": "https://github.com/steinvenic/qshare/blob/main/README.md",
        "Skill": "https://github.com/steinvenic/qshare/blob/main/SKILL.md",
    },
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=[
        "qrcode==7.3.1; python_version < '3.7'",
        "qrcode>=7.4.2,<8; python_version >= '3.7' and python_version < '3.9'",
        "qrcode>=8,<9; python_version >= '3.9'",
    ],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["qshare=qshare.cli:main"]},
)
