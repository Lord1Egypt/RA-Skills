# Kitchen 厨房手帐 · 美食生活行业模板（theme-sunset）

> **行业**：美食生活（美食/探店/旅行/生活方式/温暖治愈/节庆）
> **设计语言**：对标 Bon Appétit / 食物杂志的手帐美学——图片优先、奶油暖底色、圆角、食谱卡结构（食材清单+步骤）、星级评分、营业信息卡。**版面以「食物感」为重心：圆、软、暖。**
> **与通用库的关系**：图片网格/GIF/代码块等仍用 [`common-components.md`](./common-components.md)，套用本表色值。
> **克制原则**：主色 `#ea580c` 只在锚点出现（全文 ≤5 处）；暖底色块点缀，正文仍是大面积白底＋灰阶。

---

## 一、设计变量速查表

| 变量 | 色值 | 用途 |
|------|------|------|
| 主色（陶橙） | `#ea580c` | 星级、步骤圆标、加粗锚点（≤5 处） |
| 蜂蜜色 | `#d97706` | 彩带、评分文字、装饰点 |
| 浅底色（奶油） | `#fff7ed` | 封面色带、食谱卡、信息卡背景 |
| 浅边框 | `#fed7aa` | 食谱卡边框、评分边框 |
| 高亮色 | `#fef3c7` | 黄底高亮起始色 |
| 高亮渐变终色 | `#fde68a` | 黄底高亮结束色 |
| 标题色 | `#1c1917` | 文章标题、章节标题、子标题 |
| 正文色 | `#44403c` | 正文段落 |
| 辅助文字色 | `#78716c` | 副标题、说明、日期 |
| 弱文字色 | `#a8a29e` | 元信息、图注（≥13px） |
| 分割线色 | `#e7e5e4` | 封面分隔、发丝线 |
| 下划线色 | `#fb923c` | 关键词下划线 |
| 深底白字背景 | `#ea580c` | CTA 按钮、步骤圆标 |
| 正文字体 | `-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif` | 正文 |

### Type Scale（本模板）

| 场景 | 字号 | 行高 |
|------|------|------|
| 封面色带标签 | 12px | 1.5 |
| 文章标题 | 24px | 1.4 |
| 章节标题 | 19px | 1.4 |
| 子标题 | 17px | 1.5 |
| 正文 | 16px | 1.9 |
| 食谱步骤 | 15px | 1.8 |
| 食材项 | 14px | 1.7 |
| 图注/元信息 | 13px | 1.6 |

---

## 二、各组件完整 HTML

### 1. 全局容器

```html
<section style="max-width:677px;margin:0 auto;padding:20px 16px;">
<!-- 文章内容 -->
</section>
```

### 2. 封面（图片优先 + 标题色带 + 元信息）

顶部为封面图占位，标题落在暖色带上，底部附评分与元信息。

```html
<section style="margin:0 0 28px;">
<section style="padding:28px 20px;background:#fff7ed;border-radius:14px 14px 0 0;">
<p style="margin:0 0 10px;line-height:1.5;font-size:12px;color:#d97706;letter-spacing:2px;"><span leaf="">探店 · 上海</span></p>
<p style="margin:0 0 12px;line-height:1.4;font-size:24px;font-weight:bold;color:#1c1917;"><span leaf="">一家开在梧桐区的小馆子</span></p>
<section style="display:flex;align-items:center;">
<p style="margin:0 10px 0 0;line-height:1.5;font-size:16px;color:#ea580c;letter-spacing:1px;"><span leaf="">★★★★★</span></p>
<p style="margin:0;line-height:1.5;font-size:13px;color:#78716c;"><span leaf="">4.8 分 · 人均 ¥120</span></p>
</section>
</section>
<section style="padding:20px;background:#fafaf9;border-radius:0 0 14px 14px;">
<section style="margin:0 0 14px;padding:28px 16px;background:#ffffff;border:2px dashed #d1d5db;border-radius:10px;text-align:center;">
<p style="margin:0;line-height:1.8;color:#9ca3af;font-size:14px;"><span leaf="">【插入图片：封面主图】</span></p>
</section>
<p style="margin:0;line-height:1.6;font-size:13px;color:#78716c;"><span leaf="">📅 2026.01.07 · 📍 梧桐区 · ⏱ 30 分钟读完</span></p>
</section>
</section>
```

### 3. 引言卡（暖底编辑手记）

```html
<section style="margin:0 0 24px;padding:18px 20px;background:#fff7ed;border-radius:10px;">
<p style="margin:0 0 8px;line-height:1.5;font-size:12px;color:#d97706;letter-spacing:2px;"><span leaf="">编辑手记 EDITOR'S NOTE</span></p>
<p style="margin:0;line-height:1.8;font-size:15px;color:#44403c;"><span leaf="">这是一段引言或导读文字，用暖底卡片突出文章的核心味道，让读者带着期待往下读。</span></p>
</section>
```

