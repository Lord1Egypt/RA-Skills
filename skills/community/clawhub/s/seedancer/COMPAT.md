# COMPAT.md — seedancer ⇄ 本仓库规范 的映射与最小必要结构

> 依据：`agent/LOG/decisions/ADR-0004`（D1=a / D2=b）。**本副本非权威**，权威在源仓库/原件。

## 0. 基线（改动前的原点，必须记录）

| 项 | 值 |
| --- | --- |
| 源仓库 | **`https://github.com/taosiuman/seedancer.git`**（独立 git 仓库，非本仓库子目录） |
| 分支 | `master` |
| 基线提交 | `12c39a6ed54f321acc141807ffdc887fdfa810d6`（2026-09-24 06:08 +0800） |
| 提交信息 | `docs: sync version numbers to v8.0.0 across all documentation` |
| 提交数 / 标签数 | 23 / 11 |
| 工作区状态 | 干净（0 项未提交改动） |
| 基线 git 仓库（对比用） | `work/_baseline/seedancer.git`（原在技能目录内，v9 复审后移出） |
| 原件位置（WSL） | `\\wsl.localhost\OpenClawGateway\home\openclaw\.openclaw\agents\main\workspace\skills\seedancer` |

**⚠️ 已知事实**：`git` 命令在 `\\wsl.localhost\...` UNC 路径上**不工作**（返回空输出），
因此所有 git 操作必须在我这边的副本上做，或经 WSL 侧命令。
**⚠️ 反讽证据**：基线提交自称"把所有文档的版本号同步到 v8.0.0"，但审计（`REV-20261005-007`）证明
`README.md:11`、`docs/README-cn.md:11`、`LICENSE:4,60`、`SKILL.md:1438` 页脚、`release-notes.md:3`
**仍停留在旧版本** → 该提交**未达成其声明目标**。

## 1. 约定映射（D2=b：不套全套 `SKILL_STANDARD`）

| 本仓库标准（`SKILL_STANDARD.md`） | seedancer 现状（OpenClaw 约定） | 处置 |
| --- | --- | --- |
| `manifest.yaml` | `_meta.json`（YAML 内容 / `.json` 扩展名） + `VERSION` | **保留约定**；只做"格式合法性 + 与 frontmatter 一致性"检查，不改结构 |
| `SKILL.md`（frontmatter: name/description/…） | 同（另有 `license/author/version/attribution`） | 保留 |
| `prompt.md`（提示词正文） | 无（SKILL.md 正文即提示词） | **不新增**（D2=b） |
| `examples/example_01..03.md` | 无 | **不新增**；改为在 `references/INDEX.md` 标注"典型用法"指向已有文档 |
| `tests/test_*.md` | 无（仅 `SKILL.sh` 冒烟脚本） | **最小补充**：见 §2 |
| `CHANGELOG.md` | 有（+ `release-notes.md` + SKILL.md 内嵌日志，共三处） | 收敛为一处权威（`CHANGELOG.md`），另两处改为指针 |
| `repository` / `clawhub` 元数据 | 无 | **不新增**（发布动作未授权，`POLICY` §11 N1） |

## 2. 最小必要结构（只补这些，别的不动）

1. `references/INDEX.md`：48 篇的**唯一索引**（S3 阶段创建），含"何时必须加载"列（修 `REV-20261005-008` C-5 的 15 篇孤儿）
2. `scripts/check_consistency.py`（或 `.mjs`）：版本号多处一致 + 死链 + 索引覆盖率 + `_meta.json` 合法性
3. `tests/smoke.md`：可执行冒烟（`SKILL.sh` + 一致性脚本），附真实命令与退出码
4. `COMPAT.md`（本文件）：约定与基线的唯一说明

## 4. 已落地（S1–S6，v9.0.0 → v9.0.2）

| 阶段 | 内容 | 证据 |
| --- | --- | --- |
| S1 | `scripts/check_consistency.py` + 量化基线（5 FAIL + 2 WARN） | `seedancer_consistency_baseline.out` |
| S2 | LICENSE 归因补全（8 来源）· `_meta.json` 合法化 · frontmatter 字段 · 版本收敛 · 死链 10→0 · INDEX 建立 | `seedancer_consistency_s2*.out` |
| S3 | 48 篇 references 全部接线（《加载表》）；5 个硬门错误码归位；新增 `I3` 断言 | `seedancer_consistency_s3.out` |
| S4 | 入口去重（**S4 阶段实测** 56,037 → 41,213 字节；S6 内容恢复后为 43,243）；契约区白名单；**硬门锚点断言尚未引入**（`A1` 系 S6 新增 —— 此前本行误将 28 条锚点断言归到 S4） | `seedancer_consistency_s4*.out` |
| S5 | 版本 9.0.0 全链一致；CHANGELOG 含 v8→v9 迁移说明 | `seedancer_consistency_s5.out` |
| S6 | **按 `REV-20261005-009/010/011` 整改**：恢复 4 处丢失内容（`model-catalog.md` 新建、v7.1.0/v7.0.4 日志、提示词构建清单）；20 条加载行写进真实操作段落（取消 `(未定位)` 兜底）；**检查器重写为 v2**（M3 JSON 精确比较、M4 由 `_meta.upstream_sources` 推导、I1/I2/I3 集合精确 + 触发真实性、D1 修计量、**新增 A1 硬门锚点 28 条**、D2 契约锚点校验）；接入父仓库 CI | `seedancer_consistency_s6*.out` |

