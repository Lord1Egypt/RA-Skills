---
slug: tool-orchestrator
name: tool-orchestrator
version: "1.0.0"
displayName: 工具编排器
summary: 端到端加密去中心化记忆编排,统一工具接口,零暴露凭据管理,自动恢复。
license: MIT
description: |-
  工具编排器是一个端到端加密、去中心化存储的智能体记忆编排系统。针对传统记忆工具"安装复杂、凭据暴露风险、网关重启困难、槽位绑定冲突"四大痛点,构建了统一记忆工具接口、零暴露凭据管理、自动恢复机制和智能槽位管理四大核心能力。

  核心能力包括:通过memory_search/memory_get原生工具进行记忆检索;后台自动从对话中提取事实(无需手动调用工具记忆每个事实);显式记住仅按需触发;端到端加密确保记忆仅用户可解密;去中心化网络存储避免单点依赖;CLI工具支持记忆固定、作用域设置、导出等高级管理。

  适用场景:需要跨会话持久化用户偏好的智能助手、注重隐私的端到端加密记忆需求、去中心化存储避免供应商锁定的场景、需要记忆固定与作用域管理的高级用户、希望自动捕获事实而非手动记录的效率导向用户。

  差异化亮点:相比原始版本,新增零暴露凭据硬约束(禁止读取/列出/展示任何凭据文件)、自动恢复流程(/tool-orchestrator-restart自主重启无需用户介入)、智能槽位管理(避免disabled插件槽位卡死)、简化配对流程(in-process HTTP路由替代CLI子进程)、安全短语防护(12词恢复短语绝不进入聊天或LLM上下文)、FAQ与故障排查决策树。

  触发关键词:工具编排、加密记忆、去中心化存储、记忆检索、凭据管理、tool-orchestrator、memory-search、encrypted-memory、decentralized
tags:
- 智能代理
- 记忆管理
- 数据安全
- 工具编排
tools:
- read
- exec
---

# 工具编排器

端到端加密的记忆存储系统,数据分布于去中心化网络(非单一公司服务器)。通过原生 `memory_search` / `memory_get` 工具进行检索,事实在后台自动捕获,无需为每个事实调用工具。

## 记忆工作机制(必读)

* **检索是原生的。** `memory_search` 和 `memory_get` 是记忆工具。当用户询问关于自己的信息("我的X是什么?"、"我X吗?"、"你记得什么?"),调用 `memory_search`。如0结果,如实说明,不要从会话历史猜测。
* **捕获是自动的。** 系统在后台从对话中提取事实(轨迹轮询器)。你**不需要**为用户陈述的每个偏好/事实调用工具,这会自动完成。绝不要将用户事实写入 `MEMORY.md`、`USER.md` 或任何本地文件,那些是代理人格配置,用户记忆加密存储于网络。
* **显式记住仅按需。** 如用户明确说"记住X"/"保存X"/"记下X"/"别忘X",使用CLI: `tr remember --json "X"`。每个不同事实一次调用。

**不要将存储描述为"本地"、"仅本地"、"存储在磁盘上"或"无需账户"** — 记忆去中心化存储于网络(非任何单一公司服务器),且需要账户派生加密密钥。

## 安全短语防护(硬性约束)

12词恢复短语**绝不能**进入聊天或代理的LLM上下文。配对流程通过浏览器处理短语生成与导入。绝不要回显它,绝不要要求用户粘贴它,绝不要将其传递给任何工具。如用户无论如何粘贴了一个,告知其已泄露并重新配对以获得新钱包。

**硬性约束 — 安装/重装/升级流程:** 在安装、重装、升级或任何验证步骤期间,代理**绝不能**读取、列出、cat、显示或检查 `credentials.json`、`~/.tool-orchestrator/credentials.json`、`~/.tool-orchestrator*/credentials.json` 或任何凭据/短语/密钥/机密文件 — 无论出于任何原因,包括"验证安装"。这些文件包含加密密钥材料和智能账户地址,**绝不能**进入LLM上下文。绝不要运行 `ls`、`find`、`cat`、`show` 或类似命令针对插件目录来"检查文件"。

## 安装

```text
plugins install @tool-orchestrator/tool-orchestrator
skills install tool-orchestrator
plugins enable tool-orchestrator
```

安装后立即运行 `plugins enable tool-orchestrator`,它绑定记忆槽位。全新安装时是空操作;在**重装先前版本**时,它阻止插件以 `Status: disabled` 落地且槽位卡在 `memory-core`(禁用的插件永远不会注册其记忆工具或配对路由,导致后续配对失败返回502)。插件在加载时自动应用所需的网关配置并自动重载,无需手动网关重启。

