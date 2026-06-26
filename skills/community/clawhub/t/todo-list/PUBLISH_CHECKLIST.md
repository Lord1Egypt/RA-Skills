# Todo List Skill 发布清单

## ✅ 已完成项

### 1. 移除私人信息
- [x] 移除硬编码的对话 ID (`user:ou_bb5ebf5cd5589747a734d299cfbd9096`)
- [x] 检查并移除所有个人信息（姓名、邮箱等）
- [x] 清理 Python 缓存文件

### 2. 实现动态会话配置
- [x] 修改 `todo.py` - 移除 `USER_CHAT_ID` 常量
- [x] 修改 `merge-reminders.py` - 移除 `USER_CHAT_ID` 常量
- [x] 实现 `load_session_context()` 从配置文件读取
- [x] 修改 `create_cron_job()` 接受 channel 和 target 参数
- [x] 修改 `cmd_send_status()` 和 `cmd_send_list()` 支持参数传递
- [x] 添加友好的错误提示（缺少会话配置时）

### 3. 更新文档
- [x] 更新 `SKILL.md` 移除硬编码 ID 示例
- [x] 添加会话信息获取说明
- [x] 更新命令示例为参数化形式

### 4. 安全修复（v1.1.0）
- [x] 移除 `shell=True` 使用，改用 args 列表形式
- [x] 在 metadata 中声明依赖（Python 3, OpenClaw CLI）
- [x] 添加文件访问安全措施（路径限制、大小限制、权限检查）
- [x] 添加详细的安全说明文档
- [x] 更新 README.md 添加依赖和安全说明

## 📋 发布信息

### v1.0.0 (已发布)
- **Slug**: `todo-list`
- **Name**: `Todo List 待办事项管理`
- **ID**: `k97470e6aezf2pxdnm4b7nhkw582wk7f`
- **Changelog**: `首次发布：支持待办事项管理、标签系统、项目管理、附件功能、自动提醒`
- **状态**: ⚠️ 被标记为可疑

### v1.2.0 (已发布)
- **Changelog**: `移除feishu依赖，简化metadata格式，明确声明依赖`
- **修复内容**:
  1. 移除 reminder.py 中的 feishu 可选导入
  2. 简化 SKILL.md 的 metadata 格式（使用 `requires` 字段）
  3. 在 SKILL.md 开头添加明确的依赖说明
- **状态**: ✅ 已发布
- **Changelog**: `安全修复：移除shell=True，添加依赖声明，增强文件访问安全`
- **修复内容**:
  1. 移除 `subprocess.run(shell=True)` 使用，改用安全的 args 列表形式
  2. 在 metadata 中声明 Python 3 和 OpenClaw CLI 依赖
  3. 添加文件访问安全措施（禁止访问系统目录、文件大小限制、权限检查）
  4. 添加详细的安全说明文档
  5. 更新 README.md 添加依赖和安全说明

## 🎯 核心功能

1. **待办事项管理**
   - 添加、查看、完成、删除待办
   - 支持优先级（高/中/低）
   - 支持截止时间设置

2. **标签系统**
   - 自动提取 #标签
   - 按标签筛选任务
   - 标签统计

3. **项目管理**
   - 将标签升级为项目
   - 项目进度追踪
   - 项目详情查看

4. **附件功能**
   - 为任务添加附件
   - 附件文件管理
   - **安全措施**：路径限制、大小限制、权限检查

5. **自动提醒**
   - 合并相近时间的任务提醒
   - 多次提醒（30分钟前、15分钟前、准点）
   - 支持 OpenClaw cron 集成

6. **会话管理**
   - 动态获取会话信息
   - 配置文件持久化
   - 跨平台支持（feishu、discord 等）

## 📁 文件结构

```
todo-list/
├── SKILL.md                 # 技能说明文档（含 metadata 和安全说明）
├── TODO-REFERENCE.md        # 完整参考文档
├── README.md                # 简要说明（含依赖和安全说明）
├── PUBLISH_CHECKLIST.md     # 发布清单（本文件）
└── scripts/
    ├── todo.py              # 主脚本（已移除 shell=True）
    ├── merge-reminders.py   # 提醒合并工具
    └── reminder.py          # 提醒检查脚本
```

## 🚀 发布命令

```bash
# 发布 v1.1.0
clawhub publish ~/.openclaw/workspace/skills/todo-list \
  --slug todo-list \
  --name "Todo List 待办事项管理" \
  --version 1.1.0 \
  --changelog "安全修复：移除shell=True，添加依赖声明，增强文件访问安全"
```

## ⚠️ 安全修复详情

### 1. 命令注入风险修复
**问题**: `create_cron_job()` 使用 `subprocess.run(cmd, shell=True)`

**修复**: 改用 args 列表形式
```python
# 修复前
cmd = f'openclaw cron add --name {shlex.quote(name)} ...'
subprocess.run(cmd, shell=True, ...)

# 修复后
cmd = ["openclaw", "cron", "add", "--name", name, ...]
subprocess.run(cmd, ...)  # 不使用 shell=True
```

### 2. 依赖声明
**问题**: metadata 未声明 Python 3 和 OpenClaw CLI 依赖

**修复**: 在 SKILL.md 头部添加 metadata
```yaml
metadata:
  runtime:
    requires:
      - python3
      - openclaw-cli
```

### 3. 文件访问安全
**问题**: 可访问任意文件路径

**修复**: 添加安全检查
- 禁止访问系统敏感目录（/etc, /root, /var 等）
- 文件大小限制（最大 50MB）
- 权限检查（只访问可读文件）
- 隔离存储（附件复制到独立目录）

---

*最后更新：2026-03-14*
