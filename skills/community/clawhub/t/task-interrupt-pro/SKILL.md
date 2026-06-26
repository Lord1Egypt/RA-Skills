---
name: task-interrupt-pro
description: >-
  Task Interrupt Skill Pro - 精确停止Agent执行中的子任务进程。
  Triggers: "停止猫经理", "停止猫工头", "停止猫财子", "停止猫播播", 
  "停止我的任务", "中断猫经理", "解救猫经理", "agent任务卡住", 
  "进程无响应", "子任务卡死"。
  注意：不支持 /stop（系统级abort命令，会直接终止agent本身）！
version: 1.0.4
metadata:
  openclaw:
    emoji: "🛑"
    requires:
      env: []
      bins: ["bash"]
    always: false
    os: ["linux", "darwin"]
---

# Task Interrupt Skill Pro

> **版本**: 1.0.3
> **跨平台**: Linux ✅ + macOS ✅ (仅使用POSIX兼容调用)  
> **作者**: 猫经理（哈基咪公司）  
> **更新日期**: 2026-03-19

---

## Purpose

解决 Agent 执行任务时卡住、陷入死循环、进程无响应时，无法被用户主动终止的问题。

**核心价值：**
- 用户发送普通消息（如"停止猫经理"）即可精确停止对应 agent 的任务进程
- 避免使用 `/stop` 系统命令（会直接 abort agent 本身）
- 三层保障机制：flag 优雅退出 → SIGINT → SIGKILL
- 自动清理残留文件，无需人工干预

**与原版 Task Interrupt Skill 的区别：**
| 维度 | 原版 | Pro 版 |
|------|------|--------|
| 中断触发 | /stop（系统级，会 abort agent） | 普通消息（"停止猫经理"） |
| 目标 | 需要 agent 主动轮询检查 | 外部 kill PID，零依赖 |
| 精确性 | 停止所有子任务 | 可针对特定 agent |
| 侵入性 | 需要修改 agent 行为 | 无侵入 |

---

## When to Use

当用户发送以下任意指令时激活：

- `停止猫经理` - 停止猫经理正在执行的任务
- `停止猫工头` - 停止猫工头正在执行的任务
- `停止猫财子` - 停止猫财子正在执行的任务
- `停止猫播播` - 停止猫播播正在执行的任务
- `停止我的任务` - 停止当前 agent 的任务
- `解救猫经理` / `中断猫经理` - 同"停止猫经理"
- `进程卡住了` / `任务无响应` - 需要强制终止时

**Do NOT use for:**
- `/stop` - 这是系统级 abort 命令，会直接终止 agent 本身，勿用！

---

## Core Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           用户发送指令                                  │
│              "停止猫经理" / "停止猫财子" / "停止猫工头"                │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    主 Agent（我）接收消息                               │
│  识别关键词："停止" + agent名称                                        │
│  触发中断流程（优先级最高）                                            │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              handle-stop.sh 执行（三层保障）                             │
│                                                                         │
│  第一层：创建 stop flag                                                │
│    → /tmp/agent-stop-{SESSION_ID}.flag                                 │
│    → 进程检测到 flag → 优雅退出（trap）                                │
│                                                                         │
│  第二层：SIGINT 信号                                                   │
│    → kill -INT {PID}                                                   │
│    → 进程 trap 捕获 → 优雅退出                                        │
│                                                                         │
│  第三层：SIGKILL 兜底                                                  │
│    → kill -9 {PID}（如前两层均失效）                                   │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          清理 & 反馈                                   │
│                                                                         │
│  - PID 文件自动清理（/tmp/agent-pid-{SESSION_ID}.pid）                 │
│  - flag 文件 60 秒后自动清理                                           │
│  - 向用户返回中断结果                                                  │
└─────────────────────────────────────────────────────────────────────────┘
```

**subagent 任务模板（可中断任务）：**

```bash
#!/bin/bash
SESSION_ID="maogongtou-$$"  # 或 maocaizi, maobobo, main
FLAG_FILE="/tmp/agent-stop-${SESSION_ID}.flag"
PID_FILE="/tmp/agent-pid-${SESSION_ID}.pid"

# 记录 PID
echo $$ > "${PID_FILE}"
chmod 0600 "${PID_FILE}"

# 信号处理（收到 SIGINT/SIGTERM 时优雅退出）
trap 'echo "[TRAP] 收到停止信号"; rm -f "${PID_FILE}"; exit 0' SIGINT SIGTERM

# 主循环（每轮检查 flag）
while true; do
    if [ -f "${FLAG_FILE}" ]; then
        echo "[TRAP] 检测到 stop flag，优雅退出"
        rm -f "${PID_FILE}"
        exit 0
    fi
    # 实际任务逻辑
    echo "工作中..."
    sleep 3
