# 覆盖率测试

## pytest-cov

```bash
pip install pytest-cov
```

## 运行覆盖率

```bash
pytest --cov=myapp
pytest --cov=myapp --cov-report=term-missing
pytest --cov=myapp --cov-report=html
pytest --cov=myapp --cov-fail-under=80
pytest --cov=myapp --cov-branch
```

## .coveragerc 配置

```ini
[run]
source = myapp
branch = True
omit =
    */tests/*
    */__init__.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if TYPE_CHECKING:
```

## pyproject.toml 配置

```toml
[tool.coverage.run]
source = ["myapp"]
branch = true
omit = ["*/tests/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
]
```

## 查看 HTML 报告

```bash
pytest --cov=myapp --cov-report=html
open htmlcov/index.html
```
