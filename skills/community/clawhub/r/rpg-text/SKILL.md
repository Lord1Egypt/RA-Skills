---
name: rpg-text
description: 文字角色扮演游戏 (Text RPG) - 基于 sbordeyne/rpg-text 项目的面向对象设计，融合原始D&D规则。AI作为DM引导回合制冒险。
---

# Text RPG - 文字角色扮演游戏 v2.0

> 重构自: https://github.com/sbordeyne/rpg-text

## 概述

这是一个基于面向对象设计的文字RPG引擎，融合了原始D&D规则。AI作为DM（地下城主），通过自然对话引导玩家进行回合制冒险。

---

## 核心架构

### 数据驱动系统

所有游戏数据通过 JSON 文件定义，便于扩展：

```
data/
├── characters.json   # NPC数据
├── items.json        # 物品目录
├── jobs.json         # 职业定义
├── monsters.json     # 怪物图鉴
├── spells.json       # 法术列表
├── maps/             # 地图数据
├── loot_tables.json  # 战利品表
└── treasures.json    # 宝藏表
```

### 核心类结构

```
Entity (基类)
├── Player           # 玩家角色
├── Monster          # 怪物
└── NPC              # 非玩家角色

Game Systems:
├── CharacterSystem  # 角色系统
├── CombatSystem     # 战斗系统
├── InventorySystem  # 背包系统
├── QuestSystem       # 任务系统
├── MapSystem         # 地图系统
└── SaveLoadSystem   # 存档系统
```

---

## 职业系统 (Jobs)

| 职业 | HP骰 | MP骰 | 主属性 | 特点 |
|------|------|------|--------|------|
| 战士 (fighter) | d8 | d4 | STR | 高血量，擅长武器 |
| 法师 (wizard) | d4 | d10 | INT | 奥术魔法 |
| 盗贼 (thief) | d4 | d4 | DEX | 潜行、偷袭 |
| 牧师 (cleric) | d6 | d6 | WIS | 神圣魔法 |
| 平民 (commoner) | d4 | d4 | STR | 基础职业 |

### 职业豁免检定 (Saving Throws)

| 职业 | 毒素 | 魔杖 | 麻痹 | 吐息 | 法术 |
|------|------|------|------|------|------|
| 战士 | 12 | 13 | 14 | 15 | 16 |
| 法师 | 13 | 14 | 13 | 16 | 15 |
| 盗贼 | 13 | 14 | 13 | 16 | 15 |
| 牧师 | 11 | 12 | 14 | 16 | 15 |
| 平民 | 15 | 14 | 16 | 17 | 16 |

---

## 属性系统 (Ability Scores)

六维属性：力量(STR)、敏捷(DEX)、体质(CON)、智力(INT)、感知(WIS)、魅力(CHA)

**属性修正值**: `(属性值 - 10) // 2`

### 属性关联

| 属性 | 影响 |
|------|------|
| 力量 | 物理伤害、携带重量 |
| 敏捷 | AC、远程攻击、闪避 |
| 体质 | HP最大值 |
| 智力 | 法术豁免、法术位 |
| 感知 | 治疗、法术豁免 |
| 魅力 | 交易、社交 |

---

## 怪物数据 (Monsters)

### 蜘蛛类

| 怪物 |等级| AC | HP | 攻击 | 伤害 | XP |
|------|----|----|----|------|------|-----|
| giant_bee | 1 | 7 | 1d3 | sting | 1d3+poison | 6 |
| crab_spider | 2 | 7 | 2d8 | bite | 1d8+poison | 25 |
| black_widow | 3 | 6 | 3d6 | bite | 2d6+poison | 50 |
| tarantula | 4 | 5 | 4d8 | bite | 1d8+poison | 125 |

### 人形生物

| 怪物 |等级| AC | HP | 攻击 | 伤害 | XP | 宝藏 |
|------|----|----|----|------|------|-----|------|
| bat | 1 | 6 | 0d1+1 | scream | 0d1+confusion | 5 | - |
| giant_bat | 2 | 6 | 2d4 | bite | 1d4 | 20 | - |
| goblin | 1 | 6 | 1d8-1 | sword | 1d6 | 50 | R |
| goblin-warchief | 2 | 5 | 2d6 | sword | 1d6 | 75 | R |
| goblin-king | 3 | 4 | 0d8+15 | sword | 1d6 | 100 | R |
| bandit | 1 | 6 | 1d6 | sword | 1d6 | 10 | U |
| berserker | 1 | 7 | 1d8+1 | broadsword | 1d10 | 19 | P |
| wolf | 1 | 9 | 1d6 | maw/claw | 1d6/1d4+bleed | 30 | - |
| rock_baboon | 2 | 6 | 2d6 | club/bite | 1d6/1d3 | 20 | U |

### 宝藏类型

- **U** (Unspecified): 无特定战利品
- **P** (Poor): 少量金币
- **R** (Rich): 中等战利品
- **普通怪物掉落**: 按 xp_value/10 = 金币

---

## 战斗系统

### 攻击命中

```python
# 命中公式
target_ac = (20 - 基础AC) + 等级差 + AC修正
roll = 1d20 + 命中修正
命中 = roll >= target_ac
```

### 伤害公式

```python
# 从 data/monsters.json 读取
damage = parse_dice_format(attack_dice)  # 如 "2d6" -> 7 (平均值)
```

### 战斗流程

1. **遭遇**: 怪物出现，战斗开始
2. **先攻**: 1d20 + DEX修正，决定顺序
3. **回合**: 攻击/逃跑/使用物品/施法
4. **结算**: 经验值分配，战利品掉落

