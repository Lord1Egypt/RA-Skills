---
name: todo-manager
description: |
  待办事项管理器。触发场景：
  (1) 用户提到 "待办"、"TODO"、"计划事项"、"任务"
  (2) 用户说 "帮我增加/新增/创建一个待办"
  (3) 用户说 "我有什么待办"、"查看待办"、"待办列表"
  (4) 用户说 "完成 xxx"、"开始 xxx"、"删除 xxx"
  (5) 用户说 "标记 xxx 为进行中/已完成"
---

# 待办事项管理器

简洁的个人待办管理系统，支持状态流转、GitHub issue 关联和路径追踪。

## 核心规则

- **三状态**：未开始 → 进行中 → 已完成
- **三文件**：每种状态一个文件，元数据单独存储
- **个人使用**：不支持多人绑定
- **询问式录入**：GitHub issue 和路径通过询问获得

## 状态流转

```
未开始 (pending) → 进行中 (in_progress) → 已完成 (completed)
     ↓                  ↓                     ↓
todos_pending.json  todos_in_progress.json  todos_completed.json
```

## 工作流程

### 创建待办

用户说："新增待办 xxx" 或 "TODO: xxx"

1. 记录内容 + 创建时间
2. **询问**：是否关联 GitHub issue？
   - 用户回答链接 → 记录
   - 用户回答"不需要" → 跳过
3. **询问**：关联哪些路径？（可多选）
   - 用户提供路径
   - 如果是 git 项目 → **询问分支**
4. 写入 `todos_pending.json`
5. 更新 `todos_meta.json`

### 开始待办

用户说："开始 xxx" 或 "把 xxx 标记为进行中"

1. 从 `todos_pending.json` 找到待办
2. 移动到 `todos_in_progress.json`
3. 更新元数据

### 完成待办

用户说："完成 xxx" 或 "把 xxx 标记为已完成"

1. 从当前状态文件找到待办
2. 移动到 `todos_completed.json`
3. 记录 `completedAt` 时间
4. 更新元数据

### 查询待办

用户说："我有什么待办" 或 "查看待办"

1. 读取三个文件
2. 按状态分组展示
3. **显示全局序号**：用 1️⃣ 2️⃣ 3️⃣ 标记，方便用户说"开始 2"、"完成 4"
4. 显示元数据统计

### 删除待办

用户说："删除 xxx"

1. 从当前文件找到并删除
2. 更新元数据

## 存储位置

所有文件存放在 workspace 目录：

```
workspace/
├── todos_meta.json          # 元数据
├── todos_pending.json       # 未开始
├── todos_in_progress.json   # 进行中
└── todos_completed.json     # 已完成
```

## 数据结构

详见 [references/data-schema.md](references/data-schema.md)

## 输出格式示例

详见 [references/examples.md](references/examples.md)

## 注意事项

- 匹配待办时使用**模糊匹配**（内容关键词）
- 路径可多选，git 项目必须包含分支
- GitHub issue 为完整链接格式
- 状态变更时自动更新 `todos_meta.json`
