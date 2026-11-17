# 版本号标准对比：SemVer、各生态策略、Conventional Commits、CalVer

> 说明：本文档是 `standards-comparison.md` 的**中文本地化镜像（可选副本）**。默认/权威版本为英文 `standards-comparison.md`，以该英文版为准。技能运行时输出跟随用户语言（en/zh）。

本文件汇总 `version-decide` 技能判定逻辑背后的**官方原文**。各小节中引用的规则均逐字取自下列标准（2026-10 核实）。

> ⚠️ **权威范围。** 带缩进的引用与规则表才是「标准本身」。凡是本技能偏离字面标准之处——尤其是 **0.x 采用 npm/Cargo 语义**（minor 即破坏边界）与 **`security` → patch 默认**——均明确标注为「**自定义实现策略（局部默认）**」。这些只是发版策略建议，**不属于任何标准**，不得当作规范性权威。发版前请自行确认生态特定假设。

判定流程见 `../SKILL.md`。

---

## 一、SemVer 2.0.0（语义化版本）

来源：https://semver.org/spec/v2.0.0.html

### 核心规则（原文要点）

| 条款 | 规则 |
|---|---|
| §2 | 版本号必须为 `X.Y.Z`，各段为非负整数，**不得含前导零** |
| §3 | 已发布的版本，其内容**不得再修改**；任何修改都必须作为新版本发布 |
| §4 | **0.y.z 为初始开发阶段。任何东西都可能随时改变，公共 API 不应被视为稳定** |
| §5 | 1.0.0 定义公共 API；此后如何递增取决于该 API 如何变化 |
| §6 | 仅引入向后兼容的 bug 修复时，递增 PATCH |
| §7 | 引入新的向后兼容功能时递增 MINOR；**任何公共 API 功能被标记为废弃时也必须递增 MINOR**；patch 归零 |
| §8 | 引入任何向后不兼容变更时递增 MAJOR；minor 与 patch 归零 |
| §9 | 预发布：`-` + 点分标识符，仅 ASCII 字母数字与连字符，数字段无前导零；**预发布优先级低于对应正式版** |
| §10 | 构建元数据：`+` 后内容**不参与优先级比较**，仅供溯源 |
| §11 | 优先级比较规则（见下） |

注意 §6/§7/§8 的适用条件都带 `(x > 0)` 限定——**这正是 0.x 阶段规范留白的地方**，
也是各生态自行填补分歧的根源。

### §11 官方优先级示例（必须逐项成立）

```
1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-alpha.beta < 1.0.0-beta
          < 1.0.0-beta.2 < 1.0.0-beta.11 < 1.0.0-rc.1 < 1.0.0
```

比较规则：① 主/次/修订按数值比；② 相同 core 时预发布低于正式版；
③ 预发布逐段左到右比，**纯数字段按数值、含字母段按 ASCII 序，且数字段优先级低于非数字段**
（故 `1.0.0-1 < 1.0.0-alpha`）；④ 前缀全等时，段数多者优先级更高。

### SemVer 官方 FAQ 对 0.x 的建议

> 最简单的做法是从 0.1.0 开始初始开发版本，之后每次发布递增 minor。

---

## 二、Conventional Commits 1.0.0

来源：https://www.conventionalcommits.org/en/v1.0.0/

### 结构

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### 与 SemVer 的映射

| 提交 | 对应级别 |
|---|---|
| `fix:` | PATCH |
| `feat:` | MINOR |
| footer 含 `BREAKING CHANGE:`，或 type/scope 后加 `!` | MAJOR |
| 其他类型（`build` `chore` `ci` `docs` `style` `refactor` `perf` `test`） | **无隐式影响** |

关键条文：破坏性变更**可以是任何 type 的一部分**（§3）；除 `feat`/`fix` 外的类型
"没有对 SemVer 的隐式影响"（§14）。

### 三个易被误用的 FAQ 答案

1. **0.x 阶段怎么办？** 官方原文建议："**假装产品已经发布**"——因为可能已经有人在用你的软件。
   这与 SemVer §4「可以随时改变」和 npm/cargo 的实际行为**直接冲突**（见第四节）。
2. **revert 怎么办？** 官方明确**拒绝定义**："Conventional Commits does not make an
   explicit effort to define revert behavior." 只建议用 `revert` type + `Refs:` footer。
3. **类型用错怎么办？** 合并前用 `git rebase -i` 改；发布后只能各工具自行处理。

---

## 三、各语言 / 生态的官方版本策略

### Python — PEP 440（**不是 SemVer**）

来源：https://peps.python.org/pep-0440/（PEP 本身标注为历史文档，权威规范现维护于
PyPA 的 Version specifiers）

规范形式：

```
[N!]N(.N)*[{a|b|rc}N][.postN][.devN][+local]
```

五段含义：

