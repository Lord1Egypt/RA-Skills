---
name: dnd-module-gen
description: Generate D&D 5e adventure modules. Supports one-shot, short (3 chapters), medium (5 chapters), long (8 chapters), and sandbox. Use when the user asks to create, generate, or make a new adventure, module, or campaign setting.
---

# D&D Module Generator

## Core Rules

1. **Always write to file first.** Never inline-import generated content. Write to `<workspace>/modules/<name>.md`, then import from that path via `dnd_module action=import source_path=...`. This preserves the generated module as a reusable artifact.

2. **One-shot and short are one-step generation.** Generate the complete module in a single pass, write to file, import.

3. **Medium and long are multi-step generation.** Each step produces one section of the module. User reviews each step before proceeding. This avoids context overflow and allows course correction.

4. **Sandbox generates top-level overview first**, then each region independently.

---

## Step 0: Determine Type & Parameters

| Type | Chapters | Sessions | Steps |
|------|----------|----------|-------|
| **one-shot** | 1 | 1 (3-6h) | 1 |
| **short** | 3 | 3-8 | 1 |
| **medium** | 5 | 2-4 months | 3 |
| **long** | 8 | 6+ months | 5 |
| **sandbox** | 4-6 regions | open | 1+N |

Ask the user, or randomize. Tell them:

- 类型 / 范式 / 主题 / 环境 / 反派 / 等级 / 氛围
- 反转次数 / NPC 深度 / 结局分支 / 种子

### Paradigm Reference

| Type | Default Paradigms | Alternatives |
|------|-------------------|--------------|
| one-shot | Five-Room Dungeon, Mystery, Heist | Beat Charts, Reverse Dungeon |
| short | Three-Act, Kishōtenketsu | Race Against Time, Island Design |
| medium | Hero's Journey, Plot Point | Fish Tank, Pointcrawl, Faction Turn |
| long | Double Triangle, Conspyramid | Megadungeon, Technoir |
| sandbox | Hexcrawl, Node-Based | Decision-Based, Blorb, Faction Turn |

Full paradigm glossary: see bottom of this skill.

---

## One-shot & Short: One-Step Generation

Generate the complete module in one pass.

**Output path:** `<workspace>/modules/<name>.md`

**One-shot template:**

```markdown
# <模组名>

## 冒险概要
<2-3 sentences>

## 冒险背景
<3-5 sentences>

# <scene1: 开场/社交>
<NPC list, dialogue, mission hook>

# <scene2: 探索/地城>
<3-5 rooms with #### headings>

# <scene3: Boss/高潮>
<enemies, tactics, resolution>

# <scene4: 尾声>
<optional epilogue>

# 附录
## 主要 NPC | 怪物 | 魔法物品
```

**Short template (3 chapters, Three-Act):**

```markdown
# <模组名>

## 冒险概要 | 冒险背景 | 运作本模组

# 第一章：建立
## <scene1> ← NPC 引入 + 任务
## <scene2> ← 首次挑战 + 线索
## <scene3> ← 过渡/旅程

# 第二章：对抗
## <scene1> ← 中场反转
## <scene2> ← 核心地城 (4-8 rooms)
## <scene3> ← 揭示 + 选择点

# 第三章：解决
## <scene1> ← 最终逼近
## <scene2> ← Boss 战
## <scene3> ← 结局 (2-3 分支)

# 附录
## 主要 NPC (want/fear/secret) | 伏笔-回收表 | 怪物 | 魔法物品
```

After writing the file, import and export scene index:

```
dnd_module action=import campaign_id=<id> module_name="<name>" source_path="<workspace>/modules/<name>.md"
dnd_module action=index campaign_id=<id>
python -m nanobot.dnd.db.cli module export-scenes --campaign <id> --output "<workspace>/modules/<name>_scenes.json"
```

---

## Medium: Three-Step Generation

### Step M1 — 骨架（概念 + 势力 + NPC）

**Output:** `<workspace>/modules/<name>_skeleton.md`

