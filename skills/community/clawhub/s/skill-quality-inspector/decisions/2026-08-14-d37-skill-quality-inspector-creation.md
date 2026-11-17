# 2026-08-14 决策：新建 skill-quality-inspector 仓库（creation.md A 流程）

- **类别**：A 类新建仓库 / skills-repo-admin `workflows/creation.md` 步骤 A.1–A.11
- **触发**：用户要求"新开发一个仓库：技能质量检查官（检查质量/修复矛盾/评估风险/减少冗余/规范目录），用 skills-repo-admin 工作流程创建"。
- **仓库名**：`skill-quality-inspector`（kebab-case，领域名）；标题"技能质量检查官"；category `技能治理`；difficulty `进阶`；Level **A**。

## 1. skill-radar 搜索证据（creation.md Step 2 强制项）

用 `npx -y skills@latest find` 跑 4 组关键词（每组 rc=0），并用 WebSearch 补充：

| 关键词 | 命中（installs） | 领域相关性 |
|--------|------------------|-----------|
| skill quality | addyosmani/web-quality-skills@* (20K–44K)、addyosmani/agent-skills@code-review-and-quality (26.6K) | 多为**网页**质量 / **代码**评审，非技能仓库治理 → 离题 |
| skill audit | coreyhaines31/marketingskills@seo-audit (185.9K)、firebase/agent-skills@*-auditor (20K–92K)、trailofbits/skills@supply-chain-risk-auditor (5.9K) | 多为**第三方安全/SEO 审计**，目的是装前供应链安全，非内部仓库治理 → 离题 |
| prompt skill lint | cat-xierluo/legal-skills@skill-lint (82)、rheinmir/setup@lint (138) |  installs <500，且为通用 lint，非技能仓库质检 → 不合格 |
| skill review | firebase/agent-skills@firebase-basics (129.9K)、getsentry/skills@security-review (13.7K) | 安全评审 / 通用 review，非内部治理 → 离题 |

WebSearch 补充：`cyberuni/audit-skill`（SKILL.md 结构+安全审计，基于 OWASP Agentic Skills Top 10，无公开高 install 计数、非 skills.sh 高分）、`comeonoliver/skillshub/auditing-skills`（15 installs）、`aptratcn/skill-audit`（第三方安全扫描）。

**结论**：能命中"技能文件审计"的要么是**第三方供应链安全扫描**（目的不同：pre-install 安全，而非内部仓库的质量/矛盾/冗余/目录治理），要么是 **<500 installs 的通用 lint**。组织真正需要的"内部技能仓库治理"（矛盾修复、冗余治理、目录规范化）**无 ≥1K 社区等价物**。符合 creation.md 例外条款（搜索 3 组以上关键词、无合格社区技能）→ 全部 **original**，并在本文件记录证据。

## 2. Level 判定（A 完整型）

按 `superpower-architecture.md` 第 3 节与 `transform-superpower.md` 速查：
- 本技能有明确文件产物（质量报告、风险矩阵）与可脚本化的确定性任务（结构校验、跨文件一致性、断链/数字矛盾扫描、跨仓库重名检测）→ 倾向 A。
- 三个脚本均为真实、非 padding 的能力，且补充了组织现有两个门禁脚本**未覆盖**的跨文件一致性维度（孤儿/悬空路由、断链、数字对账、跨仓库冗余），非"为凑 A 硬造"。
- 故定 **Level A**（references≥3 / skills≥3 / scripts≥1 / assets≥1 均满足）。

## 3. 交付内容

- L3 子技能 ×5：`quality-auditor`、`contradiction-fixer`、`risk-evaluator`、`redundancy-reducer`、`directory-standardizer`（source.type 均为 original）。
- L2 references ×5：`quality-dimensions`、`contradiction-detection`、`risk-assessment`、`redundancy-reduction`、`directory-standardization`。
- L4 scripts ×3：`quality_audit.py`、`contradiction_scan.py`、`redundancy_scan.py`（stdlib-only，支持 `--help/--json/--strict`）。
- L5 assets ×2：`quality-report-template.md`、`risk-matrix.csv`。
- 根 `SKILL.md`（路由层，≤150 行无 TODO）、README（双安装命令 + 清单表）、AGENTS.md。

## 4. 脚本验证（D35 / W7）

构造 `tests/` 坏/好样本 + 跨仓库冗余样本，刻意注入缺陷并断言命中：
- `quality_audit.py`：GOOD 退出 0（全 pass）；BAD 命中 TODO / 缺 description / 缺 source / 孤儿 reference / 悬空路由 / 缺单技能安装命令（退出 1）。
- `contradiction_scan.py`：GOOD 无 findings；BAD 命中断链×3 / 重复标题 / 数字矛盾（5 vs 1）（退出 1）。
- `redundancy_scan.py`：sample_org 命中重名（shared-tool，fail）/ 近重描述 Jaccard 0.74 / 关键词重叠（api/rest/接口）（退出 1）。
- 三个脚本 `--help` 均正常（W7）。

## 5. 门禁

- `audit_architecture.py --repo skill-quality-inspector --strict` → 目标 Level A 达标（scripts 3 / assets 2 / refs 5 / skills 5）。
- `audit_readme_gates.py --repo skill-quality-inspector --strict` → 目标 error=0 / warning=0（双安装命令 + 清单表齐全）。
- 根 SKILL.md 行数 <150、无 TODO、`metadata.architecture: superpower`。

## 6. 发布与 registry

- 仓库独立 `git init` → commit → `gh repo create skills-repo/skill-quality-inspector --public --source . --remote origin --push`。
- `registry/repos.json`：新增条目（skills=5, architecture=superpower, level A），并**重算** summary / architecture_migration 计数（修正既有账实不符，不以旧数 +1）。
- 下游 `skills-lock.json` 未引用本仓库路径，无破坏风险。

## 7. 结论

按 admin 工作流程新建的治理类仓库，搜索证据支持全原创，Level A 由真实脚本化任务支撑；双门禁通过后发布并同步 registry。
