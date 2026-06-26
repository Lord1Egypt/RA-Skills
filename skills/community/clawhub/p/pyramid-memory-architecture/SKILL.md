---
name: 金字塔记忆架构
version: 3.4.0
description: 通用 AI Agent 记忆架构 Skill。采用"金字塔"分层结构:顶层(AGENTS.md)只放铁律级行为规则,中层(MEMORY.md/SOUL.md/HEARTBEAT.md)放业务规则和人格配置,底层(SKILL.md/TOOLS.md)放技术实现细节。适用于所有新建子 Agent 工作区初始化。触发场景:创建新 Agent、初始化工作区、记忆架构设计、规则录入引导、md 文件冗余检查、触发机制职责划分、任务归属标记检查。
---

# 金字塔记忆架构(Pyramid Memory Architecture)

> 本 Skill 提供一套标准化的 Agent 记忆分层架构,适用于任何新建子 Agent 工作区。
> 核心理念:**规则按触发优先级分层存放,引导只能从上往下,下层不引导回上层。**
> 版本:**v3.4** - 第9项新增:Heartbeat-Cron任务归属标记检查(杜绝重复执行)

## 📐 架构总览

```
         ▲
        / \
       /   \
      / AGENTS.md \    ← 顶层:系统注入,铁律级行为规则(每次必加载)
     /-----------\
    / MEMORY.md   \    ← 中层:主会话加载,业务规则、触发器、长期记忆
   /---------------\
  /  SOUL.md 等      \  ← 中层:人格配置、心跳清单、身份信息
 /---------------------\
/  self-improving/     \ ← 按需读取:执行经验、错误纠正、领域教训
/-----------------------\
\   SKILL.md/TOOLS.md   / ← 底层:按需读取,技术实现细节、操作流程
```

### 各层定位

| 层级 | 文件 | 加载方式 | 内容定位 |
|------|------|----------|----------|
| **顶层** | `AGENTS.md` | 系统级注入,每次必加载 | 铁律级行为规则、安全红线、引导表 |
| **中层** | `MEMORY.md` | 主会话系统注入 | 业务触发规则、长期记忆、项目规则 |
| **中层** | `SOUL.md` | 系统级注入 | 人格、身份、使命、行为准则 |
| **中层** | `HEARTBEAT.md` | 心跳触发时加载 | 待办提醒、报告队列、周期性检查清单 |
| **中层** | `IDENTITY.md` | 系统级注入 | Agent 身份卡片(名字、形象、表情) |
| **中层** | `USER.md` | 系统级注入 | 主人信息、作息、偏好 |
| **中层** | `TOOLS.md` | 系统级注入 | 本地配置笔记(设备、端口、Cookie) |
| **按需读取** | `self-improving/` | 任务前主动读取 | 执行经验、错误纠正、领域教训(memory.md / domains/ / projects/ / corrections.md) |
| **底层** | `SKILL.md` | 匹配场景时读取 | 技术实现、操作流程、选择器、正则 |
| **底层** | `docs/*.md` | 按需读取 | 详细操作文档、临时任务规则等 |

## 📝 规则录入铁律

### 录入原则

1. **按触发优先级引导**:
   - 系统注入文件(AGENTS/SOUL/MEMORY/TOOLS/IDENTITY/USER)> 按需读取文件(HEARTBEAT/memory日志/self-improving)> 外部 SKILL.md
2. **引导方向主要从上往下**:
   - ✅ AGENTS.md → 引导去 MEMORY.md / SKILL.md
   - ✅ MEMORY.md → 引导去 SKILL.md
   - ❌ 底层文件**不要引导回上层**(如 MEMORY.md 不要写"详见 AGENTS.md")
   - ⚠️ **安全锚**:底层文件如果有一条规则和顶层铁律直接相关,可以加备注:`⚠️ 此规则与 AGENTS.md 铁律相关,如有冲突以 AGENTS.md 为准`
