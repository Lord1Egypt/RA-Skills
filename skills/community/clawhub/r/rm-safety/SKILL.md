# rm-safety - RM Command Safety Check

**Intercepts risky `rm` commands to assess impact, confirm user intent, and suggest safer alternatives before execution to prevent accidental data loss.**

**拦截高危 `rm` 命令，评估影响并确认用户意图，提供安全替代方案，防止误删数据。**

---

## Trigger Conditions | 触发条件

Triggered when user requests to execute or agent prepares to execute:

当用户请求执行或我准备执行以下命令时触发：

- `rm` (any arguments | 任何参数)
- `rm -rf` / `rm -fr`
- `rm -r` / `rm -R`
- `unlink`
- `shred`
- Other direct file deletion commands | 其他直接删除文件的命令

**Not Triggered | 不触发:**
- `trash` command (recoverable deletion | 可恢复删除)
- `mv` to trash directory | 移动到 trash 目录

---

## Safety Check Flow | 安全检查流程

### 1. Intercept Command | 拦截命令

When `rm` command is detected, **stop execution immediately** and enter confirmation flow.

检测到 `rm` 命令时，**立即停止执行**，进入询问流程。

### 2. Collect Information | 收集信息

Before asking, perform these checks (read-only operations | 只读操作):

**Important: Always quote paths to prevent injection | 重要：始终引用路径防止注入**

```bash
# Check if target exists (quoted path | 引用路径) | 检查目标是否存在
ls -la -- "$path"

# If directory, count contents (safe find | 安全 find) | 如果是目录，统计内容
find -- "$path" -type f 2>/dev/null | wc -l  # files | 文件数
find -- "$path" -type d 2>/dev/null | wc -l  # directories | 目录数

# Check if inside workspace | 检查是否在 workspace 内
echo "$path" | grep -q ".openclaw/workspace" && echo "⚠️ Inside workspace" || echo "⚠️ Outside workspace"

# Check if critical directory | 检查是否是关键目录
echo "$path" | grep -qE "(Documents|Desktop|Downloads|Pictures)" && echo "⚠️ User critical directory"

# Resolve to absolute path (prevent relative path tricks | 防止相对路径欺骗)
realpath -- "$path" 2>/dev/null || readlink -f -- "$path"
```

**Safety notes | 安全说明:**
- Use `--` to stop option parsing (prevents `-rf /` tricks) | 使用 `--` 停止选项解析
- Always quote `"$path"` (prevents space injection) | 始终引用 `"$path"` 防止空格注入
- Redirect stderr `2>/dev/null` (suppress errors gracefully) | 重定向 stderr 优雅处理错误

### 3. Confirmation Format | 询问格式

**Must use this format to ask user | 必须使用以下格式询问用户：**

```
🚨 High-Risk Command Confirmation | 高危命令确认

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Command Details | 命令详情
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Command | 命令：rm [full command with arguments | 完整命令及参数]
Working Directory | 执行位置：[current directory | 当前工作目录]
Target Path | 目标路径：[absolute path | 绝对路径]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Impact Assessment | 影响评估
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Will delete X files | 将删除 X 个文件
[ ] Will delete Y directories (Z total items | 将删除 Y 个文件夹 (含 Z 个子项)
[ ] Location | 路径位置：Inside workspace / Outside workspace / User critical directory
[ ] Recoverable via trash | 是否在 trash 可恢复范围：No (rm is permanent | rm 不可恢复)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Alternatives | 替代方案
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Use trash command → Recoverable in Finder | 使用 trash 命令 → 可在 Finder 恢复
2. Backup before delete | 先备份再删除 → `cp -r <path> <backup>`
3. Move to temp directory | 移动到临时目录 → `mv <path> /tmp/xxx`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❓ Please Confirm | 请确认
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply [y] to execute | 回复 [y] 确认执行
Reply [n] to cancel | 回复 [n] 取消
Reply [backup] to backup first | 回复 [backup] 先备份再执行
Reply [trash] to use trash instead | 回复 [trash] 改用 trash 命令
```

### 4. User Response Handling | 用户响应处理

| User Reply | Action |
|------------|--------|
| `y` / `yes` / `确认` | Execute original command | 执行原命令 |
| `n` / `no` / `取消` | Cancel operation | 取消操作，不执行 |
| `backup` | Backup to `/tmp/rm-backup-<timestamp>/` then execute | 先备份到 `/tmp/rm-backup-<timestamp>/` 再执行 |
| `trash` | Use `trash` command instead | 改用 `trash` 命令执行 |

---

## Exceptions | 例外情况

**Can execute without asking | 无需询问可直接执行:**
- User explicitly says "execute without asking" **AND** path is verified safe | 用户明确说 "不用问了直接执行" **且** 路径已验证安全
- Deleting temp files under `/tmp/` (created by agent, verified by `ls -la`) | 删除 `/tmp/` 下的临时文件（且是我自己创建的，已用 `ls -la` 验证）
- User provided explicit written permission (same session) **AND** path matches permission | 用户提供了明确的书面许可（同一会话内）**且** 路径与许可匹配

**Still must ask even if user says not to | 仍需询问即使用户说不用问:**
- Deleting entire workspace directory | 删除整个 workspace 目录
- Deleting user home directory (`/Users/caesar/`) | 删除用户主目录
- Dangerous commands like `rm -rf /` (should refuse directly) | 使用 `rm -rf /` 等危险命令（应直接拒绝）
- Path contains unescaped special characters (spaces, `;`, `|`, `&`) | 路径包含未转义的特殊字符

**Must refuse directly | 直接拒绝:**
- `rm -rf /` or `rm -rf /*` (system destruction) | 系统级危险命令
- `rm -rf ~` or `rm -rf /home/*` (user data destruction) | 用户数据毁灭
- Path resolves to root or system directories | 路径解析为根目录或系统目录

---

## Activation Conditions | 激活条件

This skill activates when:

本 skill 在以下情况自动激活：
- Detects `rm`, `rm -r`, `rm -rf`, `unlink`, or `shred` in exec call | 检测到 exec 调用包含这些命令
- User mentions "delete", "remove", "erase" involving file paths | 用户提到这些词且涉及文件路径

**Path validation before execution | 执行前路径验证:**
1. Resolve to absolute path using `realpath` or `readlink -f` | 解析为绝对路径
2. Verify path exists using `test -e "$path"` | 验证路径存在
3. Check for dangerous patterns (`/`, `~`, `*`, wildcards) | 检查危险模式
4. Reject if path contains shell metacharacters unescaped | 如果包含未转义的 shell 元字符则拒绝

---

## Test Cases | 测试用例

```bash
# Should trigger confirmation | 应该触发询问
rm file.txt
rm -rf ./folder
rm -r /path/to/something

# Should NOT trigger | 不应触发
trash file.txt
mv file.txt ~/.Trash/
```

---

**Priority | 优先级:** High (security-related | 安全相关)  
**Last Updated | 最后更新:** 2026-03-24
