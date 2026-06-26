from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="wps-office-automation",
    version="1.1.0",
    author="ClawHub Developer",
    author_email="dev@clawhub.com",
    description="WPS Office automation skill for document, spreadsheet, presentation and PDF processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/clawhub/office-tool",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.md", "*.txt"],
    },
    entry_points={
        "console_scripts": [
            "wps-office-skill=main:main",
        ],
    },
)