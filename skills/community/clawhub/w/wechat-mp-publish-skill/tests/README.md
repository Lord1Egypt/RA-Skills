# 🧪 测试指南

## 目录结构

```
tests/
├── __init__.py              # 测试包初始化
├── test_api.py              # API 连接测试
├── test_search.py           # 搜索功能测试
├── test_multi_images.py     # 多图生成测试
├── test_long_article.py     # 长文章测试
├── test_pam_report.py       # PAM 报告测试
├── test_realtime_search.py  # 实时搜索测试
└── test_debug.py            # 调试测试
```

## 运行测试

### 方式 1：直接运行单个测试

```bash
cd /Users/brucesong/.openclaw/workspace/skills/wechat-mp-publish

# 测试 API 连接
venv/bin/python tests/test_api.py

# 测试搜索功能
venv/bin/python tests/test_search.py

# 测试多图生成
venv/bin/python tests/test_multi_images.py
```

### 方式 2：使用 pytest（推荐）

```bash
# 安装 pytest
venv/bin/pip install pytest

# 运行所有测试
venv/bin/python -m pytest tests/ -v

# 运行特定测试
venv/bin/python -m pytest tests/test_api.py -v

# 运行带关键字的测试
venv/bin/python -m pytest tests/ -k "image" -v
```

### 方式 3：运行测试并生成报告

```bash
# 生成 HTML 报告
venv/bin/python -m pytest tests/ --html=report.html

# 生成覆盖率报告
venv/bin/pip install pytest-cov
venv/bin/python -m pytest tests/ --cov=. --cov-report=html
```

## 测试分类

### 单元测试
- `test_api.py` - 微信 API 连接测试
- `test_search.py` - 搜索功能测试

### 集成测试
- `test_multi_images.py` - 多图生成集成测试
- `test_long_article.py` - 长文章发布测试

### 功能测试
- `test_pam_report.py` - PAM 报告生成测试
- `test_realtime_search.py` - 实时搜索测试

## 添加新测试

在 `tests/` 目录下创建新的测试文件，命名格式：`test_<feature>.py`

示例：
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新功能
"""

def test_new_feature():
    """测试新功能"""
    # 测试代码
    assert True

if __name__ == "__main__":
    test_new_feature()
    print("✅ 测试通过")
```

## 测试注意事项

1. **API Key 配置**
   - 确保 `config.yaml` 已正确配置
   - 或使用环境变量

2. **网络要求**
   - 部分测试需要网络连接
   - 确保可以访问微信 API

3. **测试数据**
   - 测试文件不应包含真实敏感数据
   - 使用 mock 或测试数据

4. **清理工作**
   - 测试后清理生成的文件
   - 避免影响其他测试

## 常见问题

### Q: 测试失败怎么办？
A: 查看错误信息，检查配置是否正确，网络连接是否正常

### Q: 如何跳过某些测试？
A: 使用 pytest 的 `-k` 参数或 `@pytest.mark.skip` 装饰器

### Q: 如何调试测试？
A: 使用 `pdb` 或在 IDE 中设置断点

---

_最后更新：2026-03-10_
