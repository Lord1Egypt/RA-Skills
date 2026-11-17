# 工具清单（Toolbox · 核心 skill 目录）

> **定位**：本 skill 达标检查（`checklist.md`）检出未达标项后的**执行器目录**——把精华的、核心的 skill 汇总成一份工具清单，作为 `install_skill` / `invoke_skill` 动作的**目标解析表**。
> **检测器 vs 执行器**：`checklist.md` 是「检测器」（逐条判达标），本清单是「执行器目录」（未达标装哪个、怎么装）。checklist 某条判 `fail` → 按该项 `actions[]` 里的 `tool-*` id 到本清单取对应工具的 `install` prompt 直接安装；已装则改 `invoke`。
> **与 skill-sources.md 的关系**：[skill-sources.md](../skill-sources.md) 是「从外部发现优秀 skill」的来源优先级与检索安装流程；本清单是从中**策展出的精华工具集**（精简、每次运行可全量加载、吃前缀缓存）。新增工具先经外部检索评估，确认为「高杠杆核心工具」后晋升进本清单。
> **待补充**：本清单持续增补（当前 4 条核心工具）。

---

## 使用规则（Agent 必读）

> ⚠️ **本清单技能均为 SkillHub 托管**：skill-map / skill-check-pro / skll-auto-upgrade / high-quality-skill-guidance 这 4 个核心 skill **不在内置推荐市场（BuiltinMarket）**，用 `find-skills` / `marketplace-skill-installer` 搜索必返回 0 结果（误判"未上架"）。**安装请直接复制下方各条的 `install` prompt 交用户执行**，切勿走市场搜索。任何清单条目的 `install` 字段已内含完整 SkillHub 安装指令。

1. checklist 检出 `install_skill` / `invoke_skill` 动作，且动作里标了 `tool-*` id → **先查本清单**。
2. 命中 → 工具未装 → 复制该工具 `install` prompt 交用户确认后安装；工具已装 → 直接 `invoke`。
3. 未命中（清单里没有）→ 回退 `references/skill-catalog/profile-theme-map.md`，按画像去 skillhub 搜（通用推荐路径）。

## 字段说明

| 字段 | 含义 |
|---|---|
| `id` | 唯一 id（`tool-<slug>`），供 checklist `actions[]` 引用 |
| `name` | 工具名（给人看） |
| `用途` | 一句话说清它做什么 |
| `install` | 复制即用的安装 prompt（含 skillhub CLI 引导） |
| `url` | 详情页链接 |
| `domain` | 领域（当前均为 `skill`） |
| `solves` | 解决的 checklist 问题（= 具体缺陷） |
| `when` | 何时用（触发场景） |
| `maps_to` | 关联 checklist 项 id |
| `预期效果` | 一句话可验证收益 |

---

## 工具条目

### tool-skill-designer · Skill Designer（高质量 Skill 设计指南）
- **用途**：教你写出高质量 SKILL.md / 设计规范的 skill
- **install**：`请根据 https://skillhub.cn/install/skillhub.md，安装 @user_4894573e/high-quality-skill-guidance`
- **url**：https://skillhub.cn/skills/user_4894573e/high-quality-skill-guidance
- **领域**：skill
- **solves**：不会写/不会改高质量 skill、skill 设计不规范、触发词/文档/结构不达标
- **when**：用户要新建/重构 skill；checklist `C-skill-03` 判 fail（反复手写长 prompt 未封装成 skill）
- **maps_to**：C-skill-03、C-prompt-01
- **预期效果**：skill 一次写到位，触发词命中、结构清晰、文档规范

### tool-skill-map · WorkBuddy Skill 全景地图
- **用途**：把已装 skill 渲染成一张可交互全景地图（分类/关联/热度），一眼看清 skill 生态
- **install**：`请根据 https://skillhub.cn/install/skillhub.md，安装 @user_7ba94f9e/skill-map`
- **url**：https://skillhub.cn/skills/user_7ba94f9e/skill-map
- **领域**：skill
- **solves**：装了一堆 skill 却看不清哪些低频、哪些吃上下文、哪些重复
- **when**：checklist `C-skill-01` 判 fail（skill 囤积 >30 全开）→ 用它可视化后决定关哪些
- **maps_to**：C-skill-01
- **预期效果**：skill 生态可视化，精简有依据、不再是盲关

### tool-skill-check-pro · WorkBuddy 技能生态管理中枢
- **用途**：「检查→跨技能深检→修复→升级→生态优化→安装推荐→可视化仪表板」七大能力，一键 skill 体检
- **install**：`请根据 https://skillhub.cn/install/skillhub.md，安装 @user_7ba94f9e/skill-check-pro`
- **url**：https://skillhub.cn/skills/user_7ba94f9e/skill-check-pro
- **领域**：skill
- **solves**：skill 坏了/该升级/该修复却不知道，只能逐个手动排查
- **when**：checklist `C-skill-01`（体检找低频）、`C-skill-02`（装生态维护类 skill）判 fail
- **maps_to**：C-skill-01、C-skill-02
- **预期效果**：skill 生态可体检、可维护，坏项与低分项被发现并给处方

### tool-skill-auto-upgrade · skill 自动升级（skill-auto-improve）
- **用途**：在 skill-check 体检结果之上，自动制定优先级改进方案、逐项确认后执行修改/升级/复盘
- **install**：`请根据 https://skillhub.cn/install/skillhub.md，安装 @user_7ba94f9e/skll-auto-upgrade`
- **url**：https://skillhub.cn/skills/user_7ba94f9e/skll-auto-upgrade
- **领域**：skill
- **solves**：体检发现了问题但没人去改、去升级，只能靠人工一个个手改
- **when**：checklist `C-skill-02` 已装 skill-check 但缺「自动改进」闭环；或 checklist「同步规则」要触发知识→checklist 更新
- **maps_to**：C-skill-02、（同步规则）
- **预期效果**：体检→改进→升级→复盘闭环自动化，skill 持续保鲜

---

## 映射表（checklist 未达标 → 对应工具）

| checklist 项 | 未达标时的工具动作 | 对应工具 |
|---|---|---|
| `C-skill-01` skill 精简 | `invoke` skill-check-pro 体检找低频 + `install` skill-map 可视化 | tool-skill-check-pro、tool-skill-map |
| `C-skill-02` 装生态维护 skill | `install` skill-check-pro（体检中枢） | tool-skill-check-pro |
| `C-skill-03` 复用 skill 而非手写 | `install` skill-designer（把高频手写 prompt 封装成高质量 skill） | tool-skill-designer |
| 同步规则（知识→checklist） | `invoke` skill-auto-upgrade 的「知识同步」能力 | tool-skill-auto-upgrade |

> 未列出的 checklist 项（如记忆/连接器/自动化领域）走 `guide` / `reconnect` / `enable_automation` / `write_memory` 等非 skill 动作，不落本清单。