3. **检查冗余时以高层级文件为准**:
   - 删除低层级已覆盖的重复内容
   - 低层级只保留自己独有的规则
4. **能引导就引导,实在引导不了再向主人推荐其他写入方式**

### 📂 注入 vs 非注入文件说明

**注入文件**(每次对话自动加载,Agent 一定能读到):
- `AGENTS.md` `SOUL.md` `MEMORY.md` `IDENTITY.md` `USER.md` `TOOLS.md`(由 OpenClaw 系统注入)
- `HEARTBEAT.md`(心跳触发时加载)

**非注入文件**(需要 Agent 主动读取,可能读不到):
- `SKILL.md`(需 `<available_skills>` 匹配才自动读取)
- `self-improving/` 目录(需任务前主动读取)
- `memory/` 日志(需 `memory_search` 或 `memory_get` 主动搜索)
- `docs/` 目录(需按路径手动读取)

**引导原则**:
- ✅ 重要规则尽量放在注入文件内,形成闭环
- ⚠️ 引导到非注入文件时,确保目标文件在 `<available_skills>` 中有 description 匹配
- ⚠️ 可以多层引导(A→B→C),前提是:每一级的 `#[锚点]` 在目标文件真实存在,且目标是系统注入文件或 description 匹配的 SKILL.md,确保 AI 能读到
- ✅ **推荐多级联链**:AGENTS.md(一行核心)→ MEMORY.md(业务展开)→ SKILL.md(技术实现)

### ⚠️ 隔离场景直写铁律
<!-- #isolated-direct-write -->

**cron 定时任务、子 agent、隔离会话中,禁止使用多级引导(详见XX),规则必须直写在 prompt 里。**

原因:隔离会话不加载 MEMORY.md/SOUL.md/HEARTBEAT.md 等注入文件,引导会断裂。

适用场景:
- OpenClaw cron 定时任务的 prompt
- `sessions_spawn` 创建的隔离子 agent
- 任何 `sessionTarget: isolated` 的场景

正确做法:
```json
{
  "payload": {
    "kind": "agentTurn",
    "message": "检查当月值班表 /path/to/duty.md,判断今天是否为值班日。\n\n如果是值班日:提醒用户做好值班准备。\n如果不是值班日:回复 NO_REPLY。"
  }
}
```

错误做法(引导会断裂):
```json
{
  "payload": {
    "kind": "agentTurn",
    "message": "详见 MEMORY.md(#duty-check)判断是否值班,如果是详见 HEARTBEAT.md(#duty-rules)推送提醒。"
  }
}
```

**总结:主会话对话可以 A→B→C 多级联链,隔离场景必须一句话写完,不要跳转。**

### 规则分类决策树
<!-- #rule-classify-tree -->

**每次写入或修改规则前，必须先过此判断矩阵。**

```
主人说要加/改一条规则
         ↓
问：这条规则描述的是什么？
         ↓
┌──────────────────────────────────────────────────────┐
│ A. 描述"什么时候做/做什么/触发条件/推送渠道"？        │
│    示例：每天23:30发文章、公众号先发草稿再发布          │
│         禁止重复参考已发过的文章、抖音走QQ小红书走微信    │
│    → MEMORY.md（业务规则层）                           │
├──────────────────────────────────────────────────────┤
│ B. 描述"怎么做/用什么工具/API/技术实现/操作步骤"？     │
│    示例：用web_search搜标题、HTML用内联样式禁止<style> │
│         调用wechat-mp-publish、封面上传流程、标题公式   │
│    → 对应的 SKILL.md（技术细节层）                     │
├──────────────────────────────────────────────────────┤
│ C. 描述"行为底线/安全红线/绝对禁止/必须先做"？         │
│    示例：必须先回答再操作、禁止未经授权删除文件         │
│         禁止私自改文件、失败一次就停手汇报              │
│    → AGENTS.md（铁律层）                              │
├──────────────────────────────────────────────────────┤
│ D. 描述"人格/身份/使命/行为风格"？                    │
│    示例：极客导师、沉稳务实、话少精准                   │
│    → SOUL.md / IDENTITY.md                            │
├──────────────────────────────────────────────────────┤
│ E. 描述"执行经验/踩坑教训/领域知识"？                  │
│    示例：OVATION 工作原则10条、360卸载失败经验          │
│    → self-improving/                                  │
└──────────────────────────────────────────────────────┘
```

