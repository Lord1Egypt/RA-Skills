# Obsidian Knowledge Base Skill

## 概述

这是一个与Obsidian知识库交互的Python技能，支持创建笔记、语义搜索、笔记管理等功能。

## 功能特性

- ✅ 创建笔记并自动添加身份标识
- ✅ 语义搜索笔记（基于向量相似度）
- ✅ 列出和管理笔记
- ✅ 获取知识库统计信息
- ✅ 重建索引
- ✅ 标准化工作经验保存

## 快速开始

### 1. 基础使用

```python
from obsidian_kb import ObsidianKB, create_note, search_notes, save_experience

# 初始化知识库
kb = ObsidianKB()

# 检查服务状态
health = kb.health_check()
print(f"服务状态: {health}")

# 创建笔记
result = create_note(
    title="Python编程技巧",
    content="# Python技巧\n\n列表推导式很方便...",
    tags=["编程", "Python"],
    folder="project_lessons"
)

# 搜索笔记
results = search_notes("Python编程", limit=5)
print(f"搜索结果: {results}")
```

### 2. 保存工作经验

```python
# 保存工作经验到指定分类
result = save_experience(
    title="调试VPN连接问题",
    content="今天遇到VPN连接问题...",
    category="运维经验",
    tags=["VPN", "网络", "调试"]
)
```

## API接口

### 服务信息
- **API地址**: `http://192.168.18.15:5000`
- **嵌入模型**: qwen3-embedding:8b
- **笔记库路径**: `/mnt/share2win/openclaw_datas/obsidian_db/`

### 主要方法

#### ObsidianKB类
- `health_check()` - 检查服务健康状态
- `create_note(title, content, tags, folder)` - 创建笔记
- `search_notes(query, limit)` - 语义搜索笔记
- `get_note(file_path)` - 获取单个笔记
- `list_notes(folder)` - 列出所有笔记
- `get_stats()` - 获取统计信息
- `rebuild_index()` - 重建索引
- `save_experience(title, content, category, tags)` - 保存工作经验

#### 便捷函数
- `check_health()` - 检查健康状态
- `create_note()` - 创建笔记
- `search_notes()` - 搜索笔记
- `save_experience()` - 保存工作经验

## 知识库目录规范

```
obsidian_db/
├── claw_memory/       ← Claw 长期记忆
├── claw_daily/        ← 每日工作日志
├── wf_overview/       ← 执行规范总览
├── wf_composite/      ← 拼图工作流文档
├── wf_i2v/            ← I2V 视频生成工作流
├── wf_audio/          ← 音频工作流
├── openclaw_ops/      ← OpenClaw 运维经验
├── project_lessons/   ← 项目经验教训
├── Templates/         ← Obsidian 笔记模板
└── _system/           ← 系统文件
```

## 身份标识规范

所有笔记自动添加YAML frontmatter：

```yaml
---
host: 4090服务器 (192.168.18.15)
agent: nanobot-001
created: 2026-03-28
updated: 2026-03-28
---
```

## 使用示例

参见 `usage_examples.py` 文件，包含完整的使用示例。

## 注意事项

- 笔记保存后会自动索引
- 语义搜索相似度>0.5通常表示高度相关
- 必须在对应子目录创建笔记，不能在根目录
- 文件命名用中文，目录命名用英文

## 兼容性

- Python 3.6+
- requests库
- 服务端需运行Obsidian向量搜索API