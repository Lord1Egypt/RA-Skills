---
name: theme-factory
version: 1.0.0
description: >
  为幻灯片、文档、报告、HTML页面等应用专业主题配色和字体。
  内置10套精选主题，也可以按需生成自定义主题。当用户说"换个配色"、
  "美化这个文档"、"选个专业的字体"、"生成一套主题"时使用。
metadata:
  author: 移植自 Anthropic
  category: design
---

# 主题工厂

为任何内容应用专业、协调的配色和字体方案。让你的PPT、文档、网页看起来像专业设计师做的！

---

## 🎯 什么时候使用

**立即触发：**
- 用户说"帮我美化一下"、"换个配色"
- 用户要做PPT、报告、文档，需要好看的主题
- 用户问"用什么字体比较专业"
- 用户要生成一套自定义的配色方案

**不要触发：**
- 纯代码，不需要视觉设计
- 数据处理，不涉及展示

---

## 🎨 10套精选内置主题

### 主题预览速览

| 编号 | 主题名称 | 风格描述 | 适用场景 |
|------|---------|---------|---------|
| 1 | 🌊 深海蓝调 | 专业、平静的海洋色调 | 商务报告、正式场合 |
| 2 | 🌅 日落大道 | 温暖、活力的橙红渐变 | 创意、营销、发布会 |
| 3 | 🌲 森林树冠 | 自然、稳重的大地色系 | 环保、健康、农业 |
| 4 | ⚪ 现代极简 | 干净、克制的黑白灰 | 科技、设计、作品集 |
| 5 | 🌟 金色时刻 | 浓郁、温暖的秋色调 | 高端产品、庆典 |
| 6 | ❄️ 北极霜冻 | 清冷、锐利的冬日感 | 科技、冰雪运动、医疗 |
| 7 | 🌹 沙漠玫瑰 | 柔和、精致的灰粉色 | 时尚、美妆、女性向产品 |
| 8 | 💡 科技创新 | 大胆、现代的赛博感 | 科技发布会、产品演示 |
| 9 | 🌿 植物园 | 清新、有机的绿色调 | 食品、健康、生活方式 |
| 10 | 🌌 午夜银河 | 戏剧化、深邃的暗色调 | 高端产品、艺术、晚宴 |

---

## 📋 每套主题详细参数

### 1. 🌊 深海蓝调 (Ocean Depths)

```css
/* 配色 */
--primary: #0D4C6B;      /* 深海蓝 - 主标题 */
--secondary: #2E8B8B;    /* 青蓝 - 副标题 */
--accent: #F5A962;       /* 暖橙 - 强调色 */
--background: #F8FAFB;   /* 近白背景 */
--text: #1A2E38;         /* 深灰文字 */

/* 字体 */
--header-font: 'Playfair Display', serif;  /* 高雅标题 */
--body-font: 'Source Sans Pro', sans-serif; /* 易读正文 */
```

**适用：** 金融报告、学术答辩、正式商务演示

---

### 2. 🌅 日落大道 (Sunset Boulevard)

```css
/* 配色 */
--primary: #D9534F;      /* 珊瑚红 */
--secondary: #F0AD4E;    /* 日落黄 */
--accent: #5BC0DE;       /* 天蓝点缀 */
--background: #FFF9F5;   /* 暖白背景 */
--text: #3C2A21;         /* 深棕文字 */

/* 字体 */
--header-font: 'Montserrat', sans-serif;  /* 现代粗体 */
--body-font: 'Lato', sans-serif;          /* 圆润正文 */
```

**适用：** 营销方案、创意提案、产品发布会

---

### 3. 🌲 森林树冠 (Forest Canopy)

```css
/* 配色 */
--primary: #2D5016;      /* 森林深绿 */
--secondary: #6B8E23;    /* 橄榄绿 */
--accent: #CD853F;       /* 古铜色点缀 */
--background: #F5F5F0;   /* 米白背景 */
--text: #2C2C2C;         /* 纯黑文字 */

/* 字体 */
--header-font: 'Lora', serif;           /* 人文气息 */
--body-font: 'Merriweather', serif;     /* 经典易读 */
```

**适用：** 环保报告、农业项目、健康产品

---

### 4. ⚪ 现代极简 (Modern Minimalist)