### 录入流程
<!-- #rule-entry-flow -->

```
主人要求写入新规则
    ↓
1. 过规则分类决策树（见上方）：判断规则属于 A/B/C/D/E 哪类
    ↓
2. 匹配层级:
   - A类 → MEMORY.md
   - B类 → 对应的 SKILL.md / docs/
   - C类 → AGENTS.md
   - D类 → SOUL.md / IDENTITY.md
   - E类 → self-improving/
    ↓
3. 🔍 全局扫描关联项:
   - 扫描全部 md 文件,找出与新规则主题相关的所有现有规则
   - 判断这些相关规则之间是否能组成「多级联链」
   - 级联链不限于 2 层,可以 A→B→C 多层,前提是每层锚点真实存在且链路可达
    ↓
4. 向主人推荐级联方案:
   - 展示发现的关联规则分布
   - 推荐最优级联路径(例如:AGENTS.md 一行核心 → MEMORY.md 业务展开 → SKILL.md 技术实现)
   - 等待主人确认后执行
    ↓
5. 生成锚点名:<!-- #[英文短横线] -->
   - 命名规则:全小写 + 短横线分隔,如 #backup-rules
   - self-improving/ 锚点需加领域前缀,如 #ops-sync-failure
    ↓
6. 写入规则(级联格式):
   - AGENTS.md 只保留「一句话核心 + 一个引导语」
   - 执行步骤、技术细节等引导到下层文件
   - 每层只保留本层独有的内容
    ↓
7. 如不确定放哪层 → 向主人推荐
```

### 级联格式铁律
<!-- #cascade-format -->

**AGENTS.md 标准格式:一句话核心 + 引导语,不写执行步骤**

```markdown
- **修改 skill 必须同步问询**:详见 SKILL.md「同步流程」(#skill-sync-flow)
- **脚本执行失败就停手**:详见 SKILL.md「失败处理」(#fail-stop)
```

**多层级联链示例:**
```
AGENTS.md(铁律核心)
  → "修改 skill 必须同步问询":详见 SKILL.md「同步流程」(#skill-sync-flow)
      ↓
SKILL.md(执行细节)
  → #skill-sync-flow:同步内容=1版本号 2版本历史 3git commit+tag
  → "发布规则详见 MEMORY.md": 详见 MEMORY.md「发布渠道」(#publish-channels)
      ↓
MEMORY.md(业务规则)
  → #publish-channels:抖音走 QQ、小红书走微信
```

**级联链前提:链路必须通**
- 每一级的 `#[锚点]` 在目标文件中真实存在
- 引导目标是系统注入文件或 `<available_skills>` 匹配的 SKILL.md,确保 AI 能读到

### Skill 同步流程
<!-- #skill-sync-flow -->

修改任何 skill 内容并测试通过后,主动询问主人是否执行同步:
1. 更新 SKILL.md 版本号
2. 更新 SKILL.md 版本历史(保留最新 2 条)
3. git commit + tag + GitHub 推送
4. **🔢 同步脚本文件版本号** - 如果 skill 目录下有脚本文件(如 `scripts/*.js`)，必须同步更新脚本文件头部的版本号注释，确保 SKILL.md 版本号、脚本文件头版本号、git tag 三处一致
- 新增 skill 先创建独立 GitHub 仓库,禁止混入 monorepo
- 每个人格的 skill 推送各自对应的 GitHub 仓库,绝不混淆

