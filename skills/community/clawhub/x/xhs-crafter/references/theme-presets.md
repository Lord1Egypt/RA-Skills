# Theme Presets

> xhs-crafter 配色方案参考，适配自 guizang-social-card-skill
> 画布基准：1080 × 1440（3:4）

---

## 硬规则

1. **一套卡片只用一个主题**，禁止混搭不同 palette 的变量。
2. **一个 accent 只用一次**——作为视觉锚点（数字、标签、分割线、CTA），其余全部用 ink / muted / line。
3. **accent-soft 仅用于背景色块**（标签底色、引用块底色），不用于文字。
4. **paper / paper-2 不可互换**——paper 是主背景，paper-2 是次级背景（卡片底、侧栏、引用块）。
5. **line 仅用于分割线和边框**，不用于文字。
6. **Midnight Ink 是唯一的暗色变体**，使用时必须同时应用 grain 和 paper-wash 覆盖。
7. **禁止自定义 hex**——用户只能从 10 套预设中选择，不得自行指定色值。约束越严，风格越稳。保护美学比给用户自由更重要。
8. **Lemon Green accent 色块面积 ≤20%**——明度极高，大面积使用会导致视觉疲劳。

---

## 一、Editorial Magazine × E-ink Palettes（6 套）

### 1. Ink Classic

经典纸墨——最通用的编辑风格，适合绝大多数内容。

```css
[data-theme="ink-classic"] {
  --paper:      #f3f0e8;
  --paper-2:    #ebe6da;
  --ink:        #0a0a0b;
  --muted:      #68625a;
  --line:       rgba(10, 10, 11, .22);
  --accent:     #111111;
  --accent-soft:#d8d2c6;
}
```

| 用途 | 说明 |
|------|------|
| 通用文章 | 黑白经典，阅读舒适 |
| 长文排版 | ink 与 paper 对比度最高，长时间阅读不疲劳 |
| 书摘 / 读书笔记 | 纸质感最强 |

> accent 与 ink 几乎同色，视觉锚点靠 **粗细 / 大小** 区分而非色相。

---

### 2. Indigo Porcelain

靛蓝瓷器——冷调理性，适合科技、数据、分析类内容。

```css
[data-theme="indigo-porcelain"] {
  --paper:      #f2f4f5;
  --paper-2:    #e5ebef;
  --ink:        #0a1f3d;
  --muted:      #5f6d78;
  --line:       rgba(10, 31, 61, .20);
  --accent:     #315d93;
  --accent-soft:#d7e1ec;
}
```

| 用途 | 说明 |
|------|------|
| 科技 / 数据 | 冷色传达专业感 |
| 行业报告 | accent 蓝适合图表标注 |
| B2B 内容 | 克制不花哨 |

> accent-soft 可用于数据表格的斑马纹底色。

---

### 3. Forest Ink

森林墨绿——自然、沉稳，适合生活方式、户外、可持续主题。

```css
[data-theme="forest-ink"] {
  --paper:      #f5f1e8;
  --paper-2:    #e8dfcf;
  --ink:        #16251b;
  --muted:      #5d665d;
  --line:       rgba(22, 37, 27, .22);
  --accent:     #2e6b4f;
  --accent-soft:#d4dfd2;
}
```

| 用途 | 说明 |
|------|------|
| 生活方式 | 暖纸底 + 绿调，自然感 |
| 户外 / 旅行 | accent 绿暗示自然 |
| 可持续 / 环保 | 色彩语义匹配主题 |

> paper 偏暖（e8 结尾），与绿色 accent 形成冷暖对比。

---

### 4. Kraft Paper

牛皮纸——手作、复古、温暖，适合美食、手作、品牌故事。

```css
[data-theme="kraft-paper"] {
  --paper:      #eedfc7;
  --paper-2:    #dfc9a8;
  --ink:        #2a1e13;
  --muted:      #755f49;
  --line:       rgba(42, 30, 19, .24);
  --accent:     #9b5a2e;
  --accent-soft:#d5b58f;
}
```

| 用途 | 说明 |
|------|------|
| 美食 / 烘焙 | 暖棕色调，食欲感 |
| 手作 / 工艺 | 牛皮纸质感匹配 |
| 品牌故事 | 复古温度感 |

> paper 本身就是暖色，不需要额外叠加 paper-wash。accent 棕色用于价格标签、分类标签。

---

### 5. Dune

沙丘——沙漠、大地色系，适合建筑、设计、极简美学。

```css
[data-theme="dune"] {
  --paper:      #f0e6d2;
  --paper-2:    #ded0b7;
  --ink:        #1f1a14;
  --muted:      #6f6557;
  --line:       rgba(31, 26, 20, .22);
  --accent:     #8f7650;
  --accent-soft:#d4c2a4;
}
```

| 用途 | 说明 |
|------|------|
| 建筑 / 空间 | 大地色系，空间感 |
| 极简美学 | 低饱和度，安静 |
| 设计作品集 | 不抢内容风头 |

> accent 与 muted 距离较近，视觉锚点需要靠 **字号 / 粗细** 加强。

---

### 6. Midnight Ink（暗色变体）

午夜墨色——唯一的暗色主题，适合夜间阅读、高端感、沉浸式内容。

```css
[data-theme="midnight-ink"] {
  --paper:      #0e0d0c;
  --paper-2:    #1a1714;
  --ink:        #ece2cf;
  --muted:      #9a8c75;
  --line:       rgba(236, 226, 207, .22);
  --accent:     #d4a04a;
  --accent-soft:#3a2a14;
}
```