done
```

---

## Components

### 1. handle-stop.sh - 核心中断脚本

**路径**: `scripts/handle-stop.sh`

**功能**:
- 创建 stop flag 文件
- 读取 PID 文件获取目标进程
- 三层终止保障（SIGINT → SIGTERM → SIGKILL）
- 清理 PID 文件
- 60 秒后自动清理 flag 文件

**用法**:
```bash
./handle-stop.sh <SESSION_ID> [reason]
```

**示例**:
```bash
./handle-stop.sh "maocaizi-82161" "Chairman stop request"
./handle-stop.sh "maojingli-test-82363" "User request"
```

### 2. task-template.sh - 可中断任务模板

**路径**: `scripts/task-template.sh`

**功能**:
- 记录当前进程 PID 到固定文件
- 设置 trap 信号处理
- 主循环中检查 stop flag
- 优雅退出时清理 PID 文件

**用法**: 将此模板包裹实际任务逻辑

### 3. Shell 工具集

| 脚本 | 路径 | 功能 |
|------|------|------|
| create-stop-flag.sh | scripts/ | 手动创建 stop flag |
| check-stop-flag.sh | scripts/ | 检查 flag 是否存在（含过期清理） |
| clear-stop-flag.sh | scripts/ | 手动清除 flag |

---

## Workflow

### 中断流程（Agent 侧）

1. **接收消息** → 检测到"停止" + agent名称关键词
2. **优先级最高** → 立即中断当前任务，不进行其他处理
3. **调用 handle-stop.sh** → `bash handle-stop.sh <SESSION_ID> [reason]`
4. **验证结果** → 检查进程是否已终止
5. **返回用户** → 发送中断结果确认

### 中断流程（详细步骤）

```bash
# 步骤1：确定目标 session
# 用户说"停止猫财子" → 猫财子的任务 SESSION_ID

# 步骤2：调用中断脚本
bash scripts/handle-stop.sh "maocaizi-82161" "Chairman stop request"

# 步骤3：验证
# 检查 /tmp/agent-pid-maocaizi-82161.pid 是否被清理
# 检查对应 PID 是否已终止

# 步骤4：返回用户
"⏹️ 猫财子任务已停止，进程已终止"
```

---

## Examples

### Example 1: 停止猫财子

**用户输入**: `停止猫财子`

**Agent 处理**:
1. 识别关键词"停止"+"猫财子"
2. 调用 `bash handle-stop.sh "maocaizi-<ID>" "Chairman stop request"`
3. 返回结果

**输出**:
```
⏹️ 猫财子任务已停止

