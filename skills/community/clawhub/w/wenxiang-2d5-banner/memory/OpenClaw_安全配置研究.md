# OpenClaw 安全配置研究

**研究日期：** 2026-03-11  
**研究员：** 阿福（OpenClaw 助手）  
**版本：** 1.0

---

## 📋 研究概述

本报告深入研究 OpenClaw 的三个关键安全配置命令，分析其作用、影响和协同效果，为生产环境提供安全配置方案。

### 研究的三个配置

1. `openclaw config set tools.profile "messaging"`
2. `openclaw config set tools.fs.workspaceOnly true`
3. `openclaw config set agents.defaults.sandbox.mode "all"`

---

## 🔐 配置一：tools.profile "messaging"

### 作用说明

**配置命令：**
```bash
openclaw config set tools.profile "messaging"
```

**配置文件位置：** `~/.openclaw/openclaw.json`

**配置字段：** `tools.profile`

### "messaging" profile 包含的工具

根据 OpenClaw 源码分析，**messaging profile** 包含以下工具：

| 工具 | 说明 | 风险等级 |
|------|------|----------|
| `message` | 发送消息到聊天频道 | 🟢 低 |
| `sessions_list` | 列出会话列表 | 🟢 低 |
| `sessions_history` | 查看会话历史 | 🟢 低 |
| `sessions_send` | 向会话发送消息 | 🟢 低 |

**关键限制：**
- ❌ **不允许** 文件操作工具（read, write, edit, apply_patch）
- ❌ **不允许** 运行时工具（exec, process, bash）
- ❌ **不允许** UI 工具（browser, canvas）
- ❌ **不允许** 自动化工具（cron, gateway）
- ❌ **不允许** 节点工具（nodes）

### 与默认 profile 的区别

| Profile | 包含工具 | 使用场景 | 风险等级 |
|---------|----------|----------|----------|
| **minimal** | 无（最严格） | 纯对话 | 🟢 最低 |
| **messaging** | 消息 + 会话管理 | 聊天机器人 | 🟢 低 |
| **coding** | 文件 + 执行 + 会话 + 内存 | 编程助手 | 🟡 中 |
| **full** (默认) | 所有工具 | 完全访问 | 🔴 高 |

**默认 profile (full) 包含的额外工具：**
- 文件系统：read, write, edit, apply_patch
- 运行时：exec, process, bash
- UI 自动化：browser, canvas
- 系统工具：nodes, cron, gateway
- 媒体工具：image, pdf, tts

### 安全性提升

**1. 攻击面减少**
- 从 20+ 个工具减少到 4 个工具
- 移除所有文件操作能力
- 移除所有命令执行能力

**2. 权限最小化原则**
- 只保留消息通信必需的工具
- 符合"最小权限"安全原则
- 即使被攻击，影响范围有限

**3. 防止提示词注入**
- 攻击者无法诱导 agent 读取敏感文件
- 攻击者无法诱导 agent 执行恶意命令
- 攻击者无法诱导 agent 修改系统文件

**4. 适用场景**
- ✅ 群聊机器人（开放群组）
- ✅ 公共频道助手
- ✅ 多用户共享环境
- ❌ 需要文件操作的个人助手
- ❌ 需要执行命令的开发助手

---

## 📁 配置二：tools.fs.workspaceOnly true

### 作用说明

**配置命令：**
```bash
openclaw config set tools.fs.workspaceOnly true
```

**配置文件位置：** `~/.openclaw/openclaw.json`

**配置字段：** `tools.fs.workspaceOnly`

### workspaceOnly=true 限制什么？

**限制范围：**
- ✅ **允许访问：** `~/.openclaw/workspace/` 目录及其子目录
- ❌ **禁止访问：** workspace 目录外的所有路径

**受影响的工具：**
| 工具 | 限制效果 |
|------|----------|
| `read` | 只能读取 workspace 内的文件 |
| `write` | 只能写入 workspace 内的文件 |
| `edit` | 只能编辑 workspace 内的文件 |
| `apply_patch` | 只能应用 workspace 内的补丁 |
| `image` | 只能访问 workspace 内的图片 |
| `pdf` | 只能访问 workspace 内的 PDF |

