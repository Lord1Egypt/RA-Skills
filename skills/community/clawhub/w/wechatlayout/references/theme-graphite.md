# Editorial 杂志 · 观点评论行业模板（theme-graphite）

> **行业**：观点评论（设计/科技评论/专业观点/深度分析/高端品牌/人文随笔）
> **设计语言**：对标 The New Yorker / Monocle 的杂志编辑排版——衬线大标题、居中报头（masthead）、罗马数字章节、大引号 Pull Quote、发丝线分隔、几乎无卡片、大量留白。**全篇几乎不用彩色，靠字重与灰阶建立层级。**
> **与通用库的关系**：代码块/图片等仍用 [`common-components.md`](./common-components.md)，主色替换为 `#374151`。
> **克制原则**：无彩色强调，仅灰阶（ink → 灰 → 发丝线）；文字承重，留白即装饰。

---

## 一、设计变量速查表

| 变量 | 色值 | 用途 |
|------|------|------|
| 主色（墨） | `#111827` | 标题、加粗锚点、Pull Quote 引号 |
| 主色浅 | `#374151` | 章节序号、左竖条引用 |
| 正文色 | `#4b5563` | 正文段落（衬线，阅读舒适） |
| 辅助文字色 | `#6b7280` | 报眉、byline、日期、图注 |
| 极弱灰 | `#9ca3af` | 罗马数字编号、装饰（仅大字号或非关键信息） |
| 浅底色 | `#f9fafb` | Standfirst 衬底、极少数块（近乎不可见） |
| 发丝线色 | `#e5e7eb` | 上下报眉线、章节分隔线 |
| 细分隔线 | `#f3f4f6` | 表格行线、签名区分隔 |
| 高亮色 | `#e5e7eb` | 灰底高亮（不用彩色） |
| 高亮渐变终色 | `#d1d5db` | 荧光笔渐变终色 |
| 下划线色 | `#9ca3af` | 关键词下划线 |
| 深底白字背景 | `#1f2937` | 深色引言底（极少用） |
| 衬线字体 | `Georgia,'Times New Roman','Songti SC','SimSun',serif` | 标题与正文 |
| 无衬线字体 | `-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC',sans-serif` | 报眉、小标签 |

### Type Scale（本模板）

| 场景 | 字号 | 行高 |
|------|------|------|
| 报眉 Kicker | 12px | 1.5 |
| 文章标题（衬线） | 26px | 1.4 |
| Standfirst 导语 | 17px | 1.9 |
| Pull Quote | 20px | 1.7 |
| 章节序号（罗马数字） | 15px | 1.5 |
| 章节标题 | 20px | 1.4 |
| 正文 | 16px | 1.9 |
| 图注/日期 | 13px | 1.6 |

---

## 二、各组件完整 HTML

### 1. 全局容器

```html
<section style="max-width:677px;margin:0 auto;padding:0 16px;">
<!-- 文章内容 -->
</section>
```

### 2. 报头（Masthead）——居中报眉 + 衬线大标题 + byline

```html
<section style="margin:40px 0 32px;text-align:center;">
<section style="margin:0 0 18px;border-top:1px solid #e5e7eb;border-bottom:1px solid #e5e7eb;padding:10px 0;">
<p style="margin:0;line-height:1.5;font-size:12px;color:#6b7280;letter-spacing:4px;"><span leaf="">DESIGN · REVIEW · 2026</span></p>
</section>
<p style="margin:0 0 16px;line-height:1.4;font-size:26px;font-weight:bold;color:#111827;letter-spacing:1px;font-family:Georgia,'Times New Roman','Songti SC','SimSun',serif;"><span leaf="">设计的克制，是一种能力</span></p>
<p style="margin:0;line-height:1.6;font-size:13px;color:#6b7280;"><span leaf="">文 / {{作者名}} · 2026.01.07</span></p>
</section>
```

### 3. Standfirst 导语段（衬线大号引文）

