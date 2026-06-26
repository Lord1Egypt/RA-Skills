---
name: seo-keyword-density
description: |
  SEO 关键词密度优化与页面审计技能。使用场景：
  (1) 用户提供页面路径和关键词，需要优化 SEO
  (2) 用户想提升某个页面的关键词密度
  (3) 用户要求优化页面的搜索引擎排名
  (4) 用户需要 SEO 审计检查（meta tags、OG、hreflang 等）
  触发词：关键词密度、SEO优化、关键词优化、keyword density、SEO审计、SEO检查
---

# SEO 关键词密度优化与页面审计

将页面关键词密度优化至 5%，确保页面内容丰富（800-1000 单词），并执行完整的 SEO 审计检查，提升搜索引擎排名。

## 核心目标

| 指标 | 目标值 | 说明 |
|------|--------|------|
| **页面单词数** | 800-1000 词 | 内容丰富的页面更受搜索引擎青睐 |
| **关键词密度** | 3-5% | 自然融入，避免堆砌 |
| **SEO 审计** | 10/10 | 完整的技术 SEO 合规 |

## 输入参数

- **页面路径**: 页面组件路径或翻译 JSON 文件路径
- **关键词**: 目标 SEO 关键词（支持多个，用逗号分隔）

## 工作流程

### 1. 收集页面文本

根据页面路径，收集所有相关文本内容：

**对于 TSX/JSX 页面组件**:
- 提取 JSX 中的静态文本
- 提取 `t()` 或 `useTranslations` 调用的翻译键
- 找到对应的翻译 JSON 文件

**对于翻译 JSON 文件**:
- 读取所有文本值
- 忽略键名，只统计值

### 2. 计算当前密度

```
关键词密度 = (关键词出现次数 / 页面总词数) × 100%
```

**词数统计规则**:
- 英文：按空格分词
- 中文：按字符计数，每个汉字算一个词

**示例**:
- 页面总词数：200
- 关键词 "video editor" 出现 3 次
- 当前密度：3 / 200 × 100% = 1.5%

### 3. 检查页面内容量

**目标单词数：800-1000 词**

搜索引擎偏好内容丰富、有深度的页面。单词数过少的页面（< 500 词）通常被视为"薄内容"（thin content），难以获得良好排名。

| 状态 | 单词数 | 行动 |
|------|--------|------|
| ❌ 不足 | < 500 | 需要大幅扩充内容 |
| ⚠️ 偏少 | 500-799 | 建议增加 200-300 词 |
| ✅ 理想 | 800-1000 | 保持现状 |
| ✅ 丰富 | > 1000 | 可接受，注意可读性 |

**内容扩充策略**:

1. **添加 FAQ 章节** - 每个 Q&A 约 50-80 词
2. **扩展功能描述** - 详细说明每个功能的用途和优势
3. **添加使用场景** - 描述不同用户群体的使用方式
4. **添加 How-to 步骤** - 分步骤教程增加可读性
5. **添加对比说明** - 与竞品或传统方式对比
6. **添加用户评价/案例** - 增加社会证明

### 4. 计算关键词目标增量

```
目标出现次数 = 页面总词数 × 5% = 页面总词数 × 0.05
需要增加次数 = 目标出现次数 - 当前出现次数
```

### 5. 优化策略

按优先级执行以下优化：

**A. 自然融入现有文本 (优先)**

在不改变语义的前提下，将关键词融入现有句子：

```json
// 优化前
"description": "Create stunning visuals with our tool"

// 优化后 (关键词: video editor)
"description": "Create stunning visuals with our video editor tool"
```

**B. 增强描述文本**

扩展简短描述，自然加入关键词：

```json
// 优化前
"feature_1": "Fast processing"

// 优化后 (关键词: video editor)
"feature_1": "Fast video processing with our professional video editor"
```

**C. 添加新内容段落**

在适当位置添加包含关键词的新内容：

- FAQ 问答
- 功能描述
- 使用场景说明
- SEO 优化段落

### 6. 优化原则

1. **保持自然**: 关键词必须读起来自然流畅，避免堆砌
2. **语义相关**: 只在语义相关的位置添加关键词
3. **分布均匀**: 关键词应均匀分布在页面各处
4. **避免过度**: 单个句子最多包含 1-2 次关键词
5. **变体使用**: 适当使用关键词变体（复数、同义词）
6. **内容深度**: 优先通过增加有价值内容来达到词数目标，而非简单堆砌

### 7. 输出格式

完成优化后，输出：