```css
/* 配色 */
--primary: #1A1A1A;      /* 纯黑 */
--secondary: #666666;    /* 中灰 */
--accent: #E63946;       /* 正红强调（唯一亮色） */
--background: #FFFFFF;   /* 纯白背景 */
--text: #1A1A1A;         /* 纯黑文字 */

/* 字体 */
--header-font: 'Inter', sans-serif;     /* 现代中性 */
--body-font: 'Inter', sans-serif;       /* 全用统一字体 */
```

**适用：** 科技公司、设计作品集、极简风格产品

---

### 5. 🌟 金色时刻 (Golden Hour)

```css
/* 配色 */
--primary: #8B4513;      /* 马鞍棕 */
--secondary: #DAA520;    /* 金麒麟色 */
--accent: #B22222;       /* 砖红点缀 */
--background: #FFF8E7;   /* 奶油色背景 */
--text: #3A2E1F;         /* 暖棕文字 */

/* 字体 */
--header-font: 'Playfair Display', serif;  /* 奢华感 */
--body-font: 'Crimson Text', serif;        /* 精致正文 */
```

**适用：** 高端产品、奢侈品、庆典活动、酒店餐饮

---

### 6. ❄️ 北极霜冻 (Arctic Frost)

```css
/* 配色 */
--primary: #1E3A5F;      /* 深蓝 */
--secondary: #4A90A4;    /* 冰蓝 */
--accent: #88D8B0;       /* 薄荷绿 */
--background: #F0F5F9;   /* 冷白背景 */
--text: #1C2B3A;         /* 冷灰文字 */

/* 字体 */
--header-font: 'Poppins', sans-serif;    /* 清爽现代 */
--body-font: 'Open Sans', sans-serif;    /* 清晰易读 */
```

**适用：** 医疗健康、科技产品、冰雪运动

---

### 7. 🌹 沙漠玫瑰 (Desert Rose)

```css
/* 配色 */
--primary: #9A8C98;      /* 灰紫 */
--secondary: #C9ADA7;    /* 干燥玫瑰 */
--accent: #F2E9E4;       /* 裸粉 */
--background: #FFFFFF;   /* 纯白 */
--text: #4A4E69;         /* 深灰紫 */

/* 字体 */
--header-font: 'Cormorant Garamond', serif;  /* 优雅衬线 */
--body-font: 'Karla', sans-serif;             /* 圆润无衬线 */
```

**适用：** 时尚美妆、女性向产品、生活方式品牌

---

### 8. 💡 科技创新 (Tech Innovation)

```css
/* 配色 */
--primary: #0F172A;      /* 深蓝黑 */
--secondary: #3B82F6;    /* 科技蓝 */
--accent: #10B981;       /* 荧光绿 */
--background: #0F172A;   /* 深色背景（深色模式） */
--text: #F8FAFC;         /* 白色文字 */

/* 字体 */
--header-font: 'Space Grotesk', sans-serif;  /* 科技感 */
--body-font: 'DM Sans', sans-serif;           /* 现代感 */
```

**适用：** 科技发布会、产品Demo、黑客松项目

---

### 9. 🌿 植物园 (Botanical Garden)

```css
/* 配色 */
--primary: #2C5F2D;      /* 深叶绿 */
--secondary: #97BC62;    /* 嫩绿 */
--accent: #FFBA00;       /* 明黄点缀 */
--background: #F8F9F4;   /* 淡绿米白 */
--text: #1E2F1E;         /* 深绿灰文字 */

/* 字体 */
--header-font: 'ABeeZee', sans-serif;      /* 圆润可爱 */
--body-font: 'Nunito', sans-serif;         /* 柔和易读 */
```

**适用：** 食品有机、健康生活、园艺植物

---

### 10. 🌌 午夜银河 (Midnight Galaxy)

```css
/* 配色 */
--primary: #0C0C1E;      /* 接近黑的深蓝 */
--secondary: #1A1A40;    /* 深紫蓝 */
--accent: #7B68EE;       /* 中紫闪星 */
--accent-2: #00CED1;     /* 青蓝星芒 */
--background: #0C0C1E;   /* 深色背景 */
--text: #E8E8F0;         /* 亮白文字 */

/* 字体 */
--header-font: 'Orbitron', sans-serif;    /* 未来感 */
--body-font: 'Rajdhani', sans-serif;      /* 锐利正文 */
```

