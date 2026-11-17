# 校验项明细（check-items）

> 配套技能：元守 yotta-publish-guard（零依赖 Python 3.8+）
> 本文档说明 `check` 各模式查什么、`pack` / `versions` / `names` 的判定口径，便于对接 CI 与排查。

## 1. 三档模式

| 模式 | 场景 | 必需 | 不强制 |
|---|---|---|---|
| full | npm + ClawHub 双渠道发布前 | SKILL.md / LICENSE / README.md / README.zh-CN.md / package.json | CHANGELOG.md（有则查版本，无则 WARN 建议） |
| github | 只推 GitHub | SKILL.md / LICENSE / README.md（英文） | README.zh-CN.md / package.json / CHANGELOG / NOTICE / publish.yml |
| self | 自用技能 | SKILL.md | 一切发布件 |

已有文件仍会被对应检查（如 github 模式下存在 README.zh-CN.md 也会查口吻）。

## 2. 通用检查项（三档都有）

- 目录名：小写连字符规范（`^[a-z0-9][a-z0-9-]{0,62}[a-z0-9]$`）。
- SKILL.md：存在；frontmatter `name` 与目录名一致；`description` / `version` / `license` 齐全。
- 安全家族 Defense Triple：显式安全技能，或未知外部技能名 / 描述命中安全关键词时，SKILL.md 须含 范围 / 授权 / 法律 声明
  （英文 Scope / authorized / legal 亦可）。已知非安全家族优先走排除集，避免“检测 / 审查”等通用词误报。
- 无残留占位符（双花括号模板变量，所有 .md/.json/.sh/.yml/.yaml）；技能自带 template/ 语料豁免。
- Markdown 代码围栏配对（三个反引号成对）。

## 3. README 检查（full / github 模式）

- 口吻黑名单（命中即 ERROR）：内部口语 / 指令措辞（别默认 / 咱们 / 你自己 / 严格记住 /
  别忘了 / 你必须 / 千万不要 / 切记 等）与「AI 帮你装」类安装引导。
- full 模式另查：README.md 含语言切换标识（`<b>Language</b>: English · 中文`）；
  README.zh-CN.md 存在且未放反（不应出现 Language=English 标识）；中英各含四方式安装
  （npx 一行装 / git clone / Download ZIP / install.sh），并禁用 npx skills 与 -g 安装推荐。

## 4. 版本五件（check 内联 + versions 子命令）

- package.json `version` ↔ SKILL.md frontmatter `version` 必须一致；
- SKILL.md 正文版本行（如「版本：0.2.1」存在）必须与版本一致（v0.2.1 新增）；
- CHANGELOG.md 顶部 `## vX.Y.Z` 与 package 一致（无标题则 WARN）；
- CLI 脚本 `VERSION = "..."` 常量一致（versions 子命令会列出 scripts/ 下所有 yotta_ 脚本）。

## 5. pack（npm pack --dry-run）

- 优先真实 `npm pack --dry-run --json`（--cache 指向可写临时目录）；npm 不可用本地回退列举
  （近似 .npmignore 规则）。
- 判定：包内无 .pyc / __pycache__；SKILL.md / LICENSE / README.md / README.zh-CN.md 四件在包内；
  NOTICE / CHANGELOG.md 存在于目录但未进包 → WARN（检查 package.json files 字段）。

## 6. names（三通道查重）

- npm：`npm view @yottameta/<slug> version`；404/ENOTFOUND → FREE。
- GitHub：`gh repo view YottaMeta/<slug>`；not found / 404 → FREE。
- ClawHub：`clawhub search --exact <slug> --limit 5`；无精确匹配 → FREE。
- 任一通道无法确认（网络 / CLI 不可用）→ 退出码 1，并输出三通道手动查重链接。
- 任一通道 TAKEN → 退出码 2（发布前必须改名或确认归属）。
- ClawHub 发布归属：`publish` 的 clawhub 命令默认 `--owner yottameta`（org handle），`--clawhub-owner` 可覆盖；勿漏传导致发布到 CLI 登录的个人账号。

## 7. 与元安 / 元审 / 元信聚合

`check --with-audit --with-vetter --with-verify` 会查找相邻技能目录 / 常见用户级技能目录下的
可选校验 CLI，跑一次并解析 JSON 摘要；未安装自动降级为「跳过」提示，不阻断。
