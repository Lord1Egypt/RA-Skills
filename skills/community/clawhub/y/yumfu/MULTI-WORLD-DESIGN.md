# YumFu - 多世界观MUD设计

## 🌍 支持的世界观

### 中文世界（武侠）
1. **笑傲江湖** - 华山派争斗、五岳剑派、日月神教
2. **倚天屠龙记** - 六大门派围攻光明顶、屠龙刀倚天剑
3. **射雕英雄传** - 五绝争霸、郭靖守襄阳
4. **天龙八部** - 三大主角、少林武当、辽国西夏

### 英文世界（奇幻）
1. **Harry Potter** - Hogwarts四学院、魔法、巫师决斗
2. **Lord of the Rings** - 中土世界、九大种族、魔戒远征
3. **Game of Thrones** - 七大王国、权力的游戏、龙
4. **The Witcher** - 猎魔人、怪物狩猎、魔法流派
5. **Warrior Cats** - 野猫部落、四大部族、星族指引

---

## 🎮 初始化流程

### 第一步：语言选择（双语提示）
```
🌍 Welcome to YumFu - Multi-World MUD! | 欢迎来到YumFu - 多世界MUD！

Please select your language / 请选择语言：
1. 中文 (Chinese)
2. English

Reply with: /yumfu lang <number>
回复：/yumfu lang <数字>
```

### 第二步：世界观选择

**中文玩家：**
```
请选择您的江湖世界：

1. 📖 笑傲江湖 (Xiào Ào Jiāng Hú)
   - 时代：明朝中期
   - 特色：剑派争斗、正邪对立
   - 门派：华山、武当、少林、日月神教...
   - 秘籍：独孤九剑、辟邪剑法、吸星大法

2. 🗡️ 倚天屠龙记 (Yǐ Tiān Tú Lóng Jì)
   - 时代：元末明初
   - 特色：神兵争夺、六大门派围攻光明顶
   - 门派：明教、武当、峨眉、少林...
   - 秘籍：九阳神功、乾坤大挪移、圣火令

3. ⚔️ 射雕英雄传 (Shè Diāo Yīng Xióng Zhuàn)
   - 时代：南宋
   - 特色：五绝争霸、襄阳保卫战
   - 门派：丐帮、全真教、桃花岛、白驼山
   - 秘籍：九阴真经、降龙十八掌、九阴白骨爪

4. 🐉 天龙八部 (Tiān Lóng Bā Bù)
   - 时代：北宋
   - 特色：三大主角、江湖与朝堂
   - 门派：丐帮、少林、逍遥派、星宿派
   - 秘籍：六脉神剑、北冥神功、凌波微步

回复：/yumfu world <数字>
```

**English Players:**
```
Choose your fantasy realm:

1. ⚡ Harry Potter Universe
   - Era: Modern magical world
   - Houses: Gryffindor, Slytherin, Ravenclaw, Hufflepuff
   - Skills: Offensive spells, Defense, Potions, Transfiguration
   - Artifacts: Elder Wand, Invisibility Cloak, Philosopher's Stone

2. 🗡️ Middle-earth (LOTR)
   - Era: Third Age
   - Races: Human, Elf, Dwarf, Hobbit, Wizard
   - Skills: Swordsmanship, Archery, Magic, Stealth
   - Artifacts: One Ring, Andúril, Mithril Armor

3. 🐉 Game of Thrones (Westeros)
   - Era: Age of Dragons
   - Houses: Stark, Lannister, Targaryen, Baratheon...
   - Skills: Combat, Intrigue, Wildfire, Dragon-riding
   - Artifacts: Valyrian Steel, Dragonglass, Dragon Eggs

4. 🐺 The Witcher (Continent)
   - Era: Post-Conjunction
   - Schools: Wolf, Cat, Griffin, Bear
   - Skills: Signs (magic), Alchemy, Swordsmanship, Monster lore
   - Artifacts: Witcher Medallions, Silver Swords

5. 🐱 Warrior Cats
   - Era: Forest Territory / Lake Territory
   - Clans: ThunderClan, RiverClan, WindClan, ShadowClan
   - Skills: Hunting, Battle moves, StarClan connection
   - Artifacts: Leader's 9 lives, Medicine Cat herbs

Reply: /yumfu world <number>
```

---

## 📁 存档结构

```json
{
  "version": 2,
  "user_id": "123456789",
  "language": "zh",
  "universe": "xiaoao",
  "character": {
    "name": "小虾米",
    "world_specific": {
      "faction": "华山派",
      "moral_alignment": "正派"
    }
  }
}
```

**英文版：**
```json
{
  "version": 2,
  "user_id": "987654321",
  "language": "en",
  "universe": "lotr",
  "character": {
    "name": "Aragorn",
    "world_specific": {
      "race": "Human",
      "faction": "Dúnedain Rangers"
    }
  }
}
```

---

## 🎨 配图风格（根据世界观）

### 中文武侠：
```
Chinese wuxia ink wash painting style, dramatic cinematic composition...
```