```markdown
# <模组名>（骨架）

## 冒险概要
<5-8 sentences: 整个 5 章的完整故事线>

## 冒险背景
<8-12 sentences: 世界历史、当前局势、核心冲突>

## 运作本模组
<level range, pacing, key choices that shape the campaign>

## 势力关系网
| 势力 | 目标 | 盟友 | 敌对 | 首领 |
|------|------|------|------|------|
<3-5 factions>

## 章节大纲
| 章 | 标题 | 核心冲突 | 情感节拍 | 关键 NPC | 反转/揭示 |
|----|------|---------|---------|---------|----------|
| 1 | ... | ... | ... | ... | - |
| 2 | ... | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... | 中期危机 |
| 4 | ... | ... | ... | ... | ... |
| 5 | ... | ... | ... | ... | 最终揭示 |

## 主要 NPC（完整）
每人: name, race, class, alignment, want, fear, secret, chapter appearances

## 伏笔-回收表
| 伏笔 | 埋入章节 | 回收章节 | 内容 |
```

**User reviews this before proceeding.** Adjust based on feedback.

---

### Step M2 — 前 3 章正文

**Output:** `<workspace>/modules/<name>_ch1-3.md`

Generate Ch.1-3 in full, each chapter following the short template structure (3-5 scenes per chapter, rooms with `####`, NPC lists with dialogue, DC values, rewards).

Merge with skeleton after user approves:

```
# 将 skeleton + ch1-3 合并写入最终文件
```

Actually: write skeleton parts that stay + ch1-3 body into `<workspace>/modules/<name>.md` as a partial file.

---

### Step M3 — 后 2 章 + 附录

**Output:** final `<workspace>/modules/<name>.md`

Generate Ch.4-5. Then assemble the complete module file:
- Skeleton (概要, 背景, 运作, 势力)
- Ch.1-3 (from M2)
- Ch.4-5 (newly generated)
- 附录 (NPC, 伏笔-回收表, 势力变化, 怪物, 魔法物品)

Import, index, and export scene index (see Import section).

---

## Long: Five-Step Generation

### Step L1 — 概念 + 双弧线大纲

**Output:** `<workspace>/modules/<name>_concept.md`

```markdown
# <模组名>（概念）

## 冒险概要 (10-15 sentences, full 8-chapter story)

## 反派时间线
| 阶段 | 章节 | 反派行动 | 玩家可见线索 |
<actions the villain takes even if players do nothing>

## 双弧线结构
### 第一弧：崛起 (Ch.1-4)
| 章 | 标题 | 核心冲突 | 虚假胜利的伏笔 |
### 第二弧：陨落与重生 (Ch.5-8)
| 章 | 标题 | 核心冲突 | 重生要素 |

## Ch.4 虚假胜利设计
<What makes players think they won? What did they actually cause?>

## Ch.8 多重结局设计
<3-5 ending branches based on accumulated player choices>

## 势力关系网 (5-8 factions, their evolution across 8 chapters)
## 主要 NPC (完整，含 arc)
```

User reviews. Adjust.

### Step L2 — 第一弧正文 (Ch.1-4)

**Output:** `<workspace>/modules/<name>_arc1.md`

Full chapter bodies for Ch.1-4. Each 4-8 scenes.

### Step L3 — 第二弧正文 (Ch.5-8)

**Output:** `<workspace>/modules/<name>_arc2.md`

Full chapter bodies for Ch.5-8.

### Step L4 — 角色个人线 + 附录

**Output:** append to final file.

For each PC, a 2-3 scene personal arc that intersects the main plot.
Generate: NPC appendix (含 arc), 伏笔-回收表 (8 章完整链), 势力变化时间线, 怪物 (含 Boss 多阶段), 魔法物品, Epilogue.

### Step L5 — 组装

Combine all parts into `<workspace>/modules/<name>.md`. Import, index, and export scene index (see Import section).

---

## Sandbox: 1+N Step Generation

