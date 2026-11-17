> **Language**: This document is in Chinese only. For English overview, see [README.md](../README.md).
>
> **语言说明**: 本文档仅提供中文版本。英文概述请查看 [README.md](../README.md)。

---
# GEO 空间锁定模板

> **问题**：角色瞬移、换位、镜头跳到错边——因为模型不记得上一镜谁站哪。
> **解药**：写一个地点的「楼层平面」几行：地标物、右边是什么、左边是什么、摄影机站哪。无角色、无动作——只有地点本身。每场戏写一次，原样粘进该场每一镜。

---

## 核心原则

### 1. 摄影机永远在一侧

180° 轴线规则：摄影机始终待在场景的一侧，绝不越线。否则左右关系翻转，观众迷失方向。

### 2. 侧面只从摄影机视角定义

- `frame-left`（画面左侧）/ `frame-right`（画面右侧）
- 模型不懂「英雄左边」——必须用画面坐标
- 位置从**地标物 + 米数**定：「在祭坛旁」「三米外」

### 3. GEO 只是地图

地点长相仍来自地点资产（其 descriptor + reference 与地图并列进提示词）。GEO 只锁定空间关系，不管材质、光影、氛围。

---

## 模板结构

```
GEO SPATIAL LAYOUT (locked across every shot — pure spatial map):
— [LANDMARK 1] = [描述 + 位置]
— [LANDMARK 2] = [描述 + 位置]
— [CHARACTER POSITION] = [相对于地标的位置]
— [180° AXIS] = [摄影机始终在哪一侧]
— [BACK-LIGHTING] = [光源方向，与摄影机位置的关系]
```

---

## 完整范例

### 范例 1：地下训练室

```
GEO SPATIAL LAYOUT (locked across every shot — pure spatial map):
— THE ROUND MAT = raised circular ritual stone disc at the center of the hall, 
  under one hard overhead light.
— DOOR = in the far wall at frame-LEFT, about eight metres from the mat.
— BENCH WITH TRAYS = at frame-RIGHT, two metres off the mat.
— SMASHED MANNEQUINS = scattered at CENTER-RIGHT, one still rocking on its base.
— 180° AXIS = camera ALWAYS stays on the door side of the room — it NEVER 
  crosses the line.
— BACK-LIGHTING = crimson horizon glow comes from BEHIND the platform, 
  rim-lighting silhouettes from camera's perspective.
```

### 范例 2：悬崖祭坛

```
GEO SPATIAL LAYOUT (locked across every shot — pure spatial map):
— PLATFORM = raised circular ritual stone disc at the edge of a cliff.
— ALTAR-MONOLITH = at the cliff edge, MID-RIGHT position relative to the platform.
— RITUAL CENTER = CENTER-LEFT, ~3 m from the altar.
— 180° AXIS = camera ALWAYS stays on the corpse-field side — it NEVER crosses 
  the line.
— BACK-LIGHTING = crimson horizon glow comes from BEHIND the platform, 
  rim-lighting silhouettes from camera's perspective.
```

### 范例 3：独立书店

```
GEO SPATIAL LAYOUT (locked across every shot — pure spatial map):
— CENTRAL READING TABLE = at frame-center, slightly left, with green banker's lamp.
— FRONT COUNTER = at frame-right foreground, with old brass register.
— TALL WOODEN SHELVES = line both side walls, receding into warm amber depth.
— NARROW WINDOW = at camera-left, warm amber light streaming in, casting long 
  diagonal shadows across the wooden floorboards.
— 180° AXIS = camera positioned in the far front-right corner, looking diagonally 
  across and down at approximately 35 degrees.
— PRIMARY LIGHT SOURCE = window at camera-left, low afternoon angle.
```

---

## 使用规则

### 1. 每场景写一次

GEO 写一次，原样粘进该场景每一镜。绝不每镜重写——否则空间关系漂移。

### 2. 切镜后重述谁站哪

模型不记得上一镜。每次切后**重报谁站哪、看向哪**：

```
FIRST FRAME AND SPATIAL BLOCKING
@HERO1 stands within 1 meter of the burned-out car, one hand resting on the 
scorched hood, body facing frame-RIGHT, gaze locked on @HERO2.
@HERO2 and @HERO3 stand together in the foreground, facing @HERO1.
Hero2 is camera-right of the pair.
Hero3 is camera-left of the pair.
Both bodies face Hero1.
Both gaze lines are locked on Hero1.
```

### 3. 给静态对白一个房间角落

不要给整间房——空间越小，模型乱放主角的余地越小。

```
✅ @HERO1 stands in the doorframe, back against the wall, hand on the handle.
❌ @HERO1 is in the room.
```

### 4. 弱写法 vs 强写法

**弱写法**（模型会随机解读）：
```
near the tree
by the taxi
around the location
somewhere in the battlefield
```

**强写法**（物理锚定）：
```
@HERO1V2 stands within 1 meter of the burned-out car, one hand planted on the 
scorched hood.
@HERO2 is camera-right of the pair, 2 meters from @HERO1, body facing frame-LEFT.
```

---

## 与 180° 轴线的关系

### 什么是 180° 轴线？

两个角色对话时，摄影机必须待在连接两角色的线的一侧。越过这条线，左右关系翻转，观众迷失方向。

### 如何在 GEO 中锁定？

```
180° AXIS = camera ALWAYS stays on the door side of the room — it NEVER 
crosses the line.
```

### 何时可以越轴？

- 角色移动带动摄影机（可见越轴桥梁）
- 插入特写（INSERT CUT）
- 明确设计的越轴（用于制造不安感）

**铁律**：越轴必须是可见的、有动机的。绝不随机越轴。

---

## 与 CINEDANCE 的关系

GEO 是 CINEDANCE 16-block 中 `LOCATION MAP` 和 `FIRST FRAME AND SPATIAL BLOCKING` 的核心输入。

```
LOCATION MAP
[粘贴 GEO SPATIAL LAYOUT]

FIRST FRAME AND SPATIAL BLOCKING
[基于 GEO 描述每个角色的位置、朝向、视线]
```

---

## 常见错误

| 错误 | 后果 | 修正 |
|---|---|---|
| 每镜重写 GEO | 空间关系漂移 | 写一次，原样粘贴 |
| 用「左边/右边」不用「画面左侧/画面右侧」 | 模型困惑 | 用 `frame-left` / `frame-right` |
| 给整间房 | 模型乱放主角 | 给一个角落 |
| 不写 180° 轴线 | 越轴导致方向混乱 | 明确写 `camera ALWAYS stays on X side` |
| 切镜后不重述谁站哪 | 角色瞬移 | 每次切后重报位置 |
| 用弱写法 | 模型随机解读 | 用物理锚定（米数 + 地标） |

---

## 检查清单

每镜提示词发出前检查：

- [ ] GEO SPATIAL LAYOUT 已逐字粘贴（与上一镜完全一致）
- [ ] 180° 轴线已锁定（`camera ALWAYS stays on X side`）
- [ ] 每个角色的位置用物理锚定（米数 + 地标）
- [ ] 每个角色的身体朝向已写明（`body facing frame-LEFT/RIGHT`）
- [ ] 每个角色的视线方向已写明（`gaze locked on @HERO2`）
- [ ] 切镜后已重述谁站哪、看向哪
- [ ] 没有用「左边/右边」——用的是「画面左侧/画面右侧」

---

**参考**：完整 16-block 架构详见 `references/cinedance-video-prompt.md`；地点资产详见 `references/lira-image-prompt.md`。
