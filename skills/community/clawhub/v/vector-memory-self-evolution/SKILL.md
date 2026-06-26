---
name: vector-memory-self-evolution
description: "向量记忆自我进化系统 - 结合 BGE 向量模型、Chroma 向量库、四层记忆架构，实现自动错误捕获、用户纠正学习、最佳实践积累、语义检索的自我进化能力。"
version: 2.1.1
author: 凌凌柒
changelog: "2.1.1 - 安全修复：移除 HF_ENDPOINT 网络重定向、补全缺失脚本（setup_memory_system.sh、start_bge_service.sh）"
---

# 向量记忆自我进化系统

基于 BGE-small-zh 向量模型和 Chroma 向量库的智能记忆系统，实现 AI 从错误和纠正中自动学习，越用越聪明。

## 核心特性

✅ **四层记忆架构**：L1 工作记忆 → L2 瑭期记忆 → L3 长期归档 → L4 向量库
✅ **自动捕获**：错误、纠正、最佳实践、事件自动记录
✅ **语义检索**：基于 BGE 的语义相似度搜索
✅ **智能流转**：自动压缩、归档、向量化
✅ **冲突检测**：新旧记忆冲突时主动告警
✅ **规则固化**：验证3次有效后自动写入 SOUL.md
✅ **代码安全扫描**：检测危险函数、硬编码敏感信息
✅ **敏感数据脱敏**：自动脱敏 API 密钥、密码等
✅ **完整进化流程**：记忆学习、聊天记录分析、完整进化报表、下次进化计划

## 🛡️ 安全说明

本插件已通过安全审计：
- ✅ 无 eval()、exec() 危险函数调用
- ✅ 无 os.system() 调用
- ✅ 无 shell=True 注入风险
- ✅ 移除了 HF_ENDPOINT 网络重定向
- ✅ 所有敏感数据自动脱敏
- ✅ 所有脚本已过安全审查

## 系统架构

```
输入层（自动捕获）
  ├─ 命令失败 → memory/errors/
  ├─ 用户纠正 → memory/corrections/
  ├─ 最佳实践 → memory/practices/
  └─ 重要事件 → memory/events/
      ↓
L1 工作记忆（当前会话）
  ├─ 临时上下文
  └─ 未验证信息
      ↓ 自动压缩（消息>10条）
L2 短期记忆（30天，memory/）
  ├─ 已验证信息
  └─ 按日期/主题分类
      ↓ 自动归档（>30天）
L3 长期归档（永久，memory_archive/）
  ├─ 按月/年分类
  └─ archive_index.json
      ↓ 自动向量化
L4 向量库（BGE+Chroma，vector_db/）
  ├─ recent_30d (权重0.7)
  ├─ medium_90d (权重0.2)
  └─ archive (权重0.1)
      ↓ 语义检索
输出层（应用记忆）
  ├─ 执行前检查（避免重复错误）
  ├─ memory_search（语义检索）
  └─ 规则应用（SOUL.md固化）
```

## 安装

### 方法一：一键安装（推荐）

```bash
# 1. 创建目录结构
cd ~/.openclaw/workspace
bash setup_memory_system.sh

# 2. 启动 BGE 服务
bash scripts/start_bge_service.sh
```

### 方法二：手动安装

```bash
# 1. 创建目录结构
mkdir -p ~/.openclaw/workspace/memory/{errors,corrections,practices,events,gaps}
mkdir -p ~/.openclaw/workspace/memory_archive
mkdir -p ~/.openclaw/workspace/vector_db/memories

# 2. 安装依赖
pip3 install chromadb sentence-transformers flask

# 3. 启动 BGE 服务
bash ~/.openclaw/start_bge_service.sh
```

## 核心脚本

### 记忆管理

| 脚本 | 功能 |
|------|------|
| `memory_api.py` | 记忆捕获、搜索 API |
| `memory_capture.py` | 记忆捕获脚本 |
| `memory_compress.py` | 记忆压缩脚本 |
| `memory_archive.py` | 记忆归档脚本 |
| `memory_vectorize.py` | 记忆向量化脚本 |
| `memory_conflict_check.py` | 记忆冲突检测 |

### 安全和进化

| 脚本 | 功能 |
|------|------|
| `redact_tool.py` | 敏感数据脱敏工具 |
| `code_security_scan.py` | 代码安全扫描器 |
| `evolution_trigger.py` | 进化触发器 |
| `check_before_execute.py` | 执行前检查 |

### 工具脚本

| 脚本 | 功能 |
|------|------|
| `quick_search.py` | 快速语义搜索 |
| `test_semantic_search.py` | 测试语义搜索 |
| `test_vector_db.py` | 测试向量数据库 |
| `setup_memory_system.sh` | 一键安装脚本 |
| `start_bge_service.sh` | BGE 服务启动脚本 |

## 使用方法

### 1. 捕获记忆

```python3
from memory_api import capture

# 捕获错误
capture(
    typ="error",
    title="npm install 权限不足",
    content="需要 sudo 或使用本地安装",
    context="全局安装依赖"
)
```

### 2. 语义检索

```python
from memory_api import search

# 语义搜索
results = search(
    query="如何高效安装 Python 包",
    n_results=5
)
```

### 3. 执行前检查

```python
from check_before_execute import check_before_execute

# 执行前检查
check_before_execute("npm install -g xxx")
# 输出: ⚠️ 历史显示需要 sudo，建议: sudo npm install
```

### 4. 触发进化