> **S6 复查基线**：`scripts/check_consistency.py` v2 = **14 项全绿**（唯一 WARN 为 K1 体积 42.1KB vs 目标 32KB）。
> **v9.0.2 / v3 复查基线**：`scripts/check_consistency.py` v3 = **16 项全绿（0 FAIL / 0 WARN）**。
> **G1 后（版本号仍为 9.0.2）**：`scripts/check_consistency.py` **v4 = 17 项全绿（0 FAIL / 0 WARN）**。
> **G2/G3'/A4 后（**v10.0.0**）**：**v5 = 19 项全绿（0 FAIL / 0 WARN）**，入口 **43,678 字节**（实测 2026-10-06，含 D7 的 5→2 重写）。
> **注**：5→2 去重使入口比 D7 **前**（43,600 字节）**微增 +78 字节**（指针比被删文本更啰嗦）—— 去重目标是**短语计数**，不是体积。
> 版本号 9.0.2 → **10.0.0**（MAJOR：新增**阻塞级** `A2`/`A4` + 入口规则改名 + 检查器 16 → 19 项）；发布范围见 `PLAN-20261006-001` **D3**（尚未发布到远端）。
> 四个数字分属不同阶段，**不是**同一时点的多项声明 —— 引用时请注明阶段。

## 3.1 检查器版本史

| 版本 | 说明 |
| --- | --- |
| v1 | 11 项；被 `REV-20261005-010` 证明 M3 空转、I1 与文档矛盾（OR）、I3 子串可骗、D1 计量错、白名单可包整份文档 |
| **v2** | 14 项；上述 5 处全部重写为**精确断言**；新增 `A1`（28 条硬门锚点）、`D2`（契约区锚点在目标文件逐字存在）与 `K1`（入口体积预算） |
| **v3** | 16 项；新增 `V3`（`skill-card.md` 版本戳 == 权威版本）与 `V4`（`skill-card.md` Publisher == `_meta.json.author`），补齐 `skill-card.md` 此前作为 V1 盲区的缺口（v9.0.2） |
| **v4** | 17 项；新增 **`A2`**（`SECTION_CONTENT` 7 节的**内容行**必须存在 + 标题在 2–6 级唯一 + 内容行数 ≥ 必需词数）；`D2` 接回此前**零引用**的 `CONTRACT_KEY_LINES`。配 `tests/attack_test.py`（**当时** 24 必拦场景 + 3 类显式已知漏检；**现行 31 必拦 + 24 已知漏检 + 7 类合法写法**）—— 见 `PLAN-20261006-001` 的 G1 |
| **v5** | **19 项**；**G2**：每个**检查组**开跑前向 **stderr** 打 `[RUN ] <编号> <说明>`（中断可见断点，stdout 契约不变）；**G3'**：新增 **`A3`**（规范枚举**顺序** —— 仅当某行**完整包含**全部规范键时校验其顺序；**WARN 级**，不阻塞构建）；**`A4`**（**文件内指针层级成立** —— `见 §主 · 子` 的主标题须唯一，子标题须为主标题范围内更深层级的标题，阻塞级。⚠️ **不保证"被指向的内容真的在那里"**，那是语义问题，字面判据表达不了）。**G3 原目标（「四项事实」5 处 → 2 处）已于 2026-10-06 执行**（用户决策 **D7 = 执行**）：保留 `{契约区注释, 定义节标题}`，把 `§核心硬规则` 第 7 条、`§门控 8` 条目、`§阶段五` 条目改为**文件内指针**（指向 §输出格式硬门）→ 短语计数 **5 → 2**，四要素定义与列举**零丢失**，检查器 **19/19 全绿**（复核 `REV-20261006-027`）|

## 3. 未决

- **装载器行为未验证**（OpenClaw 为 WSL 侧二进制，本机无可读实现）：
  `references/*.md` 是否会被自动注入上下文**未知**。
  → 因此采用保守设计：**硬门 100% 留在入口**，references 只承载详述（见 `REV-20261005-008` §4）
- 工作方式待用户确认（**D6**）：在本副本改后出 patch，还是直接在 `taosiuman/seedancer` 开分支（推荐后者）


## 7. 基线口径澄清（重要）

基线：**提交 `12c39a6`**（master HEAD，自述版本 8.0.0）；注意 `tag v8.0.0` = `46d668a` 是**更早**的提交，两者内容不同（出包与回写均以 12c39a6 为准）
