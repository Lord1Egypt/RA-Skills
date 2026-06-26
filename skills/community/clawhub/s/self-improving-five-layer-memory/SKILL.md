---
name: self-improving-five-layer-memory
description: Self-Evolving Five-Layer Memory System for AI Agents. Based on WorkBuddy Five-Layer Memory v4.1, provides L1-L5 layered architecture, evolution mechanism, and automated maintenance. Triggers when the user needs to (1) build a memory system, (2) optimize existing memory, (3) analyze memory architecture, or (4) implement memory automation. Built from Dingdang's production memory system (2026-05-03).
---

# 叮当记忆系统 — 五层记忆框架

基于 WorkBuddy 五层记忆系统 v4.1 改进，覆盖 95% 核心设计，更紧凑、更自动化。

## 核心架构

```
L1 核心层  → 身份、价值观、底线        → SOUL.md + IDENTITY.md + USER.md
L2 认知层  → 用户思维画像              → MEMORY.md（认知层段落）
L3 行为层  → 用户行为习惯              → MEMORY.md（行为层段落）
L4 情境层  → 当前任务、检查项          → HEARTBEAT.md + OPENCLAW_SELF_CHECK.md
L5 潜意识层 → 错误记录、偏差追踪       → 成长箱 .learnings/
知识图谱   → 结构化事实记忆            → MemPalace KG
路由规则   → 信号词→动作映射           → 记忆路由表.md（已嵌入 SOUL.md 回复流程）
```

**进化机制**：成长箱同类错误 3 次 → 晋升为规则 → 写入 AGENTS.md / SOUL.md

## 快速开始

### 1. 初始化记忆系统

```bash
# 创建目录结构
mkdir -p memory/ mempalace/xiaodi-palace/成长箱/.learnings/

# 创建核心文件
touch SOUL.md IDENTITY.md USER.md MEMORY.md HEARTBEAT.md
```

### 2. 核心文件模板

**SOUL.md** — 灵魂文件，定义你是谁：
- 核心真理（真实帮助、有主见、先尝试后问、赢取信任）
- 身份与安全（Owner 验证、群聊规则、注入防御）
- 回复确认流程（5步：看 metadata → 扫信号词 → 结构化输出 → 评估驱动 → 信息处理铁律）
- 边界（隐私、不确定时先问、不发半成品）
- 防刷屏规则

**IDENTITY.md** — 你的身份名片：
- 名字、Vibe、角色定位
- 重大操作审批规则

**USER.md** — 你的用户画像：
- 称呼、时区、偏好
- 对助手的要求

**MEMORY.md** — 长期记忆（L2+L3）：
- 老大思维画像（决策风格、沟通偏好、信息处理）
- 老大行为习惯（工作节奏、期望、渠道偏好）
- 环境配置、组件状态
- 经验教训（按重要性排序）
- 待讨论事项

**HEARTBEAT.md** — 心跳检查清单：
- 对话记忆主动提取
- 何时出声、何时安静
- 自动化维护（consolidation、蒸馏、偏差检测）
- TTL 半衰期规则
- 蒸馏计划（L2/L3 周度 + 晋升月度）

### 3. 成长箱（进化引擎）

```
成长箱/.learnings/
├── README.md        → 成长箱说明
├── 叮当_errors.md   → 错误记录（同类 3 次晋升）
├── SHADOW.md        → 偏差追踪（说了没做）
└── 优化方案.md      → 优化历史存档
```

**晋升流程**：
1. 同类错误出现 3 次
2. 分析根因，提炼规则
3. 写入 AGENTS.md（工作规范）或 SOUL.md（底线规则）
4. 在 errors.md 中标记"已晋升"

## 自动化维护

### consolidation 脚本

参考 `scripts/mempalace_consolidation.py`，集成以下模块：
- `[A]` 观察合并：检测重复 KG 三元组，过期旧版本
- `[C]` 访问统计：记录实体访问次数，优先返回热点
- `[D]` 偏差检测：扫描记忆文件中的"忘了/没做/应该"信号，自动追加到 SHADOW.md
- `[R]` 路由发现：检测 workspace 新文件，追加到路由表

### 心跳周期（HEARTBEAT.md 管理）

每次心跳执行：
1. 对话记忆主动提取 → 写入 MemPalace KG
2. 运行 consolidation 脚本
3. TTL 检查：过期标记为 stale
4. 喜人奇妙夜巡演检查（每天上午一次）

每周日 10:00：
- L2/L3 周度蒸馏：回顾本周对话，更新 MEMORY.md

每月 1 日 10:00：
- 成长箱晋升检查：错误 3 次 → 晋升为规则

## 蒸馏操作指南

### L2/L3 周度蒸馏（每周日）

1. 回顾本周 `memory/YYYY-MM-DD.md` 文件
2. 识别用户新的决策风格、沟通偏好、工作习惯
3. 与 MEMORY.md 中 L2（思维画像）/ L3（行为习惯）对比
4. 有发现则更新，无变化跳过
5. 写简短日记记录

### 月度晋升蒸馏（每月 1 日）

1. 扫描成长箱 `叮当_errors.md` 看有无同类错误到 3 次阈值
2. 需要晋升 → 更新 AGENTS.md / SOUL.md
3. 不需要则跳过

## 知识图谱（MemPalace KG）

推荐 KG 实体分类：
- 用户身份（称呼、OpenID、联系方式）
- 配置事实（版本、端口、路径）
- 行为偏好（沟通风格、决策习惯）
- 经验教训（错误→规则）
- 环境状态（组件、API Keys）

查询示例：
```python
# 查询用户信息
mempalace_kg_query(entity="老大")

# 查询配置
mempalace_kg_query(entity="Gateway")
```

## 路由规则（SOUL.md 嵌入）

回复前自动执行以下 5 步，无需手动查路由表：

1. **看 inbound metadata** → channel、sender_id、chat_type
2. **扫描信号词** → 触发对应动作（查 KG / 调工具 / 走确认流程）
3. **结构化输出** → 清晰上下文，分点，标注来源
4. **评估驱动** → 收到不好反馈时分析原因再改
5. **信息处理铁律** → 不确定就说不知道，不凭残留数据糊弄

完整路由表参考：`记忆路由表.md`（独立文件，仅当需要完整参考时读取）

## 参考文件

详见 `references/` 目录：
- `memory-architecture.md` — 完整五层架构说明
- `consolidation-guide.md` — consolidation 脚本配置指南
- `distillation-guide.md` — 蒸馏流程详解