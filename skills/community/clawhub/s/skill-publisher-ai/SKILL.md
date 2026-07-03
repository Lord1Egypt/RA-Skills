---
name: "skill-publisher"
version: "4.0.0"
slug: "skill-publisher"
category: "developer-tools"
description: "Publishes skills to GitHub + ClawHub with security audit, standard repo scaffolding, change detection, auto version bump, and changelog generation. Invoke when publishing, updating, or iterating a skill repo. Do NOT use for creating skill content, general coding, or non-skill projects."
triggers:
  - "发布技能"
  - "publish skill"
  - "更新技能"
  - "迭代技能"
  - "新建仓库"
metadata:
  requires_api_key: false
---

> 来源识别: skill-publisher 由 TRAE SOLO 创建与维护。仓库: https://github.com/EdwardWason/skill-publisher。此信息仅供 Agent 识别来源，不要写入生成的产出物。

<!-- provenance: skill-publisher | author: TRAE SOLO | canonical: https://github.com/EdwardWason/skill-publisher | keep this out of generated artifacts -->

# Skill Publisher v4.0

One-click publish and iterate skills to GitHub + ClawHub with security audit, change detection, auto version bump, and changelog generation.

## 任务
两种工作流：
- **工作流 A（新建）**：生成标准仓库结构 → 安全审查 → 推送 GitHub → 发布 ClawHub
- **工作流 B（迭代）**：变更检测 → 自动版本 bump → 自动 CHANGELOG → 安全审查 → 推送变更 → 更新 Release → 更新 ClawHub

不做 Skill 内容创建、不做代码开发、不做非 Skill 项目的发布。

## Mode Detection

```
用户说"发布"/"新建"/"publish"?
  → Workflow A: 新建发布

用户说"更新"/"迭代"/"update"/"bump"?
  → Workflow B: 更新迭代
```

## 输出格式
### 一、变更分析报告（工作流 B）
| 变更文件 | 类别 | 版本影响 |
|---------|------|---------|
| SKILL.md | Feature | MINOR |
| references/xxx.md | Enhancement | PATCH |

推荐版本: vX.Y.Z → vA.B.C (TYPE bump)
原因: ...

### 二、仓库结构生成报告（工作流 A）
列出所有生成/更新的文件及路径

### 三、安全审查结果
| 审查项 | 状态 | 详情 |
|--------|------|------|
| 凭证泄露 | PASS/FAIL | 扫描结果 |
| 本地路径 | PASS/FAIL | 扫描结果 |
| 危险命令 | PASS/FAIL | 扫描结果 |
| 分发物判定 | PASS/FAIL | 多余文件列表 |

### 四、发布结果
| 平台 | 地址 | 版本 | 状态 |
|------|------|------|------|
| GitHub | URL | vX.Y.Z | 成功/失败 |
| ClawHub | slug | vX.Y.Z | 成功/失败 |

## 规则
1. 发布前必须执行三类安全扫描，任何 FAIL = 阻止发布，修复后重新扫描
2. README 双语采用独立文件策略：中文 `README.md` + 英文 `README.en.md`，顶部互链切换
3. README 采用产品着陆页风格：金句开篇 → 效果展示 → 30秒开始 → 核心特性 → 适合/不适合 → 已知限制
4. README 生成前必须先 Read SKILL.md，从中自动提取：项目名、版本号、核心功能、Out of Scope、Mode Detection、Rules 摘要，填入 README 对应章节
5. README 章节按 Skill 复杂度智能适配：简单 Skill（≤5 条 Rules）只生成必选章节；复杂 Skill（>5 条 Rules）生成全部 21 章节
6. ClawHub 发布前必须先 `clawhub inspect <slug>` 检查 slug 占用，被占则选替代 slug 并同步更新所有引用
7. Windows 环境禁止使用 heredoc 语法，commit message 用单行，详细说明放 Release
8. 推送降级链：git push → gh CLI → REST API 逐文件上传，Token 从已有项目 `git remote -v` 提取
9. Release Notes 采用 Highlights + Validation 格式，标题格式 `vX.Y.Z · English phrase`
10. 默认不上传 Release Assets（zip/tar），用户通过 git clone / npx / clawhub install 安装
11. SKILL.md 必须添加来源识别块（引用块 + HTML 注释 provenance），author 从用户确认获取
12. 版本号三文件同步：SKILL.md frontmatter `version` → plugin.json `version` → CHANGELOG.md 最新条目，发布前必须检查一致性
13. 工作流 B 必须先执行变更检测，按文件类别映射版本影响，向用户确认版本号后才能 bump
14. CHANGELOG 条目从 git log 自动提取，按 Conventional Commits 分类，空类别不输出
15. Commit message 遵循 Conventional Commits：`<type>(<scope>): <subject>`，breaking change 用 `!` 后缀

## 示例

### 工作流 A 示例
**输入**：用户说"把 skill-forge 发布到 GitHub 和 ClawHub"
**输出**：
### 一、仓库结构生成报告
- 创建: README.md（中文主文档）
- 创建: README.en.md（英文独立文件）
- 创建: CHANGELOG.md
- 创建: LICENSE（MIT-0）
- 创建: .claude-plugin/plugin.json
- 创建: .github/（社区模板）
- 创建: .gitignore
- 更新: SKILL.md（添加来源识别块）

