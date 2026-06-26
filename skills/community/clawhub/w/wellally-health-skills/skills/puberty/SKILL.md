---
name: puberty
description: Track puberty development, Tanner staging, menarche timing, and assess for precocious or delayed puberty
argument-hint: <操作类型+部位+信息，如：breast B3，menarche true 11.5，testicular 8ml>
allowed-tools: Read, Write
schema: puberty/schema.json
---

# Puberty Development Assessment Skill

Assess puberty development (Tanner staging), identify precocious or delayed puberty.

## 核心流程

```
用户输入 → 解析操作类型 → 执行对应操作 → 生成/更新数据 → 保存 → 输出结果
```

## 支持的操作类型

### 女孩操作
| 操作 | 说明 | 示例 |
|------|------|------|
| breast | 记录乳房发育 | /puberty breast B3 |
| pubic | 记录阴毛发育 | /puberty pubic P2 |
| menarche | 记录初潮 | /puberty menarche true 11.5 |

### 男孩操作
| 操作 | 说明 | 示例 |
|------|------|------|
| testicular | 记录睾丸体积 | /puberty testicular 8ml |
| penis | 记录阴茎发育 | /puberty penis 6.5cm |
| voice | 记录变声 | /puberty voice true |

### 通用操作
| 操作 | 说明 | 示例 |
|------|------|------|
| bone-age | 记录骨龄 | /puberty bone-age 10.8 |
| status | 查看状态 | /puberty status |
| assessment | 综合评估 | /puberty assessment |
| check | 性早熟检查 | /puberty check |

## 步骤 1: 解析用户输入

### 操作类型识别

| Input Keywords | Operation Type |
|---------------|----------------|
| breast | breast |
| pubic, pubic hair | pubic |
| menarche | menarche |
| testicular | testicular |
| penis | penis |
| voice | voice |
| bone-age | bone-age |

### 乳房分期识别 (Tanner B分期)

| Input | Stage | Description |
|------|-------|-------------|
| B1, stage 1, pre-pubertal | B1 | Pre-pubertal |
| B2, stage 2, budding | B2 | Breast bud |
| B3, stage 3 | B3 | Breast and areola enlarge |
| B4, stage 4 | B4 | Areola protrudes |
| B5, stage 5, mature | B5 | Mature breast |

### 阴毛分期识别 (Tanner P分期)

| Input | Stage | Description |
|------|-------|-------------|
| P1, stage 1, none | P1 | No pubic hair |
| P2, stage 2, sparse | P2 | Sparse, long, light pigmented |
| P3, stage 3, coarse | P3 | Coarser, curly |
| P4, stage 4 | P4 | Adult type but small area |
| P5, stage 5, adult | P5 | Adult type |

### 睾丸体积识别

| 输入 | 分期 | 描述 |
|------|------|------|
| 4-6ml, 4ml, 6ml | G2 | 青春期开始 |
| 6-10ml | G3 | G3期 |
| 10-15ml | G4前 | 过渡期 |
| 15-20ml | G4 | G4期 |
| >=20ml | G5 | 成熟 |

### 阴茎长度识别

| 年龄 | 正常范围 | 说明 |
|------|---------|------|
| 青春期前 | <3cm | 未开始发育 |
| G2期 | 3-4cm | 开始增长 |
| G3期 | 4-6cm | 持续增长 |
| G4期 | 6-8cm | 接近成人 |
| G5期 | >=8cm | 成人大小 |

### 初潮识别

| Input | Extract Result |
|------|---------------|
| true, occurred, yes | occurred: true |
| false, not yet, no | occurred: false |
| 11.5, 11.5 years, 11.5y | age: 11.5 |

### 变声识别

| Input | Extract Result |
|------|---------------|
| true, changed, yes | voice_break: true |
| false, not yet, no | voice_break: false |

### 骨龄识别

| 输入 | 提取结果 |
|------|---------|
| 10.8, 10.8岁 | bone_age: 10.8 |
| 负0.5, -0.5 | difference: -0.5 |

## 步骤 2: 检查信息完整性

### breast Operation Required:
- stage: B stage (B1-B5)

### pubic Operation Required:
- stage: P stage (P1-P5)

