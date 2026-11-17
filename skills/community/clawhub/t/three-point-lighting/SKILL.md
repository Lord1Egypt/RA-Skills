---
name: three-point-lighting
description: |
  用户想学习室内/棚拍布光方法、问"怎么布光"、或设置人造光拍摄时调用。
  不适用于自然光拍摄（应调用 natural-light-direction）或现场光摄影
  （应调用 available-light-photography）。
  Invoke when the user wants to learn indoor / studio lighting setup, asks
  "how to set up lights," or is configuring artificial light for a shoot.
  Not for natural light shooting (use natural-light-direction) or available
  light photography (use available-light-photography).
  关键 trigger / Key triggers: "布光"、"三点布光"、"主灯辅助灯"、"studio lighting"、
  "three point lighting"、"key light fill light"、"light ratio"、
  "portrait lighting setup"、"how to light a portrait"、"studio light setup"。
source_book: 《纽约摄影学院摄影教程》 美国纽约摄影学院
source_chapter: 第十一章 p231-p241
tags: [studio-lighting, three-point-lighting, light-ratio, portrait]
related_skills: []
---

# 三步式布光法与光比控制

## R — 原文 (Reading)

> "基本布光过程...主灯→辅助灯→背景灯"——人造光布光的标准流程。光比控制情绪：1:1平淡、4:1自然、9:1戏剧性。辅助灯功率必须低于主灯，否则产生抗衡阴影。
>
> — 美国纽约摄影学院，第十一章

---

## I — 方法论骨架 (Interpretation)

人造光布光遵循三步式标准流程。第一步设主灯（key light）：确定主要光影方向，通常放在被摄体侧前方45°、略高于被摄体的位置，这是照片的主要光源和阴影方向。第二步加辅助灯（fill light）：填充主灯产生的阴影，功率必须低于主灯（推荐从主灯1/3功率开始），否则会产生与主灯抗衡的第二个阴影。第三步加背景灯（back light）：照亮背景，分离主体与背景，增加空间感。光比（主灯与辅助灯的亮度比）控制照片的情感基调：1:1（等功率）平淡无层次；4:1（辅助灯为主灯1/4功率）自然柔和，适合人像；9:1（辅助灯为主灯1/9功率）戏剧性强，适合艺术人像。两盏以上同等功率灯会造成多个阴影引起混乱。

---

## A1 — 书中的应用 (Past Application)

### 案例 1: 基本布光过程
- **问题**: 如何系统性地布置摄影室灯光
- **方法论的使用**: 先设主灯确定光影方向→加辅助灯填充阴影（功率低于主灯）→加背景灯分离主体。逐步添加，每加一盏灯观察效果。
- **结论**: 三步式流程确保布光有序可控
- **结果**: 可复现的专业布光效果

### 案例 2: 光比控制情绪
- **问题**: 如何通过光比控制照片情感
- **方法论的使用**: 1:1光比→平淡适合产品目录；4:1光比→自然适合人像；9:1光比→戏剧性适合艺术创作。
- **结论**: 光比是布光中控制情绪的核心参数
- **结果**: 同一被摄体用不同光比呈现完全不同的情感

---

## A2 — 触发场景 (Future Trigger)

### 用户会在什么情境下需要这个 skill?
1. 设置室内/棚拍灯光
2. 问"怎么布光拍人像"
3. 问"主灯和辅助灯怎么配"
4. 想控制照片的明暗对比度/情感氛围

### 语言信号
- "怎么布光？"
- "三点布光怎么设"
- "主灯辅助灯比例"
- "studio lighting setup"
- "three point lighting"
- "key light fill light ratio"
- "portrait lighting"

### 与相邻 skill 的区分
- 与 `natural-light-direction` 的区别：本 skill 关注人造光布光，natural-light-direction 关注自然光方向。
- 与 `available-light-photography` 的区别：本 skill 主动添加和控制光源，available-light 不添加人工光。

---

## E — 可执行步骤 (Execution)

当 skill 被激活后，agent 应按以下步骤执行：

1. **设置主灯**
   - 完成标准: 主灯放在被摄体侧前方45°、略高于被摄体
   - 这是照片的主要光影方向，决定整体效果
   - 主灯功率设为基准（如100%）

2. **添加辅助灯**
   - 完成标准: 辅助灯放在主灯对面，功率低于主灯
   - 推荐起点: 主灯功率的1/3（光比约3:1）
   - 根据 desired 效果调整：自然→4:1，戏剧→9:1
   - 警告: 辅助灯功率不能≥主灯，否则产生抗衡阴影

3. **添加背景灯（可选）**
   - 完成标准: 背景灯照亮背景，分离主体与背景
   - 功率通常低于主灯
   - 可增加空间感和专业感

4. **调整光比**
   - 完成标准: 根据情感目标调整主灯/辅助灯功率比
   - 1:1→平淡（产品目录）
   - 4:1→自然（标准人像）
   - 9:1→戏剧性（艺术人像）
   - 用测光表分别测量主灯和辅助灯在被摄体处的读数，计算挡数差

---

## B — 边界 (Boundary)

### 不要在以下情况使用此 skill
- 户外自然光拍摄 → 应调用 natural-light-direction
- 不添加人工光的拍摄 → 应调用 available-light-photography
- 纯器材问题（灯的类型/功率）→ 本 skill 关注布光方法而非器材选择

### 作者在书中警告的失败模式
- 辅助灯功率≥主灯→产生抗衡阴影，画面混乱
- 两盏以上同等功率灯→多个阴影引起混乱
- 电路超载：确保灯泡功率不超过反光罩额定功率

### 作者的盲点 / 时代局限
- 基于传统丝灯/闪光灯系统，未涉及LED常亮灯、柔光箱等现代设备
- 未涉及数码时代的后期光线调整能力

---

## 相关 skills (阶段 3 填充)

- composes-with: natural-light-direction（自然光方向原则适用于人造光）
- contrasts-with: available-light-photography（主动布光 vs 不添加人工光）
- composes-with: light-meter-compensation（用测光表测量光比）

---

## 审计信息

- **验证通过**: V1 ✓ / V2 ✓ / V3 ✓
- **测试通过率**: 待测试
- **蒸馏时间**: 2026-08-03