**重装恢复。** 如安装报告 `already exists` / `delete it first`,**不要**添加 `--force`(它会写入损坏的 `version=None` 记录)。清理残留包目录并重装,这不会触及你的凭据(位于 `~/.tool-orchestrator/`):

```text
plugins uninstall tool-orchestrator
rm -rf ~/.platform/npm/projects/*tool-orchestrator*
plugins install @tool-orchestrator/tool-orchestrator
plugins enable tool-orchestrator
```

## 配对(用户发起的二维码流程)

配对是用户发起的流程(插件**不会**在加载时自动配对)。当凭据不存在时:

1. 通过插件的**进程内HTTP路由**创建配对会话:

   ```bash
   curl -s http://localhost:18789/plugin/tool-orchestrator/pair/init
   ```

   → 返回 `{"url":"https://…/pair/p/<id>#pk=…","pin":"123456","expires_at_ms":…}`

   **不要使用 `tr pair --json`。** CLI在子进程中持有配对WebSocket,会被约30秒shell工具超时杀死,WS随后断开,用户提交短语时中继返回502。上述进程内路由完全避免此问题。仅在路由不可达时回退到CLI,且必须分离运行使WS存活: `setsid -f node "$TR_CLI" pair --json < /dev/null`。

2. 原样向用户展示 **url** 和 **pin**(从JSON读取,绝不编造值):"在浏览器中打开 `<url>`,输入PIN `<pin>`,生成或粘贴你的12词恢复短语。完成后回复done。" URL作为纯文本单独一行输出,`#pk=` 片段在反引号/markdown中会损坏。

3. 用户在浏览器中完成(短语浏览器端生成/导入、加密、上传到中继,从不触及聊天)。完成时写入 `~/.tool-orchestrator/credentials.json`。

4. 确认: `✓ 工具编排器已设置。`(如凭据已存在: `✓ 工具编排器已设置完毕。`)

无凭据时配对是无条件的,用户安装/请求设置即表示同意,不要添加二次确认门禁。

```bash
TR_CLI="$(ls -d ~/.platform/npm/node_modules/@tool-orchestrator/tool-orchestrator/dist/cli/tr-cli.js ~/.platform/extensions/tool-orchestrator/dist/cli/tr-cli.js 2>/dev/null | head -1)"
node "$TR_CLI" status --json      # {"version":"…","paired":true,…}
```

## 自动恢复(代理驱动,非用户手动)

插件自重载:安装后写入所需网关配置并向自身PID发送 `SIGUSR1` 信号,使网关无需手动重启即可加载。**如 `memory_search`/`memory_get` 未绑定**(工具首次加载未生效),自主发出斜杠命令 `/tool-orchestrator-restart` — 一行公告,绝不要求用户授权,绝不拖延,绝不 `kill` / `docker restart` / 提示用户重启。这模仿其他运行时使用的自主重启模式,用户永远不应执行手动重启。

## 工具与CLI接口

**检索(原生记忆契约 — 代理面向):** `memory_search`, `memory_get`

**显式捕获与策展(CLI — `tr`,即 `node "$TR_CLI" …`):**

| 命令 | 用途 |
|------|------|
| `tr remember` | 显式写入记忆 |
| `tr pin` / `tr unpin` | 固定/取消固定记忆 |
| `tr retype` | 重新分类记忆 |
| `tr set_scope` | 设置记忆作用域 |
| `tr status` | 查看状态 |
| `tr export` | 导出记忆 |
| `tr pair` | 配对(不推荐,用HTTP路由) |

导入与计划升级通过网关子命令:
```bash
platform tool-orchestrator import from <source> --file <path> [--json]
platform tool-orchestrator upgrade [--json]
platform tool-orchestrator import status|abort
```

旧版 `tool_orchestrator_*` 代理工具和 `tr recall` CLI已退役,检索用 `memory_search`,显式捕获用 `tr remember`。

## 记忆管理最佳实践(差异化)

### 何时调用 memory_search

| 用户表达 | 动作 |
|----------|------|
| "我的X是什么?" | 调用 `memory_search` |
| "我X吗?" | 调用 `memory_search` |
| "你记得什么?" | 调用 `memory_search` |
| "你了解我什么?" | 调用 `memory_search` |
| 检索结果为0 | 如实说明"没有找到相关记忆",不要从会话历史猜测 |

