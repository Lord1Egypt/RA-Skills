# Campaign 大秀 · 时尚美妆行业模板（theme-rose）

> **行业**：时尚美妆（时尚/穿搭/美妆/节庆/促销/种草/品牌 Campaign）
> **设计语言**：对标时尚 Campaign / Lookbook 的秀场排版——超大标题、高对比色块、Look 编号、产品卡（图+名+价签）、画册网格、强 CTA 横幅。**版面以「冲击力」为重心：大、浓、自信。**
> **与通用库的关系**：代码块/图片等仍用 [`common-components.md`](./common-components.md)，套用本表色值。
> **克制原则**：主色 `#e11d48` 只在锚点出现（全文 ≤5 处）；黑/白/红三色主导，其他彩度一律不出现。

---

## 一、设计变量速查表

| 变量 | 色值 | 用途 |
|------|------|------|
| 主色（胭红） | `#e11d48` | Look 编号、价格、加粗锚点（≤5 处）、CTA |
| 主色深 | `#be123c` | CTA 横幅底、折扣标签 |
| 主色浅 | `#fb7185` | 标签、竖条、装饰点 |
| 浅底色（粉白） | `#fff1f2` | 产品卡背景、引言带 |
| 浅边框 | `#fecdd3` | 产品卡边框、规格行 |
| 黑色（墨） | `#18181b` | 超大标题、Look 编号、加粗文字 |
| 高亮色 | `#ffe4e6` | 粉底高亮起始色 |
| 高亮渐变终色 | `#fecdd3` | 粉底高亮结束色 |
| 标题色 | `#18181b` | 文章标题、章节标题、子标题 |
| 正文色 | `#44403c` | 正文段落 |
| 辅助文字色 | `#78716c` | 副标题、说明、日期 |
| 弱文字色 | `#a8a29e` | 元信息、图注（≥13px） |
| 分割线色 | `#e7e5e4` | 发丝线 |
| 下划线色 | `#fb7185` | 关键词下划线 |
| 深底白字背景 | `#be123c` | CTA 横幅、折扣标签 |
| 正文字体 | `-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif` | 正文 |

### Type Scale（本模板）

| 场景 | 字号 | 行高 |
|------|------|------|
| Campaign Kicker | 12px | 1.5 |
| 超大标题（Display） | 28px | 1.3 |
| Look 编号 | 30px | 1 |
| 章节标题 | 20px | 1.4 |
| 子标题 | 17px | 1.5 |
| 正文 | 16px | 1.9 |
| 产品名/价格 | 15px | 1.5 |
| 图注/元信息 | 12px | 1.6 |

---

## 二、各组件完整 HTML

### 1. 全局容器

```html
<section style="max-width:677px;margin:0 auto;padding:20px 16px;">
<!-- 文章内容 -->
</section>
```

### 2. Campaign 封面（超大标题 + 标语 + 色块条）

```html
<section style="margin:0 0 28px;">
<section style="padding:28px 20px 24px;background:#18181b;border-radius:16px 16px 0 0;">
<p style="margin:0 0 12px;line-height:1.5;font-size:12px;color:#fb7185;letter-spacing:3px;"><span leaf="">CAMPAIGN · SS26</span></p>
<p style="margin:0 0 14px;line-height:1.3;font-size:28px;font-weight:bold;color:#ffffff;"><span leaf="">新季第一眼</span></p>
<p style="margin:0;line-height:1.7;font-size:14px;color:#d4d4d8;"><span leaf="">大胆配色，大胆穿搭。这一季，把冲突穿在身上。</span></p>
</section>
<section style="height:6px;background:linear-gradient(to right,#e11d48,#fb7185);"></section>
<section style="padding:14px 20px;background:#fff1f2;border-radius:0 0 16px 16px;">
<p style="margin:0;line-height:1.5;font-size:13px;color:#44403c;"><span leaf="">📌 本期 6 件单品 · 3 套 Look · 点击收藏</span></p>
</section>
</section>
```

### 3. 引言带（高对比引言）

```html
<section style="margin:0 0 24px;padding:20px;background:#18181b;border-radius:12px;">
<p style="margin:0;line-height:1.8;font-size:15px;color:#ffffff;"><span leaf="">这一篇，我们不聊流行趋势，只聊怎么把「敢穿」变成日常。</span></p>
<p style="margin:10px 0 0;line-height:1.5;font-size:12px;color:#fb7185;letter-spacing:2px;"><span leaf="">—— EDITORIAL</span></p>
</section>
```