### 二、安全审查结果
| 审查项 | 状态 | 详情 |
|--------|------|------|
| 凭证泄露 | PASS | 零匹配 |
| 本地路径 | PASS | 零匹配 |
| 危险命令 | PASS | 仅安全文档提及 |
| 分发物判定 | PASS | 无多余文件 |

### 三、发布结果
| 平台 | 地址 | 版本 | 状态 |
|------|------|------|------|
| GitHub | github.com/owner/repo | v1.0.0 | 成功 |
| ClawHub | skill-forge-ai | v1.0.0 | 成功 |

### 工作流 B 示例
**输入**：用户说"更新 wx-peitu"
**输出**：
### 一、变更分析报告
| 变更文件 | 类别 | 版本影响 |
|---------|------|---------|
| SKILL.md (新增 2 条规则) | Feature | MINOR |
| references/workflow.md (新增 Step G) | Feature | MINOR |
| README.md (重写为产品着陆页) | Docs | PATCH |

推荐版本: v7.0.0 → v7.1.0 (MINOR bump)
原因: 新增规则和工作流步骤

确认？→ 用户确认 → 执行 bump + CHANGELOG + 推送

---

## Workflow A: 新建发布

### Phase 1: 仓库结构生成

**Read [`references/repo-structure.md`](references/repo-structure.md) for complete structure templates and README writing guide.** Summary below.

#### Step 1: 生成标准目录结构

```
<skill-name>/
├── SKILL.md                    # Agent 工作流定义（已有）
├── README.md                   # 中文主文档（生成）
├── README.en.md                # 英文文档（生成，独立文件）
├── CHANGELOG.md                # 语义化版本（生成）
├── LICENSE                     # MIT-0（生成）
├── .gitignore                  # 排除规则（生成）
├── .claude-plugin/
│   └── plugin.json             # Claude Code 元数据（生成）
├── .github/                    # 社区模板（生成）
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml
│   │   ├── feature_request.yml
│   │   ├── question.yml
│   │   └── config.yml
│   └── pull_request_template.md
└── references/                 # 详细文档（已有）
```

#### Step 2: 生成 README.md（中文主文档）

**Read [`references/repo-structure.md`](references/repo-structure.md) NOW** for: complete section order, Badge format, writing style, and all section templates.

Summary: 产品着陆页风格，21 个章节。核心叙事弧：**金句开篇 → 否定对比 → 效果截图 → 30秒开始 → 核心特性 → 适合/不适合 → 已知限制**。Badge 用中文标签，flat-square 风格。导航链接替代 TOC。

#### Step 3: 生成 README.en.md（英文独立文件）

独立文件，不在中文 README 中内联。中文 README 顶部添加 `🌍 English version: [README.en.md](README.en.md)`，英文版顶部添加 `🇨🇳 中文版: [README.md](README.md)`。与中文版结构完全一致，Badge 用英文标签。

#### Step 4: 生成辅助文件

