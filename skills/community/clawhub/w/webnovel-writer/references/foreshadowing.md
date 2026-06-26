# 伏笔管理机制

> 长篇小说伏笔追踪系统。解决核心问题：第5章埋的伏笔，第50章回收时容易忘。

---

## 一、伏笔登记模板（JSON格式）

Agent 读写伏笔表时使用以下结构，存储为 `伏笔表.json`：

```json
{
  "novel": "小说名称",
  "lastUpdated": "2026-04-10",
  "foreshadowings": [
    {
      "id": "FS-001",
      "description": "伏笔内容简述",
      "plantedChapter": 5,
      "plantedVolume": 1,
      "plantedDetail": "埋设时的具体描写/原文关键词",
      "expectedRecallChapter": 50,
      "expectedRecallVolume": 3,
      "actualRecallChapter": null,
      "status": "planted",
      "priority": "high",
      "category": "mystery",
      "recallHints": ["回收时需要的前置铺垫"],
      "relatedCharacters": ["角色名"],
      "notes": "补充说明"
    }
  ]
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 唯一标识，格式 `FS-NNN` |
| `description` | string | 伏笔内容一句话描述 |
| `plantedChapter` | number | 埋设章节号 |
| `plantedVolume` | number | 埋设卷号 |
| `plantedDetail` | string | 埋设时的原文关键词或具体描写 |
| `expectedRecallChapter` | number/null | 预计回收章节（不确定填null） |
| `expectedRecallVolume` | number/null | 预计回收卷号 |
| `actualRecallChapter` | number/null | 实际回收章节（未回收为null） |
| `status` | enum | `planted`（已埋）/ `hinted`（已铺垫）/ `recalled`（已回收）/ `abandoned`（已废弃） |
| `priority` | enum | `high`（核心伏笔）/ `medium`（重要）/ `low`（点缀） |
| `category` | enum | `mystery`（悬疑）/ `character`（角色）/ `emotion`（情感）/ `setting`（设定）/ `plot`（情节） |
| `recallHints` | string[] | 回收前需要的前置铺垫列表 |
| `relatedCharacters` | string[] | 相关角色 |
| `notes` | string | 补充说明 |

---

## 二、埋设操作规范

### 埋伏笔时必须做的事

1. **立即登记**：在 `伏笔表.json` 中新增一条记录
2. **标记原文**：在章节笔记中标注 `[FS-NNN]` 伏笔标记
3. **设定预期**：填写 `expectedRecallChapter`（至少估算一个范围）
4. **评估优先级**：核心反转用 `high`，辅助线索用 `medium`，氛围点缀用 `low`

### 埋设原则

- **自然融入**：伏笔应像正常叙事的一部分，不能像"此处有伏笔"的标注
- **可验证**：回收时读者翻回去能找到对应描写
- **密度控制**：每章新埋伏笔不超过2条，同时活跃的未回收伏笔不超过5条
- **分级管理**：`high` 级伏笔必须在大纲中标注回收节点

---

## 三、回收前检查流程

### 写每章前的标准检查

```
步骤1：读取伏笔表，筛选 status=planted 或 status=hinted 的记录
步骤2：按 expectedRecallChapter 排序，找出"本章应回收"的伏笔
步骤3：检查 recallHints，确认前置铺垫是否已到位
步骤4：决定本章操作——回收 / 提前铺垫(hinted) / 延后（更新expectedRecallChapter）
步骤5：回收后更新 actualRecallChapter 和 status
```

### 回收前的铺垫检查

回收 `high` 级伏笔前，至少需要 **2次前置暗示**（`hinted` 状态更新）：

- 第1次暗示：回收前5-10章，轻触伏笔相关元素
- 第2次暗示：回收前1-3章，营造悬念氛围
- 正式回收：本章揭示

---

## 四、过期预警机制

### 预警规则

| 条件 | 预警级别 | 处理建议 |
|------|---------|---------|
| 埋设超过 **20章** 未回收 | ⚠️ 注意 | 检查是否需要在近期铺垫 |
| 埋设超过 **50章** 未回收 | 🔴 警告 | 必须在5章内铺垫或废弃 |
| 埋设超过 **100章** 未回收 | 🚨 紧急 | 立即决定回收或废弃，不可再拖 |
| `expectedRecallChapter` 已过但未回收 | 📅 逾期 | 更新预期章节或执行回收 |

### 预警检查方式

写作每章前，Agent 自动执行：

```bash
# 伪代码逻辑
for fs in foreshadowings:
  if fs.status == "planted":
    gap = current_chapter - fs.plantedChapter
    if gap > 100: emit("🚨紧急", fs)
    elif gap > 50: emit("🔴警告", fs)
    elif gap > 20: emit("⚠️注意", fs)
  if fs.expectedRecallChapter and fs.expectedRecallChapter < current_chapter:
    emit("📅逾期", fs)
