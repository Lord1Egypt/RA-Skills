#!/usr/bin/env python3
"""
生成标准 Python 项目结构
"""

import os
import sys
from pathlib import Path

TEMPLATES = {
    "standard": {
        "dirs": ["src/{name}", "tests", "docs", "scripts", "data/raw", "data/processed"],
        "files": [
            "README.md",
            "pyproject.toml",
            ".gitignore",
            ".pre-commit-config.yaml",
            "src/{name}/__init__.py",
            "src/{name}/main.py",
            "src/{name}/config.py",
            "tests/__init__.py",
            "tests/conftest.py",
        ]
    },
    "minimal": {
        "dirs": ["{name}", "tests"],
        "files": [
            "README.md",
            "requirements.txt",
            "{name}/__init__.py",
            "{name}/main.py",
            "tests/test_main.py",
        ]
    },
    "package": {
        "dirs": ["src/{name}", "tests/{name}", "docs"],
        "files": [
            "README.md",
            "pyproject.toml",
            "LICENSE",
            ".gitignore",
            "src/{name}/__init__.py",
            "src/{name}/core.py",
            "tests/{name}/__init__.py",
            "tests/{name}/test_core.py",
        ]
    }
}

GITIGNORE_TEMPLATE = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
venv/
env/
.env

# Distribution / packaging
dist/
build/
*.egg-info/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/

# Data
data/raw/*
!data/raw/.gitkeep
"""

PYPROJECT_TEMPLATE = """[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{name}"
version = "0.1.0"
description = "TODO: Add description"
requires-python = ">=3.9"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=23.0",
    "ruff>=0.1.0",
    "mypy>=1.0",
]

[tool.black]
line-length = 88
target-version = ["py39"]

[tool.ruff]
line-length = 88
select = ["E", "F", "I", "N", "W"]

[tool.mypy]
python_version = "3.9"
warn_return_any = true
ignore_missing_imports = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short --cov=src"
"""

README_TEMPLATE = """# {name}

TODO: Add project description.

## Installation

```bash
pip install -e ".[dev]"
```

## Usage

```python
from {name} import main
main()
```

## Development

```bash
# Run tests
pytest

# Run linting
ruff check src
black --check src

# Type checking
mypy src
```
"""

INIT_TEMPLATE = """\"\"\"{name} - TODO: Add module description\"\"\"

__version__ = "0.1.0"
"""

MAIN_TEMPLATE = """#!/usr/bin/env python3
\"\"\"Main entry point\"\"\"

def main():
    print("Hello from {name}!")

if __name__ == "__main__":
    main()
"""

CONFTES_TEMPLATE = """\"\"\"Pytest configuration and shared fixtures\"\"\"

import pytest
"""

PRECOMMIT_TEMPLATE = """repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
  
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix]
  
  - repo: https://github.com/psf/black
    rev: 23.12.0
    hooks:
      - id: black
"""


def generate_structure(project_name: str, output_path: str, template: str = "standard", force: bool = False):
    """生成项目结构"""
    output = Path(output_path)
    
    if template not in TEMPLATES:
        print(f"❌ 未知模板：{template}")
        print(f"可用模板：{', '.join(TEMPLATES.keys())}")
        return False
    
    tmpl = TEMPLATES[template]
    
    # 安全检查：输出目录已存在且非空
    if output.exists() and any(output.iterdir()):
        if not force:
            print(f"⚠️  警告：输出目录已存在且非空：{output}")
            print("使用 --force 强制覆盖，或指定其他路径")
            return False
        print(f"⚠️  强制模式：将覆盖现有文件\n")
    
    print(f"📦 生成项目结构：{project_name}")
    print(f"📁 输出路径：{output.absolute()}")
    print(f"🎨 模板：{template}\n")
    
    # 创建目录
    for dir_path in tmpl["dirs"]:
        dir_path = dir_path.format(name=project_name)
        full_path = output / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ 创建目录：{dir_path}")
    
    # 创建文件
    file_templates = {
        "README.md": README_TEMPLATE,
        "pyproject.toml": PYPROJECT_TEMPLATE,
        ".gitignore": GITIGNORE_TEMPLATE,
        ".pre-commit-config.yaml": PRECOMMIT_TEMPLATE,
        "__init__.py": INIT_TEMPLATE,
        "main.py": MAIN_TEMPLATE,
        "conftest.py": CONFTES_TEMPLATE,
    }
    
    for file_path in tmpl["files"]:
        file_path = file_path.format(name=project_name)
        full_path = output / file_path
        
        # 确定文件内容模板
        content_tmpl = ""
        for key in file_templates:
            if file_path.endswith(key):
                content_tmpl = file_templates[key]
                break
        
        if content_tmpl:
            content = content_tmpl.format(name=project_name)
        else:
            content = ""
        
        full_path.write_text(content, encoding="utf-8")
        print(f"✅ 创建文件：{file_path}")
    
    print(f"\n🎉 项目结构生成完成!")
    print(f"\n下一步:")
    print(f"  1. cd {output / project_name}")
    print(f"  2. git init")
    print(f"  3. pip install -e '.[dev]'")
    print(f"  4. pre-commit install")
    
    return True


def main():
    if len(sys.argv) < 3:
        print("用法：python generate_structure.py <项目名称> <输出路径> [模板] [--force]")
        print("模板：standard, minimal, package")
        print("\n选项:")
        print("  --force    强制覆盖已存在的目录")
        sys.exit(1)
    
    project_name = sys.argv[1]
    output_path = sys.argv[2]
    template = "standard"
    force = False
    
    for arg in sys.argv[3:]:
        if arg in TEMPLATES:
            template = arg
        elif arg == "--force":
            force = True
    
    success = generate_structure(project_name, output_path, template, force)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
