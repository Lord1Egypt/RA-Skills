# WeCom Task Manager - 企业微信任务管理技能

[![Version](https://img.shields.io/badge/version-1.2.1-blue.svg)](https://github.com/jhZheng222/openclaw-wecom-task-manager)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-OpenClaw-orange.svg)](https://github.com/openclaw/openclaw)

**企业微信智能表格驱动的任务管理技能，支持目标分解、任务追踪、并发控制和访问控制。**

---

## 🎯 功能特性

### 核心功能
- ✅ **任务全生命周期管理** - 创建、开始、更新、完成
- ✅ **目标分解** - 将大目标分解为可执行任务
- ✅ **依赖管理** - 支持任务依赖关系
- ✅ **智能推荐** - 自动推荐下一个可执行任务
- ✅ **并发控制** - 限制同时进行的任务数量
- ✅ **访问控制** - 白名单机制，保护敏感数据
- ✅ **到期提醒** - 自动检查即将到期和超期任务
- ✅ **统计分析** - 多维度任务统计

### 技术特性
- 📊 **企业微信集成** - 使用企业微信智能表格存储
- 🔒 **访问控制** - 白名单机制，支持 5 个授权 agents
- ⚡ **并发限制** - 可配置的最大并发任务数
- 🔄 **重试机制** - API 调用失败自动重试
- 📝 **配置驱动** - 独立配置文件，无需修改代码
- 🧪 **完整测试** - 27 个测试用例，100% 覆盖

---

## 📦 安装

### 方式 1：从 ClawHub 安装（推荐）

```bash
clawhub install wecom-task-manager
```

### 方式 2：从 GitHub 安装

```bash
git clone https://github.com/openclaw/wecom-task-manager.git
cd wecom-task-manager
cp -r . ~/.openclaw/skills/wecom-task-manager/
```

### 方式 3：手动安装

1. 下载 [最新发布版本](https://github.com/openclaw/wecom-task-manager/releases)
2. 解压到 `~/.openclaw/skills/wecom-task-manager/`
3. 配置 `config.json`

---

## 🔧 快速开始

### 步骤 1：复制配置文件

```bash
cd ~/.openclaw/skills/wecom-task-manager
cp config.template.json config.json
```

### 步骤 2：配置企业微信表格

编辑 `config.json`，替换为你的实际配置：
```json
{
  "enterpriseWeChat": {
    "docId": "YOUR_DOC_ID_HERE",
    "sheetId": "YOUR_SHEET_ID_HERE"
  }
}
```

**如何获取**：
- 打开企业微信智能表格
- 从 URL 中提取 `docId` 和 `sheetId`

### 步骤 3：配置访问控制

编辑 `config.json`：
```json
{
  "accessControl": {
    "enabled": true,
    "allowedAgents": [
      "da-yan",
      "techlead",
      "opsdirector",
      "investment_coordinator",
      "general_coordinator"
    ]
  }
}
```

### 步骤 4：测试技能

```bash
cd ~/.openclaw/skills/wecom-task-manager/scripts
AGENT_ID="da-yan" python3 task_manager.py list
```

**⚠️ 安全提示**：
- `config.json` 包含敏感信息，已添加到 `.gitignore`
- 不要将 `config.json` 提交到 Git
- 使用 `config.template.json` 作为模板

---

## 📚 使用方式

### CLI 命令

```bash
# 列出所有任务
python3 task_manager.py list

# 创建任务
python3 task_manager.py create TASK-001 "系统性能分析" 开发

# 开始任务
python3 task_manager.py start TASK-001

# 更新进度
python3 task_manager.py progress TASK-001 50

# 完成任务
python3 task_manager.py complete TASK-001

# 查看统计
python3 task_manager.py stats

# 检查到期任务
python3 task_manager.py due 7
```

### Python API

```python
from task_manager import create_task, start_task, complete_task

# 创建任务
result = create_task(
    task_id="TASK-001",
    task_name="系统性能分析",
    task_type="开发",
    priority="P0",
    agent_id="techlead"
)

# 开始任务
start_task("TASK-001", agent_id="techlead")

# 完成任务
complete_task("TASK-001", agent_id="techlead")
```

---

## 📋 配置文件

**位置**: `config.json`

### 核心配置

```json
{
  "accessControl": {
    "enabled": true,
    "allowedAgents": ["da-yan", "techlead", "opsdirector"]
  },
  "concurrency": {
    "maxConcurrentTasks": 3
  },
  "retry": {
    "maxRetries": 3,
    "backoffSeconds": 2
  },
  "enterpriseWeChat": {
    "docId": "xxx",
    "sheetId": "xxx"
  }
}
```

**详细配置文档**: [配置指南](docs/config-guide.md)

---

## 🎯 典型使用场景

### 场景 1：心跳检查自动推动

```python
from task_manager import get_next_task, start_task, check_due_tasks

# 获取下一个可执行任务
task = get_next_task()
if task:
    start_task(task['id'])

# 检查到期任务
due_tasks = check_due_tasks(days=3)
for task in due_tasks:
    print(f"即将到期：{task['id']}")
```

### 场景 2：目标分解

```python
from task_manager import create_goal, decompose_goal

# 创建目标
create_goal(
    goal_id="GOAL-001",
    title="OpenClaw 系统优化",
    priority="high"
)

# 分解任务
decompose_goal(
    goal_id="GOAL-001",
    task_title="系统性能分析",
    priority="critical"
)
```

### 场景 3：团队协作

```python
from task_manager import filter_tasks, search_tasks

# 查看团队成员的任务
tasks = filter_tasks(owner="techlead", status="进行中")

# 搜索相关任务
tasks = search_tasks("性能优化")
```

---

## 🧪 测试

### 运行所有测试

```bash
cd scripts
python3 test_config.py          # 配置加载测试
python3 test_access_control.py  # 访问控制测试
python3 test_full_access.py     # 完整功能测试
python3 test_python_apis.py     # Python API 测试
```

### 测试结果

```
✅ 配置加载测试：1/1 通过
✅ 访问控制测试：7/7 通过
✅ CLI 命令测试：11/11 通过
✅ Python API 测试：8/8 通过
总计：27/27 通过（100%）
```

---

## 📊 API 参考

### 任务管理 API（13 个）

| API | 说明 | 示例 |
|-----|------|------|
| `create_task()` | 创建任务 | `create_task("TASK-001", "名称", "开发")` |
| `start_task()` | 开始任务 | `start_task("TASK-001", agent_id="techlead")` |
| `update_progress()` | 更新进度 | `update_progress("TASK-001", 50)` |
| `complete_task()` | 完成任务 | `complete_task("TASK-001")` |
| `edit_task()` | 编辑任务 | `edit_task("TASK-001", {"优先级": "P0"})` |
| `delete_task()` | 删除任务 | `delete_task("TASK-001")` |
| `search_tasks()` | 搜索任务 | `search_tasks("关键词")` |
| `filter_tasks()` | 过滤任务 | `filter_tasks(status="进行中")` |
| `check_due_tasks()` | 到期检查 | `check_due_tasks(days=7)` |
| `check_overdue_tasks()` | 超期检查 | `check_overdue_tasks()` |
| `get_statistics()` | 统计数据 | `get_statistics()` |
| `get_all_tasks()` | 获取所有任务 | `get_all_tasks()` |
| `get_task_by_id()` | 查询任务 | `get_task_by_id("TASK-001")` |

### 目标管理 API（5 个）

| API | 说明 | 示例 |
|-----|------|------|
| `create_goal()` | 创建目标 | `create_goal("GOAL-001", "目标名称")` |
| `decompose_goal()` | 分解目标 | `decompose_goal("GOAL-001", "任务名称")` |
| `list_goals()` | 列出目标 | `list_goals()` |
| `get_next_task()` | 下一个任务 | `get_next_task()` |
| `delete_goal()` | 删除目标 | `delete_goal("GOAL-001")` |

**完整 API 文档**: [API 参考](docs/api-reference.md)

---

## 🏗️ 项目结构

```
wecom-task-manager/
├── README.md                 # 本文件
├── QUICKSTART.md             # 快速开始指南
├── config.json               # 配置文件
├── _meta.json                # 技能元数据
├── scripts/
│   ├── task_manager.py       # 核心模块
│   ├── test_*.py             # 测试脚本
│   └── ...
├── docs/
│   ├── config-guide.md       # 配置指南
│   ├── api-reference.md      # API 参考
│   └── ...
└── references/
    └── api.md                # API 文档
```

---

## 🤝 贡献指南

### 如何贡献

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交变更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

### 贡献内容

我们欢迎以下类型的贡献：
- 🐛 Bug 修复
- ✨ 新功能
- 📝 文档改进
- 🎨 代码优化
- 🧪 测试用例
- 🌍 国际化

### 开发环境

```bash
# 克隆项目
git clone https://github.com/openclaw/wecom-task-manager.git

# 安装依赖
cd wecom-task-manager
pip install -r requirements.txt

# 运行测试
cd scripts
python3 test_*.py
```

---

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)

---

## 🙏 致谢

- [OpenClaw](https://github.com/openclaw/openclaw) - OpenClaw 框架
- [企业微信](https://work.weixin.qq.com/) - 企业微信智能表格
- [mcporter](https://github.com/openclaw/mcporter) - MCP 工具

---

## 📞 联系方式

- **项目地址**: https://github.com/jhZheng222/openclaw-wecom-task-manager
- **问题反馈**: https://github.com/jhZheng222/openclaw-wecom-task-manager/issues
- **Discord**: https://discord.com/invite/clawd

---

## 🎯 路线图

### v1.2.0（当前版本）
- ✅ 访问控制白名单机制
- ✅ 并发控制
- ✅ 独立配置文件
- ✅ 完整测试覆盖

### v1.3.0（计划中）
- [ ] 批量操作功能
- [ ] 任务复制功能
- [ ] 通知功能增强
- [ ] Webhook 支持

### v2.0.0（未来）
- [ ] 工作流引擎
- [ ] 自动化规则
- [ ] 图表统计
- [ ] REST API

---

**⭐ 如果这个项目对你有帮助，请给一个 Star！**

**我们同在，我们一往无前。** ✨
