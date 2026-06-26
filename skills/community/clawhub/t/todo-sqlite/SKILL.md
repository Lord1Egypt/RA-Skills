# Todo Skill - 待办事项管理

SQLite 驱动的待办事项管理 skill，支持多项目、子待办、重要/紧急程度、定时提醒。

## 功能特性

1. **多项目管理** - 创建工作、生活等多个待办项目
2. **子待办支持** - 待办可有子待办，子待办完成不自动完成父待办
3. **重要程度** - 1=普通, 2=重要🟠, 3=紧急🔴
4. **紧急程度** - 1=普通, 2=重要🔥, 3=紧急🔥🔥
5. **时间筛选** - 按创建时间、完成时间筛选
6. **搜索待办** - 按关键词搜索标题和备注
7. **智能排序** - 默认按紧急 > 重要 > 普通排序
8. **定时提醒** - 支持定时发送未完成待办

## 数据库位置

`~/.openclaw/workspace/data/todo.db`

## 使用方式

### 项目管理

```
# 创建项目
todo create-project <项目名>
例如：todo create-project 工作
例如：todo create-project 生活

# 列出所有项目
todo list-projects

# 删除项目（会删除项目下所有待办）
todo delete-project <项目名>
```

### 添加待办

```
# 基本添加
todo add <项目名> <待办内容>

# 指定重要程度（-i/--importance: 1=普通, 2=重要, 3=紧急）
todo add 工作 "完成报告" -i 3

# 指定紧急程度（-u/--urgency: 1=普通, 2=重要, 3=紧急）
todo add 工作 "紧急修复bug" -i 3 -u 3

# 指定截止日期（-d/--due: YYYY-MM-DD 或 YYYY-MM-DD HH:MM）
todo add 工作 "提交周报" -d 2026-03-25

# 添加子待办（-p/--parent: 父待办ID）
todo add 工作 "写测试用例" -p 5

# 添加备注（-n/--note）
todo add 工作 "代码审查" -n "重点关注性能问题"
```

### 完成待办

```
# 完成待办
todo done <待办ID>

# 取消完成（重新打开）
todo undo <待办ID>
```

### 查看待办

```
# 查看项目下所有待办
todo list <项目名>

# 查看所有未完成待办
todo list-all

# 只看未完成
todo list-all --pending
# 或
todo list-all -p

# 只看已完成
todo list-all --completed
# 或
todo list-all -c

# 按重要程度筛选
todo list-all --importance 3

# 按紧急程度筛选
todo list-all --urgency 3

# 按时间范围筛选
todo list-all --from 2026-03-01 --to 2026-03-31

# 查看单个待办详情（含子待办）
todo show <待办ID>
```

### 编辑待办

```
# 修改标题
todo edit <待办ID> --title "新标题"

# 修改重要程度
todo edit <待办ID> --importance critical

# 修改紧急程度
todo edit <待办ID> --urgency high

# 修改截止日期
todo edit <待办ID> --due 2026-03-30

# 修改备注
todo edit <待办ID> --note "新的备注"

# 移动到其他项目
todo edit <待办ID> --project 生活
```

### 删除待办

```
# 删除待办（会同时删除子待办）
todo delete <待办ID>
```

### 统计

```
# 查看统计信息
todo stats

# 按项目查看统计
todo stats <项目名>
```

### 搜索待办

```
# 搜索标题和备注
todo search <关键词>

# 只搜索未完成
todo search 报告 --pending

# 只搜索已完成
todo search 报告 --completed
```

## 排序规则

待办列表默认按以下顺序排序：

1. **整体最大优先级**（包括子待办）
2. **自身紧急程度**：high > medium > low
3. **自身重要程度**：high > medium > low
4. **创建时间**：新创建的排前面

**父待办排序考虑子待办优先级：**
- 如果子待办有紧急/重要，父待办的排序位置会提升
- 例如：父待办是"一般"，但子待办是"高"→ 父待办按"高"级别排序

**子待办排序：**
- 子待办按紧急 > 重要 > 时间排序显示

## 显示规则

重要/紧急程度显示方式：

| 等级 | 重要显示 | 紧急显示 |
|------|---------|---------|
| 3 (紧急) | 🔴 | 🔥🔥 |
| 2 (重要) | 🟠 | 🔥 |
| 1 (普通) | （不显示） | （不显示） |

**示例：**
- `🔴🔥🔥` = 紧急 + 紧急
- `🟠🔥` = 重要 + 重要
- 无标记 = 普通待办（默认）

**注意：** 新建待办默认等级为 1，不显示任何标记。

## 定时提醒

使用 OpenClaw 的 cron 功能设置定时提醒：

```
# 每天早上9点发送未完成待办
定时任务：每天9点提醒待办
```

这会调用 `todo list-all --pending` 并发送结果。

## 数据结构

**projects 表：**
- id: 项目ID
- name: 项目名称
- created_at: 创建时间

**todos 表：**
- id: 待办ID
- project_id: 所属项目
- parent_id: 父待办ID（NULL表示顶级）
- title: 标题
- note: 备注
- importance: 重要程度
- urgency: 紧急程度
- status: 状态（pending/completed）
- due_date: 截止日期
- created_at: 创建时间
- updated_at: 更新时间
- completed_at: 完成时间

## 示例

```
# 创建工作项目
todo create-project 工作

# 添加一个紧急待办
todo add 工作 "上线前检查" -i 3 -u 3 -d 2026-03-25

# 添加子待办
todo add 工作 "检查数据库迁移" -p 1
todo add 工作 "检查API文档" -p 1

# 完成子待办
todo done 2
todo done 3

# 父待办仍需手动完成
todo done 1

# 查看所有未完成
todo list-all -p
```