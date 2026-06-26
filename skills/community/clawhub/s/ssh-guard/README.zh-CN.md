# ssh-guard

[English](./README.md)

`ssh-guard` 是一个独立仓库，包含两部分内容：

- OpenClaw 插件源码入口：`index.ts` + `openclaw.plugin.json`
- 中英文两个插件实现：`index.zh-CN.ts` 和 `index.en.ts`
- 对应的 skill 定义：`SKILL.md`

它的目标很直接：任何包含 `ssh` 的命令执行前，必须先获得明确审批。

## 通道兼容性

| 通道 | 状态 |
|------|------|
| Telegram | ✅ 支持 |
| Feishu | ✅ 支持 |
| Mattermost | ✅ 支持 |
| Weixin | ❌ 不支持 |
| 其他 | 🔍 未验证 |

## 示例流程

当用户要求 OpenClaw 执行 SSH 命令时，`ssh-guard` 会先拦截，再强制进入明确审批流程。

拦截后的提示可以是这样：

```text
我需要执行一个 SSH 命令来查看远程机器的资源使用情况，请确认后我再继续。
```

```bash
sshpass -p '<REDACTED_PASSWORD>' ssh -o StrictHostKeyChecking=no <REDACTED_USER>@<REDACTED_HOST> "uptime && echo '---' && free -h && echo '---' && df -h"
```

```text
请回复以下任一内容授权：允许 / 同意 / 可以 / 批准
如需本会话内一律允许，请回复：我已知晓风险，本次会话一律允许
```

## 为什么

对 agent 来说，执行 `ssh` 的风险明显高于普通本地命令。一个命令就可能修改远端机器、带走数据，甚至把用户自己锁在系统外。

`ssh-guard` 的作用就是在这些命令真正执行前增加一道明确审批，不把 SSH 访问当成默认可随意执行的操作。

## 功能特性

- 在包含 `ssh` 的命令执行前统一拦截，直到用户明确批准
- 同时支持单次批准和会话内一律允许两种放行方式
- 审批状态只作用于当前会话，并可继承给子代理
- 会话结束或子代理结束后自动清理审批状态
- 通过 `index.zh-CN.ts` 和 `index.en.ts` 提供中英文审批提示
- 既可以作为可发布的 OpenClaw 插件仓库，也可以作为安装/配置引导 skill 的来源

## 工作原理

1. 插件监听 OpenClaw 的工具调用钩子。
2. 当检测到命令中包含 `ssh` 的执行请求时，先拦截这次调用。
3. 按当前选择的语言版本向用户发出明确审批提示。
4. 在获得批准后，只放行：
   - 一次 SSH 执行，或
   - 当前会话内后续所有 SSH 执行
5. 会话结束或子代理结束时自动清理审批状态。

## 快速开始

1. 先选择语言版本：
   - 中文：保持 `index.ts` 默认指向 `index.zh-CN.ts`
   - 英文：把插件入口改到 `index.en.ts`，或者让 `index.ts` 导出它
2. 在 `openclaw.json` 顶层设置 `session.dmScope`。
   - 不要给 `ssh-guard` 使用 `main`
   - 只从这两个值里选：`per-channel-peer`、`per-account-channel-peer`
   - 默认建议：`per-channel-peer`
3. 在 `openclaw.json` 里把这个仓库路径加入 `plugins.load.paths`。
4. 在 `plugins.entries` 里启用 `ssh-guard`。
5. 重启或重新加载 OpenClaw。

## 仓库结构

```text
ssh-guard/
├── index.ts
├── index.en.ts
├── index.zh-CN.ts
├── openclaw.plugin.json
├── SKILL.md
├── README.md
└── README.zh-CN.md
```

## 作为 OpenClaw 插件使用

在 `openclaw.json` 里把这个目录加入 `plugins.load.paths`，然后在 `plugins.entries` 中启用 `ssh-guard`：

```json
"plugins": {
  "load": {
    "paths": [
      "/absolute/path/to/ssh-guard"
    ]
  },
  "entries": {
    "ssh-guard": {
      "enabled": true
    }
  }
}
```

`ssh-guard` 依赖隔离型的 DM 会话路由，因此不要使用顶层 `session.dmScope: "main"`。

应当从下面两个值里选择：

- `per-channel-peer`
  OpenClaw 会把私聊 sessionKey 生成为 `agent:<agentId>:<channel>:direct:<peerId>`。
  这表示同一个人在不同渠道里会拥有彼此独立的私聊会话。也就是说，同一个用户通过 Telegram 和其他渠道来找你时，不会共用同一段私聊上下文。
- `per-account-channel-peer`
  OpenClaw 会把私聊 sessionKey 生成为 `agent:<agentId>:<channel>:<accountId>:direct:<peerId>`。
  这表示 OpenClaw 不只按渠道和用户隔离私聊，还会继续按接收消息的账号隔离。同一渠道下如果挂了多个账号，每个账号都会保留独立的私聊上下文。

对 `ssh-guard` 来说，通常默认推荐 `per-channel-peer`；如果同一渠道下有多个账号，则更适合选 `per-account-channel-peer`。

为什么 `main` 不支持：

- 在 `main` 下，OpenClaw 可能把私聊工具调用路由到 `agent:main:main`
- 但 `ssh-guard` 处理用户批准消息时，会按入站会话 id 取 key
- 这两边在私聊下可能对不上，导致批准无法绑定到被拦截的命令上

这个限制只影响私聊。群聊本来就会路由成 `agent:<agentId>:<channel>:group:<groupId>`，审批 key 会稳定落在群 id 上。

当前根入口 `index.ts` 默认重新导出英文实现 `index.en.ts`。
如果你想给中文用户使用中文审批提示，可以把插件入口改为 `index.zh-CN.ts`，或者把根入口切过去再加载。

## 作为 Skill 使用

把 `SKILL.md` 放进你的 skill 加载目录，或把整个仓库作为 skill 来源。触发后，agent 应优先帮助用户安装并配置这个插件，包括语言版本选择。
