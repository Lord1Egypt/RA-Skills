<p align="center"><b>Language</b>: <a href="./README.md">English</a> · 中文</p>

<p align="center">
  <img src="assets/banner.png" alt="yotta-chain banner" width="100%" />
</p>

<h1 align="center">yotta-chain · 元链 (Yuanlian)</h1>

<p align="center">YottaMeta 的零依赖供应链依赖校验引擎：本地解析 npm / Python / Maven 的依赖清单与锁文件，检测<b>依赖混淆、lockfile 不一致、缺失锁文件、未固定版本、typo-squat</b>，并生成 <b>SBOM-lite（CycloneDX 1.5 子集）</b>。</p>
<p align="center">触发场景：构建 / 发布 / CI 前检查项目依赖是否存在供应链风险、核对锁文件与清单是否一致、排查依赖混淆暴露面、生成 SBOM。</p>
<p align="center">纯 Python 3.8+ 标准库实现，零外部依赖，Windows + Linux + macOS 通用；纯本地离线——不做在线 CVE 比对、不查询公共包仓库、不发送任何数据。</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue" /></a>
  <a href="https://agentskills.io/"><img alt="Standard: agentskills.io" src="https://img.shields.io/badge/standard-agentskills.io-orange" /></a>
  <a href="https://www.npmjs.com/package/@yottameta/yotta-chain"><img alt="npm package" src="https://img.shields.io/npm/v/@yottameta/yotta-chain" /></a>
  <a href="https://github.com/YottaMeta/yotta-chain"><img alt="GitHub stars" src="https://img.shields.io/github/stars/YottaMeta/yotta-chain" /></a>
  <a href="https://github.com/YottaMeta/yotta-chain/commits/main"><img alt="last commit" src="https://img.shields.io/github/last-commit/YottaMeta/yotta-chain" /></a>
  <a href="https://github.com/YottaMeta/yotta-chain"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
</p>

## 这是什么

供应链攻击瞄准的是开发者默认信任的部分：依赖混淆（私有包名被攻击者在公共仓库同名抢占）、typo-squat 仿冒包、过期或被手工改动的锁文件、缺失完整性哈希。元链把「供应链排查」打包成零依赖引擎，**本地**读取你的清单与锁文件——不需要 Trivy / Snyk / npm audit。

它与任何平台无关，是智能体无关的工具包，支持 Agent Skills 的智能体都能调用。**纯本地离线**——不做在线 CVE 比对、不查询包仓库、不发送任何数据。

## 核心价值

- **零依赖引擎**——npm semver + PEP 440 版本范围判定、TOML / JSON / requirements 解析器，全部用 Python 3.8+ 标准库实现。
- **依赖混淆**——.npmrc 里配置了私有仓库的 scope 却从公共仓库解析；同一包被多个仓库解析；可疑仓库地址（http / IP 字面量 / 本机）；pip extra-index 与 poetry secondary 源造成的公共回退。
- **lockfile 一致性**——清单条目在锁文件缺失、锁定版本超出声明范围、根 name / version 不一致、悬空引用、缺 integrity、同版本多来源冲突。
- **卫生**——缺失锁文件、未固定版本（`*` / `latest` / 无约束）、Maven SNAPSHOT 依赖。
- **typo-squat**——依赖名与知名 npm / PyPI 包编辑距离 ≤ 2 时提示人工复核。
- **SBOM-lite**——CycloneDX 1.5 子集 JSON（components + dependencies + purl，scope / direct / resolved / integrity 作为属性）。
- **三种输出**——text / JSON / CSV，外加 `--gate` 退出码闸门供 CI 使用。

## 为什么用它

| 优势 | 说明 |
|---|---|
| **零依赖** | Python 3.8+ 标准库；无常驻服务 / 数据库 / 外部扫描器；Windows + Linux + macOS |
| **纯本地离线** | 只解析已存在的清单 / 锁文件；不做在线 CVE 比对、不查询仓库、不发送任何数据 |
| **确定性信号** | 仓库配置 vs 实际解析来源、版本范围数学（npm semver / PEP 440）、完整性存在性——不是随机 URL 清单 |
| **CI 友好** | `scan --gate high` 只在达到指定严重度时退出 1 |
| **教学层** | 每条规则都带中文直白解释与修复提示 |

## 命令

| 命令 | 用途 |
|---|---|
| `scan` | 校验项目目录（自动识别 npm / python / maven） |
| `sbom` | 生成 SBOM-lite（CycloneDX 1.5 子集 JSON 或文本） |
| `version` | 显示版本 |

`scan` 退出码：**0** = 未发现达到 `--gate` 级别的风险；**1** = 有发现；**4** = 用法 / 路径 / 无受支持清单错误。默认 `--gate=info`（任何发现即退出 1）；CI 可用 `--gate high` 收紧。

## 快速使用

Windows 用 python，Linux/macOS 用 python3。

```bash
# 扫描当前项目（自动识别 npm / python / maven）
python3 scripts/yotta_chain.py scan --path ./

# 只看 medium 及以上，JSON 输出
python3 scripts/yotta_chain.py scan --path ./src --level medium --format json

# CI 闸门：达到 high 才退出码 1
python3 scripts/yotta_chain.py scan --path . --gate high; echo $?

# 生成 SBOM-lite（CycloneDX 1.5 子集 JSON）
python3 scripts/yotta_chain.py sbom --path . --output sbom.json

# 文本形式查看 SBOM
python3 scripts/yotta_chain.py sbom --path . --format text

# 版本
python3 scripts/yotta_chain.py version
```