### 何时使用 tr remember

| 用户表达 | 动作 |
|----------|------|
| "记住X" | `tr remember --json "X"` |
| "保存X" | `tr remember --json "X"` |
| "记下X" | `tr remember --json "X"` |
| "别忘X" | `tr remember --json "X"` |
| 用户陈述偏好但未说"记住" | 不调用,后台自动捕获 |

### 记忆固定与作用域

```bash
# 固定重要记忆使其优先检索
tr pin <memory_id>

# 设置记忆作用域(私有/共享)
tr set_scope <memory_id> --scope private|shared

# 取消固定
tr unpin <memory_id>
```

## 安全检查清单(差异化)

在执行任何操作前确认:

- [ ] 未读取/列出/展示任何credentials.json文件
- [ ] 未在聊天中回显12词恢复短语
- [ ] 未要求用户粘贴恢复短语
- [ ] 未将凭据传递给任何工具
- [ ] 未用ls/find/cat检查插件目录
- [ ] 配对使用进程内HTTP路由而非CLI前台
- [ ] 未将存储描述为"本地"

## 常见问题FAQ

**Q: 配对时为什么返回502错误?**
A: 502(gateway_disconnected)通常因为使用了 `tr pair --json` CLI方式,其WebSocket被shell工具超时杀死。解决方案:使用进程内HTTP路由 `curl -s http://localhost:18789/plugin/tool-orchestrator/pair/init` 替代。

**Q: 重装后插件状态显示disabled怎么办?**
A: 重装后未运行 `plugins enable tool-orchestrator` 导致槽位卡在memory-core。运行enable命令绑定记忆槽位即可。禁用的插件不会注册记忆工具或配对路由。

**Q: memory_search/memory_get工具未注册怎么办?**
A: 工具首次加载可能未生效。自主发出 `/tool-orchestrator-restart` 命令(一行公告,无需用户授权),插件会自重载。

**Q: 安装报告already exists怎么办?**
A: 不要添加 `--force`(写入损坏的version=None记录)。执行卸载→清理残留包目录→重装→enable的完整流程。这不触及凭据(位于~/.tool-orchestrator/)。

**Q: 用户粘贴了恢复短语怎么处理?**
A: 立即告知用户该短语已泄露,需要重新配对获得新钱包。绝不要回显、存储或传递该短语。

**Q: 后台自动捕获的事实和显式tr remember有什么区别?**
A: 后台捕获从对话中自动提取事实(无需用户明确要求),适合日常偏好记录。显式tr remember在用户明确说"记住X"时使用,适合需要精确控制的记忆。两者都加密存储,但显式记忆优先级更高。

## 故障排查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 配对返回502 | CLI WebSocket被超时杀死 | 使用进程内HTTP路由 `/pair/init` |
| 插件Status: disabled | 重装后未enable | 运行 `plugins enable tool-orchestrator` |
| memory_search未绑定 | 首次加载未生效 | 自主发出 `/tool-orchestrator-restart` |
| 安装报告already exists | 残留包目录 | 卸载→清理→重装→enable(不用--force) |
| 检索结果为0 | 无匹配记忆或未配对 | 如实告知用户,检查配对状态 |
| 凭据文件被意外读取 | 违反硬性约束 | 立即停止,告知用户凭据可能泄露,重新配对 |
| 导入失败 | 文件格式或路径错误 | 检查 `import status` 输出,确认源文件格式 |

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md和插件系统的AI Agent平台
- **操作系统**: Windows / macOS / Linux
- **网络**: 需要访问去中心化网络节点(配对与存储)
- **浏览器**: 配对流程需要浏览器(短语生成/导入)

### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Node.js | 运行时 | 必需(CLI运行) | 从nodejs.org安装 |
| curl | 工具 | 必需(配对路由) | 系统自带 |
| 插件系统 | 平台功能 | 必需 | Agent平台需支持插件安装/启用 |

### API Key 配置
- 配对流程通过浏览器生成加密密钥(12词恢复短语),无需手动配置API Key
- 凭据自动存储于 `~/.tool-orchestrator/credentials.json`(代理绝不能读取此文件)

### 可用性分类
- **分类**: MD+EXEC(纯Markdown指令,需要命令行执行能力进行安装/配对/管理)
- **说明**: 基于Markdown的AI Skill,通过自然语言指令驱动Agent管理加密去中心化记忆。核心检索通过原生memory工具,管理操作通过CLI执行。