### 对文件操作的影响

**1. 路径解析规则**
```javascript
// workspaceOnly=true 时的行为
if (workspaceOnly === true) {
  // 检查路径是否在 workspace 内
  if (!filePath.startsWith(workspaceDir)) {
    throw new Error("Access denied: path outside workspace");
  }
}
```

**2. 实际示例**

| 操作 | workspaceOnly=false | workspaceOnly=true |
|------|---------------------|--------------------|
| 读取 `C:\Users\Xiabi\Documents\notes.md` | ✅ 允许 | ❌ 拒绝 |
| 读取 `C:\Users\Xiabi\.openclaw\workspace\notes.md` | ✅ 允许 | ✅ 允许 |
| 写入 `C:\Windows\System32\malicious.dll` | ✅ 允许 | ❌ 拒绝 |
| 写入 `C:\Users\Xiabi\.openclaw\workspace\output.txt` | ✅ 允许 | ✅ 允许 |

**3. 与 Sandbox 的关系**

```
┌─────────────────────────────────────────────────────────┐
│                   主机系统 (Host)                        │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Sandbox 容器 (如果启用)                │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │           工具执行环境                        │  │  │
│  │  │  ┌───────────────────────────────────────┐  │  │  │
│  │  │  │    workspaceOnly 边界                  │  │  │  │
│  │  │  │    ┌───────────────────────────────┐  │  │  │  │
│  │  │  │    │   ~/.openclaw/workspace/      │  │  │  │  │
│  │  │  │    │   (唯一允许访问的区域)          │  │  │  │  │
│  │  │  │    └───────────────────────────────┘  │  │  │  │
│  │  │  └───────────────────────────────────────┘  │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 安全性提升

**1. 文件系统隔离**
- 防止 agent 访问系统敏感文件
- 防止 agent 修改系统配置
- 防止 agent 读取用户隐私数据（文档、照片等）

**2. 数据泄露防护**
- 即使 agent 被攻击，也无法读取 workspace 外的文件
- 保护用户文档、密码文件、SSH 密钥等
- 限制数据外泄范围

**3. 系统完整性**
- 防止恶意写入系统目录
- 防止植入恶意软件
- 防止修改启动项/注册表

**4. 纵深防御**
- 与 sandbox 配合形成多层防护
- 即使 sandbox 被突破，仍有 workspaceOnly 限制
- 符合"纵深防御"安全原则

---

## 🐳 配置三：agents.defaults.sandbox.mode "all"

### 作用说明

**配置命令：**
```bash
openclaw config set agents.defaults.sandbox.mode "all"
```

**配置文件位置：** `~/.openclaw/openclaw.json`

**配置字段：** `agents.defaults.sandbox.mode`

### sandbox.mode="all" 是什么意思？

**Sandbox 模式选项：**

| 模式 | 说明 | 安全等级 |
|------|------|----------|
| `"off"` | 不启用 sandbox，所有工具在主机运行 | 🔴 低 |
| `"non-main"` | 仅非主会话启用 sandbox（默认） | 🟡 中 |
| `"all"` | **所有会话**都启用 sandbox | 🟢 高 |

**"all" 模式的具体含义：**
- ✅ **主会话 (main session)** → 在 sandbox 中运行
- ✅ **非主会话 (non-main session)** → 在 sandbox 中运行
- ✅ **群组会话 (group/channel session)** → 在 sandbox 中运行
- ✅ **子代理 (subagent)** → 在 sandbox 中运行

### 对子任务/agent 的影响

**1. 执行环境变化**

```
┌─────────────────────────────────────────────────────┐
│                  未启用 Sandbox                      │
│  Agent → 工具 → 主机系统 (直接访问)                   │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                  启用 Sandbox (mode="all")           │
│  Agent → 工具 → Docker 容器 → 主机系统 (隔离访问)      │
└─────────────────────────────────────────────────────┘
```

**2. 工具执行位置**

| 工具 | 无 sandbox | sandbox mode="all" |
|------|-----------|-------------------|
| `exec` | 主机 PowerShell | Docker 容器内 |
| `read` | 主机文件系统 | 容器内文件系统 |
| `write` | 主机文件系统 | 容器内文件系统 |
| `browser` | 主机浏览器 | 容器内浏览器（可选） |
| `process` | 主机进程 | 容器内进程 |

**3. 工作空间访问**

根据 `sandbox.workspaceAccess` 配置：

| 配置 | 工作空间访问 | 说明 |
|------|-------------|------|
| `"none"` (默认) | 隔离的 sandbox workspace | `~/.openclaw/sandboxes/` |
| `"ro"` | 只读访问 | 挂载为 `/agent` (只读) |
| `"rw"` | 读写访问 | 挂载为 `/workspace` (读写) |

**4. 网络访问**

- **默认：** `network: "none"` (无网络)
- **可选：** `network: "bridge"` (桥接网络)
- **禁止：** `network: "host"` (主机网络)

### 安全性提升

**1. 爆破半径限制 (Blast Radius)**
- 工具执行被限制在容器内
- 即使工具被恶意利用，影响范围限于容器
- 容器可配置资源限制（CPU、内存、进程数）

**2. 文件系统隔离**
- 容器使用独立的文件系统
- 主机文件系统通过绑定挂载 (bind mounts) 控制访问
- 可配置只读根文件系统 (`readOnlyRoot: true`)

**3. 进程隔离**
- 容器内进程与主机进程隔离
- 可限制进程数 (`pidsLimit: 256`)
- 可限制能力 (`capDrop: ["ALL"]`)

**4. 安全配置示例**
```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "all",
        scope: "agent",
        workspaceAccess: "none",
        docker: {
          image: "openclaw-sandbox:bookworm-slim",
          network: "none",
          readOnlyRoot: true,
          capDrop: ["ALL"],
          pidsLimit: 256,
          memory: "1g",
          cpus: 1
        }
      }
    }
  }
}
```

**5. 防护效果对比**

| 攻击场景 | 无 sandbox | sandbox mode="all" |
|----------|-----------|-------------------|
| 恶意命令执行 | 🔴 主机执行 | 🟢 容器内执行 |
| 文件系统遍历 | 🔴 访问全系统 | 🟢 仅容器文件系统 |
| 网络扫描 | 🔴 访问内网 | 🟢 网络隔离 |
| 资源耗尽 | 🔴 耗尽主机资源 | 🟢 限制在容器配额 |
| 权限提升 | 🔴 可能获取主机权限 | 🟢 限于容器权限 |

---

## 🔄 综合建议

### 三个配置的协同效果

**1. 纵深防御体系**

```
┌─────────────────────────────────────────────────────────────┐
│                    第一层：工具策略 (Tool Policy)             │
│  tools.profile="messaging"                                   │
│  → 只允许消息工具，移除文件操作和命令执行能力                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    第二层：文件系统限制 (FS Restriction)      │
│  tools.fs.workspaceOnly=true                                 │
│  → 即使有文件工具，也只能访问 workspace 目录                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    第三层：容器隔离 (Sandbox)                 │
│  agents.defaults.sandbox.mode="all"                          │
│  → 所有工具执行都在 Docker 容器内，与主机隔离                  │
└─────────────────────────────────────────────────────────────┘
```

**2. 安全增强矩阵**

| 配置组合 | 工具限制 | 文件限制 | 执行隔离 | 安全等级 |
|----------|---------|---------|---------|---------|
| 无配置 | ❌ | ❌ | ❌ | 🔴 低 |
| 仅 messaging profile | ✅ | ❌ | ❌ | 🟡 中 |
| 仅 workspaceOnly | ❌ | ✅ | ❌ | 🟡 中 |
| 仅 sandbox | ❌ | ❌ | ✅ | 🟡 中 |
| messaging + workspaceOnly | ✅ | ✅ | ❌ | 🟢 高 |
| workspaceOnly + sandbox | ❌ | ✅ | ✅ | 🟢 高 |
| **三者全部** | ✅ | ✅ | ✅ | 🟢🟢 **最高** |

**3. 攻击场景防护效果**

| 攻击场景 | 无防护 | 仅 messaging | 三者全部 |
|----------|-------|-------------|---------|
| 提示词注入读取文件 | 🔴 成功 | 🟢 阻止（无工具） | 🟢 阻止 |
| 提示词注入执行命令 | 🔴 成功 | 🟢 阻止（无工具） | 🟢 阻止 |
| 恶意文件写入 | 🔴 成功 | 🟢 阻止（无工具） | 🟢 阻止 |
| 工具漏洞利用 | 🔴 主机受损 | 🟡 有限损害 | 🟢 容器隔离 |
| 资源耗尽攻击 | 🔴 主机崩溃 | 🟡 有限影响 | 🟢 容器配额 |

### 对现有功能的影响

**1. 周报生成功能**

| 功能 | 影响 | 解决方案 |
|------|------|----------|
| 读取工作日志文件 | ⚠️ 需要 workspaceOnly 内 | 将日志放在 workspace 内 |
| 执行 git 命令 | ⚠️ 需要 exec 工具 | messaging profile 不允许 |
| 创建周报文档 | ⚠️ 需要 write 工具 | messaging profile 不允许 |
| 发送飞书消息 | ✅ 允许 | message 工具可用 |

**结论：** 使用 messaging profile **会影响**周报生成，因为需要文件操作和命令执行工具。

**2. 飞书文档创建**

| 功能 | 影响 | 解决方案 |
|------|------|----------|
| 调用飞书 API | ⚠️ 需要 exec 或专用工具 | messaging profile 不允许 |
| 读取本地模板 | ⚠️ 需要 read 工具 | messaging profile 不允许 |
| 写入文档草稿 | ⚠️ 需要 write 工具 | messaging profile 不允许 |

**结论：** 使用 messaging profile **会影响**飞书文档创建。

**3. 知识库更新**

| 功能 | 影响 | 解决方案 |
|------|------|----------|
| 读取知识库文件 | ⚠️ 需要 read 工具 | messaging profile 不允许 |
| 写入更新内容 | ⚠️ 需要 write 工具 | messaging profile 不允许 |
| 执行索引脚本 | ⚠️ 需要 exec 工具 | messaging profile 不允许 |

**结论：** 使用 messaging profile **会影响**知识库更新。

**4. 推荐配置方案**

根据使用场景选择不同配置：

### 推荐的生产环境安全配置方案

#### 方案 A：开放群组/多用户环境（最高安全）

**适用场景：**
- 公共 Discord/Telegram 群组
- 多用户共享的 OpenClaw 实例
- 对外提供服务的聊天机器人

**配置：**
```bash
openclaw config set tools.profile "messaging"
openclaw config set tools.fs.workspaceOnly true
openclaw config set agents.defaults.sandbox.mode "all"
openclaw config set agents.defaults.sandbox.workspaceAccess "none"
openclaw config set agents.defaults.sandbox.docker.network "none"
```

**安全等级：** 🟢🟢🟢 最高  
**功能限制：** 仅消息通信，无文件操作/命令执行

---

#### 方案 B：个人助手 + 群组安全（平衡方案）⭐推荐

**适用场景：**
- 个人使用，但偶尔在群组中响应
- 需要文件操作和命令执行
- 希望保持较高安全性

**配置：**
```bash
# 使用 coding profile（允许文件和命令）
openclaw config set tools.profile "coding"

