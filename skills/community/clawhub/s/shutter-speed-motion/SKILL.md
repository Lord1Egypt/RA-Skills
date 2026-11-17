---
name: shutter-speed-motion
description: |
  用户想控制运动表现（凝固运动/表现动感）、问"快门速度怎么选"、或拍摄运动物体
  时调用。不适用于景深控制（应调用 depth-of-field-control）或曝光量计算
  （应调用 exposure-dual-control）。
  Invoke when the user wants to control motion rendering (freeze motion / convey
  movement), asks "what shutter speed to use," or is photographing moving subjects.
  Not for depth-of-field control (use depth-of-field-control) or exposure
  calculation (use exposure-dual-control).
  关键 trigger / Key triggers: "快门速度"、"运动模糊"、"凝固运动"、"追随拍摄"、
  "shutter speed"、"motion blur"、"panning"、"freeze motion"、
  "sports photography shutter"、"how to freeze action"、"convey motion in photo"。
source_book: 《纽约摄影学院摄影教程》 美国纽约摄影学院
source_chapter: 第三章 p062-p071
tags: [shutter-speed, motion, panning, sports-photography]
related_skills: []
---

# 快门速度与运动表现选择

## R — 原文 (Reading)

> "正确的快门速度是能够获得所需效果的速度，快门速度将有助于表现作品的主题...1/1000秒的速度确实将影像'凝固'住了，但这不一定是我们需要的效果。1/125秒拍摄的稍微有些模糊的影像，尽管损失了一些细节的清晰度，但似乎更好地表现了运动的感觉。"
>
> — 美国纽约摄影学院，第三章

---

## I — 方法论骨架 (Interpretation)

快门速度不仅控制曝光时间，更是表现运动的核心创造性工具。选择快门速度需考虑四因素：运动物体速度（越快需要越快快门）、运动方向（横穿视野比朝向/远离需要更快快门，因为横向运动在画面中位移更大）、与被摄体距离（越近模糊越高）、镜头焦距（越长影像穿过画面越快）。关键洞察是"正确的快门速度是能获得所需效果的速度"——1/1000秒凝固运动但可能失去动感，1/15秒完全模糊但可能最好地表现运动概念。追随拍摄技术可用较慢快门（如1/60秒）凝固运动主体同时让背景动态模糊，创造速度感。

---

## A1 — 书中的应用 (Past Application)

### 案例 1: 职业摄影师运用快门速度捕捉水
- **问题**: 如何用不同快门速度表现水的不同质感
- **方法论的使用**: 伊凡·马萨尔用高速快门停住水面呈现绝对安宁；亚历山大·劳里用中等快门"停"住浪涌但保留流动感；迈克尔·曼海姆用极慢快门让海水变成"安琪儿头发"。
- **结论**: 同一场景用不同快门速度创造完全不同的艺术效果
- **结果**: 证明了快门速度的创造性价值

### 案例 2: 追随拍摄跑步者
- **问题**: 如何用较慢快门表现运动速度感
- **方法论的使用**: 摄影师用1/60秒追随拍摄，让相机追随运动物体转动，拍摄后仍保持追随动作。结果运动主体清晰，背景动态模糊。
- **结论**: 追随拍摄是表现速度感的经典技术
- **结果**: 背景模糊线条创造强烈的速度感

---

## A2 — 触发场景 (Future Trigger)

### 用户会在什么情境下需要这个 skill?
1. 拍摄运动物体（体育/儿童/宠物/车辆）不知用什么快门速度
2. 想表现运动的速度感/动感
3. 问"为什么我拍的运动照片总是模糊"
4. 想学习追随拍摄技术

### 语言信号
- "快门速度怎么选？"
- "怎么拍出运动模糊？"
- "怎么凝固运动？"
- "追随拍摄怎么拍"
- "shutter speed for sports"
- "motion blur"、"panning technique"
- "freeze action"

### 与相邻 skill 的区分
- 与 `exposure-dual-control` 的区别：本 skill 专门深入快门与运动表现的四因素决策，exposure-dual-control 是曝光的全局框架。
- 与 `depth-of-field-control` 的区别：本 skill 关注"运动表现"，depth-of-field-control 关注"清晰范围"。

---

## E — 可执行步骤 (Execution)

当 skill 被激活后，agent 应按以下步骤执行：

1. **评估运动四因素**
   - 完成标准: 逐一评估运动速度、方向、距离、焦距
   - 快速参考: 步行1/125秒、跑步1/250秒、汽车1/500秒、飞鸟1/1000秒以上
   - 横向运动需比纵向运动快1-2挡

2. **确定创意目标**
   - 完成标准: 明确用户要凝固运动还是表现动感
   - 凝固→高速快门（1/500秒以上）
   - 动感→中速快门（1/60-1/250秒）或慢速+追随拍摄

3. **选择具体快门速度**
   - 完成标准: 给出具体快门速度建议
   - 手持安全底线: 分母≥焦距毫米数（推荐×2）
   - 判停条件: 若光线不足无法用高速快门→建议提高ISO或用三脚架

4. **追随拍摄技术（如需要）**
   - 完成标准: 若用户想表现速度感，介绍追随拍摄方法
   - 步骤: 用1/30-1/125秒→提前追踪主体→平稳转动身体→按下快门后继续追随

---

## B — 边界 (Boundary)

### 不要在以下情况使用此 skill
- 景深控制问题 → 应调用 depth-of-field-control
- 曝光量计算 → 应调用 exposure-dual-control
- 静态场景拍摄 → 快门速度选择不是核心问题

### 作者在书中警告的失败模式
- 照相机震动导致模糊（与运动模糊不同）：若某些景物清晰=聚焦问题；若哪里都不清晰=相机震动
- 长焦镜头手持拍摄需要更高快门速度

### 作者的盲点 / 时代局限
- 未涉及数码时代的高速连拍、AI主体追踪对焦等技术
- 现代相机防抖技术（IBIS）可降低手持安全快门要求约3-5挡

---

## 相关 skills (阶段 3 填充)

- depends-on: exposure-dual-control（快门选择需考虑曝光量平衡）
- contrasts-with: depth-of-field-control（运动表现 vs 清晰范围）
- composes-with: photo-three-principles（快门速度服务于主题表达）

---

## 审计信息

- **验证通过**: V1 ✓ / V2 ✓ / V3 ✓
- **测试通过率**: 待测试
- **蒸馏时间**: 2026-08-03