1. **页面单词数**: 优化前 → 优化后（目标 800-1000）
2. **关键词密度**: 优化前 → 优化后（目标 3-5%）
3. **修改摘要**: 列出所有修改的文件和位置
4. **修改详情**: 使用 Edit 工具应用所有更改

## 示例

**输入**:
```
页面路径: /your-page-slug
关键词: your main keyword, secondary keyword
```

**分析输出**:
```
页面分析:
- 页面组件: src/app/[locale]/(landing)/your-page-slug/page.tsx
- 翻译文件: src/config/locale/messages/en/your-page.json

内容量检查:
- 当前总词数: 450 词 ⚠️ 偏少（目标 800-1000）
- 需要增加: 约 350-550 词

关键词密度检查:
- "your main keyword" 出现: 5 次 (1.1%)
- "secondary keyword" 出现: 2 次 (0.4%)
- 当前综合密度: 1.5%
- 目标密度: 3-5%

优化计划:
1. 添加 FAQ 章节（6 个问题，约 400 词）
2. 扩展功能描述（每个功能 +50 词）
3. 添加使用场景说明（约 150 词）
4. 在各处自然融入关键词
5. 预计优化后: 950 词，密度 4.2%
```

## 注意事项

- 目标密度 5% 是建议值，可根据实际情况调整至 3-7%
- 过高密度可能被搜索引擎判定为关键词堆砌
- 优先优化 title、description、h1-h3 等权重较高的位置
- 中文内容的关键词密度计算需考虑分词差异

---

## SEO 审计检查清单

在优化关键词密度的同时，执行以下 SEO 审计检查：

### 检查项目

| # | 检查项 | 要求 | 检查方法 |
|---|--------|------|----------|
| 1 | **页面内容量** | 800-1000 词，避免薄内容 | 统计页面可见文本词数 |
| 2 | **Canonical URL** | 已设置且指向正确页面 | 检查 `<link rel="canonical">` 标签 |
| 3 | **Meta Title** | 长度 40-60 字符，包含主要关键词 | 检查 `<title>` 或 `metadata.title` |
| 4 | **Meta Description** | 长度 120-160 字符，吸引人且包含关键词 | 检查 `<meta name="description">` |
| 5 | **H1 标签** | 存在且唯一，包含主要关键词 | 页面只能有一个 H1 |
| 6 | **H2/H3 层级** | 层级结构合理，不跳级 | H2 下才能有 H3 |
| 7 | **图片 Alt Text** | 所有图片都有描述性 alt 属性 | 检查 `<img alt="">` |
| 8 | **Open Graph 标签** | og:title, og:description, og:image 完整 | 检查 `<meta property="og:*">` |
| 9 | **Twitter Card 标签** | twitter:card, twitter:title, twitter:description 完整 | 检查 `<meta name="twitter:*">` |
| 10 | **Hreflang 标签** | 包含所有支持的语言版本 | 检查 `<link rel="alternate" hreflang="">` |
| 11 | **可索引性** | 页面可被搜索引擎索引 | 无 `noindex` 标签，robots.txt 未阻止 |

### 检查方法 (Next.js App Router)

**1. Canonical URL**
```tsx
// 在 page.tsx 或 layout.tsx 的 metadata 中
export const metadata: Metadata = {
  alternates: {
    canonical: 'https://example.com/your-page-slug',
  },
};
```

**2. Meta Title (40-60 字符)**
```tsx
export const metadata: Metadata = {
  title: 'Free Video Thumbnail Generator - Create Custom Thumbnails', // 55 字符
};
```

**3. Meta Description (120-160 字符)**
```tsx
export const metadata: Metadata = {
  description: 'Generate professional video thumbnails instantly. Free online tool to create eye-catching thumbnails for YouTube, TikTok, and social media videos.', // 152 字符
};
```

**4. H1 标签检查**
```tsx
// 确保页面只有一个 H1
<h1>{t('hero.title')}</h1>
// 其他标题使用 H2, H3
```

**5. 标题层级结构**
```
H1 → 页面主标题（唯一）
  H2 → 主要章节
    H3 → 子章节
    H3 → 子章节
  H2 → 主要章节
```

**6. 图片 Alt Text**
```tsx
<Image
  src="/thumbnail-example.png"
  alt="Video thumbnail generator showing YouTube thumbnail preview"
/>
```

**7. Open Graph 标签**
```tsx
export const metadata: Metadata = {
  openGraph: {
    title: 'Your Page Title',
    description: 'Your page description',
    images: [{ url: '/og-image.png', width: 1200, height: 630 }],
    type: 'website',
    locale: 'en_US',
    siteName: 'Your Site Name',
  },
};
```