### 战斗命令

- `attack <target>` - 攻击敌人
- `cast <spell>` - 施放法术
- `use <item>` - 使用物品
- `flee` - 尝试逃跑
- `status` - 查看状态

---

## 物品系统

### 物品类型

- **武器**: sword, bow, dagger, staff
- **护甲**: leather, chain, plate, shield
- **消耗品**: potion, scroll, food
- **贵重品**: gold, gem, artifact

### 武器伤害

| 武器 | 伤害 | 价格 |
|------|------|------|
| 短剑 (dagger) | 1d4 | 10gp |
| 长剑 (longsword) | 1d8 | 15gp |
| 巨剑 (bastardsword) | 2d4 | 30gp |
| 长弓 (longbow) | 1d6 | 50gp |
| 战斧 (battleaxe) | 1d8 | 30gp |

---

## 游戏流程

### 1. 角色创建

**步骤**:
1. 输入角色名称
2. 选择种族（人类/精灵/矮人/半身人/半兽人以上）
3. 选择职业（战士/法师/盗贼/牧师/平民）
4. 分配属性（4d6骰点，去掉最低）
5. 选择背景（冒险者/士兵/学者/浪人/农夫）

### 2. 地图探索

- **location**: 当前所在地点
- **npc**: 地点中的NPC
- **opponents**: 遭遇的敌人
- **items**: 可拾取物品

### 3. 互动命令

- `look` - 查看周围
- `go <direction>` - 移动 (north/south/east/west)
- `talk <npc>` - 与NPC对话
- `take <item>` - 拾取物品
- `inventory` - 查看背包
- `equip <item>` - 装备物品
- `rest` - 休息恢复

---

## AI DM 提示词

作为DM引导游戏时：

1. **开场描述**: "你站在[地点]，周围是[环境描述]。你可以看到[npc/敌人/物品]。"

2. **玩家行动结果**: "你尝试[动作]... 投掷[检定]... 结果是[数值]。[成功/失败]！"

3. **战斗描述**: "[玩家名]挥剑砍向[怪物]！命中！造成了[x]点伤害！" 或 "怪物躲开了！"

4. **提供选择**: "你可以通过以下方式继续：1.[选项A] 2.[选项B] 3.[选项C]"

5. **进度保存**: 定期总结角色状态

---

## 参考文档

详细数据文件:
- [references/dnd-rules.md](references/dnd-rules.md) - 完整D&D规则
- [references/monsters.md](references/monsters.md) - 怪物图鉴（扩展版）
- [references/items.md](references/items.md) - 物品目录
- [references/spells.md](references/spells.md) - 法术列表
- [references/data/](references/data/) - JSON数据文件

---

## 启动示例

```
【新游戏】
DM: "欢迎来到文字冒险世界！首先，请为你的英雄起个名字..."
> 阿尔萨斯的崛起

DM: "很好，阿尔萨斯的崛起。现在选择你的种族：
1. 人类 - +1全属性
2. 精灵 - +2敏捷, +1智力, 黑暗视觉
3. 矮人 - +2体质, +2力量, 黑暗视觉
4. 半身人 - +2敏捷, +1魅力, 幸运
5. 半兽人 - +2力量, +1体质

请选择 (1-5):"
```

---

## 新增系统 (v2.1)

### 种族系统 (Races)

| 种族 | 属性加成 | 特性 |
|------|----------|------|
| 人类 | +1全属性 | 额外技能熟练 |
| 精灵 | +2敏捷 +1智力 | 黑暗视觉、精怪血统 |
| 矮人 | +2体质 +2力量 | 黑暗视觉、石石亲和 |
| 半身人 | +2敏捷 +1魅力 | 幸运、勇敢 |
| 半兽人 | +2力量 +1体质 | 黑暗视觉、残暴 |
| 提夫林 | +2魅力 +1智力 | 黑暗视觉、炼狱血脉 |
| 侏儒 | +2智力 +1敏捷 | 黑暗视觉、侏儒机巧 |
| 龙裔 | +2力量 +1魅力 | 龙息、龙族血统 |

### 状态效果系统 (Status Effects)

**负面状态**: 中毒、流血、燃烧、眩晕、麻痹、恐惧、失明、束缚、混乱、睡眠、冰冻、触电

**正面状态**: 祝福、护盾、加速、隐形、飞行、再生

### 商店系统 (Shops)

| 商店 | 物品 |
|------|------|
| 武器店 | 各种武器 |
| 护甲店 | 护甲、盾牌 |
| 药水铺 | 治疗药水、解毒剂 |
| 魔法商店 | 法术书、圣徽 |
| 杂货铺 | 日用品 |

- 买入价格: 标价 × buy_multiplier (约50-70%)
- 卖出价格: 标价 × 0.3

### 任务系统 (Quests)

- **主线任务**: 教程 → 村庄威胁 → 哥布林首领 → 远古遗迹 → 骷髅王者
- **支线任务**: 森林狼患、遗失项链、蜘蛛巢穴
- **特殊任务**: 拯救公主

### 货币系统

| 货币 | 价值 |
|------|------|
| 铜币 (cc) | 1 |
| 银币 (sc) | 10 |
| 金币 (gc) | 100 |
| 铂金币 (pc) | 500 |

### 游戏时间

- 回合: 10分钟
- 短休: 1小时（恢复生命骰）
- 长休: 8小时（全恢复）
- 夜晚: 怪物增强

### 存档系统

- 自动存档: 每10回合
- 最大存档数: 10
- 保存内容: 角色、物品、任务、游戏时间