### 失败处理
<!-- #fail-stop -->

当 SKILL.md 中明确写了「失败一次就停手汇报」时,第一次失败后必须立刻停止一切尝试,向主人汇报:
- 不得以任何理由继续自行尝试
- 这是保护 Cookie 和主人控制权的安全红线

### ⚠️ Skill 自包含原则
<!-- #skill-self-contained -->

**每个 SKILL.md 必须能独立指导完整操作流程，不依赖 MEMORY.md 的技术细节。**

- ✅ 业务触发逻辑（何时触发、推送渠道配置）可以引导去 MEMORY.md
- ✅ 技术实现细节（怎么执行、API 调用、排版规范、标题公式、上传流程）必须在 SKILL.md 写完整
- ❌ 违反表现：MEMORY.md 里出现"步骤1/2/3"、"用 xxx API"、"HTML 用内联样式"、"封面上传流程"等

**检查方法**：MEMORY.md 中如果出现操作步骤类内容（含"步骤/流程/API 调用/上传/生成/排版/标题公式"等技术词），视为违反自包含原则，应移至对应 SKILL.md。

### 各层"独有规则"示例

| 层级 | 应该放什么 | 不应该放什么 |
|------|-----------|-------------|
| **AGENTS.md** | 一句话核心铁律 + 引导语、安全红线、行为底线 | 执行步骤、技术细节、详细说明 |
| **MEMORY.md** | 业务触发规则、推送渠道、项目专属规则、禁止重复规则、同步规则 | 操作步骤、API 调用、HTML 排版、标题公式、封面上传流程 |
| **SOUL.md** | 人格描述、使命、能力设定、行为准则、底线 | 通用行为铁律(应放 AGENTS.md) |
| **HEARTBEAT.md** | 待办提醒、报告队列、检查项 | 推送规则详情(应引到 MEMORY.md) |
| **SKILL.md** | 操作步骤、API 调用、HTML 排版、标题公式、封面上传、技术选择器、正则、版本历史 | 业务触发逻辑、推送渠道配置、人格描述 |
| **TOOLS.md** | 本地配置笔记（设备端口、Cookie、API Key 存放路径） | 业务规则、操作流程 |

### 标准引导语格式

**统一格式:** `详见 [文件]「[章节名]」(#[锚点])`

**AGENTS.md 标准引导表示例:**
```markdown
## 🔗 其他规则引导

| 类别 | 引导位置 |
|------|----------|
| 记忆系统规则 | 详见 MEMORY.md(#clawhub-publish-rules) |
| 心跳检查清单 | 详见 HEARTBEAT.md(#reminder-tasks) |
| 技能调用说明 | 详见各 SKILL.md |
| 本地配置 | 详见 TOOLS.md |
```

**其他常见引导示例:**
- `详见 SKILL.md「规则录入流程」(#rule-entry-flow)`
- `详见 MEMORY.md「ClawHub 上架规则」(#clawhub-publish-rules)`
- `详见 self-improving/memory.md(#ops-sync-failure)`



## 🔄 冗余检查机制
<!-- #redundancy-check -->

**每 3 天执行一次 9 项检查清单，发现后按照金字塔架构规则，推荐主人清理，主人确认后执行。**

### 触发机制配置
<!-- #trigger-setup -->

冗余检查**不会自动触发**，需要手动配置触发器。根据 Agent 类型选择方案：

**方案 A：Heartbeat + 状态文件（推荐，适用于有心跳的 Agent）**