### 4. 目录（Look 清单）

```html
<section style="margin:0 0 28px;padding:20px 24px;background:#fafaf9;border-radius:12px;">
<p style="margin:0 0 14px;line-height:1.5;font-size:13px;font-weight:bold;color:#18181b;letter-spacing:2px;"><span leaf="">本期 LOOK</span></p>
<section style="margin:0 0 12px;display:flex;align-items:baseline;">
<p style="margin:0 12px 0 0;line-height:1;font-size:22px;font-weight:bold;color:#e11d48;"><span leaf="">01</span></p>
<p style="margin:0;line-height:1.6;font-size:15px;color:#44403c;"><span leaf="">通勤也敢穿的亮色西装</span></p>
</section>
<section style="margin:0 0 12px;display:flex;align-items:baseline;">
<p style="margin:0 12px 0 0;line-height:1;font-size:22px;font-weight:bold;color:#e11d48;"><span leaf="">02</span></p>
<p style="margin:0;line-height:1.6;font-size:15px;color:#44403c;"><span leaf="">一条裙子的三种场合</span></p>
</section>
<section style="margin:0;display:flex;align-items:baseline;">
<p style="margin:0 12px 0 0;line-height:1;font-size:22px;font-weight:bold;color:#e11d48;"><span leaf="">03</span></p>
<p style="margin:0;line-height:1.6;font-size:15px;color:#44403c;"><span leaf="">配饰是点睛之笔</span></p>
</section>
</section>
```

### 5. 章节标题（超大 Look 编号 + 标题）

```html
<section style="margin:36px 0 16px;display:flex;align-items:center;">
<p style="margin:0 14px 0 0;line-height:1;font-size:30px;font-weight:bold;color:#18181b;"><span leaf="">LOOK</span></p>
<p style="margin:0 14px 0 0;line-height:1;font-size:30px;font-weight:bold;color:#e11d48;"><span leaf="">01</span></p>
<section style="flex:1;height:2px;background:#fecdd3;"></section>
</section>
<p style="margin:8px 0 0;line-height:1.4;font-size:20px;font-weight:bold;color:#18181b;"><span leaf="">通勤也敢穿的亮色西装</span></p>
```

### 6. 子标题

```html
<section style="margin:24px 0 12px;padding-left:12px;border-left:3px solid #fb7185;">
<p style="margin:0;line-height:1.5;font-size:17px;font-weight:bold;color:#18181b;"><span leaf="">子标题内容</span></p>
</section>
```

### 7. 正文段落

```html
<p style="margin:0 0 20px;line-height:1.9;font-size:16px;color:#44403c;"><span leaf="">这是标准正文段落，行高 1.9，字号 16px。每个段落之间保持 20px 间距，确保阅读舒适。</span></p>
```

### 8. 关键词下划线

```html
<span leaf="" style="border-bottom:2px solid #fb7185;">关键词</span>
```

段落内示例：

```html
<p style="margin:0 0 20px;line-height:1.9;font-size:16px;color:#44403c;"><span leaf="">这段话里有一个<span leaf="" style="border-bottom:2px solid #fb7185;">关键概念</span>需要读者注意。</span></p>
```

### 9. 加粗标记（锚点层，全文 ≤5 处）

```html
<span leaf="" style="color:#e11d48;font-weight:bold;">加粗文字</span>
```

### 10. 高亮标记

```html
<span leaf="" style="background:linear-gradient(to top,#ffe4e6 0%,#fecdd3 100%);padding:2px 4px;border-radius:3px;">高亮文字</span>
```

### 11. 荧光笔

```html
<span leaf="" style="background:linear-gradient(to top,#ffe4e6 40%,transparent 40%);">荧光标记文字</span>
```

### 12. 引用块（左竖条粉白底）

```html
<section style="margin:24px 0;padding:16px 20px;background:#fff1f2;border-left:3px solid #e11d48;border-radius:0 8px 8px 0;">
<p style="margin:0;line-height:1.8;font-size:15px;color:#44403c;"><span leaf="">引用块内容，用于强调重要观点或补充说明。</span></p>
</section>
```

### 13. 产品卡（行业专属：图片 + 名称 + 价格标签）