```

---

## 五、回收质量标准

### 好的回收 vs 差的回收

| 标准 | ✅ 好的回收 | ❌ 差的回收 |
|------|-----------|-----------|
| 铺垫 | 有2+次前置暗示 | 突然跳出，无任何准备 |
| 逻辑 | 读者回看能找到线索 | 强行圆场，逻辑牵强 |
| 情感 | 读者"恍然大悟" | 读者"这也行？" |
| 节奏 | 在合适的情节高潮回收 | 随便找个地方塞进去 |
| 密度 | 同一章最多回收2条伏笔 | 一章回收5条，信息过载 |

### 回收时的操作

1. 更新 `status` → `recalled`
2. 填写 `actualRecallChapter`
3. 在章节笔记中标注 `[FS-NNN 已回收]`
4. 检查是否有依赖此伏笔的后续伏笔需要激活

---

## 六、具体示例

### 示例A：《我的死亡日期消失了》（悬疑类）

悬疑类小说伏笔密集，多为 **谜团型** 伏笔（埋设→暗示→大反转回收）。

```json
{
  "novel": "我的死亡日期消失了",
  "foreshadowings": [
    {
      "id": "FS-001",
      "description": "公司里有人余额归零后还上了三个月的班——系统存在暗示",
      "plantedChapter": 1,
      "plantedVolume": 1,
      "plantedDetail": "第1章发现'死人'还在上班",
      "expectedRecallChapter": 56,
      "expectedRecallVolume": 7,
      "actualRecallChapter": null,
      "status": "planted",
      "priority": "high",
      "category": "mystery",
      "recallHints": ["赵恒暴露异常", "寿命余额交易机制"],
      "relatedCharacters": ["陆远", "赵恒"],
      "notes": "全书开篇核心悬念，第7卷赵恒摊牌时回收"
    },
    {
      "id": "FS-002",
      "description": "老钱暗中知道系统存在，从第3卷开始守护陆远",
      "plantedChapter": 10,
      "plantedVolume": 3,
      "plantedDetail": "老钱看似随意的提醒，实际是在保护",
      "expectedRecallChapter": 100,
      "expectedRecallVolume": 13,
      "actualRecallChapter": null,
      "status": "hinted",
      "priority": "high",
      "category": "character",
      "recallHints": ["老钱多次反常行为", "第13卷老钱之死前的坦白"],
      "relatedCharacters": ["老钱", "陆远"],
      "notes": "第13卷老钱牺牲时揭示——他一直知道。催泪型回收"
    },
    {
      "id": "FS-003",
      "description": "陆远父亲是系统创建者——全书最大反转",
      "plantedChapter": 5,
      "plantedVolume": 1,
      "plantedDetail": "父亲已故15年，留下的遗物/线索",
      "expectedRecallChapter": 128,
      "expectedRecallVolume": 16,
      "actualRecallChapter": null,
      "status": "planted",
      "priority": "high",
      "category": "mystery",
      "recallHints": ["父亲遗物中的异常", "系统运行600年的线索", "道印相关设定"],
      "relatedCharacters": ["陆远", "陆远父亲"],
      "notes": "第16卷核心反转，需在前10卷埋设3-5处暗示"
    },
    {
      "id": "FS-004",
      "description": "沈清第12卷开始看到余额——她有特殊体质",
      "plantedChapter": 33,
      "plantedVolume": 5,
      "plantedDetail": "沈清对陆远异常行为的好奇/直觉",
      "expectedRecallChapter": 96,
      "expectedRecallVolume": 12,
      "actualRecallChapter": null,
      "status": "planted",
      "priority": "high",
      "category": "character",
      "recallHints": ["沈清多次展现出异常直觉", "与陆远的亲密接触"],
      "relatedCharacters": ["沈清", "陆远"],
      "notes": "催泪+惊喜型回收，前5卷沈清需要'好像感觉到了什么'的暗示"
    },
    {
      "id": "FS-005",
      "description": "方哲500年前为救女儿成为执行器",
      "plantedChapter": 30,
      "plantedVolume": 4,
      "plantedDetail": "方哲'永远在笑'的异常",
      "expectedRecallChapter": 88,
      "expectedRecallVolume": 11,
      "actualRecallChapter": null,
      "status": "planted",
      "priority": "medium",
      "category": "character",
      "recallHints": ["方哲笑容下的疲惫瞬间", "与女儿相关的话题回避"],
      "relatedCharacters": ["方哲"],
      "notes": "第11卷揭示背景，让反派有人性维度"
    }
  ]
}
```

### 示例B：《观众都是我的前世》（催泪类）

催泪类小说伏笔多为 **情感型** 伏笔（前期微妙暗示→中期铺垫→毕业时集中爆发）。

```json
{
  "novel": "观众都是我的前世",
  "foreshadowings": [
    {
      "id": "FS-001",
      "description": "999号不是前世，是来世的林昭——全书最大悬念",
      "plantedChapter": 1,
      "plantedVolume": 1,
      "plantedDetail": "999号鼓掌一次，扶手微光如心跳",
      "expectedRecallChapter": 242,
      "expectedRecallVolume": 8,
      "actualRecallChapter": null,
      "status": "planted",
      "priority": "high",
      "category": "mystery",
      "recallHints": ["Ch6扶手微光", "Ch14倒计时", "Ch17'快了'", "Ch19转头朝周衍", "Ch22光团异动"],
      "relatedCharacters": ["999号", "林昭"],
      "notes": "超长线伏笔（242章），需每20章左右给一次微弱信号"
    },
    {
      "id": "FS-002",
      "description": "苏晚也能'听到声音'，疑似持有者",
      "plantedChapter": 20,
      "plantedVolume": 1,
      "plantedDetail": "苏晚重逢时对林昭异常的直觉反应",
      "expectedRecallChapter": 182,
      "expectedRecallVolume": 7,
      "actualRecallChapter": null,
      "status": "planted",
      "priority": "high",
      "category": "character",
      "recallHints": ["苏晚多次展现不合理的直觉", "与林昭的同步反应"],
      "relatedCharacters": ["苏晚", "林昭"],
      "notes": "Ch182揭示，Ch457走进影院——唯一进入影院的现世人"
    },
    {
      "id": "FS-003",
      "description": "001号赵承乾与666号李归墟的'空殿共鸣'——亡国帝王的孤独",
      "plantedChapter": 9,
      "plantedVolume": 1,
      "plantedDetail": "001号银幕上看到666号记忆，末年相似",
      "expectedRecallChapter": 189,
      "expectedRecallVolume": 7,
      "actualRecallChapter": null,
      "status": "hinted",
      "priority": "medium",
      "category": "emotion",
      "recallHints": ["001号对666号'丧'的理解", "666号毕业时001号的反应"],
      "relatedCharacters": ["赵承乾", "李归墟"],
      "notes": "情感型伏笔——两个坐过龙椅的人的共鸣，666号毕业时爆发"
    },
    {
      "id": "FS-004",
      "description": "冷月的感知信号体系——右手悬空/握刀/松开",
      "plantedChapter": 19,
      "plantedVolume": 1,
      "plantedDetail": "冷月右手摸腰间=有意外、握刀=危险、松开=安全",
      "expectedRecallChapter": 108,
      "expectedRecallVolume": 4,
      "actualRecallChapter": null,
      "status": "planted",
      "priority": "medium",
      "category": "setting",
      "recallHints": ["多次使用感知信号", "关键时刻信号与剧情呼应"],
      "relatedCharacters": ["冷月"],
      "notes": "第4卷冷月毕业时，最后一次感知——信号本身成为催泪点"
    },
    {
      "id": "FS-005",
      "description": "沈岩提到的887号——'别的持有者的记忆'作为锦囊",
      "plantedChapter": 23,
      "plantedVolume": 1,
      "plantedDetail": "沈岩说退出后887号会发别的持有者的记忆",
      "expectedRecallChapter": 180,
      "expectedRecallVolume": 6,
      "actualRecallChapter": null,
      "status": "planted",
      "priority": "medium",
      "category": "setting",
      "recallHints": ["锦囊内容的异常", "887号与999号的对应关系"],
      "relatedCharacters": ["沈岩", "999号"],
      "notes": "与999号身份伏笔联动——887号=沈岩的999号"
    },
    {
      "id": "FS-006",
      "description": "周衍名片背面'轮回计划·外联组'——全书第一次出现轮回计划",
      "plantedChapter": 26,
      "plantedVolume": 1,
      "plantedDetail": "名片背面右下角极小字",
      "expectedRecallChapter": 155,
      "expectedRecallVolume": 6,
      "actualRecallChapter": null,
      "status": "planted",
      "priority": "high",
      "category": "mystery",
      "recallHints": ["周衍的身份疑点", "轮回计划的逐步揭示"],
      "relatedCharacters": ["周衍"],
      "notes": "Ch155周衍正面登场时部分回收，但'轮回计划'全貌更晚揭示"
    }
  ]
}
```

### 两类小说的伏笔差异总结

| 维度 | 悬疑类（《死亡日期》） | 催泪类（《观众》） |
|------|---------------------|-------------------|
| 伏笔密度 | 高，几乎每章有线索 | 中，集中在情感铺垫 |
| 回收周期 | 中等（10-30章） | 长线（100-200章） |
| 回收方式 | 逻辑反转，"原来如此" | 情感爆发，"原来他一直在…" |
| 铺垫频率 | 需要多次逻辑暗示 | 需要多次情感微场景 |
| 过期风险 | 低（回收节奏快） | 高（长线容易忘） |
| 关键提醒 | 逻辑一致性是生命线 | 情感连贯性是生命线 |

---

## 七、Agent 操作指令

### 初始化伏笔表

```bash
# 在小说工作目录创建伏笔表
cat > 伏笔表.json << 'EOF'
{"novel":"小说名","lastUpdated":"日期","foreshadowings":[]}
EOF
```

### 写每章前检查

```bash
# 读取伏笔表，关注 planted 和 hinted 状态的记录
# 按当前章节号检查是否有应回收的伏笔
# 检查预警规则（20/50/100章阈值）
python3 -c "
import json
data = json.load(open('伏笔表.json'))
current = 当前章节号
for fs in data['foreshadowings']:
    if fs['status'] in ('planted','hinted'):
        gap = current - fs['plantedChapter']
        if gap > 50: print(f'🔴 {fs[\"id\"]}: {gap}章未回收 - {fs[\"description\"]}')
        elif gap > 20: print(f'⚠️ {fs[\"id\"]}: {gap}章未回收 - {fs[\"description\"]}')
        if fs.get('expectedRecallChapter') and fs['expectedRecallChapter'] <= current:
            print(f'📅 {fs[\"id\"]}: 预期{fs[\"expectedRecallChapter\"]}章回收，已到 - {fs[\"description\"]}')
