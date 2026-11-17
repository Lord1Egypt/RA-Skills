# A 类子契约 · AVG / 文字冒险 / 跑团 TTRPG（storyforge-writing）

> 归属：A 开发创作（创作语料侧）。对应 StoryForge TEXT-ADVENTURE / TTRPG-AI-KP / TEXT-OPEN-WORLD 产品契约。
> **只出语料，不碰 runtime**：可玩开放世界、活体 KP、session 运行态是产品引擎，本 skill 只生成设定/剧本侧语料。

## 0. 现行通用内核 `AdventureContentV2`（v0.2.0 补。八能力源：TEXT-ADVENTURE.md **§2**；下文「19 个独立岗位 / 结局资格」源：同文 **§4**）

在统一的**行动 / 前置 / 检查 / 效果**协议之上，登记**八个必需能力**：
**空间 · 角色 · 背包 · 装备 · 任务 · 时间 · storylet · 结局**。

- **空间层级**：大区域 → 区域 → 地点 → 场景；行动仍绑定**稳定地点与目标 key**。
- **角色能力**：由通用 `ability` 表达，并以 `stat` / `skill` 角色区分；
  生命 / 法力 / 体力 / 经验 / 技能点 / 货币 / 时间是有**上下界**的通用资源角色。
- **装备**：通过**槽位 + 标签 + 能力修正**生效；**同一槽位最多一件**；**重放必须得到相同有效能力值**。
- **任务**：由主线 / 支线 / 环境任务分类，含阶段与目标；**一个目标允许多种通用行动完成**，
  失败**默认产生代价或新局面**（不是「重试直至成功」）。

**唯一权威写入**：行动与叙事选择分别经 `commitAdventureAction` / `commitAdventureNarrativeChoice`。
本 skill **只产语料**，不实现这两个入口，也**不得自行发明并行的写入路径**。

**施工入口（源侧）**：`docs/products/text-adventure-production/`（19 个独立岗位，每岗位只挂自己的核心 Skill；
结局资格由互斥、完备、可穷举验证的**持久决定条件**裁决，不由「数组前缀」猜测）。

## 1. 文字冒险 / 文字游戏（text-adventure）

| 语料块 | 字段 | 说明 |
|---|---|---|
| 场景树 | sceneId, parentId, order, description | DAG 场景 |
| 分支/选择 | choiceKey, sourceNodeKey, targetNodeKey | 选择指向目标场景 |
| 对白 | speakerCharacterId, nodeKey, order | 场景内台词 |
| 结局 | endingType, 达成条件 | 多结局 |
| 物品/状态 | itemLedger(itemName, chapterId)、状态机 | 携带/解锁 |
| 规则 | 文字开放世界不变量 | 经济/犯罪/旅行等约束 |

**S1→S2→S3**：只读引用冻结 WorldRelease；场景/事件在 S3 产品实例私域推进，不回写世界。

## 2. 跑团 TTRPG（TTRPG-AI-KP）

| 语料块 | 字段 | 说明 |
|---|---|---|
| 规则包 | ttrpgRulePacks(ruleSystemId, ruleSystemVersion, status, contentHash) | 稳定系统版本 |
| 场景/事件 | 场景描述、触发、NPC、结果 | KP 引导素材 |
| 玩家线 | 参与者/座位/actor 分配 | 只出"引导语料"，不模拟 |

- 跑团产品**只读引用**冻结世界；运行事件只在实例私域推进
- 本 skill 出**规则包 + 场景 + 事件 + NPC 语料**，不出活体 KP runtime

## 3. 文字开放世界（创作基线侧）

- 输出：世界规则、场景、经济/旅行/犯罪不变量、可玩路径**设计稿**
- 生成/运行/发布/私域演化归产品 runtime；本 skill 停在"语料 + 不变量清单"
- 不得用样例冒充"真实可玩"，能力边界以产品契约为准

## 4. 共性生成纪律

1. 场景/分支/对白/物品全部走**候选→采纳**（同总入口 SOP）
2. 世界引用冻结 WorldReference + 版本 + contentHash
3. 裁剪留 Context Manifest 证据
4. 影响只向未来传播；已确认历史不静默改写

## 5. 与 A-longform 的关系

文字冒险/跑团可**复用长篇的世界观/角色/规则**（worldviews/characters/powerSystems/creativeRules），
但以独立产品 work 拥有运行态；世界引用走 S2 定向（WorldReference + Brief + SourcePlan + 用户授权）。

## 6. 所有权 · 不变量 · 禁止项（v0.4.0）

**所有权**：本技能 owns 交互类产物的生成纪律；上游 owns `AdventureContentV2` 八能力与写入 API；
**作者** owns 分支与结局的取舍。

**不变量**
- `INV-I-1` `AdventureContentV2` **八能力齐备**方可交付（缺一不可）。
- `INV-I-2` 写入只经 `commitAdventureAction` / `commitAdventureNarrativeChoice`，**不得自造写入路径**。
- `INV-I-3` 跑团（TTRPG）语境下世界为**只读冻结**：规则包/场景/事件不得改写世界设定。

**禁止项**
- 不得在跑团上下文里回写世界或角色 Canon。
- 不得声称已"运行"游戏会话（本技能只产出语料）。