```html
<section style="margin:24px 0;display:flex;flex-wrap:wrap;gap:12px;">
<section style="flex:1 1 40%;min-width:140px;padding:14px;background:#fff1f2;border-radius:12px;">
<img src="产品图URL" style="width:100%;height:auto;display:block;border-radius:8px;" />
<section style="margin-top:10px;display:flex;justify-content:space-between;align-items:center;">
<p style="margin:0;line-height:1.5;font-size:14px;font-weight:bold;color:#18181b;"><span leaf="">廓形西装</span></p>
<section style="padding:2px 8px;background:#e11d48;border-radius:8px;"><p style="margin:0;line-height:1.5;font-size:12px;color:#ffffff;font-weight:bold;"><span leaf="">¥899</span></p></section>
</section>
<p style="margin:6px 0 0;line-height:1.5;font-size:12px;color:#78716c;"><span leaf="">三色可选 · 现货</span></p>
</section>
<section style="flex:1 1 40%;min-width:140px;padding:14px;background:#fff1f2;border-radius:12px;">
<img src="产品图URL" style="width:100%;height:auto;display:block;border-radius:8px;" />
<section style="margin-top:10px;display:flex;justify-content:space-between;align-items:center;">
<p style="margin:0;line-height:1.5;font-size:14px;font-weight:bold;color:#18181b;"><span leaf="">缎面半裙</span></p>
<section style="padding:2px 8px;background:#e11d48;border-radius:8px;"><p style="margin:0;line-height:1.5;font-size:12px;color:#ffffff;font-weight:bold;"><span leaf="">¥459</span></p></section>
</section>
<p style="margin:6px 0 0;line-height:1.5;font-size:12px;color:#78716c;"><span leaf="">限时 9 折</span></p>
</section>
</section>
```

### 14. Lookbook 网格（行业专属：画册图网格）

```html
<section style="margin:24px 0;display:flex;gap:8px;">
<section style="flex:1;">
<img src="图片1URL" style="width:100%;height:auto;display:block;border-radius:10px;" />
<p style="margin:6px 0 0;line-height:1.5;font-size:12px;color:#78716c;text-align:center;"><span leaf="">Look 01 正面</span></p>
</section>
<section style="flex:1;">
<img src="图片2URL" style="width:100%;height:auto;display:block;border-radius:10px;" />
<p style="margin:6px 0 0;line-height:1.5;font-size:12px;color:#78716c;text-align:center;"><span leaf="">Look 01 背面</span></p>
</section>
<section style="flex:1;">
<img src="图片3URL" style="width:100%;height:auto;display:block;border-radius:10px;" />
<p style="margin:6px 0 0;line-height:1.5;font-size:12px;color:#78716c;text-align:center;"><span leaf="">Look 01 细节</span></p>
</section>
</section>
```

### 15. Details 规格行（行业专属：材质/尺码/色号）

```html
<section style="margin:24px 0;border-top:1px solid #fecdd3;">
<section style="display:flex;justify-content:space-between;padding:12px 4px;border-bottom:1px solid #fecdd3;">
<p style="margin:0;line-height:1.5;font-size:13px;color:#78716c;"><span leaf="">材质</span></p>
<p style="margin:0;line-height:1.5;font-size:13px;color:#18181b;"><span leaf="">70% 羊毛 · 30% 涤纶</span></p>
</section>
<section style="display:flex;justify-content:space-between;padding:12px 4px;border-bottom:1px solid #fecdd3;">
<p style="margin:0;line-height:1.5;font-size:13px;color:#78716c;"><span leaf="">尺码</span></p>
<p style="margin:0;line-height:1.5;font-size:13px;color:#18181b;"><span leaf="">XS – XL</span></p>
</section>
<section style="display:flex;justify-content:space-between;padding:12px 4px;">
<p style="margin:0;line-height:1.5;font-size:13px;color:#78716c;"><span leaf="">色号</span></p>
<p style="margin:0;line-height:1.5;font-size:13px;color:#18181b;"><span leaf="">雾粉 / 墨黑 / 象牙白</span></p>
</section>
</section>
```

### 16. 折扣横幅（高对比促销）

```html
<section style="margin:28px 0;padding:20px;background:#be123c;border-radius:12px;text-align:center;">
<p style="margin:0 0 8px;line-height:1.2;font-size:32px;font-weight:bold;color:#ffffff;"><span leaf="">−30%</span></p>
<p style="margin:0;line-height:1.6;font-size:14px;color:#ffe4e6;"><span leaf="">会员专享 · 本周末截止</span></p>
</section>
```

### 17. 数据卡（粉白底）

```html
<section style="margin:24px 0;padding:24px;background:#fff1f2;border-radius:12px;text-align:center;">
<p style="margin:0 0 6px;line-height:1;font-size:36px;font-weight:bold;color:#e11d48;"><span leaf="">12w+</span></p>
<p style="margin:0;line-height:1.6;font-size:14px;color:#78716c;"><span leaf="">本季 Lookbook 浏览</span></p>
</section>
```