### Harry Potter:
```
Magical wizarding world illustration, Hogwarts castle aesthetic, soft warm lighting, watercolor style with ink accents...
```

### LOTR:
```
Epic fantasy landscape painting in Alan Lee style, Middle-earth atmosphere, dramatic mountains and forests, oil painting texture...
```

### Game of Thrones:
```
Dark medieval fantasy illustration, gritty realistic style, dramatic lighting, muted earth tones with blood-red accents...
```

### The Witcher:
```
Dark fantasy art in Slavic folklore style, monster hunter aesthetic, moody atmosphere, detailed armor and weapons...
```

---

## 🗂️ 世界观配置文件

创建 `worlds/` 目录：
```
skills/yumfu/
├── worlds/
│   ├── xiaoao.json       # 笑傲江湖
│   ├── yitian.json       # 倚天屠龙记
│   ├── shediao.json      # 射雕英雄传
│   ├── tianlong.json     # 天龙八部
│   ├── harry-potter.json # 哈利波特
│   ├── lotr.json         # 指环王
│   ├── got.json          # 权力的游戏
│   └── witcher.json      # 猎魔人
```

### 示例：`worlds/xiaoao.json`
```json
{
  "id": "xiaoao",
  "name_zh": "笑傲江湖",
  "name_en": "Swordsman",
  "language": "zh",
  "genre": "wuxia",
  "factions": [
    "华山派", "武当派", "少林寺", "日月神教", "独行侠"
  ],
  "skills": [
    "独孤九剑", "辟邪剑法", "紫霞神功", "吸星大法"
  ],
  "npcs": [
    {"name": "风清扬", "title": "剑道宗师"},
    {"name": "东方不败", "title": "日月神教教主"}
  ],
  "art_style": "Chinese wuxia ink wash painting...",
  "starting_location": "华山派"
}
```

### 示例：`worlds/harry-potter.json`
```json
{
  "id": "harry-potter",
  "name_zh": "哈利波特",
  "name_en": "Harry Potter",
  "language": "en",
  "genre": "magical-fantasy",
  "factions": [
    "Gryffindor", "Slytherin", "Ravenclaw", "Hufflepuff", "Independent Wizard"
  ],
  "skills": [
    "Expelliarmus", "Patronus Charm", "Avada Kedavra", "Legilimency"
  ],
  "npcs": [
    {"name": "Albus Dumbledore", "title": "Headmaster"},
    {"name": "Voldemort", "title": "Dark Lord"}
  ],
  "art_style": "Magical wizarding world illustration, Hogwarts castle aesthetic...",
  "starting_location": "Diagon Alley"
}
```

---

## 🌐 本地化字符串

创建 `i18n/` 目录：
```
skills/yumfu/
├── i18n/
│   ├── zh.json    # 中文UI文本
│   └── en.json    # 英文UI文本
```

### `i18n/zh.json`:
```json
{
  "welcome": "欢迎来到{world}！",
  "choose_faction": "请选择您的门派：",
  "level_up": "恭喜！您升到了{level}级",
  "combat_start": "战斗开始！",
  "hp": "体力",
  "mp": "内力"
}
```

### `i18n/en.json`:
```json
{
  "welcome": "Welcome to {world}!",
  "choose_faction": "Choose your faction:",
  "level_up": "Congratulations! You reached level {level}",
  "combat_start": "Combat begins!",
  "hp": "Health Points",
  "mp": "Magic Points"
}
```

---

## 🎯 触发指令（双语）

```
/yumfu start          # 初始化，显示语言选择
/yumfu lang <1|2>     # 选择语言
/yumfu world <数字>   # 选择世界观
/yumfu continue       # 继续游戏
/yumfu switch-lang    # 切换语言（保留进度）
```

---

## 📊 实现优先级

### Phase 1（立即实现）
1. ✅ 双语欢迎界面
2. ✅ 语言选择机制
3. ✅ 两个世界观：笑傲江湖（中文）+ Harry Potter（英文）

### Phase 2（近期）
4. ✅ 添加更多武侠世界（倚天、射雕）
5. ✅ 添加更多奇幻世界（LOTR、GoT）

### Phase 3（长期）
6. ✅ 世界观配置文件系统
7. ✅ 社区贡献新世界观（模板化）
8. ✅ 跨世界观角色导入（高级功能）

---

## 🔧 技术实现要点

### 动态加载世界观
```python
def load_universe(universe_id: str, language: str):
    config = json.load(f"worlds/{universe_id}.json")
    i18n = json.load(f"i18n/{language}.json")
    return WorldState(config, i18n)
```

### 存档兼容性
- `version: 2` 支持多世界观
- 旧存档（`version: 1`）默认为笑傲江湖
- 迁移脚本：`scripts/migrate_v1_to_v2.py`

### 配图生成
根据 `world.art_style` 动态生成提示词前缀：
```python
art_prefix = world_config["art_style"]
prompt = f"{art_prefix}, {scene_description}"
```

---

**这个设计让YumFu成为一个真正的多世界观MUD平台！** 🌍⚔️🪄