### 4. 目录（圆点列表）

```html
<section style="margin:0 0 28px;padding:20px 24px;background:#fafaf9;border-radius:12px;">
<p style="margin:0 0 14px;line-height:1.5;font-size:13px;font-weight:bold;color:#1c1917;"><span leaf="">这一篇，你会看到</span></p>
<section style="margin:0 0 12px;display:flex;align-items:flex-start;">
<section style="flex-shrink:0;width:8px;height:8px;background:#ea580c;border-radius:50%;margin:8px 12px 0 4px;"></section>
<p style="margin:0;line-height:1.6;font-size:15px;color:#44403c;"><span leaf="">招牌菜的前世今生</span></p>
</section>
<section style="margin:0 0 12px;display:flex;align-items:flex-start;">
<section style="flex-shrink:0;width:8px;height:8px;background:#ea580c;border-radius:50%;margin:8px 12px 0 4px;"></section>
<p style="margin:0;line-height:1.6;font-size:15px;color:#44403c;"><span leaf="">后厨的秘密配方</span></p>
</section>
<section style="margin:0;display:flex;align-items:flex-start;">
<section style="flex-shrink:0;width:8px;height:8px;background:#ea580c;border-radius:50%;margin:8px 12px 0 4px;"></section>
<p style="margin:0;line-height:1.6;font-size:15px;color:#44403c;"><span leaf="">值得专程跑一趟吗</span></p>
</section>
</section>
```

### 5. 章节标题（圆形序号徽章）

```html
<section style="margin:36px 0 16px;display:flex;align-items:center;">
<section style="flex-shrink:0;width:40px;height:40px;background:#ea580c;border-radius:50%;display:flex;align-items:center;justify-content:center;margin-right:14px;">
<p style="margin:0;line-height:1;font-size:17px;font-weight:bold;color:#ffffff;"><span leaf="">01</span></p>
</section>
<section>
<p style="margin:0 0 2px;line-height:1.3;font-size:19px;font-weight:bold;color:#1c1917;"><span leaf="">招牌菜的前世今生</span></p>
<p style="margin:0;line-height:1.4;font-size:12px;color:#d97706;letter-spacing:1px;"><span leaf="">SIGNATURE DISH</span></p>
</section>
</section>
```

### 6. 子标题（左竖条暖色）

```html
<section style="margin:24px 0 12px;padding-left:12px;border-left:3px solid #fb923c;">
<p style="margin:0;line-height:1.5;font-size:17px;font-weight:bold;color:#1c1917;"><span leaf="">子标题内容</span></p>
</section>
```

### 7. 正文段落

```html
<p style="margin:0 0 20px;line-height:1.9;font-size:16px;color:#44403c;"><span leaf="">这是标准正文段落，行高 1.9，字号 16px。每个段落之间保持 20px 间距，确保阅读舒适。</span></p>
```

### 8. 关键词下划线

```html
<span leaf="" style="border-bottom:2px solid #fb923c;">关键词</span>
```

段落内示例：

```html
<p style="margin:0 0 20px;line-height:1.9;font-size:16px;color:#44403c;"><span leaf="">这段话里有一个<span leaf="" style="border-bottom:2px solid #fb923c;">关键概念</span>需要读者注意。</span></p>
```

### 9. 加粗标记（锚点层，全文 ≤5 处）

```html
<span leaf="" style="color:#ea580c;font-weight:bold;">加粗文字</span>
```

### 10. 高亮标记

```html
<span leaf="" style="background:linear-gradient(to top,#fef3c7 0%,#fde68a 100%);padding:2px 4px;border-radius:3px;">高亮文字</span>
```

### 11. 荧光笔

```html
<span leaf="" style="background:linear-gradient(to top,#fef3c7 40%,transparent 40%);">荧光标记文字</span>
```

### 12. 引用块（暖底左竖条）

```html
<section style="margin:24px 0;padding:16px 20px;background:#fff7ed;border-left:3px solid #ea580c;border-radius:0 8px 8px 0;">
<p style="margin:0;line-height:1.8;font-size:15px;color:#44403c;"><span leaf="">引用块内容，用于强调重要观点或补充说明。</span></p>
</section>
```

### 13. 食谱卡（行业专属：食材清单 + 步骤）