"
```

### 埋设伏笔

```bash
# 追加新伏笔到表中
python3 -c "
import json
data = json.load(open('伏笔表.json'))
data['foreshadowings'].append({
    'id': 'FS-NNN',
    'description': '描述',
    'plantedChapter': 当前章节,
    'plantedVolume': 当前卷,
    'plantedDetail': '原文关键词',
    'expectedRecallChapter': 预期章节,
    'expectedRecallVolume': 预期卷,
    'actualRecallChapter': None,
    'status': 'planted',
    'priority': 'high/medium/low',
    'category': 'mystery/character/emotion/setting/plot',
    'recallHints': [],
    'relatedCharacters': [],
    'notes': ''
})
data['lastUpdated'] = '日期'
json.dump(data, open('伏笔表.json','w'), ensure_ascii=False, indent=2)
"
```

### 回收伏笔

```bash
# 更新伏笔状态为已回收
python3 -c "
import json
data = json.load(open('伏笔表.json'))
for fs in data['foreshadowings']:
    if fs['id'] == 'FS-NNN':
        fs['status'] = 'recalled'
        fs['actualRecallChapter'] = 当前章节
        break
data['lastUpdated'] = '日期'
json.dump(data, open('伏笔表.json','w'), ensure_ascii=False, indent=2)
"
```
