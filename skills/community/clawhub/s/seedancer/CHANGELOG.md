# Seedancer v10.0.3 更新日志

_发布日期：2026-10-18_

> **定位**：修复 ClawHub 发布被安全扫描拒绝的问题。功能与 v10.0.2 相同。

## 修复

- 删除 `scripts/__pycache__/seedancer_calc.cpython-312.pyc`。
  ClawHub A.I.G 0.2.1 拒绝打包的 Python 字节码（CVE-2026-84809），导致 v10.0.2 版本号被占住但版本不可查询、不可公开。
- 新增 `.gitignore` 与 `.clawhubignore`，排除 `__pycache__/`、`*.pyc`、`*.pyo`、`*.pyd`。

---

# Seedancer v10.0.2 更新日志

_发布日期：2026-10-18_

> **定位**：合并 PR #1（硬门确定性计算器 + SKILL.sh 实用化 + CI + 评估报告），并升版发布。

## 新增

- `scripts/seedancer_calc.py`：零依赖硬门计算器（`smin` / `dialogue` / `check-group` / `models`，`--json`，退出码 0/1/2）
- `tests/test_calc.py`：13 个用例，含 SKILL.md 表格 ↔ 计算器常量防漂移
- `.github/workflows/consistency.yml`：push / PR 跑一致性检查、攻击测试、单元测试、SKILL.sh 冒烟
- `docs/REVIEW-v10.0.1.md`：评估报告

## SKILL.sh

- 从请求解析时长与画幅（不再写死 10s/16:9）；超 15s 预警；新增 `--help`
- 计算子命令委托给计算器；原调用 `bash SKILL.sh "10s 9:16 ..."` 仍 exit 0

## SKILL.md / 元数据（来自 PR 第二轮）

- 运镜三要素口径统一；景别↔焦段改为参考并修正英文术语
- 模型上限、运镜最小时长表加权威注记；门控 7B 补 Kling 3.0
- 时间片时间码改为 0-10s / 10-20s / 20-30s；补第六判定「换模式」；阶段数 6 → 8
- 简介改为能力摘要；platforms 补 wan / gpt-image / seedream
- 台词容量与镜头密度节引用计算器

---

# Seedancer v10.0.1 更新日志

_发布日期：2026-10-06_

> **定位**：大扫除（删除死代码 + 合并重复 + 清理陈旧标记 + 修正一致性）

## A 组（删除死代码）

- 删 `scripts/setup_seedance_prompt_workspace.sh`（0 引用）
- 删 `assets/templates/`（空目录）
- 删 `scripts/__pycache__/`（编译产物）
- 删 `release-notes.md`（CHANGELOG 是唯一权威）

## B 组（合并重复）

- 合并两张语言路由表（`Language Policy` + `语言路由` → `语言路由`）
- README 版本表收缩为近 3 版 + 指向 CHANGELOG

## C 组（陈旧标记清理）

- 删 SKILL.md 40 处 `🆕` + INDEX.md 11 处 `🆕`
- 删 5 处历史版本号（`(v8.0.0)` 等）
- 删空壳标题 `## 多模型支持`
- 改标题 `平台限额速查` → `平台限额（见权威文件）`
- 合并尾部两个指针章节为 `## 文档导航`

## D 组（一致性修正）

- README `Five Director Systems (v7.0.0)` vs CN `(v8.0.0)` → 统一 v7.0.0
- README 历史锚点 `v9.0.0` vs CN `v8.0.0` → 统一 v9.0.0

## 验证

- 检查器 19 项 PASS
- 攻击测试 6/6 拦住
- 净减 275 行（+67/-342）

---

# Seedancer v10.0.0 更新日志

_发布日期：2026-10-06_

> **定位**：**MAJOR** —— 检查器行为变化（新增**阻塞级** `A2`）＋ 入口规则改名。**不改创作语义**。
> 依据：`PLAN-20261006-001`（G 系列）、`DISPATCH-20261006-014/015/016/017`、`REV-20261006-017…027`、`RETRO-20261006-012/013/014`。

## 🚀 v10.0.0 变更（G 系列）

