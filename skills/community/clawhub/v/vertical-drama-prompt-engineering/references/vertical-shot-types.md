# 竖屏镜头类型详解 / Vertical Shot Types

竖屏格式（9:16）的镜头设计不是横屏镜头的垂直压缩，而是针对纵深（Z 轴）重新设计的镜头语言。每种镜头类型在竖屏中都有其独特的构图逻辑和叙事用途。

---

## Vertical Close-Up (VCU) / 竖屏特写

### 构图特征

```
┌─────────┐
│  头顶   │
│  留白   │
├─────────┤
│  面部   │  ← 占据画面 60-80% 高度
│  上区   │
├─────────┤
│  下颌   │
│  边缘   │
└─────────┘
```

- 面部是绝对主体
- 眼睛位于画面上 1/3 线
- 背景通常虚化（shallow DoF）
- 竖屏特写比横屏特写更具侵入感，因为画面上下无逃逸空间

### 用途

- 情绪放大：震惊、愤怒、悲伤的微表情
- 台词重点：关键对白的反应镜头
- 内心独白：直接面向镜头（direct to camera）

### Prompt 要点

```
vertical close-up, 9:16 portrait, face fills 70% of frame, 
eyes on upper third line, shallow depth of field, 
background bokeh, moody cinematic lighting, 
intimate and intense emotional atmosphere
```

### 竖屏特写的变体

| 变体 | 描述 |
|------|------|
| **眼睛特写** | Extreme close-up on eyes, 瞳孔反光, 眼泪 |
| **嘴唇特写** | 轻声说话、咀嚼、抿唇的暗示 |
| **手部特写** | 握拳、松开、颤抖——情绪的外化 |

---

## Vertical Medium Shot (VMS) / 竖屏中景

### 构图特征

```
┌─────────┐
│  头顶   │
│  留白   │  ← 10-15% 画面高度
│  10-15% │
├─────────┤
│         │
│  膝盖   │  ← 主要叙事区域
│  以上   │
│         │
├─────────┤
│  脚部   │
│  留白   │  ← 5-10%
└─────────┘
```

- 膝盖以上取景
- 最常用的对话镜头
- 可以包含两人在 Z 轴上的位置关系

### 用途

- 日常对话
- 两人互动（可配合 Z 轴叠放）
- 部分环境交代

### Prompt 要点

```
vertical medium shot, 9:16, waist-up framing, 
two characters at midground, subtle depth between them, 
everyday interior setting, natural window light, 
cinematic color, grounded realistic atmosphere
```

---

## Vertical Over-the-Shoulder (VOTS) / 竖屏过肩

### 构图特征

竖屏过肩是竖屏分镜的**核心镜头**——它替代了横屏的正反打，用 Z 轴叠放处理两人对话。

```
┌─────────┐
│         │
│  远端   │
│  主体   │  ← 清晰对焦，完整可见
│         │
├─────────┤ ← ────────────── 肩部/头部轮廓线
│  前景   │
│  人物   │  ← 肩部 + 后脑勺，30-40% 画面宽度
│  后脑勺  │
└─────────┘
```

### 前景人物的位置规则

| 位置 | 效果 |
|------|------|
| 前景占画面 30-35% | 自然过肩，叙事感 |
| 前景占画面 40-50% | 压迫感，前景主导 |
| 前景超出画面边缘 | ❌ 错误，像乱入或剪影切掉 |

### 用途

- 两人对话（竖屏替代正反打）
- 制造亲密感（前/后纵深）
- 表现压制/权力（前大于后）

### Prompt 要点

```
vertical over-shoulder shot, 9:16 portrait format, 
a woman's shoulder and back of head visible in the foreground (blurred or 
semi-sharp), a man facing her in sharp focus at midground, 
shallow depth of field, foreground slightly out of focus, 
cinematic intimate conversation framing
```

### 另一种 Z 轴方向（前景看向背景）

```
vertical over-shoulder, 9:16, a man in sharp focus at midground 
looking into the distance, a partially visible woman's shoulder in the 
foreground (blurred), the man is the focal point, moody atmosphere, 
side lighting from the right
```

---

## Vertical Low-Angle (VLA) / 竖屏低角度

### 构图特征

```
        ┌─────────┐
  仰视方向 │  主体   │  ← 主体在画面上部
   ↑      │  头部   │
   │      │  上身   │
   │      ├─────────┤
   │      │  腿/脚  │  ← 脚部是画面下方
   └──────│  接地   │
          └─────────┘
```

- 镜头置于腰部高度或更低
- 主体在画面中偏上
- 背景通常是天空、天花板、灯光
- 竖屏低角度比横屏更有压迫感——画面没有横向空间可以"舒展"

### 用途

- 确立角色威严/权力
- 表现压迫、威胁
- 仰慕（当仰视对象在高位时）