**必须同时应用的覆盖：**

```css
[data-theme="midnight-ink"] {
  /* ── grain 纹理覆盖 ── */
  --grain-opacity: .06;
  --grain-blend:   overlay;

  /* ── paper-wash 水洗覆盖 ── */
  --wash-color:    rgba(212, 160, 74, .03);
  --wash-angle:    135deg;
}
```

| 用途 | 说明 |
|------|------|
| 夜间阅读 | 暗底护眼 |
| 高端 / 奢华 | 金色 accent + 暗底 = 高级感 |
| 沉浸式长文 | 减少环境光反射 |

> ⚠️ **硬性要求**：使用 Midnight Ink 时，grain 和 paper-wash 覆盖不可省略，否则暗色背景会显得死板。
> accent 金色（#d4a04a）只用于关键数字和标签，禁止大面积使用。

---

## 二、Swiss International Palettes（4 套）

Swiss 体系使用不同的变量名，accent-on 控制 accent 色块上的文字颜色。

### 硬规则（Swiss 补充）

1. **accent 色块面积 ≤ 30%**——瑞士风格的核心是留白。
2. **accent-on 仅用于 accent 背景上的文字**，不可单独使用。
3. **grey-1 / grey-2 / grey-3 严格分层**：grey-1 背景 → grey-2 边框/分割 → grey-3 次要文字。
4. **paper 永远是最浅色**，不可被 grey-1 覆盖。

---

### 1. IKB Blue

国际克莱因蓝——最经典的瑞士风格，适合品牌、宣言、科技。

```css
[data-theme="ikb-blue"] {
  --paper:    #fafaf8;
  --ink:      #0a0a0a;
  --grey-1:   #f0f0ee;
  --grey-2:   #d4d4d2;
  --grey-3:   #737373;
  --accent:   #002FA7;
  --accent-on:#ffffff;
}
```

| 用途 | 说明 |
|------|------|
| 品牌 / VI | 克莱因蓝 = 瑞士设计代名词 |
| 科技 / SaaS | 蓝色信任感 |
| 宣言 / 声明 | 强对比，权威感 |

> IKB Blue 在 accent 色块上使用白色文字（accent-on: #ffffff）。

---

### 2. Lemon Yellow

柠檬黄——活力、年轻、注意力抓取，适合消费品牌、活动、社交内容。

```css
[data-theme="lemon-yellow"] {
  --paper:    #fafaf8;
  --ink:      #0a0a0a;
  --grey-1:   #f0f0ee;
  --grey-2:   #d4d4d2;
  --grey-3:   #737373;
  --accent:   #FFD500;
  --accent-on:#0a0a0a;
}
```

| 用途 | 说明 |
|------|------|
| 消费品牌 | 黄色 = 快乐 + 注意力 |
| 活动海报 | 高可见度 |
| 社交媒体 | 在信息流中跳脱 |

> accent-on 为黑色——黄色背景上必须用深色文字以保证可读性。

---

### 3. Lemon Green

柠檬绿——清新、增长、生态，适合增长数据、健康、教育。

```css
[data-theme="lemon-green"] {
  --paper:    #fafaf8;
  --ink:      #0a0a0a;
  --grey-1:   #f0f0ee;
  --grey-2:   #d4d4d2;
  --grey-3:   #737373;
  --accent:   #C5E803;
  --accent-on:#0a0a0a;
}
```

| 用途 | 说明 |
|------|------|
| 增长 / 数据 | 绿色 = 增长语义 |
| 健康 / 教育 | 清新不刺眼 |
| 环保 / 可持续 | 色彩语义匹配 |

> Lemon Green 明度极高，accent 色块面积建议 ≤ 20%，避免视觉疲劳。

---

### 4. Safety Orange

安全橙——警示、紧急、行动，适合 CTA、限时优惠、安全提示。

```css
[data-theme="safety-orange"] {
  --paper:    #fafaf8;
  --ink:      #0a0a0a;
  --grey-1:   #f0f0ee;
  --grey-2:   #d4d4d2;
  --grey-3:   #737373;
  --accent:   #FF6B35;
  --accent-on:#ffffff;
}
```

| 用途 | 说明 |
|------|------|
| CTA / 行动号召 | 橙色 = 紧迫感 |
| 限时优惠 | 注意力抓取 |
| 安全提示 | 色彩语义匹配 |

> accent-on 为白色——橙色背景上白色文字可读性最佳。

---

## 快速选择指南

| 内容类型 | 推荐主题 | 理由 |
|----------|----------|------|
| 通用文章 / 书摘 | Ink Classic | 最安全，零出错 |
| 科技 / 数据 / B2B | Indigo Porcelain | 冷调专业 |
| 生活方式 / 户外 | Forest Ink | 自然温暖 |
| 美食 / 手作 / 品牌 | Kraft Paper | 复古手作感 |
| 建筑 / 极简 | Dune | 大地安静 |
| 高端 / 夜间 / 沉浸 | Midnight Ink | 暗色高级感 |
| 品牌 / 宣言 / 科技 | IKB Blue | 经典瑞士 |
| 消费 / 活动 / 社交 | Lemon Yellow | 活力跳脱 |
| 增长 / 健康 / 教育 | Lemon Green | 清新增长 |
| CTA / 限时 / 警示 | Safety Orange | 紧迫行动 |