```bash
# 完整进化流程
python3 ~/openclaw/workspace/scripts/evolution_trigger.py
```

### 5. 代码安全扫描

```bash
python3 ~/.openclaw/workspace/scripts/code_security_scan.py
```

## 文件结构

```
~/.openclaw/workspace/
├── MEMORY.md                      # L1 核心记忆
├── SOUL.md                        # 固化规则
├── README.md                      # 使用文档
├── setup_memory_system.sh          # 一键安装脚本 ✅ 新增
├── memory/                        # L2 短期记忆 (30天)
│   ├── errors/                    # 错误记录
│   ├── corrections/               # 用户纠正
│   ├── practices/                 # 最佳实践
│   ├── events/                    # 重要事件
│   ├── gaps/                      # 知识盲区
│   └── YYYY-MM-DD.md              # 日期记录
├── memory_archive/                # L3 长期归档
│   ├── 2026-03/
│   ├── 2026-02/
│   └── archive_index.json
├── vector_db/                     # L4 向量库
│   ├── chroma.sqlite3
│   └── memories/
├── scripts/                       # 脚本目录
│   ├── memory_capture.py
│   ├── memory_compress.py
│   ├── memory_archive.py
│   ├── memory_vectorize.py
│   ├── memory_conflict_check.py
│   ├── code_security_scan.py       # 代码安全扫描 ✅ 新增
│   ├── evolution_trigger.py        # 进化触发器 ✅ 新增
│   ├── start_bge_service.sh        # BGE 服务启动 ✅ 新增
│   └── redact_tool.py              # 脱敏工具 ✅ 新增
└── skills/
    └── vector-memory-self-evolution/  # 插件本身
        ├── SKILL.md
        ├── memory_api.py
        ├── check_before_execute.py
        ├── memory_conflict_check.py
        ├── quick_search.py
        ├── redact_tool.py
        └── test_*.py
```

## 系统要求

- Python 3.x
- ChromaDB
- sentence-transformers
- Flask (用于 BGE 服务)

## 定时任务（Cron）

```bash
# 每天凌晨 3:00 自动归档
0 3 * * * cd ~/.openclaw/workspace && python3 scripts/memory_archive.py

# 每周日凌晨 2:00 向量化新记忆
0 2 * * 0 cd ~/.openclaw/workspace && python3 scripts/memory_vectorize.py

# 每小时检查记忆冲突
0 * * * * cd ~/.openclaw/workspace && python3 scripts/memory_conflict_check.py
```

## 使用场景

### 场景 1：命令失败后的自动学习

```python
# AI 执行命令失败后自动记录
capture(
    typ="error",
    title="npm install 权限不足",
    content="permission denied",
    context="全局安装依赖",
    suggested_fix="使用 sudo 或本地安装"
)

# 下次执行前自动检查
check_before_execute("npm install")
# 输出: ⚠️ 历史显示需要 sudo，建议: sudo npm install
```

### 场景 2：用户纠正后的规则固化

```python
# 用户说"不对，要用单引号"
capture(
    typ="correction",
    title="代码风格",
    wrong="使用双引号",
    correct="项目要求单引号",
    context="AGENTS.md"
)

# 验证3次有效后自动写入 SOUL.md
if validate_count >= 3:
    promote_to_soul("代码风格: 使用单引号")
```

### 场景 3：语义检索历史经验

```python
# 用户询问"如何高效安装 Python 包"
results = search(
    query="高效安装 Python 包",
    n_results=5
)
# 返回: pip install -e . 更高效（来自最佳实践库）
```

## 注意事项

1. **BGE 服务必须运行**：确保 BGE Embedding 服务在 11434 端口运行
2. **定期备份**：记忆文件定期备份到 git
3. **敏感信息脱敏**：记录前自动脱敏密码/API Key
4. **定期清理**：90天以上记忆归档，避免向量库过大
5. **冲突解决**：新旧记忆冲突时主动询问用户
6. **安全第一**：所有代码已通过安全审计

## 故障排查

### BGE 服务无法启动

```bash
# 检查端口占用
lsof -ti:11434 | xargs kill -9

# 重新启动
bash ~/.openclaw/start_bge_service.sh
```

### 向量化失败

```bash
# 检查依赖
pip list | grep chromadb

# 重新安装
pip3 install --user --break-system-packages chromadb
```

### 记忆检索无结果

```bash
# 检查向量库
ls -lh vector_db/

# 手动向量化
python3 scripts/memory_vectorize.py
```

## 更新日志

### v2.1.1 (2026-03-29)
- ✅ **安全修复**
  - 移除所有 HF_ENDPOINT 网络重定向
  - 移除所有 eval、exec、shell=True 危险调用
  - 添加代码安全扫描功能
- ✅ **补全缺失脚本**
  - 新增 setup_memory_system.sh 一键安装脚本
  - 新增 start_bge_service.sh BGE 服务启动脚本
- ✅ **增强功能**
  - 新增敏感数据脱敏功能
  - 新增完整进化流程
  - 新增进化报表和下次计划
  - 新增聊天记录分析

### v2.1.0 (2026-03-29)
- ✅ 整合 BGE 向量模型
- ✅ 引入 Chroma 向量库
- ✅ 实现四层记忆架构
- ✅ 自动压缩、归档、向量化
- ✅ 冲突检测和规则固化

---

**创建时间**：2026-03-29
**版本**：2.1.1
**作者**：凌凌柒
**依赖**：BGE-small-zh, ChromaDB, sentence-transformers, Flask