### menarche Operation Required:
- occurred: Whether occurred (true/false)
- age: Age at menarche (if occurred)

### testicular Operation Required:
- volume: Testicular volume (ml)

### penis Operation Required:
- length: Penis length (cm)

### bone-age Operation Required:
- bone_age: Bone age value

## 步骤 3: 交互式询问（如需要）

### Scenario A: Missing Stage
```
Please provide breast development stage:
• B1 - Pre-pubertal
• B2 - Breast bud
• B3 - Breast and areola enlarge
• B4 - Areola protrudes
• B5 - Mature breast
```

### Scenario B: Missing Menarche Age
```
Please provide age at menarche:
(e.g.: 11.5 years, 12 years)
```

### Scenario C: Missing Testicular Volume
```
Please provide testicular volume:
(unit: ml, e.g.: 8ml)

## 步骤 4: 生成 JSON

### 青春期数据结构

```json
{
  "puberty_tracking": {
    "female_development": {
      "breast_stage": "B3",
      "breast_stage_age": null,
      "pubic_hair_stage": "P2",
      "pubic_hair_stage_age": null,
      "menarche": {
        "occurred": false,
        "age_at_menarche": null
      }
    },
    "male_development": {
      "testicular_volume": {
        "left": 8,
        "right": 8
      },
      "genital_stage": "G2",
      "pubic_hair_stage": "P2",
      "penis_length": null,
      "voice_break": false,
      "voice_break_age": null
    },
    "bone_age": {
      "chronological_age": 10.5,
      "bone_age": 10.8,
      "difference": "+0.3_years"
    },
    "assessment": "normal_progression",
    "notes": ""
  }
}
```

完整 Schema 定义参见 [schema.json](schema.json)。

## Step 5: Save Data

1. Read `data/puberty-tracker.json`
2. Update corresponding data
3. Write back to file
4. If detailed records exist, save to `data/puberty-records/YYYY-MM/YYYY-MM-DD_development-record.json`

## 执行指令

```
1. 解析用户输入，确定操作类型和性别
2. 根据操作类型执行相应逻辑
3. 验证输入数据和状态
4. 生成符合 schema.json 的 JSON
5. 保存到 data/puberty-tracker.json
6. 向用户输出操作结果和摘要
```

## 示例交互

### 示例 1: 记录乳房发育（女孩）
```
用户: /puberty breast B3

系统:
乳房发育已记录

乳房发育分期：B3期
描述：乳房和乳晕增大

评估：
• 分期正常
• 符合青春期发育进程

建议：
继续定期监测发育进展。
```

### 示例 2: 记录初潮（女孩）
```
用户: /puberty menarche true 11.5

系统:
初潮已记录

初潮年龄：11.5岁

评估：
• 初潮年龄正常（平均年龄：12-13岁）
• 骨龄评估建议进行
• 月经周期建立需要时间

建议：
• 记录月经周期
• 注意卫生保健
• 如有异常及时就医
```

### 示例 3: 记录睾丸发育（男孩）
```
用户: /puberty testicular 8ml

系统:
睾丸发育已记录

睾丸体积：8ml
分期：G2期（青春期开始）

评估：
• 睾丸体积符合青春期早期
• 发育正常

建议：
继续定期监测发育进展。
```

### 示例 4: 骨龄评估
```
用户: /puberty bone-age 10.8

系统:
骨龄已记录

实际年龄：10.5岁
骨龄：10.8岁
差异：+0.3岁

评估：
骨龄与实际年龄基本一致，属正常范围。

差异解读：
• < -1岁：生长延迟
• -1 至 +1岁：正常范围
• > +1岁：性早熟/加速生长
```

### 示例 5: 综合评估
```
用户: /puberty assessment

系统:
青春期发育综合评估

女孩发育评估：
• 乳房发育：B3期（10岁开始）
• 阴毛发育：P2期
• 初潮：未发生
• 骨龄：10.8岁（实际10.5岁）

发育进程：正常

性早熟检查：
• 乳房发育年龄：10岁（>8岁，正常）
• 初潮：未发生
• 结论：无性早熟迹象

建议：
• 继续定期监测
• 预计1-2年内初潮
• 注意营养和运动
```

更多示例参见 [examples.md](examples.md)。