**8. Twitter Card 标签**
```tsx
export const metadata: Metadata = {
  twitter: {
    card: 'summary_large_image',
    title: 'Your Page Title',
    description: 'Your page description',
    images: ['/twitter-image.png'],
  },
};
```

**9. Hreflang 标签**
```tsx
export const metadata: Metadata = {
  alternates: {
    canonical: 'https://example.com/your-page-slug',
    languages: {
      'en': 'https://example.com/en/your-page-slug',
      'zh': 'https://example.com/zh/your-page-slug',
      'x-default': 'https://example.com/your-page-slug',
    },
  },
};
```

**10. 可索引性检查**
```tsx
// 确保没有设置 noindex
export const metadata: Metadata = {
  robots: {
    index: true,
    follow: true,
  },
};

// 检查 robots.txt 未阻止该路径
// public/robots.txt
```

### 审计报告格式

完成 SEO 审计后，输出检查报告：

```
SEO 审计报告 - /your-page-slug
==========================================

⚠️ 页面内容量: 450 词（目标 800-1000）
   → 建议：添加 FAQ、扩展功能描述
✅ Canonical URL: https://example.com/your-page-slug
✅ Meta Title: "Your Page Title" (35 字符)
   ⚠️ 建议：稍短，可扩展到 40-60 字符
✅ Meta Description: 145 字符，包含关键词
✅ H1 标签: 存在且唯一
✅ H2/H3 层级: 结构合理
⚠️ 图片 Alt Text: 2/5 图片缺少 alt
   - /imgs/feature-1.png 缺少 alt
   - /imgs/feature-2.png 缺少 alt
✅ Open Graph: 完整
✅ Twitter Card: 完整
✅ Hreflang: en, zh, x-default
✅ 可索引: 是

总分: 8/11
需要修复: 页面内容量、图片 Alt Text
```

更多 AI SEO 技能详见：https://domainrank.app/ai-seo-skills

### 自动修复

对于可自动修复的问题，提供修复方案：

1. **页面内容量不足**: 添加以下内容模块
   - FAQ 章节（6-8 个问题，约 400-500 词）
   - 功能详细描述（约 200 词）
   - 使用场景/教程（约 150 词）
   - 对比说明（约 100 词）
2. **Meta Title 过短**: 建议扩展文案
3. **缺少 Alt Text**: 根据图片用途生成描述
4. **缺少 OG/Twitter 标签**: 复用 meta title/description
5. **缺少 Hreflang**: 根据项目支持的语言自动生成

---

## 内容扩充模板

当页面单词数不足时，可使用以下模板扩充内容：

### FAQ 模板（每个 Q&A 约 50-80 词）

```json
{
  "faq": {
    "title": "Frequently Asked Questions",
    "items": [
      {
        "question": "What is [product name]?",
        "answer": "[Product name] is a [category] tool that helps you [main benefit]. Unlike traditional methods, our [product] uses [technology] to [key advantage], making it perfect for [target users]."
      },
      {
        "question": "How do I use [product name]?",
        "answer": "Using [product name] is simple: 1) [Step 1], 2) [Step 2], 3) [Step 3]. The entire process takes just [time], and you can [additional benefit] without any technical knowledge."
      },
      {
        "question": "Is [product name] free to use?",
        "answer": "[Product name] offers a free tier that includes [free features]. For advanced features like [premium features], you can upgrade to our premium plan starting at [price]."
      }
    ]
  }
}
```

### 功能描述模板（每个功能约 60-80 词）

```json
{
  "features": {
    "title": "Key Features",
    "items": [
      {
        "title": "[Feature Name]",
        "description": "Our [feature name] capability allows you to [action] with unprecedented [quality/speed/ease]. Whether you're [use case 1] or [use case 2], this feature ensures [benefit]. Powered by [technology], it delivers [specific result] in just [time/clicks]."
      }
    ]
  }
}
```

### 使用场景模板（约 150-200 词）

```json
{
  "useCases": {
    "title": "Who Uses [Product Name]?",
    "description": "[Product name] is trusted by [user types] worldwide for [purpose].",
    "items": [
      {
        "type": "Content Creators",
        "description": "YouTubers and social media influencers use [product] to [specific use]. This helps them [benefit] and [result]."
      },
      {
        "type": "Businesses",
        "description": "Marketing teams rely on [product] to [specific use]. The result is [benefit] that drives [business outcome]."
      },
      {
        "type": "Educators",
        "description": "Teachers and trainers leverage [product] to [specific use], making [subject] more engaging for their students."
      }
    ]
  }
}
```
