---
name: text-art
description: Create text-based art (ASCII art) and emoji pixel art in various styles and themes. Use when user requests creating text art, ASCII art, emoji pixel illustrations, or pixel-style art.
metadata:
  {
    "openclaw": {
      "emoji": "🎨",
      "os": ["darwin", "linux", "win32"]
    }
  }
---

# Text Art Generator - ASCII Art & Emoji Pixel Art Creation Skill

Create various styles of text-based art including classic ASCII art and colorful emoji pixel art.

## 使用场景

✅ **USE when:**
- User requests creating ASCII art or text-based illustrations
- User wants emoji pixel art / pixel-style illustrations using emoji blocks
- User needs decorative text art for messages, comments, or social media
- User wants to convert text or concepts into visual text representations
- User asks for specific themed text art (animals, objects, symbols, etc.)
- User shares a pixel art image and wants an emoji recreation

❌ **DON'T use when:**
- User needs high-resolution photos or complex realistic graphics
- User requests vector graphics or SVG

---

## 模式一：经典 ASCII Art

使用标准 ASCII 字符构建图形轮廓，适合简洁线条风格。

### 动物主题示例
```
  /\_/\
 ( o.o )
  > ^ <
```

### 建筑/物体主题示例
```
    /\
   /  \
  /____\
  |    |
  |____|
```

### 自然主题示例
```
    *
   ***
  *****
   |||
   |||
```

---

## 模式二：Emoji 像素画（推荐用于彩色/可爱风格）

### 核心理念

每一个 emoji 相当于一个"像素格"，通过在网格上排列不同颜色的 emoji 来构建图像。
每行 emoji 数量要保持一致（用空白 emoji `　` 或透明占位符补齐），确保网格整齐。

### Emoji 调色板

根据需要从下表选择颜色 emoji，组合出图像的色彩层次：

| 颜色 | Emoji | 用途 |
|------|-------|------|
| 黑色 | ⬛ | 轮廓、眼睛、暗部 |
| 白色 | ⬜ | 高光、眼白、背景 |
| 棕色/橙棕 | 🟫 | 熊、木头、泥土 |
| 橙色 | 🟧 | 火、太阳、橙色皮肤 |
| 黄色 | 🟨 | 星星、香蕉、金色 |
| 绿色 | 🟩 | 草地、树叶、青蛙 |
| 蓝色 | 🟦 | 天空、水、蓝色物体 |
| 紫色 | 🟪 | 神秘、花朵、魔法 |
| 红色 | 🟥 | 火、苹果、红色 |
| 粉色/浅色 | 🩷 | 皮肤、花瓣、粉色 |
| 透明/空白 | 　 | 背景留空（全角空格，宽度=1个emoji） |

> **重要**：每行必须等宽！空白处用全角空格 `　`（U+3000）补齐，保证像素网格对齐。

### 设计流程

1. **草图规划**：先在脑中（或文字描述中）把图像分解为 N×M 的像素网格
2. **配色选择**：确定主色、阴影色、高光色各用哪个 emoji
3. **逐行绘制**：从上到下，逐行填写 emoji，每行长度相同
4. **细节优化**：检查轮廓是否流畅，高光/阴影是否自然

### 像素熊示例（参考风格：方块像素游戏角色）

```
　🟫🟫　　🟫🟫　
🟫🟫🟫🟫🟫🟫🟫🟫
🟫🟫⬛🟫🟫⬛🟫🟫
🟫🟫🟫🟫🟫🟫🟫🟫
🟫🟫🟫🟫🟫🟫🟫🟫
　　🟫🟫　🟫🟫　
　　🟫🟫　🟫🟫　
```

说明：
- 第1行：两侧各有耳朵凸起（用全角空格留白）
- 第2行：完整宽度的头部
- 第3行：两个黑色眼睛 ⬛
- 第4-5行：脸部/身体
- 第6-7行：两条腿

### 像素猫咪示例

```
⬛　⬛　⬛　⬛　⬛
⬛🟧🟧🟧🟧🟧⬛
⬛🟧⬛🟧⬛🟧⬛
⬛🟧🟧🟧🟧🟧⬛
⬛🟧🟧🟧🟧🟧⬛
　⬛🟧🟧🟧⬛　
　　⬛　　⬛　　
```

### 像素星星示例

```
　　🟨　　
　🟨🟨🟨　
🟨🟨🟨🟨🟨
　🟨🟨🟨　
🟨　　　🟨
```

### 像素心形示例

```
　🟥🟥　🟥🟥　
🟥🟥🟥🟥🟥🟥🟥
🟥🟥🟥🟥🟥🟥🟥
　🟥🟥🟥🟥🟥　
　　🟥🟥🟥　　
　　　🟥　　　
```

---

## 模式三：混合风格（ASCII 轮廓 + Emoji 填色）

在 ASCII 框架内用 emoji 点缀，兼顾结构感和色彩：

```
   ____
  / 🐻 \
 | ⬛  ⬛|
  \ 🐽 /
   \__/
   |  |
  /|  |\
```

---

## 风格选择指南

| 需求 | 推荐模式 |
|------|----------|
| 简洁、复古、代码注释用 | 经典 ASCII Art |
| 可爱、彩色、社交媒体用 | Emoji 像素画 |
| 参考像素游戏风格 | Emoji 像素画（方块网格）|
| 有轮廓+局部彩色 | 混合风格 |
| 用户提供像素图参考 | 分析颜色区域 → Emoji 像素画 |

---

## 输出规范

- 所有 text art 输出在代码块（` ``` `）中，方便复制
- Emoji 像素画每行 emoji 数量必须严格相等（空白用全角空格 `　` 补齐）
- 默认尺寸：8×8 到 12×12 像素格；如需更大可扩展
- 根据用户要求可提供多个尺寸/风格版本

---

## 示例请求与响应

### 请求：经典动物
```
"画一只 ASCII 猫"
```
响应：
```
  /\_/\
 ( o.o )
  > ^ <
```

### 请求：Emoji 像素动物
```
"用 emoji 画一只像素熊"
```
响应：
```
　🟫🟫　　🟫🟫　
🟫🟫🟫🟫🟫🟫🟫🟫
🟫🟫⬛🟫🟫⬛🟫🟫
🟫🟫🟫🟫🟫🟫🟫🟫
🟫🟫🟫🟫🟫🟫🟫🟫
　　🟫🟫　🟫🟫　
　　🟫🟫　🟫🟫　
```

### 请求：Emoji 像素风景
```
"用 emoji 画一个白天的风景"
```
响应：
```
🟦🟦🟦🟨🟦🟦🟦🟦
🟦🟦🟦🟦🟦🟦🟦🟦
🟦🟦🟦🟦🟦🟦🟦🟦
🟩🟩🟩🟩🟩🟩🟩🟩
🟩🟩🟫🟩🟩🟫🟩🟩
🟩🟫🟫🟫🟩🟫🟫🟩
```

---

This skill supports both classic ASCII art and emoji pixel art creation. Use emoji pixel mode for colorful, cute, and pixel-game-style illustrations.

Reference：https://textart.sh/