1. **在 `HEARTBEAT.md` 添加任务**：
   ```markdown
   ## 🔺 金字塔冗余检查（每 3 天一次）
   1. 读取 `memory/redundancy-check-state.json`，检查 `lastCheckDate`
   2. 如果距今天 ≥ 3 天，或 `lastCheck` 为 `null`（首次），则执行
   3. 按本 Skill `#redundancy-check` 的 9 项清单逐一检查
   4. 向主人汇报结果（只汇报，不擅自修改，等确认再清理）
   5. 更新 `memory/redundancy-check-state.json` 的 `lastCheck` 和 `lastCheckDate`
   ```
2. **创建状态文件** `memory/redundancy-check-state.json`：
   ```json
   {
     "lastCheck": null,
     "lastCheckDate": null
   }
   ```

**方案 B：cron 定时任务（无心跳的 Agent）**

隔离会话无法读取 Skill，必须把 9 项检查流程完整写在 cron prompt 里，不能用「详见 SKILL.md」引导。

### 9 项检查清单

1. **内容冗余**:同一规则是否出现在多个文件中
2. **引导方向**:有没有底层文件引导回顶层(违反从上往下原则)
3. **锚点一致性**:引导语里的 `#[锚点]` 是否在目标文件中真实存在
4. **引导格式**:是否都使用 `详见 [文件]「[章节名]」(#[锚点])` 格式
5. **版本历史**:各 SKILL.md 版本历史是否超过 2 条
6. **文件大小**:各 md 文件是否异常膨胀(>3KB 需检查)
7. **金字塔合规（动态词指纹检查）**:
   - **Step 1**: 扫描 workspace 下所有 SKILL.md，动态提取技术关键词（动态词指纹）：
     - skill name 和 description 中的动词（如 web_search、wechat-mp-publish、封面上传）
     - SKILL.md 正文中的 API 名、工具名、技术名词（如 HTML 内联样式、排版规范、标题公式）
   - **Step 2**: 用这些词去匹配 MEMORY.md 的所有规则
   - **Step 3**: 发现匹配 → 提示"MEMORY.md 中的规则含技术关键词 {词}，可能应该放 {skill名}.md"
   - **Step 4**: 同时检查 AGENTS.md 中是否包含操作/技术类内容（应下放至 SKILL.md）
   - **Step 5**: 检查 MEMORY.md 中是否包含铁律/红线类内容（应上移至 AGENTS.md）
8. **连接建议**:只在发现明显主题相关的规则时才建议级联,不全量扫描
9. **触发机制职责划分+健康检查+通道校验+触发-流程链路完整性**:
   - **三域扫描**:扫描当前agent自己workspace下的HEARTBEAT.md流程规则、当前agent的cron任务列表、当前agent的launchd任务列表(**只检查本agent区域,不干涉其他agent**)
   - **同域去重**:
     - Cron内部:同一个功能不能建两个cron任务
     - Launchd内部:不能重复配置
     - Cron vs Launchd:同一功能不能既配cron又配launchd脚本
     - ⚠️ HEARTBEAT.md vs Cron**不去重**(它们是配套关系:流程说明书+闹钟)
   - **触发状态健康检查**:
     - **Heartbeat**:检查当前agent的heartbeat是否启用、间隔是否正常、上次触发时间
     - **Cron**:检查当前agent的cron任务status是否为ok、Last是否有值(证明跑过)、有无失败记录
     - **Launchd**:检查PID是否存在、LastExitStatus是否为0(正常退出)、有无crash重启
     - 发现问题标记:⚠️配置了但没触发 / ⚠️触发了但失败 / ⚠️从来没跑过
   - **触发机制职责划分**:
     - 逐个分析任务特性,推荐最适合的机制:
       - **launchd**(macOS系统级):不需要OpenClaw会话的独立任务,如脚本执行、文件备份、系统健康检查
       - **Cron**(OpenClaw内置):需要精确时间点触发、隔离会话执行的任务,如"周三14:00开会""每日23:00写日志"
       - **Heartbeat**(OpenClaw主会话唤醒):不需要精确时间点,定期唤醒判断状态再执行的任务,如"每3天冗余检查""值班日判断"
   - **推送通道校验**:
     - 检查每个提醒任务的delivery target(agent+channel)是否与任务类型匹配
     - 工作类应走微信通道,舞蹈类可走石榴的QQ通道,运维类走栗子QQ通道
     - 发现问题标记:⚠️工作提醒推到了QQ / ⚠️舞蹈提醒推到了微信 / ⚠️推送到不存在的通道
   - **触发-流程链路完整性**:
     - HEARTBEAT.md有流程 → 有没有对应cron触发?(防遗漏)
     - cron有任务 → prompt有没有正确引用HEARTBEAT.md对应区块?(防断链)
     - cron prompt是否包含"读HEARTBEAT.md第X区块,按流程执行"的明确指令?(隔离会话必须一句话写完规则,不能跳转引用)
     - 有没有cron触发了但HEARTBEAT.md没对应流程的?(防空转)
   - **Heartbeat-Cron任务归属标记检查**:
     - HEARTBEAT.md每个任务是否明确标注归属?(cron/heartbeat/流程参考)
     - 已配cron的任务 → HEARTBEAT.md是否标记为"流程参考"或"走cron",避免heartbeat重复执行?
     - 没有配cron的任务 → 是否标注为"heartbeat待执行"?
     - 发现问题标记:⚠️任务归属不明 / ⚠️已配cron但HEARTBEAT未标注流程参考
   - 生成报告汇报给主人,等确认后再调整,不自动修改

