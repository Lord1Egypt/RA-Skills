# Python 项目架构最佳实践

## 标准目录结构

```
project-name/
├── pyproject.toml          # 项目配置和依赖（推荐）
├── requirements.txt        # 或传统依赖文件
├── README.md
├── LICENSE
├── .gitignore
├── .pre-commit-config.yaml
│
├── src/                    # 源代码目录
│   └── package_name/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── module_a/
│       │   ├── __init__.py
│       │   └── core.py
│       └── module_b/
│           ├── __init__.py
│           └── utils.py
│
├── tests/                  # 测试目录
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_module_a.py
│   └── test_module_b.py
│
├── docs/                   # 文档
│   ├── index.md
│   └── api.md
│
├── scripts/                # 辅助脚本
│   ├── setup.sh
│   └── deploy.sh
│
└── data/                   # 数据文件（可选）
    ├── raw/
    └── processed/
```

## 依赖管理

### 现代方式 (pyproject.toml)
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "your-package"
version = "0.1.0"
dependencies = [
    "requests>=2.28.0",
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "black>=23.0",
    "ruff>=0.1.0",
    "mypy>=1.0",
]
```

### 传统方式 (requirements.txt)
```
# requirements.txt
requests==2.31.0
pydantic==2.5.0

# requirements-dev.txt
pytest==7.4.0
black==23.12.0
ruff==0.1.6
```

## 代码组织原则

### 1. 单一职责
每个模块/类只负责一个功能领域。

### 2. 依赖倒置
高层模块不依赖低层模块，都依赖抽象。

### 3. 配置分离
```python
# config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str
    api_key: str
    debug: bool = False
    
    class Config:
        env_file = ".env"
```

### 4. 导入规范
```python
# 标准库
import os
import sys

# 第三方
import requests
from pydantic import BaseModel

# 本地
from .config import Settings
from ..utils import helper
```

## 测试架构

### pytest 配置 (pyproject.toml)
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-v --tb=short --cov=src"
```

### 测试目录结构
```
tests/
├── unit/               # 单元测试
│   ├── test_module_a.py
│   └── test_module_b.py
├── integration/        # 集成测试
│   └── test_api.py
└── conftest.py         # 共享 fixture
```

## Linting 配置

### Ruff (pyproject.toml)
```toml
[tool.ruff]
line-length = 88
target-version = "py39"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]
```

### Black (pyproject.toml)
```toml
[tool.black]
line-length = 88
target-version = ["py39"]
```

### Mypy (pyproject.toml)
```toml
[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
ignore_missing_imports = true
```

## Pre-commit 配置
```yaml
# .pre-commit-config.yaml
repos:
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
```

## CI/CD 模板 (GitHub Actions)
```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11"]
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - run: pip install -e ".[dev]"
      - run: pytest
      - run: ruff check src
      - run: black --check src
```

## 常见问题

### 循环依赖
**问题**: 模块 A 导入 B，B 又导入 A
**解决**: 
- 提取共享代码到独立模块
- 使用依赖注入
- 延迟导入（函数内部 import）

### 配置硬编码
**问题**: API 密钥、数据库 URL 写在代码里
**解决**: 
- 使用环境变量
- `.env` 文件 + python-dotenv
- 配置类集中管理

### 测试覆盖率低
**问题**: 核心逻辑没有测试
**解决**: 
- 优先测试核心业务逻辑
- 使用 pytest-cov 跟踪覆盖率
- CI 中设置覆盖率阈值