**适用：** 人工智能、太空主题、高端晚宴、艺术展

---

## 🔧 如何应用主题

### 给用户展示选项

> 🎨 我有10套精选主题，你可以选一个：
> 
> 1. 🌊 深海蓝调 - 商务正式
> 2. 🌅 日落大道 - 活力创意
> 3. 🌲 森林树冠 - 自然稳重
> 4. ⚪ 现代极简 - 干净克制
> 5. 🌟 金色时刻 - 高端奢华
> 6. ❄️ 北极霜冻 - 清冷科技
> 7. 🌹 沙漠玫瑰 - 柔和精致
> 8. 💡 科技创新 - 赛博未来
> 9. 🌿 植物园 - 清新有机
> 10. 🌌 午夜银河 - 深邃戏剧
> 
> 选几号？或者告诉我你想要什么感觉，我帮你定制！

---

### 应用到PPT/幻灯片

用户选好后，给出具体建议：

> ✅ 应用「深海蓝调」主题到你的幻灯片：
> 
> **配色方案：**
> - 标题颜色：#0D4C6B
> - 副标题颜色：#2E8B8B
> - 强调/按钮颜色：#F5A962
> - 背景色：#F8FAFB
> - 正文字色：#1A2E38
> 
> **字体建议：**
> - 标题：Playfair Display 或 宋体粗体
> - 正文：Source Sans Pro 或 微软雅黑
> 
> **排版建议：**
> - 每页不超过6行文字
> - 标题字号是正文的2.5倍
> - 重要数据用强调色突出

---

### 应用到HTML页面

直接生成CSS变量：

```css
:root {
  /* 深海蓝调主题 */
  --color-primary: #0D4C6B;
  --color-secondary: #2E8B8B;
  --color-accent: #F5A962;
  --color-background: #F8FAFB;
  --color-text: #1A2E38;
  
  --font-header: 'Playfair Display', serif;
  --font-body: 'Source Sans Pro', sans-serif;
}

/* 使用示例 */
h1, h2, h3 {
  color: var(--color-primary);
  font-family: var(--font-header);
}

body {
  color: var(--color-text);
  font-family: var(--font-body);
  background-color: var(--color-background);
}

button {
  background-color: var(--color-accent);
}
```

---

## 🎲 自定义主题生成

如果内置主题都不合适，生成自定义主题：

### 先问用户几个问题：

> 好的，我们来定制一套主题！先确认一下：
> 1. 这是给什么场景用的？（商务/创意/科技/其他）
> 2. 想要什么感觉？（正式/活泼/高端/冷静/温暖）
> 3. 有偏好的颜色吗？（比如喜欢蓝色，讨厌橙色）

### 然后生成一套完整的主题

生成后给它起个好名字，比如「晨雾咖啡」、「极光之夜」等。

---

## 💡 设计最佳实践

### 配色原则
1. **最多3种颜色** - 主色 + 辅助色 + 强调色，不要更多
2. **60-30-10法则** - 主色60%，辅助色30%，强调色10%
3. **对比度够** - 文字和背景对比度至少4.5:1（WCAG标准）
4. **同色系深浅** - 用同一种颜色的深浅做层次，比换颜色更高级

### 字体原则
1. **最多2种字体** - 标题一种，正文一种
2. **风格互补** - 衬线标题 + 无衬线正文 = 经典组合
3. **字号层级分明** - 标题是正文的2-3倍
4. **行高够** - 正文行高1.5-1.6倍，标题行高1.2倍

### 通用禁忌
❌ 不要用亮红配亮绿（色盲友好问题）
❌ 不要用纯黑（#000）做正文，太刺眼，用深灰
❌ 不要用太多种颜色，会乱
❌ 不要所有字都加粗，要有层级

---

## 📦 输出格式

每次给出主题时，必须包含：
1. 主题名称和emoji
2. 配色的hex色值（5个：主色/辅助色/强调色/背景/文字）
3. 字体推荐（标题字体 + 正文字体）
4. 具体的应用建议
5. 适用场景说明

---

**现在，想要选一套主题还是定制一套？** 🎨✨