### 执行步骤

1. **读取触发状态**：先读 `memory/redundancy-check-state.json`，判断是否满足 3 天间隔（仅 Heartbeat 方案）
2. 读取所有 md 文件内容
3. 逐项检查上述 9 项清单
3. 第7项(金字塔合规):
   a. 动态词指纹提取:扫描所有 SKILL.md,提取技术关键词
   b. 用动态词指纹匹配 MEMORY.md,发现技术细节错位→建议移至 SKILL.md
   c. 扫描 AGENTS.md,发现操作步骤类内容→建议下放至 SKILL.md
   d. 扫描 MEMORY.md,发现铁律/红线类内容→建议上移至 AGENTS.md
   e. 检查 MEMORY.md 是否违反 Skill 自包含原则(含操作步骤/API/标题公式等)
4. 第8项(连接建议):只在发现明显主题相关的规则时才建议级联(如两条都是运维安全类),不强制
5. 第9项(触发机制职责划分+健康检查+通道校验+链路完整性+归属标记):
   a. 扫描当前agent自己workspace下的HEARTBEAT.md所有流程规则(cron和launchd只查当前agent的,通过agentId过滤,不干涉其他agent)
   b. 同域去重:cron内部/cron与launchd之间的重复任务
   c. 触发状态健康检查:Heartbeat启用状态、Cron Last值、Launchd PID和ExitStatus
   d. 触发机制职责划分:逐个分析推荐最适合机制(launchd/cron/heartbeat)
   e. 推送通道校验:检查delivery target是否与任务类型匹配
   f. 触发-流程链路完整性:HEARTBEAT.md流程vs cron prompt双向检查,确保链路完整
   g. 任务归属标记检查:HEARTBEAT.md每个任务是否明确标注归属(cron/heartbeat/流程参考)
   h. 生成报告,汇报给主人,等确认后再调整
8. 按照金字塔架构规则,以高层级文件为准,删除低层级重复
9. 向主人汇报检查结果,确认后执行清理
10. **更新状态文件**：写入当前时间到 `memory/redundancy-check-state.json`（仅 Heartbeat 方案）

### 检查报告模板

