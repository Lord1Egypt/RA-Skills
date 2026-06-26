# 向量记忆自我进化系统 v2.0

基于 BGE 向量模型和 Chroma 向量库的智能记忆系统，实现 AI 从错误和纠正中自动学习。

## 快速开始

```bash
# 1. 进入插件目录
cd ~/.openclaw/workspace/skills/vector-memory-self-evolution

# 2. 查看文档
cat SKILL.md

# 3. 测试记忆捕获
python3 memory_api.py

# 4. 测试执行前检查
python3 check_before_execute.py "npm install xxx"

# 5. 测试冲突检测
python3 memory_conflict_check.py
```

## 核心功能

### 1. 记忆捕获

```python
from memory_api import capture_error, capture_correction, capture_practice

# 捕获错误
capture_error("npm install", "permission denied", "全局安装", "使用 sudo")

# 捕获纠正
capture_correction("代码风格", "双引号", "单引号", "项目规范")

# 捕获最佳实践
capture_practice("高效安装", "pip install -e .", "可编辑模式", "Python开发")
```

### 2. 语义检索

```python
from memory_api import search

# 语义搜索
results = search("如何高效安装 Python 包", n_results=5)
print(results)
```

### 3. 执行前检查

```python
from check_before_execute import check_before_execute

# 执行命令前检查
check_before_execute("npm install xxx")
```

### 4. 冲突检测

```python
from memory_conflict_check import check_conflicts, log_conflict

# 检测冲突
conflicts = check_conflicts("应该使用双引号")
if conflicts:
    log_conflict(conflicts[0])
```

## 文件说明

| 文件 | 说明 |
|------|------|
| SKILL.md | 完整插件文档 |
| README.md | 本文件 |
| memory_api.py | 记忆操作 API |
| check_before_execute.py | 执行前检查 |
| memory_conflict_check.py | 冲突检测 |

## 依赖

- BGE-small-zh (向量模型)
- ChromaDB (向量库)
- sentence-transformers (文本编码)

## 系统要求

- Python 3.8+
- 至少 4GB RAM
- 磁盘空间至少 2GB (用于向量库)

## 集成到 OpenClaw

在 openclaw.json 中配置：

```json
{
  "plugins": {
    "vector-memory-self-evolution": {
      "enabled": true,
      "autoCapture": true
    }
  }
}
```

## 故障排查

### BGE 服务未运行

```bash
cd ~/.openclaw/workspace
./scripts/start_bge_service.sh
```

### 向量库不存在

```bash
cd ~/.openclaw/workspace
python3 scripts/memory_vectorize.py
```

## 更多信息

完整文档请查看 SKILL.md

---

**版本**: 2.0.0  
**创建时间**: 2026-03-29