### 18. 分割线（高对比三圆点）

```html
<section style="margin:32px 0;display:flex;align-items:center;justify-content:center;">
<section style="width:4px;height:4px;background:#fb7185;border-radius:50%;margin:0 4px;"></section>
<section style="width:8px;height:8px;background:#e11d48;border-radius:50%;margin:0 4px;"></section>
<section style="width:4px;height:4px;background:#fb7185;border-radius:50%;margin:0 4px;"></section>
</section>
```

### 19. 强 CTA 横幅（作者签名区，渐变底白字）

```html
<section style="margin:40px 0 0;padding:28px 24px;background:linear-gradient(135deg,#e11d48 0%,#be123c 100%);border-radius:14px;text-align:center;">
<p style="margin:0 0 8px;line-height:1.6;font-size:16px;font-weight:bold;color:#ffffff;"><span leaf="">喜欢这一季？</span></p>
<p style="margin:0 0 16px;line-height:1.6;font-size:14px;color:#ffe4e6;"><span leaf="">点击「在看」，下期出同款穿搭教程</span></p>
<section style="display:inline-block;padding:8px 24px;background:#ffffff;border-radius:20px;">
<p style="margin:0;line-height:1.5;font-size:14px;font-weight:bold;color:#be123c;"><span leaf="">{{作者名}}</span></p>
</section>
</section>
```

### 20. 产品徽章

```html
<section style="display:inline-block;padding:3px 10px;background:#fff1f2;border:1px solid #fecdd3;border-radius:4px;">
<p style="margin:0;line-height:1.5;font-size:13px;color:#e11d48;font-weight:bold;"><span leaf="">品牌名</span></p>
</section>
```

---

## 三、完整文章模板骨架（Campaign）

```
全局容器
 ├─ Campaign 封面（黑底超大标题 + 标语 + 渐变条 + 信息带）
 ├─ 引言带（高对比黑底）
 ├─ 目录（Look 清单）
 ├─ 〔 章节标题（LOOK 编号 + 发丝线）    ← 循环 N 次
 │    ├─ 子标题（左竖条）
 │    ├─ 正文段落（下划线／加粗／高亮／荧光笔）
 │    ├─ 产品卡（按需）
 │    ├─ Lookbook 网格（按需）
 │    ├─ Details 规格行（按需）
 │    ├─ 折扣横幅（按需）
 │    └─ 引用块（按需）〕
 ├─ 分割线
 └─ 强 CTA 横幅（签名区）
```

---

## 四、文章类型 → 组件组合配方表

| 文章类型 | 核心组件组合 |
|---------|------------|
| 时尚／穿搭 | 封面→引言带→LOOK 章节→Lookbook 网格→产品卡→Details→强 CTA→签名 |
| 美妆／测评 | 封面→引言带→目录→章节→产品卡→数据卡→Details→签名 |
| 节庆／促销 | 封面→引言带→折扣横幅→产品卡→强 CTA→签名 |
| 种草／新品发布 | 封面→引言带→LOOK 章节→产品卡→Lookbook→Details→强 CTA→签名 |

---

## 五、Markdown → 组件映射规则表

| Markdown 元素 | 映射组件 |
|--------------|---------|
| `# 标题` | Campaign 封面（黑底超大标题 + 标语） |
| `> 引言（开头）` | 引言带（黑底高对比） |
| `## 标题` | 章节标题（LOOK 01 编号 + 发丝线） |
| `### 标题` | 子标题（左竖条） |
| 正文段落 | 正文段落（每段主动加 1-3 个关键词下划线） |
| `**文字**` | 加粗标记（锚点层，全文 ≤5 处） |
| `==文字==` | 高亮标记 |
| `<u>文字</u>` | 关键词下划线 |
| `> 引用（非开头）` | 引用块（粉白底左竖条） |
| 产品/单品语义（名称+价格） | 产品卡（图 + 名 + 价签） |
| `![说明](url)` | Lookbook 网格（2-3 图横排） |
| 规格/参数行 | Details 规格行（材质/尺码/色号） |
| `---` | 分割线（高对比三圆点） |
| `` \| 表格 \| `` | 转为 Details 规格行或通用表格 |
| `` `code` `` | 通用库行内代码（主色替换 `#e11d48`） |
| ` ``` 围栏 ``` ` | 通用库代码块（主色替换 `#e11d48`） |
