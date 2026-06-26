# SprintX OpenClaw Handoff

这是 SprintX 的第一个公开 ClawHub skill 仓库。

这个 skill 只做一件事：帮助已有的 OpenClaw 用户，用当前最安全、最短的 proof packet 把 SprintX 接起来。

```text
sx auth
-> sx project use
-> sx event
-> sx artifact add
-> sx status
-> sx brief
```

它刻意保持很窄的边界。

- 没有自定义 MCP server
- 没有隐藏的 SprintX 自动化
- 不是通用自然语言 control plane
- 不在 skill 里创建项目

链接:
- ClawHub: https://clawhub.ai/terry3838/sprintx-openclaw-handoff
- GitHub: https://github.com/terry3838/SprintX-SKILL
- SprintX handoff quickstart: https://www.sprintx.co.kr/docs/getting-started/openclaw-handoff-quickstart
- SprintX CLI quickstart: https://www.sprintx.co.kr/docs/getting-started/cli-quickstart

## 为什么需要它

OpenClaw 用户本来就可以通过 SprintX CLI 完成连接。

真正的问题是第一次接入时的信息负担太高：

- 哪个命令先执行
- `projectId` 从哪里拿
- 什么算成功
- 半路失败后下一步该做什么

这个 skill 把这些内容压缩成一条面向 operator 的清晰流程。

不是增加魔法，而是减少混乱。

## 这个 skill 会做什么

1. 检查 SprintX 前置条件
2. 先确认本地是否已经有 `sx`
3. 优先使用 handoff card / handoff URL 里的 `projectId`
4. 只有在恢复场景里才使用 `sx project list`
5. 按正确顺序执行 proof packet
6. 用 `sx status` 和 `sx brief` 验证成功
7. 失败时给出明确的 rescue guidance

## 适合谁

适合：

- 已经在使用 OpenClaw
- 已经有 SprintX 账号
- 已经有 SprintX 项目，或者能在 Web 端创建
- 想走当前最安全的 handoff 路径，而不是追求大而全的集成

不适合：

- 想在聊天里创建 SprintX 项目
- 想直接通过 skill 做 task CRUD
- 想把 review / approval 流程也塞进来
- 想要 remote MCP server 方案

## 快速开始

### 1. 安装 skill

```bash
clawhub install sprintx-openclaw-handoff
```

如果你在非交互环境里，而且已经完成审核：

```bash
clawhub install sprintx-openclaw-handoff --force --no-input
```

### 2. 调用 skill

示例提示词：

```text
Use $sprintx-openclaw-handoff to connect my existing OpenClaw runtime to SprintX.
```

### 3. 执行 proof packet

```bash
sx auth
sx project use <project-id>
sx event --type runtime.started --summary "OpenClaw handoff started"
sx artifact add --title "first-log" --reference-uri "file:///tmp/openclaw.log" --content-type "text/plain" --summary "Initial OpenClaw evidence"
sx status
sx brief
```

## 前置条件

开始前你应该已经有：

- SprintX Web 登录会话
- 一个 SprintX 项目
- `/dashboard?handoff=1&projectId=<id>` 或 handoff card 的访问权限

如果 `projectId` 已经能看到，就直接使用它。

`sx project list` 不是默认第一步，只是恢复路径。

## 信任边界

- SprintX 不是 executor。OpenClaw 执行，SprintX 负责读取和治理。
- 默认认证路径是 browser-approved `sx auth`。
- access-token override 只作为 advanced / break-glass 用途。
- 这个 skill 明确禁止把 token 粘贴到聊天里。
- provider API key 不属于这个流程。

## Advanced Operators

支持 headless / CI 场景，但这不是主路径。

```bash
sx --headless auth
```

skill 也会提到 access-token override，但会刻意放在主 onboarding 路径之外。

## 仓库结构

```text
SprintX-SKILL/
├── SKILL.md
├── README.md
├── README.ko.md
├── README.zh.md
├── CHANGELOG.md
├── LICENSE
├── LICENSE.md
├── package.json
├── references/
│   └── source-of-truth.md
├── scripts/
│   ├── check-skill.mjs
│   └── check-contract.mjs
└── .github/workflows/ci.yml
```

设计原则：

- `SKILL.md` 是唯一的 operator truth
- `README*` 是给人看的
- `references/` 保存上游 source-of-truth 链接
- CI 只做验证，不做自动 publish

## 验证

```bash
npm run check
```

会检查：

- frontmatter 结构
- 真实需要的 runtime requirement
- install metadata
- license 是否存在
- command 顺序
- `sx project list` 是否仍然只是恢复路径
- token guidance 是否仍然是 advanced-only

## 发布

```bash
clawhub publish . \
  --slug sprintx-openclaw-handoff \
  --name "SprintX OpenClaw Handoff" \
  --version 0.1.3 \
  --tags latest \
  --changelog "Add localized READMEs and tighten metadata to match real requirements"
```

目前仍然保留手动 publish。

原因很简单：ClawHub 对 skill publish 的 CLI 路径最清晰，而 plugin/package 的 auto-publish 体系要更成熟一些。
