<p align="center"><b>Language</b>: <a href="./README.md">English</a> · 中文</p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-security-audit banner" width="100%" />
</p>

<h1 align="center">yotta-security-audit · 元安</h1>

<p align="center">YottaMeta 自有的 AI 技能供应链与系统安全扫描引擎：<b>检测技能恶意模式 · 扫描系统安全基线 · 审计学生数据隐私风险</b>，纯只读、零依赖、有纪律。适用于安装新技能前、定期审计已装技能、检查系统安全基线，以及在分享班级资料前排查学生个人信息。</p>
<p align="center">检测到安全审计 / 技能安全检查 / 恶意检测 / 供应链安全 / 系统安全基线 / 学生数据 / 学生个人信息 / 隐私扫描 / 校园数据合规 / scan skills / malicious skill / 扫描技能 等意图时自动激活；安装任何新技能前建议先运行——<b>不靠关键词碰运气，按待审计的目标判定</b>。</p>
<p align="center">Python 3.8+ 标准库实现，零依赖；Windows + Linux 通用；只读检测、报告默认脱敏、含授权与法律边界声明。</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-security-audit"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-security-audit" /></a>
  <a href="https://github.com/YottaMeta/yotta-security-audit"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-security-audit" /></a>
  <a href="https://github.com/YottaMeta/yotta-security-audit/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-security-audit" /></a>
  <a href="https://github.com/YottaMeta/yotta-security-audit"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## 这是什么

AI 技能正成为供应链攻击的新入口：一个「看起来正常」的技能，可能在安装期或运行期悄悄窃取凭据、外传数据、植入后门。元安把这类高危模式固化成 13 类检测器，并配合系统安全基线与学生数据隐私风险扫描，在安装前、运行中与资料分享前识别风险。

它不是某个平台的专属功能，而是一份与智能体无关的工具包：装进任何支持 Agent Skills 的智能体即可按需调用。只读检测、报告脱敏、绝不改动系统，也不需要常驻服务。

## 核心价值

- **三模式覆盖**：技能模式（默认）扫描 AI 技能目录；系统模式扫描系统安全基线（Windows / Linux 平台感知）；教育版扫描学生数据隐私风险（目录 / 成绩表 / 文档）。
- **威胁捕获模型**：8 检测点（供应链 / 命令执行 / 网络请求与数据外传 / 文件操作与敏感路径访问 / 提示注入 / 远程脚本下载执行 / 编码混淆 / 其他）+ 13 行为项；双视角报告（安全健康度评分 0-100）。
- **13 类检测器**：覆盖后门、凭据窃取、数据外传、持久化、供应链安装钩子、隐藏字符、高熵载荷等高危模式。
- **只读有纪律**：所有检测均为读取操作；系统模式也只运行只读命令，绝不执行修复、删除或查杀。
- **报告默认脱敏**：不输出私钥内容、环境变量值、完整凭据，只给路径、模式与建议。
- **学生数据不回显原文**：教育版只输出规则类别、位置、命中计数与脱敏样例，不提供明文回显选项。
- **自动发现技能目录**：扫描全部已装技能时自动发现 17 类智能体技能目录。
- **自扫不误报**：扫描器可扫描自身而不产生中高危误报（签名规则数据文件自动豁免）。

## 核心优势

| 优势 | 说明 |
|---|---|
| **检测器可解释** | 13 类检测器各有明确关注点与默认级别，命中即定位到具体模式与处置建议 |
| **平台感知** | 系统模式按 Windows / Linux 自适应，只读命令不写系统 |
| **分级退出码** | 0=干净 / 1=medium / 2=high / 3=critical / 4=错误，便于接入自动化与 CI |
| **规则可扩展** | 规则表位于 scripts/audit_rules.py，可用 --ioc-db 传入自有威胁情报 |
| **授权与法律边界** | 只允许审计已获授权目标；未经授权扫描他人系统违反《网络安全法》与《刑法》285/286 条 |
| **零依赖** | Python 3.8+ 标准库，无 daemon / 无数据库；Windows + Linux 通用 |
| **生态分发** | GitHub + npm 双源同步发布；npx / git clone / Download ZIP / install.sh 四种安装方式 |