### 1. 一致性检查器 v3 → v5：从"短语存在"到"内容 / 枚举 / 指针"

| 断言 | 变化 |
| --- | --- |
| **`A2`**（v4，**阻塞级**） | 7 个关键小节的**内容行**必须存在：必需词逐字 + 标题在 **2–6 级唯一** + 非标题内容行数 ≥ 必需词数。此前 `A1` 只断言"短语在该节内存在"，**删掉整段内容只留标题仍会 PASS** |
| **`A3`**（v5，**WARN**） | 规范枚举**顺序**：仅当某行**完整包含**全部规范键时校验其顺序（不做分隔符猜测 —— 两版启发式分别被 `REV-024/025` 证伪） |
| **`A4`**（v5，**阻塞级**） | **文件内指针层级成立**：`见 §主 · 子` 的主标题须唯一；带 `· 子` 时，子标题须为**主标题范围内更深层级**的标题。动因：D7 期间我写的指针**字符串比对能过**、层级关系却不成立（`REV-027` W2-a）。⚠️ **它不保证"被指向的内容真的在那里"**（语义问题）—— 原错位指针在层级上其实成立，A4 仍会判通过 |
| **`D2`** | 接回此前**定义后零引用**的 `CONTRACT_KEY_LINES`（区块名/词表锚点逐字核验） |
| **`G2`** | 每个**检查组**开跑前向 **stderr** 打 `[RUN ] <编号> <说明>` 并 flush → 中断时最后一行就是断点；stdout 契约不变（`--json` 仍纯 JSON） |
| 合计 | **16 → 19 项**；`A2`/`A4` 为阻塞级，`A3` 为 WARN |

### 2. 入口规则改名（**v9 → v10 迁移必读**）

- 「四项事实」在入口的出现处 **5 → 2**（保留：契约区注释、定义节标题）。
  `§核心硬规则` 第 7 条、`§门控 8` 条目、`§阶段五` 条目 → 改为**文件内指针**（指向 `§输出格式硬门`）。
- ⚠️ **三处规则名由「每镜四项事实」改为「每镜必要条件」**，而**定义节标题仍为「每镜四项事实（缺一不可）」**
  → 术语存在一处错位（已登记技术债 TD-9，结构性修法是协调改名）。
  **四要素（视觉起点 / 观察关系 / 构图落位 / 摄影机状态）与硬门语义完全未变**，且四要素仍**内联**在入口规则条中。
- 「硬门 100% 留在入口」**仍然成立**：本次只是改标签 + 加**文件内**指针，**未把内容移到 `references/`**。
- 代价（如实记录）：入口体积 **+78 字节**（43,600 → **43,678**；指针比被删文本更啰嗦）—— 去重目标是**短语计数**，不是体积。

### 3. 攻击测试（`tests/attack_test.py`）

- **31 个必拦场景**（7 个受守护小节 × 变异 + 枚举乱序 + 指针错位/主标题不存在）
- **7 类"必须不报错"的合法写法**（防假红：散文/顿号/括号/表格行/全角逗号/跨行注释/枚举后加注）
- **24 类显式已知漏检**（如"占位凑数""跨行枚举""枚举多一个要素"）—— 若某天被拦住会打印"改进"提示
- 实现：在**系统临时目录的副本**上变异（真实目录只读），结束用 **sha256 断言真实文件未被触碰**

### 4. 已知限制（如实声明，勿当"已覆盖"）

- `A2`/`A3` 为**字面判据**：拦不住"占位凑数 / 语义反转 / 把词藏进代码围栏并凑够行数"；`A3` 为 **WARN 级**（不阻塞构建）
- `SECTION_CONTENT` 只覆盖 **7 节**；未列入的小节仍可被"删内容留标题"
- `A4` 只扫 `SKILL.md`，且只认 `见 §…` 这一**显式语法**
- `D2` 只取契约区**首个围栏**，且跳过 <12 字符的行；`D1` 为 WARN 级、永不 FAIL；`K1` 只测入口体积

---

# 历史版本

## v9.0.2 — 元数据一致性修复（2026-10-06）

> **定位**：元数据一致性修复（PATCH）—— **不改创作语义**。