# 限制文件访问范围
openclaw config set tools.fs.workspaceOnly true

# 仅非主会话启用 sandbox（群组自动隔离）
openclaw config set agents.defaults.sandbox.mode "non-main"

# 工作空间只读访问
openclaw config set agents.defaults.sandbox.workspaceAccess "ro"

# 容器网络隔离
openclaw config set agents.defaults.sandbox.docker.network "none"
```

**安全等级：** 🟢🟢 高  
**功能保留：** 完整的文件操作和命令执行能力  
**群组防护：** 群组会话自动 sandbox 隔离

---

#### 方案 C：开发环境（功能优先）

**适用场景：**
- 纯个人使用
- 需要完整的开发工具链
- 信任所有输入源

**配置：**
```bash
# 使用 full profile（所有工具）
openclaw config set tools.profile "full"

# 仍建议限制文件访问
openclaw config set tools.fs.workspaceOnly true

# 可选：非主会话 sandbox
openclaw config set agents.defaults.sandbox.mode "non-main"
```

**安全等级：** 🟡 中  
**功能保留：** 完整功能  
**建议：** 仅在完全信任的环境使用

---

#### 方案 D：混合配置（多 Agent）

**适用场景：**
- 需要同时支持安全群组响应和个人开发
- 使用多 Agent 配置

**配置：**
```json5
{
  agents: {
    list: [
      {
        id: "main",
        default: true,
        tools: {
          profile: "coding"  // 主 agent：完整功能
        },
        sandbox: {
          mode: "off"  // 主 agent：无 sandbox（信任）
        }
      },
      {
        id: "group",
        tools: {
          profile: "messaging"  // 群组 agent：仅消息
        },
        sandbox: {
          mode: "all",  // 群组 agent：强制 sandbox
          workspaceAccess: "none"
        }
      }
    ]
  }
}
```

**安全等级：** 🟢🟢 高（群组）/ 🟡 中（个人）  
**功能：** 根据 agent 分配不同权限

---

### 配置检查命令

**查看当前配置：**
```bash
# 查看工具 profile
openclaw config get tools.profile

