# Raphael AI 生图技能

> 完全免费、无限、无水印。无需注册。

## 技能定位

本技能通过 **OpenClaw Browser** 控制 Raphael AI 网站生成图片。
**执行者：紫灵主 Agent（器灵）。其他 Agent 以请求方式调用。**

---

## 工作流程（Agent 调用方式）

### 步骤 1：发送请求

向紫灵（主 Agent）发送消息，格式：

```
📷 生图请求
提示词：[你的描述]
风格：[可选，如 Fantasy / Photo / Cinematic]
```

或直接说：
- "帮我生成一张奇幻风格的森林图"
- "生成一张电商产品主图，无线耳机"

### 步骤 2：紫灵执行

紫灵自动完成：
1. 打开 `https://raphaelai.org/zh/ai-image-generator`
2. 输入提示词
3. 点击「生成」
4. 等待完成（10-20秒）
5. 提取图片 URL 并下载
6. 发送给你

### 步骤 3：接收图片

紫灵通过 Discord 将图片发到当前频道。

---

## 快速参考

**网址：** https://raphaelai.org/zh/ai-image-generator

**提示词公式：**
```
[主体] + [动作] + [环境] + [光线] + [风格] + [输出限制]
```

**示例提示词：**
```
A cinematic portrait of a wise old wizard holding a glowing staff, 
epic fantasy landscape background, dramatic golden hour lighting, 
fantasy style, film grain, no text no watermark

A modern minimalist smartwatch product photo on clean white marble, 
soft studio lighting from the left, shallow depth of field, 
professional e-commerce photography, no text no watermark
```

**风格关键词（直接写在提示词里）：**
- 照片 → `photo style`
- 动漫 → `anime style`
- 奇幻 → `fantasy style`
- 电影感 → `cinematic style`
- 胶片 → `film style`
- 霓虹黑色电影 → `neon noir style`
- 蒸汽波 → `vaporwave style`
- 吉卜力 → `ghibli style`

---

## 24 种视觉风格

| # | 风格 | 英文 | 适合场景 |
|---|------|------|---------|
| 01 | 📷 照片 | Photo | 产品/写实 |
| 02 | 🎌 动漫 | Anime | 插画/角色 |
| 03 | 🐉 奇幻 | Fantasy | 魔法世界/史诗 |
| 04 | 👤 人像 | Portrait | 人物特写 |
| 05 | 🏔️ 风景 | Landscape | 自然/建筑 |
| 06 | 🚀 科幻 | Sci-Fi | 未来/太空 |
| 07 | 🎥 电影感 | Cinematic | 戏剧性/短片 |
| 08 | 🖼️ 油画 | Oil Painting | 艺术/古典 |
| 09 | 👾 像素艺术 | Pixel Art | 游戏/复古 |
| 10 | 💧 水彩 | Watercolor | 柔和/插画 |
| 11 | 🌸 吉卜力 | Ghibli | 宫崎骏风/梦幻 |
| 12 | 📻 复古 | Vintage | 怀旧/胶片 |
| 13 | 📷 胶片 | Film | 真实感/自然光 |
| 14 | 🖋️ 水墨 | Ink Wash | 中国风/水墨 |
| 15 | 🌙 梦境核心 | Dreamcore | 超现实/梦幻 |
| 16 | 🌿 太阳朋克 | Solarpunk | 生态乌托邦 |
| 17 | 🌆 霓虹黑色电影 | Neon Noir | 赛博朋克/暗调 |
| 18 | 🪵 大地 | Earth | 自然/暖色调 |
| 19 | 👑 巴洛克金色 | Baroque Gold | 华丽/金色 |
| 20 | 📺 蒸汽波 | Vaporwave | 80年代/复古 |
| 21 | 📐 蓝图 | Blueprint | 技术/建筑 |
| 22 | 🍂 侘寂 | Wabi-Sabi | 日式极简 |
| 23 | 🎌 超平 | Ultra Flat | 扁平插画 |
| 24 | 🏗️ 粗野主义 | Brutalist | 混凝土/几何 |

---

## 常用场景模板

### 🛍️ 电商产品主图
```
[产品名] product photo on clean [背景], soft studio lighting, 
shallow depth of field, professional e-commerce photography, 
no text no watermark
```

### 🎬 YouTube 缩略图
```
[主题] YouTube thumbnail, expressive face close-up, dramatic lighting, 
bold graphic background, high contrast, centered composition, 
no text watermark
```

### 📱 社交媒体配图
```
[主题] Instagram post, editorial composition, sufficient text safe area, 
warm natural tones, modern aesthetic, no text watermark
```

### 🌄 奇幻概念图
```
[场景描述], epic fantasy landscape, dramatic lighting, 
cinematic composition, fantasy style, no text watermark
```

### 🎨 品牌 Logo
```
[品牌名] minimalist flat [类型] logo, centered icon mark, 
clean vector style, white background, no text
```

---

## 技术说明

- **执行方式：** 通过 OpenClaw Browser (profile=openclaw) 自动化
- **网站：** https://raphaelai.org/zh/ai-image-generator
- **图片提取：** 从 DOM 获取 `cdn.raphaelai.org` URL 后 curl 下载
- **保存路径：** `~/.openclaw/workspace/media/`
- **无需 API Key / 无需注册**

## 限制与注意事项

1. 生成等待约 10-20 秒，耐心等待
2. 不指定风格时默认"照片"风格
3. 图片通常为 1024x1024 或 512x512
4. 下载后通过 Discord 发送原文件（非截图）
5. 可商用，无水印