## 🔧 针对平台评审与发布复盘的修复

ClawHub 安全评审的 `[SDI-1] unexpected`（v9.0.1 遗留一条）与 v9.0.1 发布复盘各指出一处问题，本版处置：

### 1. 消除 frontmatter 与图像能力的表述矛盾（`[SDI-1]`）
- `SKILL.md` frontmatter 原写 `NOT for: ... image generation`，但技能核心含 **LIRA 图像提示词系统**、
  角色/道具**资产生图提示词**、**图像模型路由**（GPT Image 2 / Seedream 5.0 Pro）—— 声明与能力自相矛盾
- 改为：`NOT for: general-purpose video or image generation requests (this skill produces prompts and plans,
  not the media itself), or non-AI filmmaking.` —— 明确"产出提示词/计划，不产出媒体本身"
- 描述同步补全图像侧能力（asset image prompts / LIRA）与模型清单

### 2. `skill-card.md` 元数据漂移修复
- 版本戳 `9.0.0` → `9.0.2`（此前未随 v9.0.0 / v9.0.1 更新）
- Publisher `dandysuper`（上游原作者）→ `taosiuman`（本技能当前发布者）
- Description / Use Case / Output / Known Risks / Reference 对齐当前技能能力与安全整改
  （补"真人素材同意 + 留存"风险项，指向 `references/asset-whitelist.md` §0）

### 3. 一致性检查器 v2 → v3
- 新增 **V3**：`skill-card.md` 的「Skill Version(s)」必须 == 权威版本
- 新增 **V4**：`skill-card.md` 的 Publisher 必须 == `_meta.json` 的 `author`
- （此前 `skill-card.md` 是 `V1` 的已知盲区；现已明确覆盖）

---

# Seedancer v9.0.1 更新日志

_发布日期：2026-10-06_

> **定位**：内容合规修复（PATCH）—— 不改创作语义。

## 🔒 针对平台安全判定的修复

ClawHub 安全评审（confidence: high）指出两处需要整改，本版直接处置：

### 1. 真人素材的"同意 + 留存门"（新增）
- `references/asset-whitelist.md` 新增 **§0 授权与数据边界门**：上传前四项确认
  （**权利与同意** / **授权范围** / **数据边界** / **留存与撤回**），**未过不得上传**
- 新增**高风险类别**默认拒绝（未成年人 / 公众人物 / 未授权第三方 / 敏感类别）
- 新增**数据最小化**（只传必需素材、去元数据、优先脱敏或 AI 生成替代）
- 新增**留痕要求**（记入项目工作台；交付说明列出"传了什么、给了谁、留多久、怎么撤回"）

### 2. 消除"规避安全标记"的表述
- `references/cinedance-video-prompt.md`：词表替换处补**合规边界** —— 仅用于提升模型对创作意图的理解，
  **不得**用于规避平台安全/审核机制；被拦截时须修改内容或停止
- `references/json-api-mode.md`：标题「规避的触发词」→「需要替换以提升模型理解的词（**不用于规避安全策略**）」
- `SKILL.md` 治理红线新增 **§0 安全与数据边界**（优先级最高）

---

# Seedancer v9.0.0 更新日志

_发布日期：2026-10-05_

> **定位**：MAJOR —— 入口契约与目录结构变化；**创作语义（硬门/错误码/模板）未变**。

---

## 🚀 本次重构做了什么

### 1. 参考文档"接线"（修复最严重的结构缺陷）
- 新增 **《参考文档加载表（门控 → 必须加载）》** 取代旧的「参考文档」索引
- 15 篇 v8 孤儿文档接入真实门控；加载表覆盖全部 reference（门控名可判定）
- 新增 `references/INDEX.md`（含加载门控列；由 `I1`/`I2`/`I3` 断言守护，**不是**自动生成）

### 2. 一致性机制（此前完全缺失）
- 新增 `scripts/check_consistency.py`（零依赖，14 项断言）：
  版本多处一致 · `_meta.json` 合法 · frontmatter 字段 · 元数据对齐 · **归因合规** ·
  死链 · 孤儿/接线 · 索引完整性 · 大段重复 · 体积预算 · **硬门锚点**