SESSION_ID: maocaizi-82161
PID: 82161
状态: 已终止 ✅
```

### Example 2: 停止卡住的任务

**用户输入**: `猫经理任务卡住了，请停止`

**Agent 处理**:
1. 识别"停止"+"猫经理"+"卡住"
2. 查找所有猫经理相关的 PID 文件
3. 逐个调用 handle-stop.sh
4. 返回汇总结果

---

## Error Handling

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| "未找到 PID 文件" | 进程已退出或 SESSION_ID 错误 | 跳过 kill，提示用户进程可能已终止 |
| "进程未响应 SIGINT" | 进程处于不可中断状态 | 自动升级到 SIGTERM → SIGKILL |
| "Permission denied" | 无权限 kill 该进程 | 提示用户需要更高权限 |

### 兜底机制

即使所有层都失效，仍可通过以下方式强制终止：
```bash
# 直接 kill -9（强制终止）
kill -9 {PID}
```

---

## Changelog

### 1.0.4 (2026-03-28) - 安全+逻辑双修复版
**来源**: 大哥Gemini审核 + 猫经理自检

#### 修复内容
| Bug | 文件 | 严重性 | 说明 |
|-----|------|--------|------|
| validate_process返回值错误 | handle-stop.sh | 🔴 高 | cmdline不匹配时返回0，调用方误判为成功并执行kill。改为返回2，跳过kill |
| FLAG_FILE符号链接攻击 | handle-stop.sh | 🔴 高 | 创建flag文件前未检查符号链接，攻击者可覆盖任意文件。添加symlink检查 |
| REASON JSON注入 | handle-stop.sh | 🟡 中 | REASON写入JSON未转义。添加sed转义 |

#### 变更详情
| 场景 | 旧行为(v1.0.3) | 新行为(v1.0.4) |
|------|---------------|---------------|
| 进程cmdline不含SESSION_ID | 返回0→调用方继续kill | 返回2→跳过kill |
| FLAG_FILE已是符号链接 | 可能覆盖任意文件 | 安全拒绝+退出 |
| REASON含特殊字符 | JSON结构破坏 | 转义后安全写入 |

### 1.0.3 (2026-03-19) - 体验优化版
**命令行校验优化**：豆包建议，将"拒绝kill"改为"警告+跳过kill"。

#### 改进内容
- **原问题**：bash -c变量展开场景下命令行不含SESSION_ID，被安全拒绝
- **改进方案**：命令行校验改为警告+跳过kill，不拒绝操作
- **理由**：flag机制已能保证优雅退出，kill只是兜底
- **效果**：体验更平滑，不影响真实任务场景

#### 变更详情
| 场景 | 旧行为(v1.0.2) | 新行为(v1.0.3) |
|------|---------------|---------------|
| bash -c变量展开 | 安全拒绝+不kill | 警告+跳过kill |
| 真实脚本格式 | 正常kill | 正常kill |

### 1.0.2 (2026-03-19) - 综合改进版
**跨平台安全增强**：整合Kimi+豆包建议，添加审计日志+格式校验+flock原子锁。

#### 新增功能
| 功能 | 来源 | 说明 |
|------|------|------|
| 审计日志 | 豆包建议 | 所有操作记录到 `/tmp/agent-interrupt-audit.log` |
| SESSION_ID严格格式 | 豆包建议 | 必须为 `^[a-z0-9]+-[a-z0-9]+$` 格式，拒绝非法格式 |
| flock原子锁 | Kimi建议 | PID文件读写使用flock防止竞争条件 |
| 权限检查 | 综合 | 校验PID文件权限，防止权限过宽 |
| 孤儿检测提示 | Kimi建议 | 日志中包含进程验证详情 |

#### 安全改进
- **拒绝非法SESSION_ID格式**：非`{name}-{id}`格式直接拒绝
- **文件权限检查**：警告权限过宽的PID文件
- **完整审计链**：STARTED→VALIDATED→TERMINATING→SUCCESS/FAILED

#### 脚本改进
- **handle-stop.sh**：审计日志+严格格式校验+flock原子锁读取
- **task-template.sh**：审计日志+flock原子锁写入PID

### 1.0.1 (2026-03-19) - 安全加固版
**ClawHub安全扫描修复**：安全扫描发现2个问题，已全部修复。

#### 问题1修复：instructions.md JS示例清理
- **原问题**：引用了不存在的`require('task-interrupt')`模块
- **修复**：删除所有JS示例代码，纯化文档为Bash方案

#### 问题2修复：handle-stop.sh多重安全校验
| 安全机制 | 原风险 | 修复方案 |
|---------|--------|---------|
| PID文件类型检查 | 符号链接攻击 | 拒绝符号链接类型PID文件 |
| 文件所有权验证 | 其他用户伪造 | 验证文件属于当前用户或root |
| 进程命令行验证 | 误杀无关进程 | 进程命令行必须包含SESSION_ID标识 |
| 命令行注入防护 | 特殊字符注入 | SESSION_ID清理（字母数字短横线） |
| PID纯数字提取 | 注入恶意PID | 提取纯数字PID |
| 分阶段SIGINT | 进程来不及优雅退出 | SIGINT后等待3秒再SIGTERM |
| 删除pgrep fallback | 盲目匹配误杀 | 删除不安全的pgrep fallback |

### 1.0.0 (2026-03-19)
- **Initial Pro release**
- 支持精确停止特定agent的任务
- 三层中断保障机制（flag→SIGINT→SIGKILL）
- 避免与系统/stop命令冲突
- 自动清理残留文件

---

## References

- **原版 Task Interrupt Skill**: [ClawHub](https://clawhub.com)
- **OpenClaw Skills 文档**: [官方文档](https://docs.openclaw.ai/tools/skills)
- **架构参考**: 豆包AI + Kimi AI 协作设计

---

## 安装说明

### 自动安装（推荐）

将 `task-interrupt-pro` 目录放入 agent 的 `skills/` 目录：

```bash
# 对于猫经理
cp -r task-interrupt-pro ~/.openclaw/viking-maojingli/skills/

# 对于猫工头
cp -r task-interrupt-pro ~/.openclaw/viking-maogongtou/skills/

# 对于猫财子
cp -r task-interrupt-pro ~/.openclaw/viking-maocaizi/skills/

# 对于猫播播
cp -r task-interrupt-pro ~/.openclaw/viking-maobobo/skills/
```

### 权限设置

```bash
chmod +x skills/task-interrupt-pro/scripts/*.sh
```

### 验证安装

```bash
# 检查脚本可执行
ls -la skills/task-interrupt-pro/scripts/*.sh

# 测试 handle-stop.sh（Dry run）
echo "test-session" > /tmp/agent-pid-test-session.pid
bash scripts/handle-stop.sh "test-session" "test"
```

---

**作者**: 猫经理（哈基咪公司）  
**版本**: 1.0.0  
**日期**: 2026-03-19

---

## 🙏 致谢

**非常感谢开发者 @guyxlouspg 和他的猫小咪团队提供的一切思路和帮助及公布的开源成果，让我们哈基咪OPC公司能够顺利跑通整个流程，顺利开发了 Task Interrupt Pro！向前辈致敬！**

---

*Task Interrupt Pro - 哈基咪OPC公司首个Skill成果*  
*开发日期: 2026-03-19*
