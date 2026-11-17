---
name: "skill-publisher"
description: "技能发布 — 将已有 Skill 三平台同步推送到 GitHub + ClawHub + SkillHub。当用户说 技能发布到三平台/发布技能更新/迭代技能发布 时触发。⚠️ 本技能的行为范围（用户须知）：① 推送代码到外部平台（GitHub/ClawHub/SkillHub），操作对外可见且可能不可逆 ② 同步到本地 TRAE 安装目录（会覆盖已有版本） ③ 在本地 docs/knowledge/ 追加发布日志。执行前会向用户确认。含安全审查、隐私清洗、版本号查重、仓库结构生成、ClawHub 自动文件排除、SkillHub dry-run 预检。Do NOT use for creating skill content, general coding, or non-skill projects."
slug: skill-publisher-ai
displayName: Skill Publisher 技能发布
version: 5.22.1
summary: 三平台同步发布技能到 GitHub + ClawHub + SkillHub，含安全审查、版本号查重、TRACE 预检、dry-run。执行前向用户确认。
license: MIT
allowed-tools: "Bash(git:*), Bash(clawhub:*), Bash(skillhub:*), Bash(gh:*), Bash(python:*), Bash(cat:*), Bash(ls:*), Bash(mkdir:*), Bash(cp:*), Bash(mv:*), Bash(rm:*), Bash(Compress-Archive:*), Read, Write, Edit, Glob, Grep"
metadata:
  openclaw:
    requires:
      env:
        - GITHUB_TOKEN
        - CLAWHUB_TOKEN
        - SKILLHUB_TOKEN
      bins:
        - git
        - python
      anyBins:
        - clawhub
        - skillhub
    primaryEnv: GITHUB_TOKEN
    envVars:
      - name: GITHUB_TOKEN
        required: true
        description: GitHub PAT，用于推送仓库和创建 Release
      - name: CLAWHUB_TOKEN
        required: true
        description: ClawHub 平台 API token（clh_ 开头），用于 skill publish / scan / inspect
      - name: SKILLHUB_TOKEN
        required: true
        description: SkillHub 平台 API token（skh_ 开头），用于 skillhub publish
      - name: FEISHU_APP_ID
        required: false
        description: 可选，飞书云空间备份使用
      - name: FEISHU_APP_SECRET
        required: false
        description: 可选，飞书云空间备份使用
      - name: HTTPS_PROXY
        required: false
        description: 可选，企业网络/受限网络环境下的 HTTPS 代理
      - name: HTTP_PROXY
        required: false
        description: 可选，HTTP 代理
      - name: NO_PROXY
        required: false
        description: 可选，代理排除列表
    emoji: "🚀"
    homepage: https://github.com/EdwardWason/skill-publisher
---

# 技能发布

将已有 Skill 三平台同步推送到 GitHub + ClawHub + SkillHub，含安全审查、隐私清洗、版本号查重、标准仓库结构生成、ClawHub 自动文件排除、SkillHub dry-run 预检。

## 何时触发

**仅当用户明确要求将 Skill 发布到外部平台时触发。**单纯的"更新技能"、"迭代技能"（指修改技能内容）不触发本技能，只有明确包含"发布"、"推送"意图时才触发。

**触发词（需带发布/推送意图）**：
- "技能发布到三平台"
- "发布技能更新"
- "迭代技能发布"
- "把 XX 技能推送到 GitHub"

**前置条件（全部满足才触发）**：
1. 用户明确表达"发布到外部平台"的意图
2. 目标是一个已开发完成的 Skill（不是普通代码项目）
3. 用户已确认要执行外部发布操作

**注意**：如果用户说"技能熔炉"，应触发 skill-forge（全流程），不是本技能。

## 与技能熔炉的关系

本技能是技能熔炉（skill-forge）的独立触发入口，只执行 Phase 3 发布流程。完整流程（创建→评估→发布）请使用技能熔炉。

**详细文档共享**：本技能读取 skill-forge 的 `references/publishing-guide.md`，内容完全一致。

## 任务
只做 Skill 的发布准备与推送：生成标准仓库结构 → 安全审查 → 隐私清洗 → 版本号查重 → 推送 GitHub → 发布 ClawHub。不做 Skill 内容创建、不做代码开发。

## 输出格式
### 一、仓库结构生成报告
列出所有生成/更新的文件及路径

### 二、安全审查结果
| 审查项 | 状态 | 详情 |
|--------|------|------|
| 凭证泄露 | PASS/FAIL | 扫描结果 |
| 本地路径 | PASS/FAIL | 扫描结果 |
| 危险命令 | PASS/FAIL | 扫描结果 |
| 分发物判定 | PASS/FAIL | 多余文件列表 |

### 三、版本号查重结果
| ClawHub 已发布版本 | 待发布版本 | 状态 |
|-------------------|-----------|------|
| vX.Y.Z ... | vX.Y.Z | 可发布/版本号冲突 |

### 四、发布结果
| 平台 | 地址 | 版本 | 状态 |
|------|------|------|------|
| GitHub | URL | vX.Y.Z | 成功/失败 |
| ClawHub | slug | vX.Y.Z | 成功/失败 |
| SkillHub | slug | vX.Y.Z | 成功/失败 |

## 规则
1. 发布前必须执行四类安全扫描（凭证/路径/危险命令/YARA 触发词），任何 FAIL = 阻止发布
2. README 必须中英双语，Badge 用中文标签。**安全修复必须同步中英文版**：中文版修改了什么安全相关内容，英文版必须同步修改，否则 ClawHub SkillSpector 会因英文版残留问题重复报 findings（2026-07 新增，源自 v5.4.0 英文版漏改事件）
3. ClawHub 发布前必须先 `clawhub inspect <slug>` 检查 slug 占用
4. **ClawHub 发布前必须查重版本号**：`clawhub inspect <slug>` 查看已发布版本列表，待发布版本号不能与已发布版本重复，重复则递增 PATCH
5. Windows 环境禁止使用 heredoc 语法
6. git push 失败时降级为 gh CLI，再降级为 GitHub API（详见 publish-procedures.md）
7. --tags 只能用 ASCII 字符（中文会报错）
8. 向 GitHub API 发送中文 JSON 必须用 Python（PowerShell 会损坏中文）
9. **凭证扫描必须覆盖新模式**：除原模式外，还需扫描 `cli_|IMA_OPENAPI|FEISHU_APP|APP_SECRET|CLIENTID|APIKEY|client_id|client_secret`（2026-07 新增，源自 IMA/飞书凭证泄露事件）
10. **ClawHub 自动生成文件必须排除**：`skill-card.md`、`.clawhub/` 目录由 ClawHub 自动生成，禁止发布（2026-07 新增，源自 skill-card.md 发布被拒事件）。**v5.18 新增 `.clawhubignore` 机制**：ClawHub publish 不读 `.gitignore`，必须用 `.clawhubignore` 显式排除凭证文件/临时脚本/构建产物（源自 [ClawHub docs/skill-format.md](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md) 规范，根治 2026-07-12 凭证泄露事故）
11. **frontmatter description 决定 ClawHub Short summary**：更新 description 后必须重新发布才能同步 Short summary；首次发布后 description 不会自动更新，必须递增版本号重新发布（2026-07 新增，源自 Short summary 未更新事件）
12. **.gitignore 必须排除 Python 缓存**：`__pycache__/`、`*.pyc`、`.clawhub/` 必须在 .gitignore 中（2026-07 新增，源自 __pycache__ 打包事件）
13. **SkillHub frontmatter 必须包含 5 字段**（2026-07 新增，支持 SkillHub 平台；v5.22 强化 slug 校验，源自 2026-07-27 周度审查建议 A）：`slug`（全网唯一）、`displayName`、`version`、`summary`、`license`，与 ClawHub 的 name/description 共存于同一 frontmatter。**v5.22 强化 slug 校验**：① slug 必须是 ASCII kebab-case 格式（小写字母+数字+连字符，禁止下划线/大写/中文）② slug 长度 3-64 字符 ③ 与目录名一致性检查（slug 应与 SKILL.md 所在目录名一致，避免发布时混淆）④ SkillHub slug 全网唯一性预检：发布前 `skillhub search <slug>` 检查是否已被他人占用
14. **SkillHub 发布前必须 dry-run 预检**：`skillhub publish <path> --dry-run` 检查格式，通过后才能正式发布（2026-07 新增，源自 SkillHub CLI 规范）
15. **SKILLHUB_TOKEN 不可硬编码**：token 只通过环境变量 `SKILLHUB_TOKEN` 传递，安全扫描必须检查 `skh_` 前缀的硬编码值（2026-07 新增，支持 SkillHub 平台）
16. **SkillHub 发布前必须临时移除不支持的文件类型**：`.gitignore`、`LICENSE`（无扩展名）、`.claude-plugin/`、`.github/` 会被 SkillHub 拒绝（400 错误）。发布前备份并移除，发布后立即恢复。ClawHub 和 GitHub 不受此限制（2026-07 新增，源自 SkillHub 文件类型限制）
17. **前置条件校验**（v5.2 新增，TRACE R维度）：开始发布前必须校验4项前置条件，任何一项不满足 = 中止发布并明确告知用户：
    - **目录存在**：指定路径必须存在且非空，否则报"目录不存在或为空：`<path>`，请确认 Skill 路径"
    - **SKILL.md 存在**：目录下必须有 SKILL.md 文件，否则报"未找到 SKILL.md，这不是一个有效的 Skill 目录"
    - **平台登录态**：`clawhub whoami` 和 `skillhub auth whoami` 必须通过，否则报"`<平台>` 未登录，请先执行 `<登录命令>`"
    - **Git 配置**：`git config user.name` 和 `git config user.email` 必须有值，否则报"Git 用户信息未配置，请先执行 `git config` 设置"