## 安装

以下四种方式任选，顺序即推荐优先级；技能文件一律从 **npm** 获取（GitHub 无代理较慢，npm 支持镜像）。

### 方式一：npm 一行装（推荐）

```text
# 可选国内加速：npm config set registry https://registry.npmmirror.com
npx -y @yottameta/yotta-chain --agent <智能体名称>      # 装到指定智能体默认用户级技能目录
npx -y @yottameta/yotta-chain --dir <智能体的技能目录>  # 指到技能目录本身（如 ~/.codex/skills）
```

- `--agent <name>` 自动装到该智能体默认用户级目录；`--list` 可查看各智能体默认目录。
- `--dir <路径>` 装到指定的技能目录；未收录的智能体用 `--dir` 指到它的技能目录。
- npmmirror 未同步新包（404）：加 `--registry=https://registry.npmjs.org/`（国内需代理），或稍等镜像缓存。

### 方式二：git clone（开发者 / 有 git 环境）

```text
git clone https://github.com/YottaMeta/yotta-chain.git <智能体的技能目录>/yotta-chain
```

### 方式三：GitHub 下载压缩包（手动 / 无 git 环境）

在 GitHub 仓库 `YottaMeta/yotta-chain` 点 **Code → Download ZIP**，解压后把 `yotta-chain` 文件夹放进智能体技能目录。

### 方式四：install.sh（多智能体一键脚本）

```text
bash install.sh --agent <name>   # 装到指定智能体默认用户级目录
bash install.sh --dir <path>     # 装到指定目录
bash install.sh --list           # 列出智能体 -> 默认目录
```

> 方式一走 npm 源（npmmirror / npmjs），不依赖 GitHub；方式二 / 三走 GitHub，国内无代理可能失败。
## 让智能体使用

给智能体下指令即可，例如：

```text
发布前用 yotta-chain scan --gate high 扫一遍仓库，按严重度汇总发现并给出修复建议。
```

智能体会运行引擎、按严重度汇报发现，并用 `references/rules.md` 里的中文说明逐条解释。

## 检测规则

| 规则 | 严重度 | 说明 |
|---|---|---|
| `confusion_scope_registry` | high | .npmrc 为某 scope 配置私有仓库，锁文件却从公共仓库解析（依赖混淆） |
| `confusion_mixed_registry` | high | 同一包被解析自多个不同仓库主机 |
| `lockfile_missing_entry` | high | 清单声明的依赖在锁文件中缺失 |
| `lockfile_range_unsatisfied` | high | 锁定版本不满足声明范围（npm semver / PEP 440） |
| `lockfile_dangling_ref` | high | 锁文件某包依赖的包不在锁文件包列表 |
| `lockfile_duplicate_conflict` | high | 同名同版本存在多个不同 resolved / integrity 来源 |
| `missing_lockfile` | medium | 声明了依赖但没有锁文件 |
| `lockfile_root_mismatch` | medium | 锁文件根 name / version 与清单不一致 |
| `lockfile_integrity_missing` | medium | 锁文件条目缺少 integrity / 哈希 |
| `confusion_extra_index` | medium | pip / poetry / pipenv 同时配置公共仓库与私有源（公共成为回退源） |
| `confusion_suspicious_registry` | medium | 仓库 / 索引地址是 http、IP 字面量或本机地址 |
| `confusion_registry_mismatch` | medium | 配置了私有默认仓库，包却从公共仓库解析 |
| `unpinned` | low / medium | 依赖未固定版本（`*` / `latest` / 无约束） |
| `typosquat` | low | 名字与知名包编辑距离 ≤ 2，疑似拼写仿冒 |
| `snapshot` | low | Maven 依赖使用 SNAPSHOT 版本 |

## 支持的生态（v0.1.4）

- **npm** — `package.json` + `package-lock.json`（v1 / v2 / v3）/ `npm-shrinkwrap.json` / `yarn.lock` / `pnpm-lock.yaml` / `bun.lock` + `.npmrc`（作用域仓库映射）；
- **Python** — `requirements*.txt`（含 `--index-url` / `--extra-index-url` / `-r` 递归）、`pyproject.toml`（PEP 621 / poetry）、`poetry.lock`、`uv.lock`、`Pipfile` / `Pipfile.lock`；
- **Maven** — `pom.xml`（基础：未固定版本 / SNAPSHOT / 可疑仓库 URL / 属性与 dependencyManagement 解析）。
- `bun.lockb` 只识别不深度解析；`go.mod` / `Cargo.lock` 暂不支持。

JSON 扫描结果同时包含 `scannedFiles`（实际读取输入）与 `files`（产生发现的文件）。干净扫描可以出现 `files: []`，但 `scannedFiles` 仍会列出清单与锁文件。

## 边界

- 只读本地文件；不联网、不做在线 CVE 比对、不查询包仓库、不发送任何数据。
- 不做在线 CVE 比对——那是 Trivy / Snyk / npm audit 的地盘；本引擎提供本地确定性解析与启发式信号。
- 依赖混淆检测是**本地近似**：真正确认「私有包名被公共仓库抢占」需要在线核对，引擎给出强信号供人工复核。
- 只读不写：绝不改锁文件、不升级依赖。

## 开发与校验

```bash
python3 -m py_compile scripts/yotta_chain.py
python3 scripts/test_yotta_chain.py   # 52/52
```

## Changelog

版本历史见 [CHANGELOG.md](./CHANGELOG.md)。

## License

[MIT](./LICENSE)