文章第一段使用更大字号的衬线导语，直接给出核心观点。

```html
<p style="margin:0 0 24px;line-height:1.9;font-size:17px;color:#111827;font-family:Georgia,'Times New Roman','Songti SC','SimSun',serif;"><span leaf="">真正的高级感来自克制：少用颜色、少用装饰、把力量留给文字本身。这是一段 Standfirst 导语，字号 17px，承托全文第一观点。</span></p>
```

### 4. 导读（罗马数字列表，无卡片）

```html
<section style="margin:32px 0;">
<section style="margin:0 0 14px;">
<p style="margin:0;line-height:1.5;font-size:12px;color:#6b7280;letter-spacing:3px;"><span leaf="">CONTENTS</span></p>
</section>
<section style="margin:0 0 12px;display:flex;align-items:baseline;border-bottom:1px solid #f3f4f6;padding-bottom:12px;">
<p style="margin:0 14px 0 0;line-height:1.5;font-size:14px;color:#9ca3af;font-family:Georgia,'Times New Roman',serif;"><span leaf="">I.</span></p>
<p style="margin:0;line-height:1.6;font-size:15px;color:#374151;"><span leaf="">为什么克制成为稀缺品</span></p>
</section>
<section style="margin:0 0 12px;display:flex;align-items:baseline;border-bottom:1px solid #f3f4f6;padding-bottom:12px;">
<p style="margin:0 14px 0 0;line-height:1.5;font-size:14px;color:#9ca3af;font-family:Georgia,'Times New Roman',serif;"><span leaf="">II.</span></p>
<p style="margin:0;line-height:1.6;font-size:15px;color:#374151;"><span leaf="">减法设计的三个抓手</span></p>
</section>
<section style="margin:0;display:flex;align-items:baseline;">
<p style="margin:0 14px 0 0;line-height:1.5;font-size:14px;color:#9ca3af;font-family:Georgia,'Times New Roman',serif;"><span leaf="">III.</span></p>
<p style="margin:0;line-height:1.6;font-size:15px;color:#374151;"><span leaf="">把留白当作预算</span></p>
</section>
</section>
```

### 5. 章节标题（罗马数字 + 发丝线）

```html
<section style="margin:44px 0 18px;border-top:1px solid #e5e7eb;padding-top:20px;">
<section style="margin:0 0 8px;display:flex;align-items:baseline;">
<p style="margin:0 12px 0 0;line-height:1.5;font-size:15px;color:#9ca3af;font-family:Georgia,'Times New Roman',serif;letter-spacing:1px;"><span leaf="">I.</span></p>
<p style="margin:0;line-height:1.4;font-size:20px;font-weight:bold;color:#111827;letter-spacing:0.5px;font-family:Georgia,'Times New Roman','Songti SC','SimSun',serif;"><span leaf="">为什么克制成为稀缺品</span></p>
</section>
</section>
```

### 6. 子标题（衬线加粗，无竖条）

```html
<section style="margin:28px 0 12px;">
<p style="margin:0;line-height:1.5;font-size:17px;font-weight:bold;color:#111827;font-family:Georgia,'Times New Roman','Songti SC','SimSun',serif;"><span leaf="">子标题文字</span></p>
</section>
```

### 7. 正文段落（衬线）

```html
<p style="margin:0 0 22px;line-height:1.9;font-size:16px;color:#4b5563;font-family:Georgia,'Times New Roman','Songti SC','SimSun',serif;"><span leaf="">这是标准正文段落，衬线字体、行距宽裕，文字自身承重。每个段落之间保持充足留白，让阅读节奏舒缓而不紧迫。</span></p>
```

### 8. 关键词下划线（灰）

```html
<span leaf="" style="border-bottom:2px solid #9ca3af;padding-bottom:1px;">关键词</span>
```

段落内示例：