```html
<section style="margin:28px 0;border:1px solid #fed7aa;border-radius:14px;overflow:hidden;">
<section style="padding:14px 20px;background:#fff7ed;border-bottom:1px solid #fed7aa;">
<p style="margin:0;line-height:1.5;font-size:14px;font-weight:bold;color:#1c1917;"><span leaf="">🍽 食材清单（2 人份）</span></p>
</section>
<section style="padding:14px 20px;display:flex;">
<section style="flex:1;">
<p style="margin:0 0 8px;line-height:1.7;font-size:14px;color:#44403c;"><span leaf="">○ 番茄 3 个</span></p>
<p style="margin:0 0 8px;line-height:1.7;font-size:14px;color:#44403c;"><span leaf="">○ 鸡蛋 2 枚</span></p>
<p style="margin:0 0 8px;line-height:1.7;font-size:14px;color:#44403c;"><span leaf="">○ 葱花 适量</span></p>
</section>
<section style="flex:1;">
<p style="margin:0 0 8px;line-height:1.7;font-size:14px;color:#44403c;"><span leaf="">○ 食用油 2 勺</span></p>
<p style="margin:0 0 8px;line-height:1.7;font-size:14px;color:#44403c;"><span leaf="">○ 盐 半勺</span></p>
<p style="margin:0 0 8px;line-height:1.7;font-size:14px;color:#44403c;"><span leaf="">○ 糖 1 小勺</span></p>
</section>
</section>
<section style="padding:14px 20px;background:#fafaf9;border-top:1px solid #fed7aa;">
<section style="margin:0 0 12px;display:flex;align-items:flex-start;">
<section style="flex-shrink:0;width:24px;height:24px;background:#ea580c;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:2px 10px 0 0;"><p style="margin:0;line-height:1;font-size:13px;color:#ffffff;font-weight:bold;"><span leaf="">1</span></p></section>
<p style="margin:0;line-height:1.8;font-size:15px;color:#44403c;"><span leaf="">番茄切块，鸡蛋打散加盐备用。</span></p>
</section>
<section style="margin:0 0 12px;display:flex;align-items:flex-start;">
<section style="flex-shrink:0;width:24px;height:24px;background:#ea580c;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:2px 10px 0 0;"><p style="margin:0;line-height:1;font-size:13px;color:#ffffff;font-weight:bold;"><span leaf="">2</span></p></section>
<p style="margin:0;line-height:1.8;font-size:15px;color:#44403c;"><span leaf="">热锅冷油，先炒蛋至凝固盛出。</span></p>
</section>
<section style="margin:0;display:flex;align-items:flex-start;">
<section style="flex-shrink:0;width:24px;height:24px;background:#ea580c;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:2px 10px 0 0;"><p style="margin:0;line-height:1;font-size:13px;color:#ffffff;font-weight:bold;"><span leaf="">3</span></p></section>
<p style="margin:0;line-height:1.8;font-size:15px;color:#44403c;"><span leaf="">下番茄炒出汁，回锅鸡蛋调味翻匀。</span></p>
</section>
</section>
</section>
```

### 14. 营业信息卡（行业专属：地址/营业时间/电话）

```html
<section style="margin:28px 0;padding:18px 20px;background:#fff7ed;border-radius:12px;">
<p style="margin:0 0 12px;line-height:1.5;font-size:13px;font-weight:bold;color:#ea580c;letter-spacing:1px;"><span leaf="">门店信息</span></p>
<section style="margin:0 0 8px;display:flex;">
<p style="margin:0 8px 0 0;line-height:1.7;font-size:14px;color:#78716c;"><span leaf="">📍</span></p>
<p style="margin:0;line-height:1.7;font-size:14px;color:#44403c;"><span leaf="">上海市徐汇区某某路 88 号</span></p>
</section>
<section style="margin:0 0 8px;display:flex;">
<p style="margin:0 8px 0 0;line-height:1.7;font-size:14px;color:#78716c;"><span leaf="">🕐</span></p>
<p style="margin:0;line-height:1.7;font-size:14px;color:#44403c;"><span leaf="">周一至周日 11:00 – 22:00</span></p>
</section>
<section style="margin:0;display:flex;">
<p style="margin:0 8px 0 0;line-height:1.7;font-size:14px;color:#78716c;"><span leaf="">📞</span></p>
<p style="margin:0;line-height:1.7;font-size:14px;color:#44403c;"><span leaf="">021-8888 8888（建议订位）</span></p>
</section>
</section>
```

### 15. 图片网格（双图/三图，带说明）

双图示例（三图同构，gap 6px、字号 11px）：

```html
<section style="margin:24px 0;display:flex;gap:8px;">
<section style="flex:1;">
<img src="图片1URL" style="width:100%;height:auto;display:block;border-radius:10px;" />
<p style="margin:6px 0 0;line-height:1.5;font-size:12px;color:#78716c;text-align:center;"><span leaf="">餐前小菜</span></p>
</section>
<section style="flex:1;">
<img src="图片2URL" style="width:100%;height:auto;display:block;border-radius:10px;" />
<p style="margin:6px 0 0;line-height:1.5;font-size:12px;color:#78716c;text-align:center;"><span leaf="">招牌主菜</span></p>
</section>
</section>
```

