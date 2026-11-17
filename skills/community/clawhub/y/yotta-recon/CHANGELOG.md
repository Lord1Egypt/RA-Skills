# Changelog

## v0.1.10 (2026-11-05)

- 质量门禁与打包文档修正；发布前测试接入。
- 发布门禁批次：发布工作流在 `npm publish` 前执行版本/发布面检查与 `npm test`；测试版本断言改为从 `package.json` 读取；补齐测试脚本。
- 打包与文档：发布包内容、CHANGELOG / README 与交付说明对齐；规则摘要与注册清单同步。

# 更新日志

## v0.1.9 (2026-11-01)

- 安装器 containment：目标根 / 嵌套链接 fail-closed；受管 Hub 链接解析真实目标；精简安装器同口径。

## v0.1.8 (2026-10-01)

- 安装器卫生批次：`bin/install.js` / `install.sh` 统一（未知参数报错 exit 2、`--help` / `--version`、残留清理白名单、嵌套载荷保留）；由模板单一真源渲染，接入漂移门禁。

## v0.1.7 (2026-09-19)

版本对齐维护：修复历史发布元数据与包内版本不一致；无功能变更。

## v0.1.6 (2026-09-13)

- 文档 hygiene 清理：移除历史公开文档中的内部表述，版本同步 0.1.6。
- 发布工作流 `.github/workflows/publish.yml` 纳入版本库，标签推送可触发 GitHub Actions。
- 发布包排除测试脚本与 Python 缓存，避免 `__pycache__` / `.pyc` 进入 npm 包体。

## v0.1.5 (2026-08-29)

- 安装方式统一为四方式（对齐发布规范 §3.3.1）：方式一 `npx -y @yottameta/yotta-recon --agent <name>` / `--dir <dir>`（推荐，走 npm 源）；方式二 `git clone https://github.com/YottaMeta/yotta-recon.git`；方式三 GitHub Download ZIP；方式四 `bash install.sh --agent/--dir/--list`。移除 `npx skills` 与 `-g` 推荐；中英双 README 安装节同步。
- 版本对齐：package.json / SKILL.md / CHANGELOG / 引擎 VERSION / 测试断言 / README 锚点 = 0.1.5。
- 无功能变更（仅文档与版本同步）。
## v0.1.4 (2026-08-28)

中英双语 README 对齐（英文门面 + 中文全档）：

- **README.md 改为英文**：作为 GitHub / npm / ClawHub 首页的英文门面（翻译 + 精简，覆盖定位 / 核心价值 / 命令 / 快速使用 / 安装 / 升级卸载 / 常见问题 / 相关技能 / 边界 / 开发校验全流程）。
- **新增 README.zh-CN.md**：原中文完整主文档整体平移，顶部加语言切换链接。
- **package.json**：description 改英文；files 加 README.zh-CN.md；版本 0.1.3 → 0.1.4。
- **ClawHub 分类**：按 §12 安全类统一 --categories security --topics security（历史单串 topic 遗留走网页后台整改）。
- 版本四处对齐：package.json / SKILL frontmatter / 引擎 VERSION / 文档。
- 边界（B 方案）：references / CHANGELOG / 测试注释不翻译；SKILL 触发描述保持中文。

## v0.1.3 (2026-08-26)

- **ClawHub 展示名 + 分类修正（三源重发）**：v0.1.2 发布到 ClawHub 时展示名未传 `--name`（默认成 `yotta-recon`，漏「元析」前缀），且 `--topics` 被误传成带空格的单个串，导致 ClawHub 把它存成单一 topic `security network recon`、界面连成 `#security-network-recon` 派生新分组。
- 本版修正：展示名显式传 `元析 yotta-recon`；分类用逗号分隔传 `--topics security,network,recon`，落回 `security` 分组下的三个独立 topic 标签（`#security #network #recon`）。
- 版本 0.1.2 → 0.1.3（package.json / SKILL.md frontmatter / 引擎 VERSION / 测试断言对齐）。
## v0.1.2 (2026-08-26)

- **ClawHub 补分类（三源重发）**：v0.1.1 发布到 ClawHub 时未传 `--categories`/`--topics`，导致技能在 ClawHub 落入 Uncategorized（无分组）；按 2026-08-26「ClawHub 发布必带分类」红线，本版重新发布并补上分类。
- ClawHub 分类：`security`（分组）+ topics `security, network, recon`；GitHub / npm / ClawHub 三源同步发布。
- 版本 0.1.1 → 0.1.2（package.json / SKILL.md frontmatter / 引擎 VERSION 对齐）。

## v0.1.1 (2026-08-26)

- 中文名统一为「元析」（去掉「（元征）」双名）：SKILL.md / README / package.json / 引擎 TOOL_CN 与 docstring / 测试断言 / NOTICE 同步。
- 版本 0.1.0 → 0.1.1（SKILL.md frontmatter + package.json + 引擎 VERSION 对齐）。

## v0.1.0 (2026-08-26)

YottaMeta 自有实现首版（网络侦察方向参考开源社区 network-security-scanner 类技能思路，已完全重写，零依赖）：

- **零依赖自研引擎**（scripts/yotta_recon.py，Python 3.8+ 标准库）：TCP connect 端口扫描（并发/限速/超时可调）+ 服务 banner 抓取 + 协议探测（HTTP / SSH / FTP / SMTP / POP3 / IMAP / Redis / MySQL / PostgreSQL / TLS / MongoDB）。
- **Scope Guard 授权纪律**：未授权目标默认拒绝（退出码 3）；回环地址默认放行；--scope 授权文件 / --assume-authorized --yes 显式授权；check-scope 授权预检；交互确认（AI 无输入自动拒绝）。
- **版本提取与已知风险提示**：内置风险映射（ProFTPD 1.3.5 / vsftpd 2.3.4 / 旧版 OpenSSH / Apache 等），只提示「请人工核实」，不提供利用细节。
- **三种输出**：文本表格 / JSON（stdout 纯净）/ Markdown 报告（scan_id + 时间 + 授权来源，操作留痕）。
- **本机清单**：local 子命令读取本机监听端口（Linux/macOS 读 /proc/net/tcp；Windows 用系统 netstat 只读查询）。
- **测试**：scripts/test_yotta_recon.py 61 项全绿（解析 / Scope Guard / 真实本地服务指纹 / 输出 / CLI 退出码）。
- **文档**：SKILL.md / README.md / references（scope-guard / service-fingerprints / protocol-probes）/ assets/banner.png。
- 版权：YottaMeta 纯自有 MIT + NOTICE 品牌声明。
