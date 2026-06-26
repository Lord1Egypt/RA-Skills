# qgdata 发布到 PyPI 指南

本文档用于指导 `qgdata` 的一次完整发布流程，包含本地检查、构建、上传与验证。

## 1. 发布前准备

- 确认版本号：`qgdata/__init__.py` 中的 `__version__`
- 确认变更记录（建议维护 `CHANGELOG.md`）
- 确认 `README.md`、`LICENSE`、`pyproject.toml` 元数据正确
- 清理历史构建产物：`dist/`、`build/`、`*.egg-info/`（如有）

## 2. 本地检查

在项目根目录执行：

```bash
python -m pip install --upgrade pip build twine
python -m pip install -e .
python -m twine --version
```

可选快速导入检查：

```bash
python -c "import qgdata; print(qgdata.__version__)"
```

## 3. 构建发行包

```bash
rm -rf dist build *.egg-info
python -m build
python -m twine check dist/*
```

成功后会生成（示例）：

- `dist/qgdata-<version>-py3-none-any.whl`
- `dist/qgdata-<version>.tar.gz`

## 4. 先发布到 TestPyPI（推荐）

```bash
python -m twine upload --repository testpypi dist/*
```

安装验证：

```bash
python -m pip install -i https://test.pypi.org/simple/ qgdata==<version>
```

## 5. 正式发布到 PyPI

```bash
python -m twine upload dist/*
```

建议使用 API Token 登录：

- 用户名固定为：`__token__`
- 密码为 PyPI 或 TestPyPI 生成的 token

## 6. 发布后验证

```bash
python -m pip install --upgrade qgdata
python -c "import qgdata as qg; print(qg.__version__)"
```

并做一次最小功能验证：

```python
import qgdata as qg

qg.set_token("demo-token")
pro = qg.pro_api()
# pro.list_apis() 或 pro.query(...) 按实际服务验证
```

## 7. 常见问题

- `File already exists`：同版本不能重复上传到 PyPI，需要升级版本号后重新发布
- `twine check` 失败：优先检查 `README.md` 格式和 `pyproject.toml` 元数据
- 安装后导入失败：确认发布包中包含 `qgdata` 包目录