## 功能体系

| 能力 | 说明 |
|---|---|
| 技能模式（--target skill） | 扫描 AI 技能目录，13 类检测器命中恶意模式；自动发现 17 类智能体技能目录 |
| 系统模式（--target system） | 系统安全基线扫描（启动项、计划任务、服务、防火墙、共享、权限点等） |
| 教育版（--target edu） | 学生数据隐私风险扫描（目录 / CSV / xlsx / docx）；--path 必填，报告一律脱敏 |
| 单目录扫描（--path） | 安装新技能前，先扫描其目录 |
| 报告输出 | 文本 + --json 结构化 + --report 生成 Markdown 报告 |
| 级别过滤（--severity） | 只报告 high 及以上 |

## 13 类检测器

| 检测器 | 关注点 | 默认级别 |
|---|---|---|
| DownloadExec | 下载后通过管道或落地文件交给 shell 执行 | critical |
| Obfuscation | 动态求值、编码字符串构造、base64 解码后执行 | high |
| Persistence | 定时任务、启动代理/守护、shell 配置、注册表启动项写入 | high |
| Exfiltration | 读取敏感文件后外传、打包上传 | high |
| CredentialTheft | SSH/云凭据/浏览器数据/钥匙串访问 | critical |
| NetworkCall | 反向连接、原始套接字、HTTP 客户端（多为上下文相关） | medium |
| PrivilegeEscalation | 权限位修改、setuid、加入管理员组 | high |
| SocialEngineering | 社会工程话术命名（文件名） | medium |
| Base64 | 超长 base64 编码串（解码含敏感关键字则升级） | medium→high |
| IOCMatch | 已知恶意 IP/域名/URL 模式/文件哈希 | critical |
| PostInstallHook | 安装期生命周期脚本（下载/执行为 critical） | high→critical |
| HiddenChar | 零宽字符与双向覆盖字符 | medium |
| Entropy | 高熵编码串（疑似混淆/加密载荷） | medium |

> 规则表位于 `scripts/audit_rules.py`（签名数据文件，自扫豁免），可用 `--ioc-db` 传入自有威胁情报。

## 教育版（--target edu）

教育版盘点学生数据放在哪、存了哪几类个人信息、是否存在出本机风险：

| 规则 | 关注点 | 默认级别 |
|---|---|---|
| EDU-ID-001 | 身份证号（18 位 + 校验位） | critical |
| EDU-ID-002 / EDU-ID-003 | 手机号 / 邮箱 | high / medium |
| EDU-ID-004 | 学籍号 / 考生号字段（字段驱动） | medium |
| EDU-QI-001..004 | 姓名+成绩组合 / 出生日期 / 家庭住址 / 家长联系方式 | high |
| EDU-SA-001..004 | 健康与身心状况 / 资助与家庭境况 / 生物识别 / 显式未成年人标记 | critical |
| EDU-HR-001..003 | 出本机路径 / 文件名疑似含姓名 / AI 工具与临时目录 | high / high / medium |

- 解析范围：CSV / TSV / TXT / MD / JSON / XML / HTML / YAML，以及 xlsx / docx（标准库只读轻解析）；PDF、图片、旧版 Office、压缩包不解析（不做 OCR），计入「未解析 / 跳过」；
- 脱敏固定可复算：身份证 / 学籍号 / 手机号保留末 4 位，姓名保留姓，地址保留前 3 个字符，邮箱保留首字符与域名；
- 不做学生年龄或身份推断、不做跨文件个体关联、不联网、不缓存原文；只扫描显式指定的 `--path`，不做自动发现；
- 规则包是只读 JSON，可用 `--edu-rules` 换成学校自备词表；详见 `references/student-data-scan.md`。

## 使用示例

