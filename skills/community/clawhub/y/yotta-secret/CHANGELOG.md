# Changelog

## v0.2.4 (2026-11-05)

- 发布包排除测试脚本；发布前测试接入。
- 发布门禁批次：发布工作流在 `npm publish` 前执行版本/发布面检查与 `npm test`；测试版本断言改为从 `package.json` 读取；补齐测试脚本。
- 打包与文档：发布包内容、CHANGELOG / README 与交付说明对齐；规则摘要与注册清单同步。

## v0.2.3 (2026-11-01)

- 安装器 containment：目标根 / 嵌套链接 fail-closed；受管 Hub 链接解析真实目标；精简安装器同口径。

## v0.2.2 (2026-10-01)

- 安装器卫生批次：`bin/install.js` / `install.sh` 统一（未知参数报错 exit 2、`--help` / `--version`、残留清理白名单、嵌套载荷保留）；由模板单一真源渲染，接入漂移门禁。
- 自带安装器测试（`test/install.test.js`）更新为统一行为断言。

## v0.2.1 (2026-09-25)

安全修复：默认输出全遮 —— 只保留类型前缀。

- 背景：`mask_secret()` 保留首尾各 4 个字符（长密钥仍露出 8 位明文）；私钥块规则的 `snippet` 直接写入密钥正文前 200 字符；git 历史扫描的 `snippet` 是整行原文（ClawHub T09 High）。
- 修复：打码只保留可识别类型前缀（`ghp_` / `sk-` 等，最长 8 字符），其余一律 `****`；私钥块 `snippet` 只给 `[PRIVATE KEY REDACTED]`；git 历史 `snippet` 用打码后的命中片段重建。`--show-secret` 行为不变。
- 安装器加固：拒绝对符号链接目标写入、不做整目录删除。
- 回归：新增 4 项用例，测试 97/97 通过。

## v0.2.0 (2026-09-09)

- 评测完善批 2：新增 references/faq.md（12 条常见问题 + 速查索引 + 安装排障）；SKILL.md 增加 FAQ 速查节。
- 安装器错误处理：用法/目标/安装错误统一退出码与修复建议；新增 test/install.test.js。
- package.json 补 npm test 脚本；版本对齐 0.2.0（package / SKILL / CHANGELOG / CLI）。

## v0.1.2 (2026-08-29)

- 安装方式统一为四方式（对齐发布规范 §3.3.1）：方式一 `npx -y @yottameta/yotta-secret --agent <name>` / `--dir <dir>`（推荐，走 npm 源）；方式二 `git clone https://github.com/YottaMeta/yotta-secret.git`；方式三 GitHub Download ZIP；方式四 `bash install.sh --agent/--dir/--list`。移除 `npx skills` 与 `-g` 推荐；中英双 README 安装节同步。
- 版本对齐：package.json / SKILL.md / CHANGELOG / 引擎 VERSION / 测试断言 / README 锚点 = 0.1.2。
- 维护修复：generic 规则新增 URL 区间跳过（_inside_url），修复 URL 路径内高熵段误报（shields.io badge / git clone）；3 条回归测试，94/94 全绿。
- 无功能变更（仅文档与版本同步）。

## 0.1.1 (2026-08-28)

README 安装说明修复 + 围栏修复（三源同步重发）：

- **README.md / README.zh-CN.md 安装节重构**：移除 `npx -y @yottameta/yotta-secret --agent codex` 固定智能体安装行（违反安装规范：npx 用 -g 或 --dir，--agent 仅 install.sh 用），改为标准三方式（npm 一行 / install.sh / 手动复制 + 17 类智能体目录表）。
- **代码围栏修复**：中文 README 中单反引号伪围栏（`bash … `）改为标准三反引号 ```bash … ```（Markdown 渲染修复，线上 0.1.0 为坏版本）。
- 版本对齐：package.json / SKILL frontmatter / 引擎 VERSION / 测试断言 / CHANGELOG = 0.1.1。
- 无功能 / 引擎变更。

## 0.1.0 (2026-08-27)

- 初始版本：零依赖密钥 / 凭据泄露源头扫描引擎（Python 3.8+ 标准库）。
- 五类检测：cloud（AWS / Google / OpenAI / GitHub / Slack / Stripe / JWT 等 20+ 云厂商与 SaaS 规则）、
  private_key（PEM / PGP / OpenSSH / PuTTY 私钥块）、credential（口令赋值，含后缀式 key）、
  url_userinfo（URL 内嵌账号密码）、generic（高熵长 token）。
- 三重判定：正则格式 → Shannon 熵阈值 → 值级校验（纯哈希 / UUID / 占位符 / 示例值过滤）。
- 子命令：scan（文件 / 目录 / stdin / git 历史）、verify（单值判定）、mask（脱敏，与元史同源）、
  entropy（信息熵）。
- 输出：text / JSON / CSV；默认打码（--show-secret 才明文）。
- 测试：91/91 全绿。
