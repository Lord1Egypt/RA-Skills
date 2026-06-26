# Z 轴纵深：竖屏分镜的核心语言

## 竖屏不是裁剪的横屏

把一张 16:9 横屏截图上下裁掉两边，不会得到好的竖屏画面——你会得到一个失去横向关系、同时也没有纵深关系的"残帧"。

竖屏分镜的本质是：**在一条纵深走廊里调度人物。**

横屏的叙事空间是矩形的平面（X 轴 × Y 轴），竖屏的叙事空间是纵深的走廊（Z 轴 × Y 轴）。Z 轴是竖屏唯一的深度维度，必须成为分镜设计的核心。

---

## Three-Layer Depth System / 三层纵深系统

竖屏画面在任何时候都应该包含三个纵深层：

```
前景 Foreground (Z=0)    ──→  最近层，通常是主要叙事主体或框架道具
中景 Midground (Z=1)      ──→  中间层，主体或第二主体
背景 Background (Z=2)    ──→  最远层，环境、群演、天光、墙面
```

### 各层的内容原则

| 层级 | 内容类型 | 竖屏注意事项 |
|------|----------|--------------|
| **前景 (Z=0)** | 主体轮廓、框架道具（门框、树枝）、次要人物 | 不能太空；常用门框、窗框做前景框架 |
| **中景 (Z=1)** | 主要叙事主体 | 清晰对焦区域 |
| **背景 (Z=2)** | 空间交代、光源、环境人物 | 保持细节但不要抢焦点 |

### 典型好的三层示例

**场景：走廊尽头女人回眸**

```
Prompt: "a woman in a dark red qipao turning to look back in a dimly lit corridor, 
vertical 9:16 format, three-layer depth: faded wooden door frame in foreground, 
woman in medium shot at midground, vanishing corridor with single light source at far end as background"
```

---

## 前后叠放法则：替代正反打

横屏两人对话用正反打（OTS 或过肩双镜），竖屏用 Z 轴叠放：

### 叠放的三种模式

**模式 A：男前女后（男性主导）**

```
前景 Z=0：男性背影，肩部占据左侧 35%
中景 Z=1：女性正面，面对镜头
→ 观众视线穿过男性肩部，到达女性面部
→ 权力关系：男性在前 = 主动/压迫
```

**模式 B：女前男后（女性主导）**

```
前景 Z=0：女性侧脸/背影
中景 Z=1：男性中景
→ 反向设置，女性主导
```

**模式 C：同 Z 轴平排（平等关系）**

```
中景 Z=1：两人并肩或略错位平排
→ 用于朋友、搭档、平等对话
```

### 叠放的 Prompt 写法

❌ 错误：
```
two people talking, facing each other, close-up shots
```
（没有纵深关系，只是两个人并排）

✅ 正确：
```
vertical 9:16 portrait, a man sitting in foreground with his back partially visible 
on the left side, a woman facing him in sharp focus at midground, shallow depth 
of field, foreground slightly blurred, strong sense of Z-axis depth in a narrow room
```

---

## 高低落差法则：楼梯即权力

竖屏里确立权力关系最有效的工具不是横向位置，而是**垂直高度差**。

### 落差三角

```
         高位 (High Z)
           /\
          /  \
    楼梯/窗台   对方
         \  /
          \/
         仰拍视角
```

楼梯、二楼走廊、窗台、台阶——这些是竖屏短剧里最核心的**权力锚点**。

### 落差类型与语义

| 落差类型 | 视觉表现 | 叙事语义 |
|----------|----------|----------|
| **物理高差** | 一人在楼梯上方，一人在下方 | 明确的权力层级 |
| **镜头高差** | 低角度仰视 = 高位感 | 威严、压迫、崇拜 |
| **体型高差** | 前景主体更大（接近 Z=0） | 主动、控制 |
| **道具高差** | 坐在椅子上 vs. 站在旁边 | 微妙的权力暗示 |

### 含楼梯的典型 Prompt

```
vertical 9:16 shot, a man standing on top of a stone staircase looking down, 
a woman at the bottom of the stairs looking up, low angle on the woman, 
rain falling, moody atmosphere, cinematic lighting from above
```

---

## 透视锚定：纵深移动的参照系

当核心人物在 Z 轴上移动（走进走廊深处、远离镜头）时，画面中必须包含**至少一个锚点**，否则纵深关系无法被感知。

### 锚点类型

| 锚点类型 | 示例 |
|----------|------|
| **人物锚点** | 前景有另一个人作为比例参照 |
| **物体锚点** | 门框、柱子、椅子作为空间比例尺 |
| **光线锚点** | 远处窗户的光作为纵深距离的视觉暗示 |

### 有锚点 vs. 无锚点

❌ 无锚点（失去纵深感）：
```
a woman walking down a long empty corridor towards a light at the end
```
→ 走廊看起来像隧道，人物大小关系无法判断

✅ 有锚点：
```
a woman walking down a long corridor towards a bright window at the end,
a child sitting on a wooden bench in the foreground (anchor point),
the woman appears smaller as she moves deeper into the corridor
```
→ 孩子的存在建立了空间比例，纵深感成立

---

## 常见竖屏纵深构图

### 1. 走廊纵深（Corridor Depth）

最经典的竖屏纵深：前景门框/框架 + 中景主体 + 背景光源

```
Prompt: "vertical 9:16, a traditional Chinese corridor with red lanterns, 
a young woman in white standing at the far end under a lantern, 
wooden door frame in foreground creating depth layers, 
morning light streaming from behind, cinematic atmosphere"
```

### 2. 窗框纵深（Window Frame Depth）

前景窗框分割画面，引导视线到中景主体

```
Prompt: "vertical portrait, a wooden window frame in the foreground (slightly 
blurred), a man reading a letter in the midground by a desk, 
snow falling outside the window in the background, 9:16 format"
```

### 3. 楼梯纵深（Staircase Depth）

Z 轴高度差 + 纵深感结合，权力与空间同时建立

### 4. 镜子纵深（Mirror Depth）

前景镜子反射中景/背景，增加虚拟纵深层

### 5. 门缝纵深（Door Gap Depth）

从门缝拍摄，天然的两层纵深 + 外部背景

---

## 竖屏纵深 Prompt 模板

```
vertical 9:16 [shot type], [foreground element with Z=0 description], 
[main subject at midground Z=1], [background environment Z=2], 
[depth of field instruction], [lighting direction and quality], 
[atmosphere/mood]
```

### 模板示例

```
vertical 9:16 medium shot, a wooden door frame blurred in the foreground (Z=0), 
a woman in a dark dress standing in the center at midground (Z=1), 
a large window with moonlight visible behind her (Z=2), 
shallow depth of field, soft side lighting from the left, 
mysterious and tense atmosphere, cinematic color grading
```