```html
<p style="margin:0 0 22px;line-height:1.9;font-size:16px;color:#4b5563;font-family:Georgia,'Times New Roman','Songti SC','SimSun',serif;"><span leaf="">这段话里有一个<span leaf="" style="border-bottom:2px solid #9ca3af;padding-bottom:1px;">关键概念</span>值得读者停顿一下。</span></p>
```

### 9. 加粗标记（墨色，锚点层全文 ≤5 处）

```html
<span leaf="" style="color:#111827;font-weight:bold;">加粗文字</span>
```

### 10. 高亮标记（灰底）

```html
<span leaf="" style="background:#e5e7eb;color:#374151;padding:2px 4px;border-radius:2px;">高亮文字</span>
```

### 11. 荧光笔（灰渐变）

```html
<span leaf="" style="background:linear-gradient(180deg,transparent 55%,#d1d5db 55%);padding:0 2px;">荧光标记</span>
```

### 12. 引用块（发丝线左竖条，斜体）

```html
<section style="margin:28px 0;padding:10px 0 10px 20px;border-left:2px solid #e5e7eb;">
<p style="margin:0;line-height:1.9;font-size:15px;color:#6b7280;font-style:italic;font-family:Georgia,'Times New Roman','Songti SC','SimSun',serif;"><span leaf="">这是一段引用文字，左竖条用发丝线，文字用辅助灰与斜体，保持杂志式的克制。</span></p>
</section>
```

### 13. Pull Quote 大引号（行业专属，居中衬线大字）

用于段落之间插入的金句，全篇 ≤2 处。

```html
<section style="margin:36px 0;padding:24px 20px;text-align:center;">
<p style="margin:0 0 14px;line-height:1;font-size:56px;color:#9ca3af;font-family:Georgia,'Times New Roman',serif;"><span leaf="">"</span></p>
<p style="margin:0;line-height:1.7;font-size:20px;font-weight:bold;color:#111827;font-family:Georgia,'Times New Roman','Songti SC','SimSun',serif;"><span leaf="">少即是多，但更重要的是：少得有道理。</span></p>
<section style="margin:14px auto 0;width:32px;height:1px;background:#e5e7eb;"></section>
<p style="margin:10px 0 0;line-height:1.5;font-size:12px;color:#6b7280;letter-spacing:2px;"><span leaf="">—— 编者按</span></p>
</section>
```

### 14. 数据卡（灰阶极简）

```html
<section style="margin:32px 0;text-align:center;padding:28px 20px;border-top:1px solid #e5e7eb;border-bottom:1px solid #e5e7eb;">
<p style="margin:0;line-height:1;font-size:38px;font-weight:bold;color:#111827;letter-spacing:1px;font-family:Georgia,'Times New Roman',serif;"><span leaf="">98%</span></p>
<p style="margin:14px 0 0;line-height:1.6;font-size:14px;color:#6b7280;"><span leaf="">数据说明文字</span></p>
</section>
```

### 15. 表格（发丝线表格，无底色表头）

```html
<section style="margin:28px 0;">
<section style="display:flex;padding:12px 16px;border-bottom:1px solid #374151;">
<p style="margin:0;flex:1;line-height:1.5;font-size:14px;font-weight:bold;color:#111827;"><span leaf="">列标题 A</span></p>
<p style="margin:0;flex:1;line-height:1.5;font-size:14px;font-weight:bold;color:#111827;"><span leaf="">列标题 B</span></p>
</section>
<section style="display:flex;padding:12px 16px;border-bottom:1px solid #f3f4f6;">
<p style="margin:0;flex:1;line-height:1.5;font-size:14px;color:#4b5563;"><span leaf="">内容 A1</span></p>
<p style="margin:0;flex:1;line-height:1.5;font-size:14px;color:#4b5563;"><span leaf="">内容 B1</span></p>
</section>
<section style="display:flex;padding:12px 16px;">
<p style="margin:0;flex:1;line-height:1.5;font-size:14px;color:#4b5563;"><span leaf="">内容 A2</span></p>
<p style="margin:0;flex:1;line-height:1.5;font-size:14px;color:#4b5563;"><span leaf="">内容 B2</span></p>
</section>
</section>
```

