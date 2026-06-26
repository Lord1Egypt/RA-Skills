# Smart Todo - WorkBuddy 智能代办管理 Skill

> 一个让 AI 助手帮你管代办的 Skill。自动检测重复、捕获工作上下文、跟踪任务状态。

## 功能特性

| 功能 | 说明 |
|------|------|
| 优先级管理 | P0(最高)、P1(普通)，P0 超时自动提醒 |
| 状态跟踪 | 未开始 → 进行中 → 已完成/暂停/终止，完整生命周期 |
| 智能重复检测 | 名称相似度≥70% 或 描述相似度≥80% 即触发警告（OR 逻辑） |
| 上下文保存 | 自动捕获工作文件、对话历史、任务状态 |
| 工作中断检测 | 检测任务切换，自动保存当前进度 |
| 自动归档 | 已完成/终止的任务自动转入归档 |

## 安装

### 方式一：通过 WorkBuddy 安装（推荐）

```bash
# 在 WorkBuddy 中执行
skills add https://github.com/13770626440/smart-todo
```

### 方式二：手动安装

```bash
# 克隆仓库
git clone https://github.com/13770626440/smart-todo.git

# 复制到 WorkBuddy skills 目录
cp -r smart-todo ~/.workbuddy/skills/
```

## 安装后配置

编辑 `assets/config.json`，修改 `storage_path` 为你的代办存储路径：

```json
{
  "storage_path": "D:\\my-todos",
  ...
}
```

## 使用方法

安装后，在 WorkBuddy 中直接用自然语言操作：

```
加入代办：修复登录bug，用户反馈登录经常超时
```
```
查看代办
```
```
完成 T001
```
```
先放下这个  （自动触发中断检测）
```

## 触发关键词

- **添加代办**："加入代办"、"创建代办"、"记一下"、"添加到待办"
- **查看代办**："查看代办"、"我的待办"、"待办列表"
- **更新代办**："完成代办"、"更新代办"、"修改代办"
- **工作中断**："先放下"、"换个事"、"等一下"、"先做别的"

## 配置选项

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `storage_path` | 代办文件存储路径 | `~/smart-todo-data` |
| `notification_interval_minutes` | 提醒间隔（分钟） | 20 |
| `similarity_name_threshold` | 名称重复检测阈值 | 0.7 |
| `similarity_desc_threshold` | 描述重复检测阈值 | 0.8 |
| `max_name_length` | 简略名称最大长度 | 10 |
| `context_lines_from_history` | 保留对话历史条数 | 10 |
| `p0_alert_threshold_hours` | P0 超时提醒阈值（小时） | 1 |

## 重复检测逻辑

采用 OR 组合策略，任一维度触发即报警：

```
名称相似度 >= 70%  ─┐
                    ├─ 任一满足 → 触发重复警告
描述相似度 >= 80%  ─┘
```

> 使用 `difflib.SequenceMatcher` 进行模糊匹配，对中文做了针对性优化。

## 技术栈

- Python 3（标准库，无第三方依赖）
- Markdown 格式存储
- WorkBuddy Skill 架构

## 文件结构

```
smart-todo/
├── SKILL.md              # Skill 定义文件
├── README.md             # 本文件
├── LICENSE               # MIT 许可证
├── scripts/
│   ├── todo_manager.py   # 核心 CRUD + 重复检测
│   └── context_capture.py # 上下文捕获
├── assets/
│   └── config.json       # 配置文件
└── references/
    └── todo_template.md  # 模板参考
```

## 支持这个项目

如果觉得这个 Skill 对你有帮助，欢迎请我喝杯咖啡：

- [爱发电](https://afdian.net/) — 你的用户名
- 微信赞赏码 — 见下方

<p align="center">
<img src="assets/sponsor-wechat.jpg" width="200" alt="微信赞赏码">
</p>

## 许可证

[MIT License](LICENSE)

## 更新日志

### v1.0.0 (2026-03-31)
- 基础 CRUD 功能
- 重复检测（名称+描述双维度 OR 逻辑）
- 上下文捕获
- 工作中断检测
- 自动归档
