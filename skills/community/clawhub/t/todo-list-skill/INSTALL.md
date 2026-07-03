# todo-list Skill — 安装指南

> 版本：v1.5 | 日期：2026-06-11

---

## ⚠️ 安装前置条件（必须完成）

### Step 0：安全扫描（必须）

按用户 Profile 规范，安装前必须完成安全扫描：

```bash
# 1. 进入目录
cd /home/qwenpaw/.qwenpaw/workspaces/default/todos

# 2. 依赖包扫描
pip install pip-audit 2>/dev/null
pip-audit 2>/dev/null || echo "No vulnerabilities"

# 3. 代码安全扫描
grep -rn "password\|secret\|token\|api_key" src/ --include="*.py" || echo "No secrets"
grep -rn "execute.*%" src/ --include="*.py" || echo "No SQL injection risk"

# 4. 阅读 SECURITY.md
cat SECURITY.md
```

**确认后继续**：必须用户确认才能安装。

---

## Step 1：检查依赖

```bash
# Python 版本要求
python3 --version  # >= 3.8

# 检查必需依赖
python3 -c "import sqlite3; import datetime; print('OK')"

# 可选依赖（中文分词，无则用正则替代）
python3 -c "import jieba; print('jieba OK')" 2>/dev/null || echo "jieba not installed (optional)"
```

---

## Step 2：初始化数据库

```bash
cd /home/qwenpaw/.qwenpaw/workspaces/default/todos
python3 -m src.cli init
```

**预期输出**：
```
✅ 数据库初始化完成
✅ Schema 版本：v1.0（业务 schema，与 skill 版本 v1.4 不同步）
✅ 备份文件已创建：todos.db.bak
```

---

## Step 3：验证安装（详细步骤）

按顺序执行，每步成功后进入下一步：

```bash
cd /home/qwenpaw/.qwenpaw/workspaces/default/todos

# === 第 1 步：CLI 可用 ===
python3 -m src.cli --help
# 预期输出：usage: todos add/list/done/del/...
# 如果报错：ModuleNotFoundError → 确保在 todos/ 目录

# === 第 2 步：数据库初始化 ===
python3 -m src.cli init
# 预期：✅ 数据库初始化完成

# === 第 3 步：健康检查（空数据库）===
python3 -m src.cli list
# 预期：今日暂无待办
# 如果报错：database locked → 等待 5 秒重试

# === 第 4 步：添加测试 TODO ===
python3 -m src.cli add "安装验证测试" --priority low
# 预期：✅ 已添加：安装验证测试 [LOW]

# === 第 5 步：查询验证 ===
python3 -m src.cli list
# 预期：看到"安装验证测试"，状态 pending

# === 第 6 步：完成验证 ===
python3 -m src.cli done "安装验证测试"
# 预期：✅ 已完成：安装验证测试

# === 第 7 步：统计验证 ===
python3 -m src.cli stats
# 预期：显示 completed 计数 +1

# === 第 8 步：归档恢复验证 ===
python3 -m src.cli list --status completed --all
# 预期：看到"安装验证测试"

# === 第 9 步：清理（可选）===
# 测试数据自动在 7 天后归档清理，无需手动删除

# === 验证完成 ===
echo "✅ 安装验证全部通过"
```

**验证检查清单**：

| # | 检查项 | 命令 | 预期结果 | 状态 |
|---|--------|------|----------|:----:|
| 1 | CLI 可用 | `python3 -m src.cli --help` | 显示 usage | ⬜ |
| 2 | 数据库初始化 | `python3 -m src.cli init` | ✅ 完成 | ⬜ |
| 3 | 空列表查询 | `python3 -m src.cli list` | 无待办 | ⬜ |
| 4 | 添加 TODO | `python3 -m src.cli add "测试" --priority low` | ✅ 已添加 | ⬜ |
| 5 | 查询 TODO | `python3 -m src.cli list` | 看到测试项 | ⬜ |
| 6 | 完成 TODO | `python3 -m src.cli done "测试"` | ✅ 已完成 | ⬜ |
| 7 | 统计正常 | `python3 -m src.cli stats` | 显示数据 | ⬜ |

**全部通过才能继续安装后续步骤。**

---

## Step 4：配置钉钉推送（可选）

如需定时提醒，需要配置钉钉 channel：

```bash
# 检查钉钉 channel 配置
qwenpaw channels list  # 或咨询管理员

# 测试钉钉推送
qwenpaw channels send --channel dingtalk --text "TODO 测试推送"
```

---

## Step 4.5：首次使用配置提醒通道（v1.5.0 新增）

```bash
# 交互式配置
python3 -m src.reminder setup

# 或直接指定通道
python3 -m src.reminder setup --channel workbuddy   # WorkBuddy 对话内（推荐）
python3 -m src.reminder setup --channel dingtalk     # 钉钉推送（降级）
```

配置存储在 `todos/config.json`：

```json
{
  "reminder_channel": "workbuddy",
  "setup_completed": true,
  "setup_date": "2026-06-11T10:30:00"
}
```

**撤回重新配置**：

```bash
python3 -m src.reminder setup --force
```

---

## Step 5：配置定时任务（可选）

### 每日逾期检查

```bash
# 每天 00:05 检查逾期
qwenpaw cron create \
  --name "todos-check-overdue" \
  --agent-id default \
  --cron "5 0 * * *" \
  --command "cd /home/qwenpaw/.qwenpaw/workspaces/default/todos && python -m src.cli check_overdue"
```

### 每日汇总推送

```bash
# 每个工作日 18:00 推送未完成清单
qwenpaw cron create \
  --name "todos-daily-push" \
  --agent-id default \
  --cron "30 18 * * 1-5" \
  --command "cd /home/qwenpaw/.qwenpaw/workspaces/default/todos && python -m src.cli push"
```

---

## Step 6：注册为 QwenPaw Skill（可选）

如需在 skills marketplace 显示：

```bash
# 检查 manifest.yaml 是否存在
cat manifest.yaml

# 确认 skills 列表可见（如果 qwenpaw 支持本地 skills）
qwenpaw skills list | grep todo
```

---

## 卸载

```bash
# 1. 删除定时任务
qwenpaw cron list  # 找到 todos 相关的 job
qwenpaw cron delete <job_id>

# 2. 备份数据（可选）
cp todos/todos.db ~/todos_backup_$(date +%Y%m%d).db

# 3. 删除目录
rm -rf /home/qwenpaw/.qwenpaw/workspaces/default/todos
```

---

## 常见问题

| 问题 | 解决 |
|------|------|
| `ModuleNotFoundError: No module named 'src'` | 确保在 `todos/` 目录下执行 |
| `Database is locked` | 等待 5 秒重试，或检查是否有其他进程占用 |
| `Permission denied: todos/` | `chmod 755 todos/` |
| 钉钉推送失败 | 检查钉钉 webhook 配置 + 网络连通性 |
| 定时任务不触发 | 检查 `qwenpaw cron list` 确认任务存在 |