### 16. 分割线（居中菱形）

```html
<section style="margin:40px auto;width:24px;display:flex;align-items:center;justify-content:center;">
<p style="margin:0;line-height:1;font-size:12px;color:#9ca3af;"><span leaf="">◆</span></p>
</section>
```

### 17. 结语（无卡片，纯文字收束）

```html
<p style="margin:36px 0 0;line-height:1.9;font-size:16px;color:#111827;font-family:Georgia,'Times New Roman','Songti SC','SimSun',serif;"><span leaf="">结尾用一个短段落收束全文观点，不加装饰、不设按钮——让最后一句话自己停留。</span></p>
```

### 18. 作者签名区（发丝线上分隔）

```html
<section style="margin:44px 0 0;padding:24px 0 0;border-top:1px solid #e5e7eb;text-align:center;">
<p style="margin:0 0 8px;line-height:1.6;font-size:14px;color:#6b7280;"><span leaf="">— 本文作者：{{作者名}} —</span></p>
<p style="margin:0;line-height:1.6;font-size:13px;color:#9ca3af;"><span leaf="">关注我们，获取更多深度内容</span></p>
</section>
```

---

## 三、完整文章模板骨架（Editorial）

```
全局容器
 ├─ 报头（居中报眉 + 衬线大标题 + byline）
 ├─ Standfirst 导语段
 ├─ 导读（罗马数字列表）
 ├─ 〔 章节标题（罗马数字 + 发丝线）    ← 循环 N 次
 │    ├─ 子标题（衬线加粗）
 │    ├─ 正文段落（下划线／加粗／高亮／荧光笔）
 │    ├─ 引用块（按需）
 │    ├─ Pull Quote 大引号（按需，全文 ≤2 处）
 │    ├─ 数据卡（按需）
 │    └─ 表格（按需）〕
 ├─ 分割线
 ├─ 结语段
 └─ 作者签名区
```

> 本模板**不出现彩色**、不用卡片；任何组件都优先考虑「能否用文字层级+发丝线完成」。

---

## 四、文章类型 → 组件组合配方表

| 文章类型 | 核心组件组合 |
|---------|-------------|
| 设计/科技评论 | 报头→Standfirst→章节（罗马数字）→正文→引用块→Pull Quote→结语→签名 |
| 专业观点/深度分析 | 报头→导读→章节→正文→数据卡→Pull Quote→结语→签名 |
| 高端品牌/案例复盘 | 报头→导读→章节→正文→数据卡→表格→Pull Quote→签名 |
| 禅意/极简随笔 | 报头→Standfirst→章节→正文→分割线→结语→签名（最少组件） |

---

## 五、Markdown → 组件映射规则表

| Markdown 元素 | 映射组件 |
|--------------|---------|
| `# 标题` | 报头（居中衬线标题 + byline） |
| `> 引言（开头）` | Standfirst 导语段（衬线大号） |
| `## 标题` | 章节标题（罗马数字 I./II./III. + 发丝线） |
| `### 标题` | 子标题（衬线加粗，无竖条） |
| 正文段落 | 正文段落（衬线，每段 1-3 个灰下划线） |
| `**文字**` | 加粗标记（墨色，锚点层 ≤5 处） |
| `==文字==` | 高亮标记（灰底） |
| `<u>文字</u>` | 关键词下划线（灰） |
| `> 引用（非开头）` | 引用块（发丝线左竖条 + 斜体） |
| `---` | 分割线（居中菱形） |
| `` \| 表格 \| `` | 表格（发丝线） |
| `- 项` / `1. 项` | 转为带缩进的正文段落（无序列表前缀「·」） |
| `` `code` `` | 通用库行内代码（主色替换 `#374151`） |
| ` ``` 围栏 ``` ` | 通用库代码块（主色替换 `#374151`） |
| `![说明](url)` | 通用库图片组件（说明用灰斜体） |
