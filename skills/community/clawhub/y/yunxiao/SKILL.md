---
name: yunxiao
description: 云效项目协作操作助手。支持工作项（任务/需求/缺陷）的查询、创建、更新等操作。当用户提到"云效"、"工作项"、"任务管理"、"项目管理"或需要操作 devops.aliyun.com 时触发。
---

# 云效项目协作 API

通过云效 OpenAPI 管理工作项（任务、需求、缺陷等）。

---

## 🤖 AI 决策指南

### 用户意图识别

| 用户说法 | 意图 | 执行动作 |
|----------|------|----------|
| "查看我的任务" / "我有什么工作项" | 查询工作项 | 指定项目后调用 `list_workitems.py` |
| "查看任务详情" | 查询单个工作项 | 调用 `get_workitem.py <id>` |
| "创建一个任务" / "新建工作项" | 创建工作项 | **先确认项目**，再调用 `create_workitem.py` |
| "更新任务" / "修改任务标题" | 更新工作项 | 调用 `update_workitem.py` |
| "完成任务" / "关闭任务" | 更新状态 | 调用 `update_workitem.py --status` |
| "列出所有项目" | 查看项目 | 调用 `list_projects.py` |

### ⚠️ 创建任务时的交互流程

**重要**：创建工作项时，如果用户没有指定项目，必须先询问用户！

1. 用户说："帮我创建一个任务"
2. AI 先查询项目列表：`python3 list_projects.py`
3. AI 展示可选项目，询问用户："要创建在哪个项目？"
4. 用户选择后，再创建任务

**不要**在未确认项目的情况下直接使用默认项目创建！

---

## 📋 命令速查

### 查询项目列表

```bash
python3 ~/.openclaw/workspace/skills/yunxiao/scripts/list_projects.py
```

### 查询工作项详情

```bash
python3 ~/.openclaw/workspace/skills/yunxiao/scripts/get_workitem.py <workitem_id>
```

### 创建工作项

```bash
# 必须指定项目
python3 ~/.openclaw/workspace/skills/yunxiao/scripts/create_workitem.py \
  --subject "任务标题" \
  --project "AI 产研"

# 完整参数
python3 ~/.openclaw/workspace/skills/yunxiao/scripts/create_workitem.py \
  --subject "任务标题" \
  --project "AI 产研" \
  --type "任务" \
  --priority "高" \
  --desc "任务描述"
```

### 更新工作项

```bash
# 修改标题
python3 ~/.openclaw/workspace/skills/yunxiao/scripts/update_workitem.py <id> --subject "新标题"

# 修改描述
python3 ~/.openclaw/workspace/skills/yunxiao/scripts/update_workitem.py <id> --desc "新描述"
```

---

## 📁 脚本说明

| 脚本名 | 用途 |
|--------|------|
| `yunxiao_api.py` | API 基础模块 |
| `list_projects.py` | 查询项目列表 |
| `get_workitem.py` | 查询单个工作项详情 |
| `create_workitem.py` | 创建工作项（需指定项目） |
| `update_workitem.py` | 更新工作项 |
| `list_workitems.py` | 查询工作项列表（需指定项目） |

---

## 🔧 API 端点

**基础 URL**: `https://openapi-rdc.aliyuncs.com`

**认证方式**: 请求头 `x-yunxiao-token`

| 操作 | 方法 | 路径 |
|------|------|------|
| 搜索项目 | POST | `/oapi/v1/projex/organizations/{orgId}/projects:search` |
| 查询详情 | GET | `/oapi/v1/projex/organizations/{orgId}/workitems/{id}` |
| 创建 | POST | `/oapi/v1/projex/organizations/{orgId}/workitems` |
| 更新 | PUT | `/oapi/v1/projex/organizations/{orgId}/workitems/{id}` |

---

## 📝 工作项类型

- **任务** (Task): 开发任务、测试任务等
- **需求** (Req): 产品需求
- **缺陷** (Bug): Bug 修复
- **风险** (Risk): 项目风险

---

## ⚠️ 权限要求

Token 需要以下权限：
- 项目协作 > 项目 > 只读（查询项目列表）
- 项目协作 > 工作项 > 只读（查询）
- 项目协作 > 工作项 > 读写（创建、更新）

---

*最后更新: 2026-03-16*