| 段 | 含义 |
|---|---|
| **Epoch** `N!` | 编号方式整体切换时使用（如从日期版 `2014.04` 切到语义版 `1!1.0`）。绝大多数项目不需要 |
| **Release** `N(.N)*` | 正式版本号，`1` / `1.4` / `1.4.2` 皆可；比较时短段补零，故 `X.Y` 与 `X.Y.0` 等价 |
| **Pre-release** `aN` / `bN` / `rcN` | **无连字符**：`1.0.0a1`、`1.0.0rc1` |
| **Post-release** `.postN` | 正式版之后的修订（如打包脚本修正） |
| **Dev-release** `.devN` | 预发布之前的开发快照 |
| **Local** `+label` | 下游集成分支的私有标记，**不改变版本类型** |

与 SemVer 的最大差异：**预发布不用连字符**。`1.0.0-rc.1` 会被规范化成 `1.0.0rc1`，
最终写进 PyPI 元数据、文件名和 lockfile 的是后者。手工写版本号时用 PEP 440 形式。

PyPA 官方 versioning 讨论页明确指出实践中的例外：**安全漏洞修复常常不得不包含
破坏性变更，却仍以 patch 版本发布**。

> ⚠️ **自定义实现策略（非标准）。** 本技能据此把 `security` 默认映射为 patch，
> 但这只是现实中的发版惯例，**并非** PEP 440 或 SemVer 的规则。`SKILL.md` 中要求对该场景额外确认。

### Rust — Cargo

来源：https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html

**兼容判定：最左非零段相同即为兼容**（与 SemVer「所有 pre-1.0.0 包互不兼容」不同）：

| 依赖声明 | 实际范围 |
|---|---|
| `1.2.3` | `>=1.2.3, <2.0.0` |
| `0.2.3` | `>=0.2.3, <0.3.0` |
| `0.0.3` | `>=0.0.3, <0.0.4` |

预发布默认**不匹配**，必须显式指定；且 `1.0.0-alpha` 不会自动升到 `1.0.1-alpha`。

### Go — 语义化导入版本（Semantic Import Versioning）

来源：https://go.dev/doc/modules/version-numbers

- **v2 起模块路径必须带主版本后缀**：`example.com/mod` → `example.com/mod/v2`。
  这是为了实现导入兼容规则：导入路径相同则必须向后兼容。
- v0 / v1 **不允许**后缀（`gopkg.in/` 例外，用 `.v2` 形式）。
- 好处：**不同主版本可在同一构建中共存**，解决菱形依赖冲突。
- 历史项目未加后缀却发过 v2 的，标记为 `v2.0.0+incompatible`。
- v0 与 v1 的关系：v1 多数情况下仍与最后一个 v0 兼容，**v1 是"承诺兼容"而非"相对 v0 破坏"**。

### Node.js — 运行时自身的版本策略

来源：https://nodejs.org/en/blog/announcements/evolving-the-nodejs-release-schedule

2026 年 10 月起改为**每年一个主版本**（4 月 Current，10 月转 LTS），
并新增 **Alpha 通道**（10 月至次年 3 月，6 个月），**Alpha 阶段允许 semver-major 变更**，
采用标准 SemVer 预发布格式（如 `27.0.0-alpha.1`）。此前是每年两个主版本、奇偶分 Current/LTS。

### CalVer（日历版本）

来源：https://calver.org/

`YY.MM.PATCH`（Ubuntu 24.10、pip 26.0.1、Black 26.3.1）、`YYYY.MM.DD`（yt-dlp 2026.08.19）、
`YY.MINOR`（Apple 自 2025 年起全线改为年份编号：iOS 26 / macOS 26 / Xcode 26）。

Neo4j 是最近的迁移案例：**2025 年 1 月起从 SemVer 切换到 CalVer**（`YYYY.MM.PATCH`），
并在 2025.06 把 Cypher 语言版本从服务端解耦、独立演进。

适用信号：发布节奏与日历强相关、支持周期需要一眼可辨、版本号要表达"新鲜度"而非兼容性。

---

## 四、标准间的冲突点（判定逻辑必须处理的地方）

| 冲突 | SemVer 2.0.0 | 实际生态行为 |
|---|---|---|
| **0.x 是否可随意破坏** | §4：可以随时改变，API 不稳定 | npm `^0.2.3` = `[0.2.3, 0.3.0)`、Cargo 同；**minor 递增就是破坏边界**。Composer（PHP）却把 `^0.2.3` 当 `[0.2.3, 1.0.0)`，更宽松 |
| **0.x 阶段的提交规范** | §4：不保证 | Conventional Commits 官方却建议"假装已发布" |
| **0.x 有无递增规则** | 无明确规定 | 学术研究（arXiv 2101.00836）实测 Cargo/npm/Packagist 均未严格遵循，且 0.y.z 发布频率并不比 ≥1.0.0 更高；大量项目长期不跨 1.0.0 |
| **废弃算哪级** | §7：必须 MINOR | 无争议 |
| **安全修复含破坏** | 未规定 | 实践中常以 patch 发版 |

> ⚠️ **自定义实现策略（非标准）。** 0.x 阶段本技能采用 **npm/Cargo 语义**（minor 即破坏边界）。
> 这只是策略选择：它贴合包管理器的实际解析行为、能真实保护依赖方，但 SemVer §4 本身对 0.x 未做规定。技能会在输出中显式提示，以免被误当作标准要求。