### 16. 数据卡（暖底大数字）

```html
<section style="margin:24px 0;padding:24px;background:#fff7ed;border-radius:12px;text-align:center;">
<p style="margin:0 0 6px;line-height:1;font-size:36px;font-weight:bold;color:#ea580c;"><span leaf="">4.8</span></p>
<p style="margin:0;line-height:1.6;font-size:14px;color:#78716c;"><span leaf="">大众点评评分 · 3268 条评价</span></p>
</section>
```

### 17. 分割线（暖色装饰点）

```html
<section style="margin:32px 0;display:flex;align-items:center;justify-content:center;">
<section style="width:60px;height:2px;background:#fb923c;border-radius:1px;"></section>
<section style="width:8px;height:8px;background:#ea580c;border-radius:50%;margin:0 8px;"></section>
<section style="width:60px;height:2px;background:#fb923c;border-radius:1px;"></section>
</section>
```

### 18. 作者签名区／CTA（暖色渐变装饰条）

```html
<section style="margin:40px 0 0;border-radius:14px;overflow:hidden;">
<section style="height:4px;background:linear-gradient(to right,#ea580c,#f59e0b);"></section>
<section style="padding:24px;background:#fff7ed;text-align:center;">
<p style="margin:0 0 8px;line-height:1.6;font-size:15px;color:#44403c;"><span leaf="">喜欢这篇探店，欢迎点赞、在看、转发</span></p>
<section style="display:inline-block;margin-top:12px;padding:8px 22px;background:#ea580c;border-radius:20px;">
<p style="margin:0;line-height:1.5;font-size:14px;font-weight:bold;color:#ffffff;"><span leaf="">{{作者名}}</span></p>
</section>
</section>
</section>
```

### 19. 产品徽章（暖色）

```html
<section style="display:inline-block;padding:3px 10px;background:#fff7ed;border:1px solid #fed7aa;border-radius:4px;">
<p style="margin:0;line-height:1.5;font-size:13px;color:#ea580c;font-weight:bold;"><span leaf="">菜品名</span></p>
</section>
```

---

## 三、完整文章模板骨架（Kitchen）

```
全局容器
 ├─ 封面（色带标题 + 评分 + 封面图占位 + 元信息）
 ├─ 引言卡（编辑手记）
 ├─ 目录（圆点列表）
 ├─ 〔 章节标题（圆形序号徽章）    ← 循环 N 次
 │    ├─ 子标题（左竖条暖色）
 │    ├─ 正文段落（下划线／加粗／高亮／荧光笔）
 │    ├─ 图片网格（按需）
 │    ├─ 引用块（按需）
 │    ├─ 食谱卡（按需，含步骤）
 │    └─ 营业信息卡（按需）〕
 ├─ 分割线
 └─ 作者签名区／CTA
```

---

## 四、文章类型 → 组件组合配方表

| 文章类型 | 核心组件组合 |
|---------|------------|
| 美食／探店 | 封面→编辑手记→目录→章节→图片网格→营业信息卡→签名 |
| 食谱／家常菜 | 封面→编辑手记→章节→正文→食谱卡（食材+步骤）→图片网格→签名 |
| 旅行／生活 | 封面→编辑手记→目录→章节→图片网格→引用块→数据卡→签名 |
| 节庆／温暖治愈 | 封面→编辑手记→章节→正文→高亮标记→分割线→CTA→签名 |

---

## 五、Markdown → 组件映射规则表

| Markdown 元素 | 映射组件 |
|--------------|---------|
| `# 标题` | 封面（暖色带 + 评分 + 元信息） |
| `> 引言（开头）` | 引言卡（编辑手记） |
| `## 标题` | 章节标题（圆形序号徽章 01/02/03，末章 `∞`） |
| `### 标题` | 子标题（左竖条暖色） |
| 正文段落 | 正文段落（每段主动加 1-3 个关键词下划线） |
| `**文字**` | 加粗标记（锚点层，全文 ≤5 处） |
| `==文字==` | 高亮标记 |
| `<u>文字</u>` | 关键词下划线 |
| `> 引用（非开头）` | 引用块（暖底左竖条） |
| `- 食材项`（含 ○ 或份量） | 食谱卡食材清单 |
| `1. 步骤`（步骤语义） | 食谱卡步骤（圆形编号） |
| `![说明](url)` | 图片网格（2-3 图横排带说明） |
| `---` | 分割线（暖色装饰点） |
| `` \| 表格 \| `` | 转为营业信息卡（地址/时间/电话）或通用表格 |
| `` `code` `` | 通用库行内代码（主色替换 `#ea580c`） |
| ` ``` 围栏 ``` ` | 通用库代码块（主色替换 `#ea580c`） |