```bash
# 扫描所有已发现的技能（17 类智能体目录）
python3 scripts/yotta_audit.py --target skill

# 扫描单个技能目录
python3 scripts/yotta_audit.py --path ./some-skill

# 系统安全基线（当前平台）
python3 scripts/yotta_audit.py --target system --platform auto

# JSON + 生成 Markdown 报告
python3 scripts/yotta_audit.py --path ./some-skill --json --report report.md

# 只报告 high 及以上
python3 scripts/yotta_audit.py --path ./some-skill --severity high

# 教育版：盘点一个班级资料目录
python3 scripts/yotta_audit.py --target edu --path ./班级资料

# 教育版：单文件 + JSON + Markdown 报告（报告不得写入被扫描目录）
python3 scripts/yotta_audit.py --target edu --path ./成绩表.xlsx --json --report ./edu-report.md
```

**exit code 语义**：0 = 干净 / 仅 low；1 = medium；2 = high；3 = critical；4 = 扫描器错误。

## 安装

以下四种方式任选，顺序即推荐优先级；技能文件一律从 **npm** 获取（GitHub 无代理较慢，npm 支持镜像）。

### 方式一：npm 一行装（推荐）

```text
# 可选国内加速：npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-security-audit --agent <智能体名称>      # 装到指定智能体默认用户级技能目录
npx -y @yottameta/yotta-security-audit --dir <智能体的技能目录>  # 指到技能目录本身（如 ~/.codex/skills）
```

- `--agent <name>` 自动装到该智能体默认用户级目录；`--list` 可查看各智能体默认目录。
- `--dir <路径>` 装到指定的技能目录；未收录的智能体用 `--dir` 指到它的技能目录。
- npmmirror 未同步新包（404）：加 `--registry=https://registry.npmjs.org/`（国内需代理），或稍等镜像缓存。

### 方式二：git clone（开发者 / 有 git 环境）

```text
git clone https://github.com/YottaMeta/yotta-security-audit.git <智能体的技能目录>/yotta-security-audit
```

### 方式三：GitHub 下载压缩包（手动 / 无 git 环境）

在 GitHub 仓库 `YottaMeta/yotta-security-audit` 点 **Code → Download ZIP**，解压后把 `yotta-security-audit` 文件夹放进智能体技能目录。

### 方式四：install.sh（多智能体一键脚本）

```text
bash install.sh --agent <name>   # 装到指定智能体默认用户级目录
bash install.sh --dir <path>     # 装到指定目录
bash install.sh --list           # 列出智能体 -> 默认目录
```

> 方式一走 npm 源（npmmirror / npmjs），不依赖 GitHub；方式二 / 三走 GitHub，国内无代理可能失败。
## 升级 / 卸载

- **升级**：重新安装最新版覆盖即可——重跑你用的安装命令（如 `npx -y @yottameta/yotta-security-audit --agent <name>` 或 `bash install.sh --agent <name>`）。技能目录内旧文件会被替换；不影响项目中其他文件。
- **卸载**：删除目标智能体 skills 目录下的 `yotta-security-audit` 文件夹（各智能体目录见上表）即可。卸载后本技能不再生效。

## 常见问题

- **会主动修复风险吗？** 不会。元安只读检测与报告，绝不执行修复、删除或查杀。发现风险应建议用户先隔离、停止使用，再人工复核。
- **只扫技能不够吗，为什么还要系统模式？** 恶意技能常通过启动项、计划任务、服务等持久化到系统。系统模式帮你检查这些基线点，双模式互补。
- **扫描别的机器合规吗？** 只允许对已获授权目标检测。未经授权扫描他人系统违反《网络安全法》与《刑法》285/286 条，使用者自行承担法律责任。
- **首次运行会不会误报？** 检测器按模式与上下文给级别，NetworkCall / 高熵 / URL 等多属上下文相关提示，需结合场景判断；扫描器自扫有豁免，不产生中高危误报。

## 相关技能

同属 YottaMeta 技能矩阵（安全家族）：[yotta-vetter](https://github.com/YottaMeta/yotta-vetter)（元审，安装前四阶段初审）先做来源→代码→权限→风险审查，发现 high 及以上会引导跑元安深度扫描；[yotta-memory](https://github.com/YottaMeta/yotta-memory)（元忆）负责跨会话长期记忆。

## 开发与校验

本项目内运行：`python tools/validate-skill.py yotta-security-audit`。

## 许可证

MIT © YottaMeta —— 详见 [LICENSE](./LICENSE)。品牌声明见 [NOTICE](./NOTICE)。