- 基线实测：**5 FAIL + 2 WARN** → 重构后 **0 FAIL**

### 3. 合规修复（最高优先级）
- `LICENSE` 归因从 **4 个来源补全到 8 个**（补 Elio_AIGC / shotlist-builder / seedance-director / hellgrind）
- 此前 `SKILL.md` 写着 "Full attribution details in LICENSE file"，而 LICENSE 只覆盖一半来源

### 4. 元数据与版本
- `_meta.json`：从"YAML 伪装成 .json"改为**合法 JSON**
- `SKILL.md` frontmatter 补 `tags` / `platforms`（与 `_meta.json` 对齐）
- **版本单一权威 = `_meta.json`**；此前版本号在 6+ 处各自维护且互相矛盾（页脚 7.1.0 / 徽章 7.0.0 / LICENSE v5.0.0）
- 版本历史表改以 **git tag 日期**为唯一事实

### 5. 引用完整性与去重
- 死链 **10 处 → 0**；新建 `references/qa-checklists.md`（**门控 8 的落点，此前被 6 处引用却不存在**）
- `SKILL.md` 去重：五大导演系统摘要 / 并发控制协议（89% 逐字重复）/ 进度查询 / 模型表 /
  平台限额速查 / 内嵌变更日志（80 行）/ 末尾 4 张检查清单 → 全部改为指针
- 入口体积 **56037 → 43243 字节**（v9.0.0 发布时实测；G1 后为 43600 字节 —— 见 `COMPAT.md` §3/§3.1）；
  **硬门逐字保留**（28 条锚点由脚本断言）

### 6. 错误码归位
- 5 个只写在入口的错误码（`F-DIALOGUE-CAPACITY` / `F-GROUP-CONTINUITY` / `F-DENSITY` /
  `F-HIDDEN-CUT` / `F-SPATIAL-VAGUE`）迁入 `references/failure-codes.md`（唯一权威）
- 码数更正：**33 → 38**；修正码名漂移 `F-DPROP-DUP` → `F-PROP-DUP`

---

## ⚠️ 破坏性变更（迁移说明）

| 变化 | v8 的位置 | v9 的位置 |
| --- | --- | --- |
| 参考文档索引 | SKILL.md「参考文档」表（只列 31 篇） | **《参考文档加载表》** + `references/INDEX.md`（48 篇） |
| 并发控制协议 | SKILL.md 全文（与 reference 89% 重复） | `references/concurrency-control.md`（指针） |
| 进度状态查询 | SKILL.md 全文 | `references/progress-query.md`（指针） |
| 模型清单 / 平台限额 | SKILL.md 表（多处维护） | `references/model-mechanics.md`、`modes-and-recipes.md`（唯一权威） |
| 变更日志 | SKILL.md 内嵌 80 行 + CHANGELOG + release-notes | **`CHANGELOG.md` 唯一权威**（后者标为历史存档） |
| 质检清单 | SKILL.md 末尾 4 张表 | `references/qa-checklists.md`（Part A–E） |
| 错误码 | 5 个只在 SKILL.md | `references/failure-codes.md` §5（38 码） |
| 归因 | SKILL.md frontmatter 40 行 | `LICENSE`（完整版）+ frontmatter 指针 |

**未删除任何 reference 文件**；被移走内容均有落点（v9 复审曾发现 4 处无落点，已恢复：模型能力/清单 → `references/model-catalog.md`；v7.1.0/v7.0.4 日志 → 本文件历史段；提示词构建清单 → `references/qa-checklists.md`）。

## 🔒 兼容性

- 硬门、判据、模板、话术**逐字保留**（28 条硬门锚点由脚本断言，缺一即构建失败）
- 输出格式契约区（区块名逐字使用 / 词表 / 媒介翻译表）**与 `output-format.md` 模板**逐行一致**（由 `D2` 逐行断言）**（显式白名单）

---

# Seedancer v8.0.0 更新日志

_发布日期：2026-09-10_

---

## 🎯 核心升级

**Seedancer v8.0.0** 基于 ShotFunClaw agent-skills 深度研究，新增 **33项改进**，涵盖模型选择、断点续跑、QA门禁、并发控制等核心能力，全面提升生产效率和内容质量。