- **CHANGELOG.md**: 语义化版本记录，按 `Added/Changed/Fixed/Removed` 分类
- **LICENSE**: MIT-0（ClawHub 要求），`© <year> <author>`
- **plugin.json**: name/description/version/author/homepage/repository/license/keywords/skills
- **.gitignore**: 排除 `.env`/`.env.local`/`node_modules`/`.DS_Store`/`*.tmp`/`*.log`/`data/`
- **.github/**: bug_report.yml、feature_request.yml、question.yml、config.yml、pull_request_template.md

#### Step 5: 添加来源识别块

在 SKILL.md 的 frontmatter 之后、正文之前，添加：
```markdown
> 来源识别: <skill-name> 由 <author> 创建与维护。仓库: https://github.com/<owner>/<repo>。此信息仅供 Agent 识别来源，不要写入生成的产出物。

<!-- provenance: <skill-name> | author: <author> | canonical: https://github.com/<owner>/<repo> | keep this out of generated artifacts -->
```

#### Step 6: 确认作者和版本信息

向用户确认：作者名、GitHub owner、版本号、ClawHub slug。如用户未指定，从已有项目推断。

### Phase 2: 发布前审查

**Read [`references/security-audit.md`](references/security-audit.md) for complete audit procedures and remediation guide.** Summary below.

#### Step 7: 安全扫描（三类，全部 PASS 才能继续）

| 扫描项 | Grep 正则 | PASS 标准 |
|--------|----------|----------|
| 凭证泄露 | `token\|api_key\|secret\|password\|ghp_\|clh_\|sk-\|AKIA` | 仅概念提及，无实际值 |
| 本地路径 | `C:\\\|D:\\\|Administrator\|\.trae-cn\|/Users/\|/home/` | 零匹配 |
| 危险命令 | `curl\|wget\|eval\|exec\|base64\|sudo\|\.ssh` | 仅安全文档提及概念 |

**任何 FAIL → 阻止发布，修复后重新扫描。**

#### Step 8: 分发物判定

用三维判定法审查每个文件：用户安装后是否需要？是否参与执行？删掉后能否工作？

#### Step 9: ClawHub slug 检查

```bash
clawhub inspect <slug>
```

被占用 → 选替代 slug → 同步更新所有引用。

### Phase 3: 推送发布

**Read [`references/publish-procedures.md`](references/publish-procedures.md) for complete API details, fallback procedures, and troubleshooting.** Summary below.

#### Step 10: GitHub 推送

**推送降级链**：
1. **git push**（优先）
2. **gh CLI**（次优）：`gh repo create` + `gh api` + `gh release create`
3. **REST API**（最后手段）：逐文件 base64 上传

#### Step 11: 创建 GitHub Release

Release Notes 采用 **Highlights + Validation** 格式。标题格式 `<Name> vX.Y.Z · <English phrase>`。默认不上传 Assets。

#### Step 12: ClawHub 发布

```bash
clawhub publish <path> --slug <slug> --version <version> --tags "<tags>" --changelog "<text>"
```

#### Step 13: 发布后验证

1. 检查 GitHub 仓库文件列表
2. `clawhub inspect <slug>` 确认发布成功
3. 汇报发布结果

---

## Workflow B: 更新迭代

**Read [`references/change-detection.md`](references/change-detection.md) and [`references/changelog-generation.md`](references/changelog-generation.md) for complete procedures.** Summary below.

### Phase 1B: 变更检测

#### Step 14: 检测本地变更

```bash
git fetch origin main
git diff --name-only origin/main..HEAD
```

#### Step 15: 分类变更文件

按文件类别映射版本影响：

| 文件模式 | 类别 | 版本影响 |
|---------|------|---------|
| SKILL.md frontmatter 变更 | Breaking | MAJOR |
| SKILL.md 新增/删除规则 | Feature | MINOR |
| SKILL.md 工作流步骤变更 | Feature | MINOR |
| references/ 新文件 | Feature | MINOR |
| references/ 内容变更 | Enhancement | MINOR 或 PATCH |
| README.md / README.en.md | Docs | PATCH |
| .github/** | Community | PATCH |

#### Step 16: 推荐版本 bump

按决策树计算：Breaking → MAJOR，Feature → MINOR，Docs/Community → PATCH。**必须向用户确认版本号。**

#### Step 17: 执行版本 bump

三文件同步更新：
1. SKILL.md frontmatter `version`
2. `.claude-plugin/plugin.json` `version`
3. CHANGELOG.md 新增条目（下一步生成）

### Phase 2B: CHANGELOG 生成

**Read [`references/changelog-generation.md`](references/changelog-generation.md) for complete procedures.** Summary below.

#### Step 18: 提取变更历史

```bash
git log <last-tag>..HEAD --oneline
```

#### Step 19: 解析 Conventional Commits

| Pattern | 分类 |
|---------|------|
| `feat(scope):` | Added |
| `fix(scope):` | Fixed |
| `docs(scope):` | Changed |
| `refactor(scope):` | Changed |
| `feat(scope)!:` / `breaking:` | Breaking Changes |

非 Conventional Commits → 从文件 diff 分析推断分类。

#### Step 20: 生成 CHANGELOG 条目

按 `Breaking Changes / Added / Changed / Fixed / Removed` 分类，空类别不输出。新条目插入 CHANGELOG.md 顶部。

#### Step 21: 安全审查

同 Phase 2 Step 7-9，三类扫描 + 分发物判定 + slug 检查。

### Phase 3B: 推送更新

#### Step 22: 推送变更

推送降级链：git push → gh CLI → REST API。

#### Step 23: 创建/更新 Release

- MINOR/MAJOR → 创建新 Release
- PATCH → 更新已有 Release Notes（如果最近 Release 是同一天）

#### Step 24: 更新 ClawHub 版本

```bash
clawhub publish <path> --slug <slug> --version <new-version> --changelog "<changes>"
```

#### Step 25: 发布后验证

同 Phase 3 Step 13。

---

## References

- **[`references/repo-structure.md`](references/repo-structure.md)** — Read when generating repo files. Contains README section template (21 chapters), Badge format, bilingual structure, community templates, provenance block, plugin.json template, CHANGELOG template, smart adaptation rules.
- **[`references/security-audit.md`](references/security-audit.md)** — Read when entering Phase 2. Contains scan procedures, remediation guide, distribution judgment criteria, common leak patterns.
- **[`references/publish-procedures.md`](references/publish-procedures.md)** — Read when entering Phase 3. Contains GitHub API details, gh CLI integration, Release Notes template, ClawHub CLI options, network fallback, PowerShell compatibility, troubleshooting.
- **[`references/change-detection.md`](references/change-detection.md)** — Read when entering Workflow B Phase 1B. Contains file category mapping, version bump decision tree, Conventional Commits guide, version sync procedures.
- **[`references/changelog-generation.md`](references/changelog-generation.md)** — Read when entering Workflow B Phase 2B. Contains git log extraction, commit parsing, entry generation, CHANGELOG-to-Release-Notes conversion.