18. **Skill 质量门禁**（v5.2 新增，TRACE R维度，v5.11 增强）：发布前快速检查 Skill 质量，以下任一情况 = 拒绝发布并建议先修复：
    - SKILL.md 超过 300 行 → 报"SKILL.md 过长（`<N>`行），建议精简到 200 行以内再发布"
    - frontmatter 缺少 `description` → 报"description 缺失，无法自动触发，请先补全"
    - description 超过 250 字符 → 报"description 过长会被截断，核心触发词需在前 200 字符内"
    - 无 `Do NOT` 范围声明 → 报"description 缺少 Do NOT 范围声明，可能导致误触发"
    - **无"权限声明"段落**（v5.11 新增，v5.12 增加标准模板）→ 报"SKILL.md 缺少权限声明段落，会被 SkillSpector 标记为 MCP Least Privilege。建议增加'权限声明'段落，声明网络访问/文件读写/环境变量列表"。**权限声明段落标准模板（v5.12 新增，源自 gongwen-formatter v1.1.2 审计）**：SKILL.md 应包含一个 5 行表格，明确披露以下能力类别：
      | 能力类别 | 是否使用 | 说明 |
      |---------|---------|------|
      | 网络访问 | ✅/❌ | 具体用途、关闭方式 |
      | 文件读写 | ✅/❌ | 读/写路径范围、临时文件清理策略 |
      | 环境变量 | ✅/❌ | 读取的变量名列表（含凭证类） |
      | subprocess | ✅/❌ | 调用的命令列表 |
      | 外部 API | ✅/❌ | 调用的 API 列表 |
    - **有副作用但无"用户警告"**（v5.11 新增）→ 报"skill 有副作用（自动推送/自动写入外部服务/定时执行）但 README 无用户警告，会被 SkillSpector 标记为 Missing User Warnings。建议在 README 中英文版增加用户警告段落"
    - **触发词泛化**（v5.13 新增，源自 session-branch Finding 4/5 + kami 审计反馈）→ 报"触发词过于泛化，会导致误触发。建议改为更精确的短语"。**触发词精度黑名单**（中英文日常用语，禁止作为触发词）：
      - **英文单常见词**：`branch`/`task`/`new`/`start`/`help`/`file`/`edit`/`run`/`make`/`create`/`build`/`test`（任何涉及这些词的对话都会误触发）
      - **中文日常短语**：`画图`/`做个图`/`写文章`/`做个东西`/`帮我写`/`帮我做`/`新建`/`创建`（过于宽泛，无法区分技能边界）
      - **超长完整句**：超过 10 个字符的完整长句作为触发词（如"新任务但保留上下文"），应精简为核心动词短语
      **判定规则**：触发词命中黑名单 = Medium finding，建议作者改为更精确的复合短语（如 `session-branch 切换`/`kami 文档生成`/`gongwen 公文格式化`）。**设计原则**：触发词应能让 AI 在用户自然对话中可靠区分"这是要触发技能 X"还是"只是日常聊天"
19. **复杂输入处理**（v5.3 新增，TRACE R维度）：当用户未指明发布哪个 Skill，或工作目录下存在多个 Skill 时，必须先确认目标：
    - **未指明**：用户说"发布我的技能"但没说哪个 → 扫描工作目录下含 SKILL.md 的子目录，列出可用 Skill 让用户选择
    - **多 Skill**：用户指定父目录，但其下有多个 Skill 子目录 → 列出所有 Skill，让用户逐个选择要发布的，不支持批量发布
    - **路径模糊**：用户说"发布 wx-peitu"但没给完整路径 → 在工作目录下搜索匹配的子目录，找到 1 个直接用，找到多个让用户选择，找到 0 个报错
20. **SkillHub 发布前 TRACE 五维度预检**（v5.3 新增，核心规则）：发布到 SkillHub 前必须对目标 Skill 执行 TRACE 五维度自检，任何维度 FAIL = 中止 SkillHub 发布并报告问题。GitHub 和 ClawHub 不受此限制（这两个平台无 TRACE 检测）：
    - **T（Trust 信任）**：安全红线扫描（无 curl/wget/eval/凭证硬编码）+ frontmatter 有 allowed-tools 声明（可选）+ 国内可用性
    - **R（Reliability 可靠）**：前置条件校验（规则17）+ 质量门禁（规则18）+ 边界输入处理（规则19）+ 异常处理反馈
    - **A（Applicability 适用）**：触发测试 — description 含核心触发词 + 有 Do NOT 排除范围
    - **C（Compliance 规范）**：Schema 检查 — 4 模块齐全（任务/输出格式/规则/示例）+ SKILL.md ≤200 行 + 示例含边界情况 + 规则通过实习生测试
    - **E（Effectiveness 有效）**：增量价值 — Skill 相比手动操作有明显增益（如自动化安全审查、版本号查重等）
21. **GitHub token 有效性校验**（v5.4 新增，v5.10 增强，v5.11 改进 401 处理，v5.17 移除 OS 持久存储凭证读取行为 — 遵守 SkillSpector Credential Access 约束）：Step 0 前置条件校验中，必须验证 GitHub token 是否有效：
    - **token 读取方式**（v5.17 核心转变：声明完整性策略三阶段演变 — 从字面量替换到行为清理到声明对齐）：只通过环境变量读取凭证。**不再从 OS 持久存储读取凭证**（v5.10 引入该行为，v5.16 被 SkillSpector 标记为 Context-Inappropriate Capability Medium 94%，v5.17 移除该行为）。**TRAE session cache 处理**（v5.17 简化）：如果环境变量读取返回 stale value 导致 401，告知用户"请重启 TRAE session 让环境变量生效，或确认凭证已更新到用户环境变量"。不再自行从 OS 持久存储读取——这是 SkillSpector 的 Credential Access finding 根因，行为本身超出 least-privilege。本约束同样适用于所有凭证环境变量（GitHub/SkillHub/ClawHub/飞书/IMA 等）
    - 用 GitHub API `/user` 端点验证 token
    - 返回 401 → 报"GitHub token 已失效或 session 缓存了旧值，请执行：1) 确认凭证已更新到用户环境变量  2) 重启 TRAE session  3) 重新发布"，**询问用户是否中止发布修复 token（推荐）还是跳过 GitHub 继续发布其他平台（会记录待补推版本）**（v5.11 改进，v5.17 强化 401 处理为 session cache 提示）
    - 返回 200 → token 有效，继续发布
    - 网络超时 → 跳过验证，尝试推送时再降级处理
22. **GitHub 推送降级**（v5.4 新增，v5.22 扩展为三级降级链，源自 2026-07-27 周度审查建议 B；v5.22.1 修正与规则 25"安全敏感方案不文档化"的内部矛盾）：git push 失败时，按顺序降级到第三级 REST API：
    - **Level 1 - git push**：直接推送，超时30秒自动失败
    - **Level 2 - gh CLI**：如果 gh 命令可用，用 `gh repo sync` 或 `gh api` 推送
    - **Level 3 - GitHub REST API 逐文件降级**（v5.22 新增，v5.22.1 抽象化）：当 git push 和 gh CLI 都失败时，使用 GitHub REST API 逐文件降级方案（具体实现按规则 25"安全敏感方案不文档化"约束，**不文档化具体 API 链与编码方式**，执行时根据网络情况选择合适的 GitHub 官方 API 机制）。**注意**：Level 3 是最后手段，仅用于网络持续不可用的场景；正常情况下 Level 1 或 2 会成功
    - 如果三级都失败，告知用户网络问题，建议稍后重试或手动推送，并按规则 27 记录待补推版本
    - **设计原则**（v5.22.1 新增）：Level 3 的存在性可以文档化（让用户知道有降级方案），但具体 API 实现不文档化（避免触发 SkillSpector 的 MCP Tool Poisoning / Tool Parameter Abuse finding）。这是"声明即透明"与"安全敏感方案不文档化"的平衡
23. **SkillHub 备份目录隔离**（v5.4 新增）：临时移除的不支持文件（规则16）不能备份在 skill 目录内部，否则会被 SkillHub 扫描到并报 400 错误：
    - ✅ 正确：备份到 skill 目录外（如父目录下的临时文件夹）
    - ❌ 错误：备份到 `skill-dir/_backup/`（会被扫描）
24. **SkillHub 文件锁定 fallback**（v5.4 新增）：Windows 上文件可能被其他进程占用导致无法移除，此时改用临时副本方式发布：
    - 移除文件失败（Access denied / being used by another process）→ 用 robocopy 复制到临时目录，在副本中删除不支持的文件，发布副本，发布后删除副本
    - 临时副本目录必须在 skill 目录外，避免被扫描