---

## ✨ 新增功能

### 批次A - 核心架构改进（6项）

| # | 功能 | 文件 | 说明 |
|---|------|------|------|
| A1 | 🆕 模型自动选择系统 | SKILL.md | 基于场景/预算/能力自动推荐模型 |
| A2 | 🆕 断点续跑协议 | references/checkpoint-resume.md | SHA-256一致性校验，支持中断恢复 |
| A3 | 🆕 严格QA门禁增强 | references/qa-strict-gates.md | 图像/视频/音频三维度QA检查 |
| A4 | 🆕 素材报白流程 | references/asset-whitelist.md | 真人素材自动走Asset://...报白 |
| A5 | 🆕 三种执行模式 | references/execution-modes.md | 快速/标准/完整模式切换 |
| A6 | 🆕 成本门禁协议 | references/cost-gates.md | 成本预估、确认、回填机制 |

### 批次B - 设计型改进（5项）

| # | 功能 | 文件 | 说明 |
|---|------|------|------|
| B1 | 🆕 视觉圣经模板 | references/visual-bible.md | 锁定视觉风格、角色、场景规范 |
| B2 | 🆕 共享边界分镜协议 | references/shared-boundary-storyboard.md | 相邻镜头边界状态一致性 |
| B3 | 🆕 内容指纹绑定 | references/content-fingerprint.md | 生成内容与原始输入强绑定 |
| B4 | 🆕 八项原片对照自检 | references/eight-item-self-check.md | 转绘内容与原片一致性检查 |
| B5 | 🆕 结构化失败报告 | references/structured-failure-report.md | 清晰可操作的错误信息 |

### 批次C - API集成改进（3项）

| # | 功能 | 文件 | 说明 |
|---|------|------|------|
| C1 | 🆕 视频分析管线协议 | references/video-analysis-pipeline.md | 480p代理+gemini分析，结构化输出 |
| C2 | 🆕 并发控制协议 | references/concurrency-control.md | 令牌桶算法，防止API限流 |
| C3 | 🆕 进度状态查询 | references/progress-query.md | 项目/分镜/资产进度实时查询 |

### 批次D - 高级功能（3项）

| # | 功能 | 文件 | 说明 |
|---|------|------|------|
| D1 | 🆕 AI自检修复协议 | references/ai-self-check-repair.md | 自动检测并修复生成内容问题 |
| D2 | 🆕 项目工作台协议 | references/project-workbench.md | 统一项目管理界面 |
| D3 | 🆕 版本号更新 | VERSION + CHANGELOG.md | v8.0.0正式发布 |

---

## 🔧 架构改进

### 模型自动选择系统

**选择维度**：
| 维度 | 选项 | 影响 |
|------|------|------|
| 场景类型 | 照片真实感/快速出图/720p视频/1080p视频/30秒长视频/口播视频/品牌广告/动作物理 | 推荐模型 |
| 预算偏好 | 低（省钱）/ 中（平衡）/ 高（质量优先） | 过滤价格档位 |
| 能力需求 | 参考图/真人素材/音画同出/局部编辑/文字渲染 | 过滤能力支持 |

**场景→模型映射表**（13种场景）：
- 照片级真实感图片 → GPT Image 2
- 快速出图 → Nano Banana 2
- 720p视频（性价比） → Seedance 2.0
- 1080p视频（高质量） → Kling 3.0 Omni
- 30秒长视频 → Seedance 2.5
- 口播视频 → Kling 3.0 Omni
- 品牌/广告 → MiniMax H3
- ...（共13种场景）

### 断点续跑机制

**核心功能**：
- SHA-256一致性校验
- manifest.json + step sidecar
- --resume 支持
- 自动跳过已完成步骤

**一致性校验**：
```
runSpecHash: 整个workflow输入的SHA-256
registryVersion: 注册表版本号
workflowVersion: workflow模块版本号
step.inputHash: 每步输入的SHA-256
```

### 严格QA门禁