# 查看文件限制
openclaw config get tools.fs.workspaceOnly

# 查看 sandbox 配置
openclaw config get agents.defaults.sandbox.mode

# 查看完整配置
openclaw config show tools
openclaw config show agents
```

**安全检查：**
```bash
# 检查 sandbox 状态
openclaw sandbox explain

# 安全审计
openclaw audit security
```

---

## 📊 总结

### 核心发现

1. **tools.profile "messaging"**
   - 只允许 4 个消息相关工具
   - 移除所有文件操作和命令执行能力
   - 适合开放群组/多用户环境

2. **tools.fs.workspaceOnly true**
   - 限制文件访问在 workspace 目录内
   - 保护系统文件和用户隐私
   - 与 sandbox 形成纵深防御

3. **agents.defaults.sandbox.mode "all"**
   - 所有会话在 Docker 容器中运行
   - 隔离工具执行，限制爆破半径
   - 可配置资源限制和网络隔离

### 最佳实践

| 场景 | 推荐配置 | 安全等级 |
|------|---------|---------|
| 开放群组 | messaging + workspaceOnly + sandbox all | 🟢🟢🟢 |
| 个人 + 群组 | coding + workspaceOnly + sandbox non-main | 🟢🟢 ⭐ |
| 纯个人 | coding/full + workspaceOnly | 🟢 |
| 开发环境 | full + (可选) workspaceOnly | 🟡 |

### 最终建议

**对于大多数用户，推荐方案 B（平衡方案）：**
```bash
openclaw config set tools.profile "coding"
openclaw config set tools.fs.workspaceOnly true
openclaw config set agents.defaults.sandbox.mode "non-main"
```

**理由：**
- ✅ 保留完整的个人助手功能
- ✅ 群组会话自动隔离（sandbox）
- ✅ 文件系统限制保护系统安全
- ✅ 不影响周报生成、飞书文档、知识库更新
- ✅ 安全与功能的最佳平衡

---

**报告完成时间：** 2026-03-11 11:30 GMT+8  
**信息来源：** OpenClaw 官方文档、源码分析、配置审计