### Prompt 要点

```
vertical low-angle shot, 9:16, camera at waist level looking up, 
a powerful man standing above, slightly top of frame composition, 
dramatic uplighting from below, dark and imposing atmosphere, 
cinematic portrait format, strong authoritative presence
```

---

## Vertical High-Angle (VHA) / 竖屏高角度

### 构图特征

```
  俯视方向
     ↓
    ┌─────────┐
    │  脚部   │  ← 脚部在画面上方
    ├─────────┤
    │  头部   │  ← 主体在画面下部
    │  上身   │
    └─────────┘
```

- 镜头置于头顶高度或更高
- 主体在画面中偏下
- 背景通常是地面、桌面、或俯视角度的环境

### 用途

- 表现脆弱、渺小、被动
- 场景 overview（建立镜头）
- 俯视的冷漠/怜悯

### Prompt 要点

```
vertical high-angle shot, 9:16, camera angled down from above, 
a woman sitting alone at a small table, her face in lower third of frame, 
overhead perspective, dim interior, vulnerable and isolated mood, 
cinematic portrait format
```

---

## Vertical Aerial (VAE) / 竖屏航拍

### 构图特征

```
┌─────────┐
│  主体   │  ← 高空俯视，主体变小
│  缩小   │
├─────────┤
│  环境   │  ← 环境成为画面主角
│  展开   │
└─────────┘
```

- drone 或摇臂垂直向下
- 主体可能只是画面中的一个点
- 环境叙事占主导

### 用途

- 开场建立镜头（establishing）
- 情绪转场
- 空间总览
- 悲剧/宿命感的视觉隐喻（人物渺小）

### Prompt 要点

```
vertical aerial shot, 9:16 top-down drone view, 
a small figure walking alone on a long empty road in a vast field, 
the figure is a tiny dot in the center of the frame, 
nature and environment dominate the composition, 
aerial cinematic atmosphere, melancholic establishing shot
```

---

## Vertical Depth Wide (VDW) / 竖屏纵深全景

### 构图特征

```
┌─────────┐
│  远方   │  ← 背景 Z=2，主体小而远
│  背景   │
├─────────┤
│  中景   │  ← Z=1，主体的主要活动区域
│  主体   │
├─────────┤
│  前景   │  ← Z=0，框架道具或最近的人物
│  框架   │
└─────────┘
```

- 三层纵深全部可见
- 环境交代 > 人物细节
- 走廊感、纵深感最强的镜头

### 用途

- 交代空间（走廊、房间、楼梯）
- 情绪铺垫
- 人物与环境关系的建立

### Prompt 要点

```
vertical wide shot, 9:16 portrait, strong Z-axis depth, 
wooden door frame in foreground (Z=0, slightly blurred), 
woman in traditional dress standing in a courtyard at midground (Z=1), 
traditional Chinese architecture and archway in the background (Z=2), 
deep focus, warm late afternoon light, cinematic narrative atmosphere
```

---

## 竖屏功率关系总结 / Power Dynamics in Vertical Frame

竖屏格式天然适合建立权力关系，因为：

1. **没有横向逃逸空间**——低角度仰视时，压迫感更强
2. **Z 轴前/后关系直观**——前景更大 = 权力，主动
3. **高低落差更显著**——竖长画面让楼梯的高度差更夸张

### 权力镜头速查

| 叙事目标 | 推荐镜头 | 关键构图 |
|----------|----------|----------|
| 确立男主权力 | VLA（低角度） + 男性在高位 | 仰视 + 顶置构图 |
| 表现女主脆弱 | VHA（高角度） + 低位 | 俯视 + 脸部在下 1/3 |
| 两人对峙压迫感 | VOTS（女前男后） | 前大后小 |
| 平等对话 | VMS 同 Z 轴 | 两人同大小 |
| 仰慕/崇拜 | VLA + 仰视对象在高处 | 低角度穿过楼梯仰望 |
| 宿命/孤独感 | VAE + 人物渺小 | 航拍小点 |

---

## Shot Type Quick Reference / 镜头速查

| 缩写 | 全称 | 中文 | 主要用途 |
|------|------|------|----------|
| VCU | Vertical Close-Up | 竖屏特写 | 情绪放大 |
| VMS | Vertical Medium Shot | 竖屏中景 | 对话、互动 |
| VOTS | Vertical Over-the-Shoulder | 竖屏过肩 | 替代正反打 |
| VLA | Vertical Low-Angle | 竖屏低角度 | 威严、压迫 |
| VHA | Vertical High-Angle | 竖屏高角度 | 脆弱、渺小 |
| VAE | Vertical Aerial | 竖屏航拍 | 建立、情绪 |
| VDW | Vertical Depth Wide | 竖屏纵深全景 | 环境交代 |