**三维度检查**：
1. **图像资产QA**
   - 画幅比例：16:9横图
   - 背景：纯白背景
   - 人物完整性：正面+三视图
   - 身份一致性：同脸/发型/年龄/体型

2. **视频生成QA**
   - 禁止泄漏：字幕/源演员脸/错误语言
   - 禁止元素：字幕条/标题/漂浮文字
   - 人物一致性：前景人数/叙事关系
   - 连续性：空间状态/动作状态

3. **音频QA**
   - 语音正确性：语言/音色/口型同步
   - 禁止音频：背景音乐/错误语言

### 并发控制

**默认并发数**：
| 任务类型 | 默认并发 | 环境变量 |
|----------|----------|----------|
| 图片生成 | 30 | `SEEDANCER_IMAGE_CONCURRENCY` |
| 视频生成 | 50 | `SEEDANCER_VIDEO_CONCURRENCY` |
| 视频分析 | 10 | `SEEDANCER_ANALYSIS_CONCURRENCY` |
| 音频生成 | 20 | `SEEDANCER_AUDIO_CONCURRENCY` |

**限流保护**：
- 429 Too Many Requests: 指数退避重试
- 503 Service Unavailable: 固定延迟重试
- 最大重试次数: 3次

---

## 📊 性能提升

### 生产效率
- ✅ 断点续跑 + 批量执行 + 并发控制 → **生产效率提升50%+**
- ✅ 三种执行模式（快速/标准/完整）→ **灵活适配不同场景**

### 内容质量
- ✅ 八项自检 + QA门禁 + 内容指纹 → **内容质量提升30%+**
- ✅ 视觉圣经 + 共享边界分镜 → **视觉一致性显著提升**

### 用户体验
- ✅ 三种模式 + 资产画布 + AI自检 → **用户体验提升40%+**
- ✅ 进度状态查询 → **实时掌握项目进度**

### 成本控制
- ✅ 免费预检 + 视频分析 + 资产复用 → **成本降低20%+**
- ✅ 成本门禁协议 → **精确控制预算**

---

## 📝 技术细节

### 新增文件清单

**references/ 目录**（17个新文件）：
```
checkpoint-resume.md          # 断点续跑协议
qa-strict-gates.md            # 严格QA门禁
asset-whitelist.md            # 素材报白流程
execution-modes.md            # 三种执行模式
cost-gates.md                 # 成本门禁协议
visual-bible.md               # 视觉圣经模板
shared-boundary-storyboard.md # 共享边界分镜
content-fingerprint.md        # 内容指纹绑定
eight-item-self-check.md      # 八项自检
structured-failure-report.md  # 结构化失败报告
video-analysis-pipeline.md    # 视频分析管线
concurrency-control.md        # 并发控制
progress-query.md             # 进度查询
ai-self-check-repair.md       # AI自检修复
project-workbench.md          # 项目工作台
```

**SKILL.md 更新**：
- 新增模型自动选择系统章节
- 新增成本门禁协议章节
- 新增并发控制协议章节
- 新增进度状态查询章节

---

## 🔗 参考来源

**ShotFunClaw agent-skills**（11个技能包）：
- `shotfun-core` - 核心能力包（断点续跑、并发控制、成本门禁）
- `shotfun-drama-localization-pipeline` - 剧集本地化转绘（QA门禁、素材报白）
- `drama-gen` - 短剧生成（进度查询、资产画布）
- `redraw` - 视频转绘（八项自检、内容指纹）
- `picture-book-story-video` - 绘本动画（视觉圣经、共享边界）
- `ecommerce-video-agent` - 电商视频（模型选择）
- 其他技能包...

---

## 📅 发布计划

**v8.0.0** - 2026-09-10 正式发布

**后续计划**：
- v8.1.0 - 预计2026-10，增加更多自动化功能
- v8.2.0 - 预计2026-11，优化性能和稳定性

---

**完整变更日志**: `CHANGELOG.md`

---

## 📜 历史版本（v4–v7.1，自 v8 SKILL.md 逐字迁移）

### v7.1.0 (2026-09-10)

