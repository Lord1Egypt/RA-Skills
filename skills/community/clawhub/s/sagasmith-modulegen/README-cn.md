# ✍️ SagaSmith Module Generator

[English](README.md) | [中文](README-cn.md)

**D&D 5e 冒险模组 AI 生成器**

> 一句话让 AI 写出完整可跑的 D&D 冒险——带章节结构、NPC 欲望与秘密、伏笔回收链、DC 数值、怪物数据。

独立 skill，零依赖，纯 `SKILL.md`。兼容 Claude Code / Codex / Cursor / Copilot / OpenClaw / Hermes 等所有支持 SKILL.md 标准的 agent。

---

## 生态

| 仓库 | 定位 |
|------|------|
| ✍️ **SagaSmith-module-gen-skills**（本仓库） | 独立模组生成 skill |
| 🎲 [SagaSmith-agent](https://github.com/dajiaohuang/SagaSmith-agent) | 完整 AI DM 运行时 |
| 📦 [SagaSmith-skills](https://github.com/dajiaohuang/SagaSmith-skills) | 全家桶 skill 插件包 |

---

## 不是"创意点子生成器"

大多数 AI 写模组是这样的：你让它"想个冒险"，它给你一段散文式描述，没有结构、没有数值、没有关卡设计。

SagaSmith Module Generator 产出的是**可直接导入跑团的完整模组文件**：

- ✅ 按章节组织的 `# heading` 结构（`dnd_module action=import` 直读）
- ✅ 房间级 `####` 子标题 + 类型标注（`room` / `statblock` / `list`）
- ✅ NPC 全维度：`name / race / class / alignment / want / fear / secret`
- ✅ 伏笔-回收表 + 势力关系网 + 结局分支
- ✅ DC 数值 + 怪物数据 + 魔法物品
- ✅ 导出场景索引 JSON（DM 无需查库即可导航）

---

## 5 种类型 × 25 种范式

| 类型 | 章节 | 默认范式 | 更多范式 | 产出规模 |
|------|------|----------|----------|----------|
| 🎯 **One-shot** | 1 | Five-Room Dungeon | Heist, Mystery, Reverse Dungeon | 1 次，3-6h |
| 📖 **Short** | 3 | Three-Act | Kishōtenketsu, Race Against Time, Island Design | 3-8 次 |
| 📚 **Medium** | 5 | Hero's Journey | Plot Point, Faction Turn, Fish Tank | 2-4 月战役 |
| 🏰 **Long** | 8 | Double Triangle | Conspyramid, Megadungeon, Technoir | 6+ 月战役 |
| 🗺️ **Sandbox** | 4-6 区域 | Hexcrawl | Node-Based, Blorb, Decision-Based | 开放探索 |

---

## 生成范式

| 驱动类型 | 范式 | 一句话 |
|----------|------|--------|
| 空间 | **Five-Room Dungeon** | 入口守卫 → 谜题/社交 → 陷阱/反转 → Boss → 奖励 |
| 空间 | **Hexcrawl** | 六角格地图，每格独立遭遇与地点 |
| 空间 | **Megadungeon** | 多层地城，环形路线，内部派系 |
| 故事 | **Three-Act** | 建立 → 对抗 → 解决，Ch.2 中场反转 |
| 故事 | **Hero's Journey** | 平凡世界 → 跨越门槛 → 试炼 → 深渊 → 归来 |
| 故事 | **Double Triangle** | Ch.1-4 崛起 → Ch.5-6 陨落 → Ch.7-8 救赎 |
| 故事 | **Kishōtenketsu** | 起承转合，无需反派 |
| 故事 | **Seven-Point Story** | Hook → PT1 → Pinch1 → Midpoint → Pinch2 → PT2 → Resolution |
| 玩法 | **Heist** | 情报 → 计划 → 执行 → 意外 → 脱逃 |
| 玩法 | **Mystery** | Hook → 3 地点 → 每点 3 线索 → 揭示（三线索法则） |
| 玩法 | **Conspyramid** | 6 层阴谋 + 6 层应对金字塔 |
| 玩法 | **Faction Turn** | 派系独立于玩家推进 |
| 玩法 | **Race Against Time** | 限时：X 轮完成 Y 目标 |
| 角色 | **Plot Point** | 主线章节 + 角色个人线并行 |
| 角色 | **Fish Tank** | 事件 + 派系已就位，玩家是投入的变量 |
| 角色 | **Blorb** | 准备实体，不准备情节。Prep > rules > improv |
| 混合 | **Iceberg Diagram** | 表面钩子 → 隐藏深度 |
| 混合 | **Reverse Dungeon** | 玩家防守，怪物进攻 |

---

## 生成流程

### 单步（One-shot / Short）
一次性产出完整模组 → 写入文件 → 导入数据库

### 多步（Medium / Long）
**M1** → 骨架（概要 + 势力 + 章节大纲 + NPC 全维度）→ 用户审核  
**M2** → 前半章节正文 → 用户审核  
**M3** → 后半章节 + 附录（伏笔回收表、势力变化、怪物、魔法物品）→ 组装成最终文件

### 沙盒
**S1** → 世界骨架（区域总览 + 势力网 + 随机遭遇表）  
**S2-N** → 每个区域独立生成（特征 + 势力 + 事件线 + 地点 × 3-6）

每一步都有用户审核节点——不会在无人确认的情况下推进到下一步，避免幻觉堆积。

---

## 快速安装

```bash
# Claude Code / Codex / Cursor / Copilot
npx skills add dajiaohuang/SagaSmith-module-gen-skills

# ClawHub
npx clawhub install sagasmith-modulegen
```

---

---

## 使用示例

### One-shot — 单次冒险

```
用户: 帮我生成一个 2 级 Halloween 主题 one-shot，
      用 Five-Room Dungeon 范式，反派是稻草人精魂

Agent:
✅ 参数确认：One-shot · Five-Room Dungeon
   主题：万圣节/南瓜田 · 反派：稻草人精魂 (CR 1 × 3)
   等级：2 · 氛围：恐怖喜剧

[生成完整模组 → modules/pumpkin_horror.md]

输出摘要：
📜 南瓜田的恐怖 / The Pumpkin Horror
   Scene 1: 丰收节庆典 (入口守卫 — 失踪儿童事件)
   Scene 2: 老磨坊的谜语 (谜题 — 稻草人只会说字谜)
   Scene 3: 活过来的南瓜田 (反转 — 稻草人是受害者)
   Scene 4: 谷仓 Boss 战 (高潮 — 真正的幕后: 绿鬼婆)
   Scene 5: 丰收节归来 (奖励 — 村民的感激 + 1 件魔法物品)
```

### Short — 三幕短战役

```
用户: 帮我生成一个 5 级沙漠盗墓 short 模组，
      用 Kishōtenketsu 范式，反派是木乃伊领主

Agent:
✅ 参数确认：Short (3 Ch) · Kishōtenketsu (起承转合)
   主题：沙漠/古墓 · 反派：木乃伊领主 + 圣甲虫集群
   等级：5 · 反转：木乃伊在守护封印更邪恶的东西

[生成 3 章 → 每章 3 场景 → modules/desert_tomb.md]

输出摘要：
📜 沙海之下的封印
   第一章「起」— 绿洲商队的委托，三个 NPC 各有秘密
   第二章「承」— 深入地下金字塔，5 个陷阱房间
   第三章「转」— 木乃伊并非敌人，真正威胁是封印下的
                    古老存在。结局分支：释放 / 加固 / 摧毁
   附录：NPC 全维度 · 4 个伏笔回收 · 木乃伊领主数据
```

### Medium — 五章战役

```
用户: 生成一个 medium 模组，7 级都市政治主题，
      用 Hero's Journey 范式

Agent:
[Step M1] 骨架生成中...
   5 章大纲 · 4 个派系 · 12 个 NPC (全部 want/fear/secret)
   详见 modules/city_of_masks_skeleton.md，请审核。

用户: Ch.2 的反派动机不够强，改成他被勒索

Agent:
✅ 已调整：议长是被 Zhentarim 用家族秘密勒索的

[Step M2] 前 3 章正文生成中...
   Ch.1 平凡世界 · Ch.2 跨越门槛 · Ch.3 试炼
   详见 modules/city_of_masks_ch1-3.md

[Step M3] 后 2 章 + 附录生成中...
   Ch.4 深渊 · Ch.5 归来
   伏笔回收表 (5 章全链) · 势力变化时间线 · Boss 三阶段
   ✅ 最终文件：modules/city_of_masks.md
```

### Long — 八章史诗

```
用户: 生成一个 long 模组，1-20 级奇幻史诗，
      用 Double Triangle 范式

Agent:
[Step L1] 概念 + 双弧线大纲...
   反派时间线 (8 章) · 双弧线结构 · Ch.4 假胜利设计
   Ch.8 多重结局 (4 分支) · 22 个 NPC 含个人弧光
   详见 modules/the_last_circle_concept.md

[经过 5 步渐进生成...]

✅ 最终模组：modules/the_last_circle.md
   📊 8 章 · 48 场景 · 22 NPC · 12 伏笔回收链
   👤 每个 PC 2-3 场景个人线 · Boss 四阶段
```

### Sandbox — 开放世界

```
用户: 生成一个沙盒，维京主题群岛探索

Agent:
[Step S1] 世界骨架...
   6 个区域 · 3 个派系 · 随机遭遇表 (1d12)
   详见 modules/viking_isles_world.md

用户: 生成北岛区域

Agent:
[Step S2] 区域：北岛·霜骨群岛
   特征：被龙裔部族控制的冻土岛链
   势力：白霜部族 · 事件线 × 3
   地点：龙骸港 · 霜语洞穴 · 长老议会厅 · 热泉圣所
   ✅ 已追加到 modules/viking_isles.md
```

---

## 致谢

- [ackiles/dnd-dm-skill](https://github.com/ackiles/dnd-dm-skill) — D&D DM skill 先驱
- 25 种范式源自 TRPG 社区数十年的设计积累（Five-Room Dungeon、Three Clue Rule、Hexcrawl 等）

---

## 许可证

MIT
