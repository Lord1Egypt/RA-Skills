# 岐关车.skill

> 把「查岐关车班次、选车、复制微信下单链接」这件事，交给 CLI 和 AI Skill。

**珠海校区出发，少点开几层页面。**

[![npm version](https://img.shields.io/npm/v/qg-skill.svg)](https://www.npmjs.com/package/qg-skill)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Node.js 18+](https://img.shields.io/badge/Node.js-18%2B-green.svg)](https://nodejs.org)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-blueviolet)](SKILL.md)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-ff7a00.svg)](https://docs.openclaw.ai/tools/skills)

&nbsp;

`qg-skill` 同时提供两件东西：

- 一个全局命令行工具：`qg` / `qg-list`
- 一个 Codex / OpenClaw Skill：`qgcar-skill`

它可以查询岐关车班次，列出 `Code`，再用 `qg link CODE` 生成微信可打开的 `BusOrderWrite` 下单入口链接。

⚠️ **本项目只生成微信订单填写入口链接，不会自动提交乘客信息、不会保存身份证信息、不会代替你支付。**

[安装](#安装) · [使用](#使用) · [ai--openclaw-用法](#ai--openclaw-用法) · [支持路线](#支持路线) · [开发与发布](#开发与发布)

---

## 安装

### 一键部署

安装 CLI，并把 Skill 同时安装到 `~/.codex/skills/qgcar-skill` 和 `~/.openclaw/skills/qgcar-skill`：

```bash
curl -fsSL https://raw.githubusercontent.com/qybaihe/qg-skill/26ed8e31342968836b672d0ea7ab2a275361779c/install.sh | bash
```

脚本会优先从 npm 安装 `qg-skill`；如果 npm 包还没发布，会自动 fallback 到 GitHub 源码构建安装。

### 只安装 CLI

```bash
npm install -g qg-skill
```

安装后检查：

```bash
qg --help
qg routes
```

### 只安装 Skill

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/qybaihe/qg-skill ~/.codex/skills/qgcar-skill
```

OpenClaw 用户也可以装到：

```bash
mkdir -p ~/.openclaw/skills
git clone https://github.com/qybaihe/qg-skill ~/.openclaw/skills/qgcar-skill
```

如果你只安装 Skill，也需要确保机器上能运行 `qg` 命令：

```bash
npm install -g qg-skill
```

---

## 使用

### 1. 查今天可订班次

```bash
qg list --today --available
```

输出会包含 `Code`：

```text
Date: 2026-04-07

珠海中大岐关服务点 -> South Campus
Code  Line   Board  Arrive  From                To                       Price   Seats  Type    Status
----  -----  -----  ------  ------------------  -----------------------  ------  -----  ------  ---------
1     16:00  16:20  18:00   珠海中大岐关服务点  广中大南校区 岐关服务部  ¥40.00  34     direct  available
```

### 2. 用 Code 生成微信下单入口

```bash
qg link 1
```

复制到剪贴板：

```bash
qg link 1 --copy
```

### 3. 指定路线、日期、站点

```bash
qg list --start zhuhai --to south --station zhuhai --today --available
qg list --start zhuhai --to east --station boya --tomorrow --available
qg list --start south --to zhuhai --date 2026-04-10 --available
```

### 4. 不经过列表，直接按时间生成链接

```bash
qg link --start zhuhai --to south --station zhuhai --time 16:00
```

`--time` 支持匹配线路时间或实际上车时间，最终链接会使用对应站点的实际上车时间。

---

## AI / OpenClaw 用法

安装后一轮新对话里可以直接让 Codex 或 OpenClaw 帮你订票：

```text
Use $qgcar-skill to find a Qiguan bus from Zhuhai to South Campus today and generate a WeChat order link.
```

也可以自然语言说：

```text
帮我查今天珠海中大去南校区的可订班次，然后给我 16:00 那班的微信下单链接
```

OpenClaw 里可以这样说：

```text
让 OpenClaw 用 qgcar-skill 帮我查今天珠海中大去南校区的可订班次，并生成微信下单链接
```

Skill 会指导 AI 走安全流程：

```text
qg list ... --available
qg link CODE
```

不会自动提交订单或支付。

OpenClaw 可用性检查：

```bash
openclaw skills list
openclaw skills info qgcar-skill
```

---

## 支持路线

### Campus Key

| key | 含义 |
|---|---|
| `zhuhai` | 珠海校区侧 |
| `south` | 南校区 |
| `east` | 东校区 |

### 珠海站点

| key | 站点 |
|---|---|
| `zhuhai` | 珠海中大岐关服务点 |
| `boya` | 博雅苑 |
| `fifth` | 中大五院正门 |

默认规则：

| 命令 | 默认含义 |
|---|---|
| `qg list` | 今天，珠海中大 -> 南校区 |
| `qg --start zhuhai` | 今天，珠海中大 -> 南校区 |
| `qg list --start south` | 今天，南校区 -> 珠海中大 |
| `qg list --start east` | 今天，东校区 -> 珠海中大 |
| `qg list --start zhuhai --all` | 今天，珠海中大 -> 南校区和东校区 |

路线必须有一侧是 `zhuhai`，不支持 `south -> east`。

---

## 日期

不输入日期默认今天。

```bash
qg list --today
qg list --tomorrow
qg list --date 2026-04-10
qg list --date fri
```

日期限制为一周内。

---

## 项目结构

```text
qg-skill/
├── SKILL.md              # Codex Skill 入口
├── agents/openai.yaml    # Skill UI 元数据
├── references/qg-cli.md  # AI 使用 CLI 的详细参考
├── src/                  # TypeScript CLI 源码
├── dist/                 # 编译后的 CLI
├── install.sh            # 一键安装脚本
├── package.json          # npm 包配置
└── README.md
```

---

## 开发与发布

本地开发：

```bash
npm install
npm run build
npm link
qg list --today --available
qg link 1
```

发布到 npm：

```bash
npm login
npm publish --access public
```

也可以在 GitHub 仓库设置 `NPM_TOKEN` secret，然后手动触发 `Publish` workflow。

推送到 GitHub：

```bash
git remote add origin https://github.com/qybaihe/qg-skill.git
git push -u origin main
```

---

## 注意事项

- 这是非官方工具，接口和站点信息可能会变化。
- `priceMark` 会随查询刷新，所以建议先 `qg list`，再立刻 `qg link CODE`。
- 微信链接打开后仍需要你自己确认乘客、订单和支付。
- 不建议在 CLI 或 Skill 里保存身份证、手机号等乘客隐私信息。

MIT License © [qybaihe](https://github.com/qybaihe)