### Step S1 — 世界骨架

**Output:** `<workspace>/modules/<name>_world.md`

```markdown
# <沙盒名>（世界）

## 世界概况
<8-12 sentences: map scope, core conflict, faction landscape>

## 区域总览
| 区域 | 地形 | 控制势力 | 危险等级 | 关键地标 |
<4-6 regions>

## 势力关系网
| 势力A | 关系 | 势力B | 说明 |

## 随机遭遇总表 (1d12)
## 关键 NPC 总表
```

### Step S2-N — 每个区域独立生成

For each region, user says "生成区域X" or "all regions":

**Output per region:** appended to `<workspace>/modules/<name>.md`

```markdown
# 区域<N>：<名称>
## 区域特征 (3-5 sentences)
## 势力 (who controls this, what they want)
## 事件线 (2-4, each: trigger→process→outcome)
## 地点 (3-6 key locations with #### room headings)
```

After all regions: import, index, and export scene index (see Import section).

---

## Import & Scene Index

After the module file is complete:

```
# 1. Import into database
dnd_module action=import campaign_id=<id> module_name="<name>" source_path="<workspace>/modules/<name>.md"

# 2. Verify structure
dnd_module action=index campaign_id=<id>

# 3. Export scene index JSON (saved alongside the .md file)
python -m nanobot.dnd.db.cli module export-scenes --campaign <id> --output "<workspace>/modules/<name>_scenes.json"
```

The `_scenes.json` file mirrors the structure of `references/dnd-dm-skill/srd/scenes_index.json`:
- Scene boundaries with line numbers
- Keywords/tags per scene
- Room-type annotations
- Sub-section headings

This gives the DM a human-readable scene map they can reference without querying the database.

Report chapter/scene/chunk counts after import. If module already exists, ask user before deleting and re-importing.

---

## Paradigm Glossary

**Space-driven:**
- **Five-Room Dungeon**: entrance guardian → puzzle/RP → trick/setback → climax → reward/revelation
- **Node-Based**: nodes (places, NPCs, events) connected by clues/geography/time. Non-linear.
- **Hexcrawl**: hex grid map, each hex has encounters/locations. Random encounter tables.
- **Megadungeon**: multi-level dungeon, looping routes, factions within.
- **Island Design**: independent modular elements, any order.

**Story-driven:**
- **Three-Act**: establish → confront → resolve. Midpoint twist in Ch.2.
- **Hero's Journey**: ordinary world → cross threshold → trials → abyss → return.
- **Double Triangle**: rise (Ch.1-4) → fall (Ch.5-6) → redemption (Ch.7-8). Ch.4: false victory.
- **Kishōtenketsu** (起承转合): introduce → develop → twist → harmony. No required antagonist.
- **Beat Charts**: Hook → alternating Developments & Cliffhangers → Resolution.
- **Hamlet's Hit Points**: alternating hope/fear beats.
- **Seven-Point Story**: Hook → PT1 → Pinch1 → Midpoint → Pinch2 → PT2 → Resolution.

**Play-driven:**
- **Heist**: intel → planning → execution → complication → escape.
- **Mystery**: Hook → 3 cool locations → 3 clues per node → reveal. Three Clue Rule.
- **Conspyramid**: 6-layer conspiracy + 6-layer response pyramid.
- **Faction Turn**: factions advance independently of players.
- **Race Against Time**: clock: X rounds to complete Y.
- **Survival**: resource management focus.

**Character-driven:**
- **Plot Point Campaign**: main Episodes + character Savage Tales.
- **Fish Tank Intrigue**: events + factions; players are the variable dropped in.
- **Technoir Transmission**: 36-node table, 2d6 pick 3 seeds, define triangle.
- **Decision-Based**: clear choices → modular world → adaptation.
- **Blorb**: prep entities not plots. Prep > rules > improv.

**Hybrid:**
- **Iceberg Diagram**: surface hook → hidden depths.
- **Reverse Dungeon**: players defend, monsters attack.