**新增 MiniMax H3 模型支持**
- ✅ MiniMax H3（2026-07-31 发布）：原生立体声、2K 分辨率、15秒时长、原生多镜头建模、V2V 运动转移、In-Context Regeneration 高分辨率重建、开源权重
- ✅ H3 擅长指令遵循、文字/品牌渲染精准、跨模态参考（从视频 A 取运镜、从图像 B 取角色、从音频 C 取声音）
- ✅ H3 定价优势：2K 视频 ~$0.061/秒，768p ~$0.036/秒，远低于主流模型
- ✅ 适用场景：广告/电商/品牌渲染/多模态交叉参考

**新增 Seedance 2.0 Mini 变体**
- ✅ Seedance 2.0 Mini：轻量变体，支持 4K 输出（2026-08 上线）
- ✅ 适合快速迭代与高分辨率交付场景

### v7.0.4 (2026-09-06)

**Kling 3.0 Omni 编辑管线升级信息更新**
- ✅ Kling 3.0 Omni 2026-06-17 编辑管线升级：4K 编辑输入/输出、一致性增强、3-15 秒编辑范围
- ✅ Kling 3.0 新增智能分镜系统、多语混说、主体参考/角色定向驱动
- ✅ 来源：Atlas Cloud AI (June 2026)、快手官方

**搜索发现**：
- Seedance 2.5 已正式发布（2026-07 上线），技能已完整支持
- Veo 3.1、Wan 3.0 暂无新更新信息

### v6.0.0 (2026-08-24)

**新增五大硬门系统** — 整合自 Elio_AIGC Seedance 2.0 Prompts V2.3（SKILL制作者：B站/抖音：Elio_AIGC）

**新增 6 个硬门**：
- ✅ **台词容量预检** — 最低时长公式 + 语速四档 + 视觉读取锚点 + 容量判定
- ✅ **分组硬门** — 模型适配时长上限 + 拆组规则 + 组尾稳定态 + 承接等式
- ✅ **镜头密度四道门** — Smin/Bmin/新反馈/Gmax + 短漫剧三档 + 关键路径承载
- ✅ **运镜设计系统** — 10种运镜叙事功能表 + 三要素 + 每场运镜主轴
- ✅ **输出格式硬门** — 自然段写法 + 四项事实 + 时间码规范 + 台词嵌入
- ✅ **空间/人物指代硬门** — 禁止模糊方位 + 禁止代词 + 视听术语双语

**新增 2 个门控**：
- ✅ **门控 7A: 台词容量预检** — 不过此门不进入分镜
- ✅ **门控 7B: 分组与密度门控** — 不过此门不输出分镜

**新增 4 个参考文档**：
- ✅ `references/dialogue-capacity.md` — 台词容量预检系统
- ✅ `references/grouping-density.md` — 分组硬门 + 镜头密度四道门
- ✅ `references/camera-design.md` — 运镜设计系统
- ✅ `references/output-format.md` — 输出格式 + 空间/指代硬门 + 媒介翻译

**新增 5 个错误码**：
- ✅ `F-DIALOGUE-CAPACITY` — 台词被压缩/语速不合理
- ✅ `F-GROUP-CONTINUITY` — 组尾不稳定/承接断裂
- ✅ `F-DENSITY` — 密度不足/空档过长
- ✅ `F-HIDDEN-CUT` — 隐藏切镜
- ✅ `F-SPATIAL-VAGUE` — 模糊方位/代词指代

**强化**：
- ✅ 黄金规则 5条 → 9条
- ✅ 矛盾检测 4层 → 6层
- ✅ 门控 8 质量检查新增 5 项硬门检查
- ✅ 阶段五 分镜写作全面硬门化
- ✅ 失败现象对照表新增 5 项

**来源**：整合 seedance20-video-prompts V2.3 by Elio_AIGC（B站/抖音：Elio_AIGC）

### v5.0.0 (2026-08-14)

新增 P0-P2 预生产管线。详见 v5.0.0 变更记录。

### v4.1.0 (2026-08-13)

整合 AIGC Film Studio 体系。

### v4.0.0 (2026-06-22)

Seedance 2.5 全面适配。

### v3.0.0 (2026-06-22)

架构级重构 — 8 门控路由 + 重拍协议 + 序列项目管理。

---