```
## 冗余检查报告(YYYY-MM-DD)

| 检查项 | 状态 | 详情 |
|--------|------|------|
| 内容冗余 | ✅/❌ | ... |
| 引导方向 | ✅/❌ | ... |
| 锚点一致性 | ✅/❌ | ... |
| 引导格式 | ✅/❌ | ... |
| 版本历史 | ✅/❌ | ... |
| 文件大小 | ✅/❌ | ... |
| 金字塔合规 | ✅/❌ | 动态词指纹检查结果 + 层级错位详情 |
| 连接建议 | 💡/无 | 仅明显相关时建议 |
| 触发机制划分+链路完整性 | ✅/⚠️ | 三域职责划分+健康检查+通道校验+触发-流程链路完整性(仅本agent区域) |

发现问题:[描述]
层级放错建议:[描述]
重复触发风险:[同一任务出现在两个及以上机制中时列出]
触发健康告警:[配置了但没触发/触发了但失败/从来没跑过的任务]
通道校验告警:[工作提醒推到了QQ/舞蹈提醒推到了微信/推送到不存在的通道]
链路完整性告警:[HEARTBEAT有流程但无cron触发/cron有任务但HEARTBEAT无对应流程/cron prompt未正确引用HEARTBEAT区块]
归属标记告警:[任务归属不明/已配cron但HEARTBEAT未标注流程参考/未标注heartbeat待执行]
归类建议:[每个任务推荐放的触发机制及理由]
连接建议:[仅明显相关时才提]
建议操作:[描述]
```

## 🚀 快速部署

### 方式一:一键初始化脚本(推荐)

*   **Mac / Linux 用户**:
    ```bash
    ./scripts/init.sh my-new-agent
    ```
*   **Windows 用户 (PowerShell)**:
    ```powershell
    .\scripts\init.ps1 my-new-agent
    ```

### 方式二:手动初始化

创建新子 Agent 时,按以下结构初始化:

```
workspace-{name}/
├── AGENTS.md          ← 顶层铁律模板
├── MEMORY.md          ← 中层业务规则模板
├── SOUL.md            ← 中层人格配置模板
├── IDENTITY.md        ← 身份卡片模板
├── USER.md            ← 主人信息模板
├── TOOLS.md           ← 本地配置模板
├── HEARTBEAT.md       ← 心跳清单模板
├── docs/              ← 详细文档目录
└── self-improving/    ← 自我进化目录
```

## 📋 模板文件

各层模板详见 `templates/` 目录(v2.0 教学版):

| 模板 | 路径 | 说明 |
|------|------|------|
| AGENTS.md | `templates/AGENTS.md` | 顶层铁律模板(带使用说明注释) |
| MEMORY.md | `templates/MEMORY.md` | 中层业务规则模板(带示例) |
| SOUL.md | `templates/SOUL.md` | 中层人格配置模板(带安全锚示例) |
| IDENTITY.md | `templates/IDENTITY.md` | 身份卡片模板 |
| USER.md | `templates/USER.md` | 主人信息模板 |
| TOOLS.md | `templates/TOOLS.md` | 本地配置模板 |
| HEARTBEAT.md | `templates/HEARTBEAT.md` | 心跳清单模板 |

## 📖 版本历史

| 版本 | 日期 | 变更 |
| v3.4 | 2026-05-31 | **第9项新增任务归属标记检查**:1新增HEARTBEAT-Cron任务归属标记检查(每个任务必须标注归属:走cron/走heartbeat/流程参考);2防止已配cron的任务被heartbeat重复执行;3HEARTBEAT.md已配cron任务应标注为"流程参考"未配cron任务标注为"heartbeat待执行";4发现问题标记告警;5生成报告不自动修改 ✅ |
| v3.3 | 2026-05-31 | **第9项重构为触发-流程链路完整性**:1明确HEARTBEAT.md=Cron配套关系(流程说明书+闹钟)不去重;2新增同域去重(cron内部/cron与launchd);3新增Agent隔离(只查本agent区域,按agentId过滤,不干涉其他agent);4新增推送通道校验(agent+channel匹配);5新增触发-流程链路完整性双向检查(HEARTBEAT流程vs cron prompt);6新增cron prompt规范(隔离会话一句话写完规则,禁止跳转引用);7生成报告不自动修改 ✅ |