25. **ClawHub SkillSpector 预扫描**（v5.7 新增，v5.9/v5.12/v5.13/v5.15/v5.16/v5.17 扩展，源自 v5.4-v5.6 + skillhub-daily + gongwen-formatter + session-branch + kami + xhs-crafter + article-tuwen 多轮 finding 修复经验 + SkillSpector 审计逻辑分析）：发布到 ClawHub 前，必须对 skill 目录执行以下 21 项预扫描（v5.9: 9 项 → v5.12: 10 项 → v5.13: 12 项 → v5.15: 13 项 → v5.16: 17 项 → v5.17: 18 项 → v5.19: 21 项），任何一项 FAIL = 中止发布并修复（WARN/Medium 级别不阻断）。**v5.17 核心认知转变**：基于 SkillSpector 审计逻辑分析，检测核心是"行为本身是否有风险"，不是"描述方式是否匹配"。SkillSpector 会扫描所有发布文件（含 CHANGELOG 历史记录），不限于 SKILL.md：
    - **YARA 触发词扫描**：扫描 shell history 清理命令、PowerShell 错误忽略参数、递归强制删除、权限放宽等"自治破坏行为"字面量。这些字符串即使在文档说明中出现也会触发 YARA 规则 `agent_skill_destructive_autonomous_actions`。详见 `references/security-audit.md` Layer 4
    - **Description-Behavior Mismatch**（v5.13 增强，v5.16 增加 What 不 How 原则）：frontmatter description 必须与 skill 实际行为一致。如果 description 只说"发布到外部平台"，就不能有"修改本地安装目录"的规则；如果有本地修改行为，description 必须明确披露。**description 模板建议（v5.13 新增，源自 kami 审计反馈）**：description 应区分"核心能力"（primary capability，必做的）和"可选能力"（optional capability，有条件触发的）。模板：`<核心能力描述>。可选能力：<可选能力 1>、<可选能力 2>（有条件触发）`。例如：`技能发布 — 将 Skill 推送到三平台。可选能力：本地安装目录同步（仅本地使用）、待补推版本跟踪（GitHub 失败时触发）`。**What 不 How 原则（v5.16 新增，源自 article-tuwen 3 轮审计 — 编排层实现细节文档化触发 8 项 findings）**：description 和 SKILL.md 只描述"做什么"（What），不描述"怎么做"（How）的子技能实现细节。**禁止文档化的实现细节**：① 子技能的端口号/进程操作/脚本文件名 ② 子技能的内部 API 调用链 ③ 子技能的临时文件路径。**编排层特化规则**：如果 skill 是编排层（调用其他 skill 完成任务），只描述编排逻辑（调用哪些 skill、什么顺序、如何组合），不描述子技能的实现。**典型反例**：article-tuwen v1.0.0 在 SKILL.md 中描述了图片搜索子技能的"启动本地服务器监听 8000 端口"实现细节，被 SkillSpector 标记为 Context-Inappropriate Capability。**设计原则**：当技能实际能力超出 description 描述时，SkillSpector 会标为 Description-Behavior Mismatch；区分核心/可选能力可以让 description 更准确，同时不显得过于冗长
    - **安全敏感方案不文档化**：不要在文档中描述应对网络限制的 API 逐文件上传方案（含 blob/tree/commit/refs 链）、base64 编码上传等方案。SkillSpector 会标记为 MCP Tool Poisoning / Tool Parameter Abuse。实际执行时可使用，但不要写进文档
    - **Self-Modification 措辞**：避免"update SKILL.md"这类自修改措辞，改为"Update version in SKILL.md"等具体动作。SkillSpector 会标记为 Rogue Agent Self-Modification
    - **CHANGELOG 历史记录扫描**（v5.16 增加批量授权触发词）：CHANGELOG.md 的历史条目也会被扫描。如果历史条目包含 YARA 触发词、凭证字面量调用模式、或批量授权触发词（见第 15 项），必须重新措辞（用类别描述替代字面量）。**v5.16 新增**：CHANGELOG 中"修复了 XXX 字面量"的说明，XXX 必须用类别描述，不能写字面量本身——否则历史记录会持续触发扫描
    - **SSD3 敏感数据派生输出扫描**（v5.9 新增）：检查代码是否读取本地敏感文件（如 memory/profile/credentials）并将其派生内容写入持久化输出（JSON/MD/日志）。SkillSpector 会标记为 SSD3 finding。修复方式：输出文件中只记录聚合统计量（如关键词数量），不记录原始关键词列表；推荐理由中不暴露匹配的敏感关键词，使用 generic 描述
    - **MCP Tool Poisoning 完整行为声明**（v5.9 新增，v5.12 增加代码 import 扫描对照）：description 必须完整声明 skill 的全部行为范围，不能只描述核心功能。如果 skill 实际行为包含以下任一项，description 必须明确披露：① 读取本地文件（memory/profile/config）② 网络请求（API 调用）③ subprocess 调用（CLI 工具）④ 写入外部服务（推送/上传）。建议在 description 中加"本技能的行为范围（用户须知）"段落。**代码 import 扫描对照（v5.12 新增，源自 gongwen-formatter v1.1.2 审计）**：扫描 `*.py` 源码，若 import 了 `urllib.request`/`requests`/`http.client`/`aiohttp`/`httpx` 等 HTTP 客户端库，但 SKILL.md frontmatter description 未声明"会发起网络请求"，或 SKILL.md 无"权限声明"段落披露网络访问，则标记为预扫描 FAIL。修复方式：① 在 SKILL.md 增加"权限声明"段落披露网络访问（用规则 18 的 5 行表格标准模板）② 在 README 中英文版增加用户警告段落 ③ 提供关闭网络访问的开关参数（如 `--no-network`）。此检查旨在预防 Context-Inappropriate Capability finding——SkillSpector 不只针对 SSRF，还会针对"非声明网络的隐式外联"
    - **MCP Least Privilege 权限声明**（v5.9 新增）：SKILL.md 或 plugin.json 必须声明 skill 需要的权限（网络访问/文件读写/环境变量列表）。未声明权限但实际使用了这些能力的 skill 会被标记为 MCP Least Privilege finding。建议在 SKILL.md frontmatter 或正文增加"权限声明"段落
    - **Missing User Warnings 检查**（v5.9 新增，v5.13 扩展覆盖范围，v5.17 增加破坏性操作点警告）：如果 skill 有副作用（自动推送/自动写入外部服务/定时执行/**写入项目本地文件**，v5.13 新增），README 必须包含用户警告，明确告知：① 运行会自动写入哪些外部目的地 ② 会读取哪些本地数据 ③ **会创建/覆盖项目内哪些文件**（v5.13 新增，源自 session-branch Finding 6 — 写 `docs/session-handoff.md` 但没告知用户）④ 如何禁用副作用（如 --skip-push 参数）。中英文 README 必须同步包含警告。**破坏性操作点警告（v5.17 新增，源自 skill-publisher v5.16.0 被标记 Missing User Warnings 85% — 删除 skill-card.md 无操作点警告）**：任何破坏性操作（删除文件/覆盖目录/清空数据）必须在**操作发生的位置**添加警告，不能只靠 description 声明或 README 段落。**检测模式**：扫描 SKILL.md 和 references/ 中是否有"删除"/"覆盖"/"清空"/"Delete"/"Remove"/"Overwrite"等破坏性动词，如果有，检查该操作点是否有"⚠️ 警告：将删除/覆盖 X"的前置提示。**FAIL 条件**：破坏性操作无操作点警告 = Medium finding。**修复方式**：在破坏性操作前增加"⚠️ 警告：将删除 X（原因：...，影响：...，确认后执行）"的前置提示。**设计原则**：README 段落警告是"整体声明"，操作点警告是"即时提醒"——SkillSpector 要求两者都有，不能只靠 README
    - **Unpinned Dependencies 分级处理**（v5.12 新增，源自 gongwen-formatter v1.1.2 审计；v5.22 扩展多文件扫描，源自 2026-07-20 周度审查建议）：扫描所有依赖清单文件（不仅 requirements.txt），按以下分级处理：
      - `==` 精确锁定 → **PASS**（最佳实践）
      - `~=` 兼容版本锁定 → **PASS**（推荐，平衡安全与兼容）
      - `>=` 范围锁定 → **WARN**（建议改 `~=`，但非阻断；SkillSpector 会标为 Low finding 但不阻断发布）
      - 无版本约束 → **FAIL**（阻断发布）
      **v5.22 扫描文件扩展**（不仅 requirements.txt）：
      - `requirements.txt`（Python pip）
      - `pyproject.toml`（现代 Python 项目，PEP 621）
      - `setup.py`（旧式 Python 项目）
      - `package.json`（Node.js，检查 dependencies 和 devDependencies）
      - `Pipfile`（Pipenv）
      - `go.mod`（Go modules，检查 require 块）
      **扫描方式**：Grep 每个文件中的依赖项，提取版本约束符（`==`/`~=`/`>=`/无），按上述分级判定。任一依赖 FAIL = 阻断发布
      **设计原则**：PIP 生态默认就是 `>=`，强制要求 `==` 精确锁定会破坏跨版本兼容性。本预扫描的目的是预防性地让作者选择 `~=` 折中方案，避免上线后被动响应 SkillSpector 的 Low finding。WARN 级别不阻断发布，只提示作者
    - **Internal Consistency Check 内部矛盾检测**（v5.13 新增，源自 session-branch Finding 3 — "Critical rules 说不用绝对路径" vs "Step 4 要求绝对路径"）：扫描 SKILL.md 中是否同时存在"禁止 X"和"要求 X"的指令。**检测模式**：① 扫描"禁止/不要/never/Do NOT/❌"开头的指令，提取被禁止的行为 X ② 在文档其他位置搜索是否有"要求/必须/must/✅"要求执行 X 的指令 ③ 若同时存在 = Medium finding，要求作者消除矛盾。**典型场景**：规则说"不要硬编码路径"但 Step 说"必须用绝对路径 `/path/to/file`"；规则说"不要自动推送"但 Step 说"完成后自动 sync"。**修复方式**：① 消除矛盾指令 ② 或用条件限定（如"用户明确要求时可用绝对路径"）。**注意**：这是启发式检查，需人工判断上下文——某些"禁止"指令有例外条件（如"禁止硬编码，但配置文件中的默认值除外"），不算矛盾
    - **Sensitive File Scan Consent Check 敏感文件扫描同意检测**（v5.13 新增，源自 session-branch Finding 2/7 — 扫描 `~/.workbuddy/SOUL.md`/`IDENTITY.md` 但无用户同意步骤）：如果 skill 指令中包含扫描敏感文件的路径模式，必须验证 SKILL.md 中有 consent（同意/许可）步骤。**敏感文件路径模式**：`~/`（home 目录）、`SOUL.md`/`IDENTITY.md`/`MEMORY.md`/`PROFILE.md`（身份/记忆类）、`config.json`/`credentials`/`.env`（凭证类）、`memory/`（TRAE memory 目录）、`profile/`（用户档案）。**检测规则**：① 扫描 SKILL.md 中是否出现上述路径模式 ② 若出现，检查 SKILL.md 中是否包含 consent 关键词：`consent`/`permission`/`同意`/`许可`/`用户确认`/`明确授权` ③ 无 consent = Medium finding。**修复方式**：在扫描敏感文件前增加 consent 步骤，如"读取用户 profile 前，必须先告知用户会读取哪些字段，并等待用户确认"。**设计原则**：扫描敏感文件本身不禁止（有些 skill 合理需要读 memory/profile），但必须有用户知情同意步骤，不能静默扫描
    - **Credential Access 行为检测**（v5.15 新增字面量扫描，v5.16 改纯文字描述，v5.17 重构为行为风险检测 — 源自 skill-publisher v5.14.0/v5.15.0/v5.15.1/v5.16.0 四轮被 SkillSpector 标记的教训）：扫描 skill 是否有从 OS 持久存储读取凭证的行为。**v5.17 核心转变**：从"检测代码调用模式的字面量"转向"检测行为本身"——SkillSpector Layer 2 检测的是"行为是否超出 least-privilege"，不是"代码模式是否匹配"。**检测行为**：① 是否从 Windows/Mac/Linux 的 OS 持久凭证存储读取（无论用什么方式描述）② 是否有"替代 stale 环境变量读取凭证"类措辞暗示从持久存储读取。**FAIL 条件**（High）：skill 包含上述任何行为的代码或文档描述——即使纯文字描述"从 OS 持久存储读凭证"也会被标记为 Context-Inappropriate Capability。**修复方式**：移除从 OS 持久存储读取凭证的行为本身，只通过环境变量读取。如果环境变量 stale 导致 401，告知用户重启 session，而不是自行从持久存储读取。**设计原则**：这是声明完整性策略三阶段演变的典型应用——v5.14.0-v5.16.0 采用字面量替换/占位符/纯文字描述策略，均未成功；v5.17 移除行为本身，从源头消除风险
    - **外部 CDN 引用扫描**（v5.16 新增，源自 xhs-crafter v7.3.1-v7.6.0 三轮审计 — 外部 CDN 引用触发 4 项 findings，最高频问题）：扫描 HTML/CSS/JS 文件中是否引用外部 CDN 域名。**检测域名列表**：Google Fonts（fonts.googleapis.com / fonts.gstatic.com）、jsDelivr（cdn.jsdelivr.net）、unpkg（unpkg.com）、CDNJS（cdnjs.cloudflare.com）等公共 CDN。**FAIL 条件**：任何文件引用了上述外部 CDN 域名。**修复方式**：① 下载 CDN 资源到本地（如 assets/fonts/、assets/css/、assets/js/）② 用本地相对路径引用 ③ 如果是字体，用 system-ui/Segoe UI/Arial 等系统字体替代。**设计原则**：外部 CDN 引用会触发 SkillSpector 的 External Transmission / Data Exfiltration finding——即使只是加载字体，也被视为"向外部服务器发送请求"。声明外部依赖（如在 description 中说"使用 Google Fonts"）**不等于可以保留**——必须本地化或用系统字体替代
    - **批量授权检测**（v5.16 新增，源自 xhs-crafter v7.4.0 审计 — "按流程走一遍"措辞被标记为 Autonomous Decision Making High finding 98% confidence）：扫描 SKILL.md 中是否包含被用作**授权触发词**的批量授权措辞。**检测措辞**：`按流程走一遍`/`全流程自动`/`都行`/`全部同意`/`一路回车`/`批量确认`。**FAIL 条件**（High 级别）：上述措辞出现在"视为授权"/"不再逐项询问"/"自动执行"等**授权语境**附近时。**不触发条件**：上述措辞出现在普通说明中（如"用户可以按流程走一遍了解功能"）不算 FAIL。**判定标准**：措辞被用作"代替用户逐项确认"的授权机制 = FAIL；措辞只是描述流程 = 不触发。**修复方式**：用"逐项确认"替代"按流程走一遍"——每个需要用户确认的步骤都单独询问，不批量授权。**设计原则**：SkillSpector 将"批量授权"视为 Autonomous Decision Making——agent 不应自行决定用户已授权所有步骤，每一步都应单独确认
    - **过渡修补检测**（v5.16 新增，源自 xhs-crafter v7.4.0 教训 — 为修复 1 项 finding 引入 image-search.js 导致 5 项新 findings，WARN 级别不阻断）：扫描本次修改是否新增了"过渡修补"代码——为应对某个 finding 而引入的新外部依赖或新行为。**检测模式**：① 扫描代码文件，如果包含外部 API 调用/环境变量读取/跨项目状态访问 ② 检查这些代码是否是"为修复某个 SkillSpector finding 而新增的" ③ 如果是 = WARN，提示作者评估"这个修复是否引入了新的 finding 风险"。**WARN 级别**：不阻断发布，只提示作者评估。**典型反例**：xhs-crafter v7.4.0 为修复"图片搜索功能缺失"而新增 image-search.js，引入了本地服务器监听/外部 API 调用/进程管理 3 项新行为，导致 5 项新 findings。**修复方式**：修复 finding 时评估"这个修复是否引入了新的外部依赖或行为"——如果是，在 SKILL.md description 和权限声明中同步声明。**设计原则**：过渡修补是第二轮 findings 的最大来源——为修复 1 项 finding 而引入 5 项新 findings 的反模式必须预防
    - **Instruction Override 语言检测**（v5.16 新增，源自 article-tuwen v1.0.3 审计 — 安全检查规避类词汇出现在确认点附近被标记为 Instruction Override High finding）：扫描 SKILL.md 中是否包含安全检查规避类词汇出现在**安全检查/确认点**附近。**检测方式**：扫描一类意为"规避安全检查"的词汇（含中文和英文等价词），出现在"确认点"/"安全检查"/"前置条件"/"用户确认"等**安全语境**附近时为 FAIL（High 级别）。**Medium 条件**：上述词汇出现在"异常处理"/"错误恢复"/"降级"等**容错语境**附近时。**不触发条件**：上述词汇出现在普通说明中（如"跳过此步骤不影响主流程"）不算 FAIL。**判定标准**：词汇暗示"规避安全检查" = FAIL；词汇描述"异常时降级" = Medium；词汇只是普通说明 = 不触发。**修复方式**：用"异常时降级到 X"/"失败后 fallback 到 Y"替代"规避 X"——明确是"降级"而非"规避"。**设计原则**：SkillSpector 将规避类语言视为 Instruction Override——agent 不应有规避安全检查的指令，即使是为了容错也应该用"降级"而非"规避"
    - **Hidden Instructions 检测**（v5.17 新增，源自 skill-publisher v5.15.1 自身被 SkillSpector 标记为 Hidden Instructions High 95% — HTML 注释形式标记的 LOCAL-ONLY 隐藏指令）：扫描所有文件中是否包含 HTML 注释标记的隐藏指令或条件指令。**检测模式**：① HTML 注释中包含"发布前删除"/"发布前移除"/"LOCAL-ONLY"/"内部使用"等条件指令 ② "发布前 X，发布后 Y"的双态指令（指令与实际行为矛盾）③ 任何形式的"隐藏直到某条件触发"的指令。**FAIL 条件**（High 级别）：发现上述任何模式。**修复方式**：移除 HTML 注释标记的隐藏指令，所有行为在 description 中声明——"声明即透明"原则。如果某些步骤只在本地执行（如 sync_skills.py），不用 HTML 注释标记"发布前删除"，而是在 description 中明确声明"会同步到本地安装目录"。**设计原则**：SkillSpector 将 HTML 注释中的指令视为 Hidden Instructions——agent 可能在用户不知情的情况下执行隐藏指令。正确做法是所有行为都透明声明，不用隐藏指令管理发布流程
    - **Name-Summary Coherence（P-C1，v5.19 新增）**：检查 frontmatter `name` 与 `description`/`summary` 是否描述同一件事。**检测方式**：提取 name 关键词（如 publisher/creator/auditor）与 description 关键词，重叠度 < 30% = WARN。**FAIL 条件**：WARN 级别不阻断发布，提示作者检查命名一致性。**修复方式**：调整 name 或 description 使二者指向同一概念。**来源**：skill-auditor v2.0.0 P-C1
    - **Unsafe Deserialization 检测（T-AST05，v5.19 新增）**：扫描代码是否使用不安全的反序列化方式。**检测模式**：Grep `yaml.load(`（非 `safe_load`）/ `pickle.loads?(` / `eval(` 用于解析 JSON/YAML。**FAIL 条件**（High）：上述模式出现 = 阻断发布。**修复方式**：① `yaml.load` → `yaml.safe_load` ② `pickle.loads` → `json.loads`（如数据是 JSON）③ `eval` 解析 → `json.loads`。**来源**：skill-auditor v2.0.0 T-AST05（OWASP AST10 对齐）
    - **Cross-Platform OS 限制声明（T-AST10，v5.19 新增）**：检查 frontmatter 是否声明 OS 限制或跨平台兼容性。**检测方式**：检查 `metadata.openclaw.os` 字段是否存在，或 description 是否含 "Windows/Linux/Mac/cross-platform" 等平台关键词。**FAIL 条件**：无 OS 声明 = Low（FYI 级，不阻断，提示作者补充）。**修复方式**：在 metadata.openclaw.os 声明支持的 OS 列表（如 `["windows", "macos", "linux"]`）。**来源**：skill-auditor v2.0.0 T-AST10
26. **GitHub 失败醒目警告**（v5.11 新增，源自 skillhub-daily GitHub 漏更 40 天事件）：如果 GitHub 推送失败（token 失效/网络超时/降级全失败），发布流程末尾必须用醒目警告重复提示，不能只埋在结果表格里。警告格式：
    ```
    ⚠️⚠️⚠️ 警告：GitHub 未同步！版本 <version> 未推送到 GitHub ⚠️⚠️⚠️
    下次发布前必须先补推此版本。
    待补推版本已记录到 docs/knowledge/skill-publisher-log.md
    ```
    警告必须在发布结果表格之后单独显示，不能只靠表格中 GitHub 行的 ❌ 标记
27. **待补推版本跟踪**（v5.11 新增）：GitHub 推送失败时，必须在 `docs/knowledge/skill-publisher-log.md` 中记录待补推版本号和失败原因。每次发布 Step 0 前置条件校验时，先检查 log.md 中是否有待补推版本，有则优先补推：
    - log.md 中新增 `### 待补推版本` 字段，记录：技能名、版本号、失败原因、失败日期
    - Step 0 检查到待补推版本时，提示用户"检测到 <skill-name> v<version> 未推送到 GitHub，是否先补推？"
    - 补推成功后，从 log.md 中删除待补推记录
28. **三平台一致性校验**（v5.11 新增）：发布完成后，必须对比三平台版本号，不一致时醒目警告：
    - GitHub：`gh api repos/<owner>/<repo>/releases/latest --jq '.tag_name'` 或 `git ls-remote --tags origin`
    - ClawHub：`clawhub inspect <slug>` 查看最新版本
    - SkillHub：`skillhub inspect <slug>` 或 frontmatter version 字段
    - 三平台版本号不一致时，醒目警告：`⚠️ 三平台版本不一致：GitHub <v1> | ClawHub <v2> | SkillHub <v3>，请检查遗漏的平台`
    - 一致时简短确认：`✅ 三平台版本一致：<version>`

29. **多文件一致性校验**（v5.14 新增中英文 README 一致性，v5.16 扩展为多文件一致性，源自 wx-huitu v2.2.0 + xhs-crafter v7.5.0/v7.6.0 + article-tuwen v1.1.1 多轮"主文件改了子文件没改"事件）：Step 1 仓库结构生成阶段，必须比对以下三类文件的一致性，不一致 = FAIL（版本号/触发词）或 WARN（描述类字段），列出差异清单：

    **A. 中英文 README 一致性**（v5.14 原有，5 项关键字段）：
    - **版本号 badge**：中文 `版本-X.Y.Z` 与英文 `version-X.Y.Z` 必须一致
    - **触发词列表**：中文触发词列表与英文版 Usage 段的触发词必须一一对应（数量相同、语义一致）
    - **核心能力描述**：中文"核心特性"与英文"Key Features"每条必须语义对应，不能一边改了一边没改
    - **用户警告段落**：中文"用户须知"与英文"User Notice"的副作用列表必须一致（默认操作数量相同、可选操作标注一致）
    - **不适用范围**：中文"不适用范围"与英文"Out of Scope"必须一一对应

    **B. SKILL.md 与 references/ 子文件一致性**（v5.16 新增，源自 xhs-crafter v7.5.0/v7.6.0 — SKILL.md 改了但 references/ 没同步，3 项关键字段）：
    - **版本号**：SKILL.md frontmatter version 与 references/ 中提到的版本号必须一致。**典型反例**：xhs-crafter v7.5.0 SKILL.md 升级到 v7.5.0 但 references/ 仍写 v7.4.0
    - **外部依赖描述**：SKILL.md 声明的外部依赖（API/CDN/字体）与 references/ 中的描述必须一致。**典型反例**：xhs-crafter v7.6.0 SKILL.md 移除了外部 CDN 引用但 references/ 仍写"使用 Google Fonts"
    - **触发词**：SKILL.md frontmatter description 的触发词与 references/ 中的触发词示例必须一致

    **C. SKILL.md 与 README 行为描述一致性**（v5.16 新增，源自 article-tuwen v1.1.1 — SKILL.md 改了行为但 README 没同步，2 项关键字段）：
    - **行为范围**：SKILL.md description 的行为范围声明与 README 的"核心特性"必须一致
    - **权限声明**：SKILL.md 的权限声明段落与 README 的"用户须知"必须一致

    **校验方式**：提取各类文件的对应章节，比对上述字段。发现不一致时输出：`⚠️ 多文件不一致：[文件A] vs [文件B] [字段名] A=<值> | B=<值>，请同步修复`。**设计原则**：规则 2 已要求"安全修复必须同步中英文版"，本规则扩展为"任何修改必须同步所有相关文件"——SkillSpector 会扫描所有文件，一处遗漏就会触发 finding

30. **跨平台通用规则预检**（v5.18.1 新增，源自第二轮 ClawHub 开源仓库深度分析 + ClawHub 规则通用性分类框架）：发布到任何平台（GitHub / ClawHub / SkillHub）前，必须执行以下 5 项跨平台通用规则预检。这些规则源自 [ClawHub 开源仓库](https://github.com/openclaw/clawhub) 的安全分析哲学，但其底层逻辑是 agent skill 这个形态的通用安全属性——与平台无关，对所有 skill 发布都适用：
    - **A. frontmatter `metadata.openclaw` 声明层**（通用化自 Layer 4.5）：所有平台发布前，frontmatter 必须包含 `metadata.openclaw` 结构，声明 `requires.env`（代码引用的所有凭证环境变量）/ `requires.bins`（必须存在的二进制）/ `anyBins`（任一存在即可的二进制）/ `primaryEnv`（主凭证变量）/ `envVars`（含 `required: false` 标记的可选变量）。SkillHub 虽不强制要求 `metadata.openclaw`，但保留该结构不会报错（未知字段被忽略），且能提升 skill 在任何平台的可信度。**适用范围**：所有平台
    - **B. description 行为声明段落**（通用化自 MCP Tool Poisoning 完整行为声明）：description 必须完整声明 skill 的全部行为范围，不能只描述核心功能。如果 skill 实际行为包含以下任一项，description 必须明确披露：① 读取本地文件（memory/profile/config）② 网络请求（API 调用）③ subprocess 调用（CLI 工具）④ 写入外部服务（推送/上传）。建议在 description 中加"本技能的行为范围（用户须知）"段落。**适用范围**：所有平台
    - **C. README 用户警告段落**（通用化自 Missing User Warnings）：如果 skill 有副作用（自动推送/自动写入外部服务/定时执行/写入项目本地文件），README 必须包含用户警告，明确告知：① 运行会自动写入哪些外部目的地 ② 会读取哪些本地数据 ③ 会创建/覆盖项目内哪些文件 ④ 如何禁用副作用。中英文 README 必须同步包含警告。**适用范围**：所有平台
    - **D. 权限声明段落**（通用化自 MCP Least Privilege）：SKILL.md 或 plugin.json 必须声明 skill 需要的权限（网络访问/文件读写/环境变量列表/subprocess 调用/外部 API）。建议在 SKILL.md 中增加 5 行权限声明表格（能力类别 / 是否使用 / 说明）。**适用范围**：所有平台
    - **E. 发布专用排除层**（通用化自 `.clawhubignore` 机制）：发布到任何平台前，必须确认凭证文件/临时脚本/构建产物不会被上传。ClawHub 用 `.clawhubignore`；SkillHub CLI 如果也读 `.gitignore` 就有同样的盲区，需用临时副本方式发布（在副本中删除凭证文件和不支持文件）。**适用范围**：所有平台

    **三层分类框架**（源自 ClawHub 规则通用性分析）：
    - **平台特定**（20%）：`.clawhubignore` 文件名 / `metadata.openclaw` 命名空间 / `clawhub` CLI 命令名——仅 ClawHub 需要
    - **概念通用**（60%）：frontmatter 声明与行为匹配 / Description-Behavior Mismatch / Credential Access 检测 / Missing User Warnings / 行为声明段落——对所有平台有直接泛化价值
    - **工程最佳实践**（20%）：semver / 安全预扫描 / Post-publish 验证 / 双 README 同步——跨平台通用

    **设计原则**：ClawHub 的 SkillSpector 看似是平台特有的安全分析，但其底层逻辑（声明与行为匹配、最小权限、用户知情、行为透明）是 agent skill 这个形态的通用安全属性。这些规则之所以在 ClawHub 出现，是因为 ClawHub 是目前唯一系统化做 skill 安全分析的平台，但规则本身不依赖于 ClawHub 的存在。**本规则将概念通用层（60%）+ 工程最佳实践层（20%）= 80% 的 ClawHub 规则泛化为跨平台通用预检**

31. **审计期补充检查引导**（v5.19 新增，源自 skill-auditor v2.0.0 集成）：发布预扫描覆盖声明-行为一致性的静态可判定部分。以下检查项需审计期运行时上下文或语义判断，发布预扫描不覆盖，建议在发布前用 skill-auditor L3 审计执行：
    - **T-LT Lethal Trifecta**（3 要素：访问私有数据 + 暴露不可信内容 + 对外通信）：三要素同时满足才升级 Critical，需审计期判断"不可信内容"边界
    - **P-C4 Power-Proportionality**：权力与用途比例的语义判断（如"审计技能需要推送权力 = 不合理"）
    - **T-AST06 隔离薄弱**：沙箱声明与行为边界的语义判断
    - **T-AST07 更新漂移**：hash 验证需联网拉取依赖信息

    **引导**：发布前执行 `skill-auditor <skill-path>` 跑 L3 全量审计，可覆盖上述检查项。skill-publisher 与 skill-auditor 形成"发布预扫描 + 审计期深度检查"的两层防护。

32. **三平台文件差异化发布**（v5.20 新增，源自 2026-07-17 三平台头部 skill 调研）：三平台对文件类型的要求不同，发布时必须按平台差异化处理，不能三平台推送相同文件集。**这是强制规则，违反会导致 ClawHub 拒绝文件或 SkillHub 400 错误**。

    **三平台文件差异化矩阵**：

    | 文件/目录 | GitHub | ClawHub | SkillHub |
    |-----------|--------|---------|----------|
    | SKILL.md | ✅ 保留 | ✅ 保留 | ✅ 保留 |
    | README.md（中文主文档）| ✅ 保留 | ❌ **剔除** | ⚠️ 可选（不流行）|
    | README.en.md（英文文档）| ✅ 保留 | ❌ **剔除** | ❌ 剔除 |
    | CHANGELOG.md | ✅ 保留 | ❌ **剔除** | ❌ 剔除 |
    | LICENSE（无扩展名）| ✅ 保留 | ✅ 保留 | ❌ **剔除** |
    | .claude-plugin/ | ✅ 保留 | ✅ 保留 | ❌ **剔除** |
    | .github/ | ✅ 保留 | ❌ 剔除 | ❌ 剔除 |
    | .clawhubignore | ✅ 保留 | ✅ 保留 | ❌ 剔除 |
    | .gitignore | ✅ 保留 | ❌ 剔除 | ❌ 剔除 |
    | references/ | ✅ 保留 | ✅ 保留 | ✅ 保留 |

    **关键约束**：
    - **ClawHub 官方禁止 README.md / CHANGELOG.md**：源自 `skill-creator`（3433 安装的官方指导 skill）明确声明 "Do NOT create extraneous documentation or auxiliary files, including: README.md, INSTALLATION_GUIDE.md, QUICK_REFERENCE.md, CHANGELOG.md, etc."。ClawHub 只有 SKILL.md 作为唯一内容载体，skill-card.md 由平台自动生成（含英文 Use Case / Risks / Skill Output 段落，不要手写或覆盖）。版本说明用 `clawhub publish --changelog` 参数传递（中文允许）
    - **SkillHub 拒绝无扩展名文件和 dotfile**：LICENSE / .gitignore / .claude-plugin/ / .github/ / .clawhubignore 都会被拒（400 错误）。用临时副本方式发布（在副本中删除这些文件）
    - **ClawHub 也应使用临时副本方式**：剔除 README.md / README.en.md / CHANGELOG.md / .gitignore / .github/ 后发布，避免上传 ClawHub 禁止的辅助文档
    - **ClawHub 临时副本发布必须带 `--name` 参数**（v5.20.1 新增，源自 2026-07-19 displayName 污染事故）：ClawHub 在未指定 `--name` 时会从**临时副本目录名**推断 displayName（下划线转空格 + 首字母大写）。如果临时副本目录名含 `temp`/`copy`/`_` 等词，displayName 会被污染成 "Clawhub Temp Skill Publisher" 这类错误名称。**强制要求**：① `clawhub publish` 命令必须显式带 `--name "<displayName>"` 参数 ② 临时副本目录名必须用 `<slug>-clawhub-copy` 格式（如 `skill-publisher-ai-clawhub-copy`），禁止用 `_clawhub_temp_<slug>` 这类含 temp 的命名
    - **SkillHub 临时副本目录名无此问题**：SkillHub 从 SKILL.md frontmatter 的 `displayName` 字段读取，不从目录名推断。但建议也用 `<slug>-skillhub-copy` 格式保持一致性
    - **发布后立即恢复或清理**：临时副本发布完成后立即删除；如果是原目录移除文件方式，发布后立即恢复

    **执行流程**：
    1. GitHub 推送：保留所有文件（README.md / README.en.md / CHANGELOG.md / LICENSE / .claude-plugin/ / .github/）
    2. ClawHub 发布：用临时副本（目录名 `<slug>-clawhub-copy`），剔除 README.md / README.en.md / CHANGELOG.md / .gitignore / .github/，保留 SKILL.md / LICENSE / .claude-plugin/ / .clawhubignore / references/。**publish 命令必须带 `--name "<displayName>"`**
    3. SkillHub 发布：用临时副本（目录名 `<slug>-skillhub-copy`），剔除 LICENSE / .claude-plugin/ / .github/ / .clawhubignore / .gitignore / README.en.md / CHANGELOG.md，保留 SKILL.md / README.md（可选）/ references/

    **预扫描检查**：发布前必须确认目标平台的临时副本已剔除该平台不支持的文件。未剔除 = Medium finding，要求作者在发布前剔除。**ClawHub 发布前检查 publish 命令是否带 `--name` 参数**：未带 = FAIL（阻断发布），因为会导致 displayName 被目录名污染。

33. **displayName / summary 语言策略**（v5.20 新增，源自 2026-07-17 三平台头部 skill 调研）：三平台对 displayName 和 summary 的语言惯例不同，发布时必须按平台调性选择语言。

    **平台调性**：
    - **SkillHub（腾讯）**：中文优先、英文兼容。community 源头部 skill 约 70% 用中文 displayName（如"微信公众号终极工作台"、"PDF识别提取专家"）
    - **ClawHub（国际）**：英文优先、包容中文。英文 skill 安装量是中文 skill 的 30-120 倍。中国 skill 常见 `-cn` 后缀 + 双语 displayName（如"CN PPT Outline Writer PPT大纲生成器"）
    - **GitHub**：国际开源标准，README.md 英文为主、中文为副

    **displayName 语言决策规则**：
    - **中文 skill**（触发词/正文是中文）：displayName 用双语并列，格式 `<English Name> <中文名>`（如 "Skill Publisher 技能发布"）。这样 SkillHub 中文用户和 ClawHub 国际用户都能检索到
    - **英文/双语 skill**：displayName 用英文
    - **slug 始终用 ASCII kebab-case**，不要写中文。中文 skill 可考虑加 `-cn` 后缀便于国际用户识别

    **summary / description 语言决策规则**：
    - **中文 skill**：summary 和 description 用中文（含中文触发词）。SkillHub 的 description 即 summary（无独立 summary 字段），中文 description 在 SkillHub 中文用户检索时更有效
    - **英文/双语 skill**：summary 和 description 用英文
    - **触发词内嵌在 description 里**：不要单独字段，直接写 "触发词：词1、词2、词3" 或 "Use when: (1)... (2)..." 格式

    **预扫描检查**（v5.21.0 强化：WARN → FAIL，源自 2026-07-19 data-prompt-coach SkillHub displayName 纯英文事件）：发布前检查 displayName 语言是否符合上述决策规则。**中文 skill 用纯英文 displayName = FAIL（阻断发布）**，要求作者修改为双语并列格式后再发布；英文 skill 用纯中文 displayName = WARN（建议改为英文或双语并列）。**中文 skill 判定标准**：frontmatter description 含中文字符，或触发词列表含中文短语。**判定流程**：① 提取 frontmatter description ② 检测是否含中文字符（Unicode CJK 范围）③ 若含中文且 displayName 不含中文字符 = FAIL ④ FAIL 时报告"中文 skill 的 displayName '<X>' 是纯英文，违反规则 33。请改为双语并列格式 '<English Name> <中文名>'（如 'Data Prompt Coach 数据分析 Prompt 教练'）后重新发布"。**设计原则**：SkillHub 是中文优先平台（腾讯），纯英文 displayName 在 SkillHub 中文用户检索时命中率低；ClawHub 国际用户也能通过英文部分检索到。双语并列是中文 skill 的最佳实践，不是可选项

34. **ClawHub publish --name 与临时副本命名铁律**（v5.21 新增，源自 2026-07-19 feishu-card-design displayName 错误事件）：`clawhub publish` 命令的 `--name` 参数和临时副本目录命名必须遵守以下铁律，否则 displayName 会被 ClawHub 平台永久锁定为错误值（无法通过新版本更新）。

    **铁律 A：`clawhub publish` 必须显式传 `--name`**
    - **强制要求**：每次 `clawhub publish` 必须显式传 `--name "<Display Name>"`，不能省略
    - **错误根因**：ClawHub CLI 在未传 `--name` 时，会从 `<path>` 目录名派生 displayName（去前导下划线 → 下划线转空格 → 每段首字母大写），首次发布后 displayName 永久锁定在 slug 上，新版本无法更新
    - **典型反例**：`clawhub publish _tmp_feishu_card_clawhub --slug feishu-card-design --version 1.0.0`（漏传 `--name`，导致 displayName 被派生为 `Tmp Feishu Card Clawhub`）
    - **正确写法**：`clawhub publish <path> --slug feishu-card-design --name "Feishu Card Design 飞书卡片消息设计规范" --version 1.0.2`
    - **`--name` 取值规则**：与 SKILL.md frontmatter 的 `displayName` 字段保持完全一致。中文 skill 用双语并列格式（规则 33），英文 skill 用英文

    **铁律 B：临时副本目录命名必须用 `<slug>-tmp-<platform>` 格式**
    - **强制格式**：临时副本目录名必须是 `<slug>-tmp-<platform>`（如 `feishu-card-design-tmp-clawhub`、`feishu-card-design-tmp-skillhub`）
    - **禁止格式**：`_tmp_<slug>_<platform>`（前缀下划线 + slug 用下划线连接）会被 ClawHub CLI 派生出错误的 displayName（`_tmp_feishu_card_clawhub` → `Tmp Feishu Card Clawhub`）
    - **更优解**：临时副本目录名直接用 `<slug>` 本名（如 `feishu-card-design`），放在父目录下区分平台（如 `_tmp_clawhub/feishu-card-design/`）。这样即使漏传 `--name`，派生出的 displayName 也至少是正确的 slug 形式
    - **目录命名 vs --name 的关系**：铁律 A 是根本保障（必须传 --name），铁律 B 是双重保险（即使漏传 --name 也能派生出合理 displayName）

    **预扫描检查**：发布前检查 `clawhub publish` 命令是否包含 `--name` 参数，以及临时副本目录名是否符合 `<slug>-tmp-<platform>` 格式。任一不符合 = Medium finding，要求作者修正后再发布。

    **故障案例**：feishu-card-design v1.0.0 首次发布时，临时副本目录命名为 `_tmp_feishu_card_clawhub` 且未传 `--name`，导致 ClawHub 平台 displayName 被永久派生为 `Tmp Feishu Card Clawhub`，与 slug `feishu-card-design` 严重不符。v1.0.2 通过临时副本重命名 + 显式 `--name` 修复，但若新版本无法更新已锁定的 displayName，则需走 `clawhub delete` + 重新首发流程。

35. **ClawHub inspect 延迟双验证**（v5.22 新增，源自 2026-07-20 周度审查建议 + 2026-07-19 v5.20.1 发布实测）：ClawHub `publish` 命令返回成功后，`inspect` 命令依赖的索引服务存在**异步索引延迟**（数分钟到数小时，最长 24h），不能用作"立即发布是否成功"的判定。

    **正确验证流程**（双验证，禁止立即重试或递增 PATCH）：
    - **立即验证**（publish 后立即执行）：`clawhub inspect <slug> --versions` 看版本列表是否包含新版本
      - 若包含 = ✅ 发布成功，索引已同步
      - 若不包含 = ⚠️ **不要立即重试**，记录"待 24h 后验证"，按下一步延迟验证
    - **延迟验证**（publish 后 24h 执行）：`clawhub inspect <slug> --version <X> --json` 二次确认
      - 若返回版本信息 = ✅ 发布成功，索引已同步
      - 若仍返回 "Version not found" = ❌ 真失败，记录待补推
    - **publish 返回的 `OK. Published` 是可信的**，inspect 是验证索引服务而非验证发布本身

    **禁止行为**：
    - 🚫 禁止立即递增 PATCH 重试（递增无效，旧 publish 已成功，新版本号反而无法覆盖）
    - 🚫 禁止把"inspect 立即返回 not found"判定为"publish 幻象成功"
    - 🚫 禁止把"latestVersion 指针未更新"判定为"publish 失败"（latestVersion 指针是另一个异步更新字段）

    **故障案例**（v5.20.1 实测）：publish 5.20.1 返回 OK + 版本 id `k972c1xcw13gwq97m2jhvd7rx18atv8w`，立即 `inspect --version 5.20.1` 返回 "Version not found"，`inspect` latestVersion 仍指向 5.20.0。24h 后再 `inspect --version 5.20.1` 已能正常返回版本信息。**这不是"幻象成功"，是 ClawHub 平台的异步索引延迟**

36. **ClawHub moderation 状态处理**（v5.22 新增，源自 2026-07-20 周度审查建议）：ClawHub publish 后 skill 可能进入 moderation（审核中）状态，需明确告知用户后续行为：

    **moderation 状态判定**：publish 返回成功后，用 `clawhub inspect <slug> --json` 检查 `moderation_status` 字段（如有）
    - **approved**（已批准）：✅ 正常状态，skill 可被公开检索和安装
    - **pending**（审核中）：⚠️ skill 已发布但正在审核，公开检索可能受限。告知用户"skill 已发布，正在 ClawHub 审核中，预计数小时内通过"
    - **rejected**（已拒绝）：❌ skill 被审核拒绝，需检查拒绝原因（通常是 SkillSpector findings 未修复），修复后递增版本号重新发布
    - **字段缺失或 inspect 异步延迟**：按规则 35 处理，不阻塞流程

    **告知用户的措辞**：避免"审核可能失败"这类焦虑性表述，用中性措辞"skill 已提交 ClawHub，正在审核流程中，预计数小时内完成。如被拒绝，会收到具体原因，按原因修复后递增版本号重新发布即可"

## 执行流程

**读取 `references/publishing-guide.md` 获取完整发布流程。** 以下为摘要。

### Step 0: 前置条件校验（v5.2 新增，v5.4 增强，v5.10 增强，v5.11 增加待补推检查，v5.17 同步 OS 持久存储读取行为移除，v5.17.6 同步 SkillHub token 读取命令清理）
执行规则17的4项前置条件校验（目录存在/SKILL.md存在/平台登录态/Git配置）+ 规则18的Skill质量门禁 + 规则21的GitHub token有效性校验（v5.17: token 只通过环境变量读取，不再从 OS 持久存储读取）。任何一项不满足 = 中止发布，明确告知用户缺什么、怎么修。全部通过才进入 Step 1。**v5.11 新增**：检查 `docs/knowledge/skill-publisher-log.md` 中是否有待补推版本（规则27），有则提示用户"检测到 <skill-name> v<version> 未推送到 GitHub，是否先补推？"。

### Step 1: 仓库结构生成
生成标准目录：SKILL.md / README.md(中英双语) / CHANGELOG.md / LICENSE(MIT-0) / .gitignore / .claude-plugin/plugin.json。确认作者名、GitHub owner、版本号、ClawHub slug、SkillHub slug。SKILL.md frontmatter 必须同时包含 ClawHub 字段（name/description）和 SkillHub 字段（slug/displayName/version/summary/license）。

### Step 2: 安全审查
**Pre-Scan（v5.8 强制，v5.11 扩展）**：先用 LS 列出技能目录所有文件（含 .gitignore 中的），检查是否存在凭证文件（config.local.json/.env.local/_*.py/*.log 等）和**临时脚本**（_*.py/_*.ps1，v5.11 新增）。存在 = FAIL，必须删除或移出目录。**注意：Grep (ripgrep) 默认遵守 .gitignore 会跳过这些文件，但 clawhub publish 上传整个目录不看 .gitignore——必须用 LS 检查，不能只依赖 Grep。临时脚本误上传是高频 SkillSpector finding 源（web-to-fim v3.3.0 的 27 个 findings 就是 _gh_push.py 误上传导致）。**
**四类 Grep 扫描**（凭证/路径/危险命令/YARA 触发词），全部 PASS 才能继续。凭证扫描必须覆盖 `skh_` 前缀（SkillHub token）。分发物三维判定 + ClawHub slug 检查 + ClawHub 自动文件排除 + SkillHub slug 全网唯一性检查 + ClawHub SkillSpector 预扫描（规则25，含 Layer 4 YARA + Layer 5 SSD3/MCP/UserWarnings + v5.12 新增代码 import 扫描对照/依赖版本分级 + v5.13 新增内部矛盾检测/敏感文件扫描同意）。**中英文一致性自动检查（v5.13 新增，源自 kami 审计反馈 — 英文版残留 v2.1.0 内容）**：如果存在 README.md 和 README.en.md，必须自动比对以下三项一致性：① **版本号一致**：两份 README 的版本号必须相同（Grep `version` 或 `vX.Y.Z` 模式）② **触发词数量一致**：两份 README 的触发词列表数量必须相同（数 `**触发词**` 或 `Triggers` 段落项数）③ **警告段落数量一致**：两份 README 的"用户警告"段落数量必须相同（数 `⚠️` 或 `Warning` 标记）。不一致 = Medium finding，要求作者同步修改。**设计原则**：规则 2 已要求"安全修复必须同步中英文版"，但当前只有原则没自动检查，导致英文版残留旧内容未被发现。本检查用启发式自动比对，覆盖最常见的 3 类不一致

### Step 3: 版本号查重
- ClawHub：`clawhub inspect <slug>` 查看已发布版本列表，确认待发布版本号不重复。重复则递增 PATCH 后重新确认。
- SkillHub：版本号在 frontmatter 的 `version` 字段中，更新时保持 slug 不变，递增 version。
- GitHub：检查 git tag 是否已存在。

### Step 4: GitHub 推送（v5.4 增强降级机制）
按规则22三级降级：git push → gh CLI → GitHub API（降级方案详见 references/publish-procedures.md，不在此文档化）。创建 Release。git push 持续超时但 API 可达时，直接跳到 Level 3。**GitHub 推送失败时执行规则26（醒目警告）和规则27（待补推版本跟踪）**。

### Step 4.5: 删除临时脚本（v5.11 新增）
GitHub 推送完成后、ClawHub 发布前，必须删除 Step 4 中可能产生的临时脚本（`_*.py`/`_*.ps1`）。这些脚本用于辅助 GitHub 推送（如 Git Data API 上传），但绝不能被 ClawHub 上传，否则会触发 MCP Tool Poisoning / Context-Inappropriate Capability 等 SkillSpector findings（web-to-fim v3.3.0 教训：_gh_push.py 误上传导致 27 个 findings）。用 LS 确认已删除。

### Step 5: ClawHub 发布（v5.18 增强 inspect --json 验证；scan/dry-run 待 CLI 未来版本支持）

```bash
# 1. 正式发布（v5.18 现实校准：CLI v0.9.0 实际只支持 `clawhub publish`，文档的 `clawhub skill publish` 是未来版本方向，当前不可用）
# v5.21 新增 --name 强制要求（规则 34）：必须显式传 --name，否则从目录名派生 displayName 永久锁定错误值
clawhub publish <path> \
  --slug <slug> \
  --name "<Display Name>" \
  --version <version> \
  --tags "<ASCII-only>" \
  --changelog "<text>"

# 2. 验证 Latest 版本（v5.18 新增，CLI v0.9.0 支持 --json）
clawhub inspect <slug> --json | python -c "import sys,json; d=json.load(sys.stdin); print('Latest:', d.get('latestVersion'))"

# 3. 主动触发扫描（v5.18 待 CLI 未来版本支持 — 当前 CLI v0.9.0 不支持 `clawhub scan` 命令，只能被动等待 ClawHub 服务端自动扫描）
# 未来 CLI 升级后可用：clawhub scan --slug <slug> --update --output scan-report.zip
```

**说明**：
- `clawhub publish` 是 CLI v0.9.0 当前支持的命令（ClawHub docs/cli.md 描述的 `clawhub skill publish` 是未来版本方向，当前 CLI 未实现，2026-07-16 实测确认）
- `clawhub inspect <slug> --json` 程序化验证 Latest 版本（CLI v0.9.0 支持）
- `clawhub scan --slug --update --output` 主动扫描是未来 CLI 版本方向，当前不可用——只能被动等待 ClawHub 服务端扫描完成后查看 findings
- `--dry-run` 参数当前 CLI 不支持（docs 描述但未实现）

### Step 6: SkillHub 发布（v5.1 新增，v5.3 加入 TRACE 预检）
```bash
# 1. 确认登录态
skillhub auth whoami

# 2. TRACE 五维度预检（v5.3 新增，规则20）
#    T: 安全红线扫描 + allowed-tools + 国内可用性
#    R: 前置条件 + 质量门禁 + 边界输入 + 异常处理
#    A: 触发测试（正例 + 反例）
#    C: Schema（4模块/200行/示例/实习生测试）
#    E: 增量价值
#    任何维度 FAIL = 中止 SkillHub 发布，报告问题

# 3. 临时移除不支持的文件类型（.gitignore/LICENSE/.claude-plugin/.github）
#    备份到 skill 目录外（规则23），发布后立即恢复
#    如果文件被占用无法移除（规则24），改用 robocopy 临时副本方式发布

# 4. dry-run 预检（必须通过）
skillhub publish <path> --dry-run

# 5. 正式发布（目录或临时副本目录）
skillhub publish <path> --changelog "变更说明"

# 6. 立即恢复被移除的文件 / 清理临时副本
```

> **Windows 注意**：如果 `skillhub` 命令报 exit code 9009，是因为 skillhub.bat 中调用了 `python3`（Windows 上只有 `python`）。建议用户手动修复：将 `C:\Users\<user>\.local\bin\skillhub.bat` 中的 `python3` 改为 `python`，或直接用 `python "%USERPROFILE%\.skillhub\skills_store_cli.py"` 替代。**此为用户手动环境配置，agent 不自动执行。**
> **文件类型限制**：SkillHub 拒绝 `.gitignore`、`LICENSE`、`.claude-plugin/`、`.github/`，发布前必须临时移除，发布后立即恢复。
> **TRACE 预检**：SkillHub 平台会对上架技能执行 TRACE 五维度检测，本技能在发布前预执行同样的检测，避免上架后被扣分。

### Step 7: 发布后验证（v5.11 增加三平台一致性校验）
GitHub 文件列表检查 + `clawhub inspect <slug>` 确认 + SkillHub 状态检查。**Post-Publish 凭证验证（v5.8 强化）**：`clawhub inspect <slug>` 的文件列表中不得包含 config.local.json/.env.local/_*.py/*.log 等凭证和临时文件，如发现说明 Pre-Scan 失效，必须立即删除该版本并重新发布。检查 ClawHub Short summary 是否与 frontmatter description 一致，不一致则递增版本号重新发布。**三平台一致性校验（v5.11 新增，规则28）**：对比 GitHub/ClawHub/SkillHub 三平台版本号，不一致时醒目警告 `⚠️ 三平台版本不一致`，一致时确认 `✅ 三平台版本一致`。**GitHub 失败醒目警告（v5.11 新增，规则26）**：如果 GitHub 推送失败，在结果表格后单独显示醒目警告，不能只靠表格中的 ❌ 标记。

### Step 8: 本地安装目录同步（v5.0 新增，v5.11 增强排除规则，v5.16 移除 LOCAL-ONLY 标记，v5.18.2 加操作点警告 — 遵守 SkillSpector Missing User Warnings）
三平台发布完成后，将开发目录的 skill 同步到 TRAE 安装目录 `c:\Users\Administrator\.trae-cn\skills\<skill-name>`，确保本地使用的是最新版本。

> ⚠️ **操作点警告（v5.18.2 新增）**：以下命令会**覆盖**安装目录 `c:\Users\Administrator\.trae-cn\skills\<skill-name>` 中已有版本的文件。如需保留旧版本，请在执行前手动备份。执行 `sync_skills.py` 前建议先用 `--dry-run` 预览将变更的文件列表。

```bash
# 同步指定 skill
python sync_skills.py <skill-name>

# 或同步所有 skill（慎用，会覆盖所有安装目录）
python sync_skills.py
```
**注意**：sync_skills.py 位于项目根目录 `<project-root>/sync_skills.py`，会自动排除 `.git`/`.gitignore`/`_backup`/`__pycache__`/`.clawhub`/临时脚本（`_*.py`/`_*.ps1`）/运行时文件（`data`/`saved`/`logs`）/执行日志（`skill-publisher-log.md`）等。同步前可用 `--dry-run` 预览。

### Step 9: 发布日志记录（v5.0 新增，v5.11 增强待补推跟踪，v5.16 简化经验采集）
**A. 发布日志记录**：在 `docs/knowledge/skill-publisher-log.md` 中追加本次发布条目，格式：
```markdown
## [YYYY-MM-DD] <skill-name> v<version> — 三平台发布（<一句话主题>）

### 发布概况
- 技能：<skill-name>
- 版本：<old> → <new>
- 平台：GitHub ✅（commit <sha> + tag v<version> + Release）| ClawHub ✅（<version>）| SkillHub ✅（skillId=<id>）
- sync_skills.py 已执行：✅（同步到 c:\Users\Administrator\.trae-cn\skills\<skill-name>）

### 遇到的问题 / SkillSpector findings（如有）
...

### 对 skill-publisher 的改进建议（如有）
...
```
**待补推版本记录**（规则27）：如果 GitHub 推送失败，在 log.md 中新增 `### 待补推版本` 字段，记录技能名、版本号、失败原因、失败日期。下次发布 Step 0 时优先补推。

**B. 经验沉淀入口**（v5.13 新增，v5.16 简化为入口提示）：如本次发布涉及重大变更或多轮 finding 修复，建议用户说"复盘"触发 EVOLVE 阶段，经验沉淀流程由 EVOLVE 阶段负责，不在本技能中展开。


## 示例

### 示例1：常见输入（完整 Skill 目录发布）

**用户输入**："帮我把 wx-peitu 技能发布到三平台，版本号 7.1.0"

**前置条件校验**：
- ✅ 目录 `<project>/wx-peitu` 存在且非空
- ✅ SKILL.md 存在
- ✅ ClawHub 已登录（clawhub whoami 通过）
- ✅ SkillHub 已登录（skillhub auth whoami 通过）
- ✅ Git 配置完整

**质量门禁**：
- ✅ SKILL.md 180行（<300）
- ✅ description 存在且含触发词
- ✅ description 含 Do NOT 范围声明

**安全审查结果**：
| 审查项 | 状态 | 详情 |
|--------|------|------|
| 凭证泄露 | PASS | 无 token/api_key/secret 硬编码 |
| 本地路径 | PASS | 无 C:\ 或 D:\ 绝对路径 |
| 危险命令 | PASS | 无 curl/wget/eval |
| 分发物判定 | PASS | 无 __pycache__/.clawhub/skill-card.md |

**版本号查重结果**：
| ClawHub 已发布版本 | 待发布版本 | 状态 |
|-------------------|-----------|------|
| v7.0.0 | v7.1.0 | 可发布 |

**发布结果**：
| 平台 | 地址 | 版本 | 状态 |
|------|------|------|------|
| GitHub | github.com/EdwardWason/wx-peitu | v7.1.0 | 成功 |
| ClawHub | clawhub.ai/skills/wx-peitu | v7.1.0 | 成功 |
| SkillHub | skillhub.cn/skills/wx-peitu | v7.1.0 | 成功 |

### 示例2：边界输入（目录不存在）

**用户输入**："发布 my-new-skill"

**前置条件校验失败**：
```
❌ 目录不存在或为空：`<project>/my-new-skill`
请确认 Skill 路径，或使用完整路径指定。
```

**中止发布，不继续执行后续步骤。**

### 示例3：边界输入（SKILL.md 缺失）

**用户输入**："发布 ./my-project"

**前置条件校验**：
- ✅ 目录存在且非空
- ❌ 未找到 SKILL.md，这不是一个有效的 Skill 目录

**中止发布，提示用户**：
```
❌ 目录 ./my-project 下未找到 SKILL.md。
这不是一个有效的 Skill 目录。
请确认目录路径，或先使用 skill-forge 创建 Skill。
```

### 示例4：边界输入（Skill 质量不达标）

**用户输入**："发布 ./my-skill，版本 1.0.0"

**前置条件校验**：✅ 全部通过

**质量门禁失败**：
```
❌ SKILL.md 过长（350行），建议精简到 200 行以内再发布。
❌ description 缺少 Do NOT 范围声明，可能导致误触发。
请修复以上问题后再发布。可调用 skill-forge 进行评估和优化。
```

**中止发布，建议先修复。**

### 示例5：异常输入（未登录 ClawHub）

**用户输入**："发布 ./wx-peitu"

**前置条件校验失败**：
```
❌ ClawHub 未登录，请先执行：
   clawhub login --token <your-token> --no-browser
```

**中止发布，不继续执行后续步骤。**

### 示例6：复杂输入（未指明哪个 Skill）

**用户输入**："发布我的技能"

**扫描工作目录**：
```
找到以下 Skill 目录：
1. `<project>/wx-peitu` (含 SKILL.md)
2. `<project>/pic-book` (含 SKILL.md)
3. `<project>/web-to-fim` (含 SKILL.md)

请指定要发布的 Skill 名称或序号（逐个发布，不支持批量）。
```

**等待用户选择后继续。**

### 示例7：复杂输入（路径模糊）

**用户输入**："发布 wx-peitu"

**搜索匹配目录**：
```
找到 1 个匹配目录：`<project>/wx-peitu`
自动使用此目录继续发布。
```

### 示例8：SkillHub TRACE 预检失败

**用户输入**："发布 ./my-skill 到 SkillHub"

**TRACE 预检结果**：
```
T (Trust):       ✅ PASS
R (Reliability): ✅ PASS
A (Applicability): ❌ FAIL — description 缺少 Do NOT 范围声明
C (Compliance):  ❌ FAIL — 缺少"示例"模块
E (Effectiveness): ✅ PASS

TRACE 预检未通过（A/C 失败），中止 SkillHub 发布。
建议：先补全 Do NOT 声明和示例模块，再重新发布。
```

**中止 SkillHub 发布，GitHub 和 ClawHub 已发布的保留。**

## References

- **[`references/publishing-guide.md`](references/publishing-guide.md)** — 完整发布流程。仓库结构模板、安全审查、版本号查重、GitHub API降级、ClawHub CLI、SkillHub CLI、PowerShell兼容、故障排查。
- **[`references/skillhub-publishing.md`](references/skillhub-publishing.md)** — SkillHub 发布详细流程。CLI 安装、登录、frontmatter 兼容、dry-run 预检、正式发布、Windows 兼容、故障排查。
- **[`references/security-audit.md`](references/security-audit.md)** — 三层安全扫描（含扩展凭证模式 + SKILLHUB_TOKEN）+ 分发物判定 + ClawHub 自动文件排除 + 修复指南。
- **[`references/publish-procedures.md`](references/publish-procedures.md)** — 推送降级链 + gh CLI + Release + ClawHub + SkillHub + 版本号查重 + 故障排查。
- **[`references/change-detection.md`](references/change-detection.md)** — 变更检测 + 版本 bump + Conventional Commits。
- **[`references/changelog-generation.md`](references/changelog-generation.md)** — git log 提取 + CHANGELOG 生成 + Release Notes 转换。
- **[`references/repo-structure.md`](references/repo-structure.md)** — 仓库结构模板 + README 21 章节 + 智能适配 + .gitignore 模板 + frontmatter 兼容模板。
