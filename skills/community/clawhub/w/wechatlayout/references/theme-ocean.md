# Report 研报 · 企业金融行业模板（theme-ocean）

> **行业**：企业金融（企业/产品发布/行业分析/金融/商业案例/数据报告）
> **设计语言**：对标 Bloomberg / FT / McKinsey 的研报排版——报告式页眉（编号+部门+日期）、执行摘要框、KPI 进度条、斑马纹数据表、分析师注、免责声明。**版面以「数据可信」为重心：结构化、表格化、信息密度高但秩序井然。**
> **与通用库的关系**：代码块/图片等仍用 [`common-components.md`](./common-components.md)，套用本表色值。
> **克制原则**：主色 `#2563eb` 只在锚点出现（全文 ≤5 处）；大面积白底＋蓝灰阶，彩色只做点缀。

---

## 一、设计变量速查表

| 变量 | 色值 | 用途 |
|------|------|------|
| 主色（皇家蓝） | `#2563eb` | KPI 数值、进度条、加粗锚点（≤5 处） |
| 主色深 | `#1e40af` | 深底表头、CTA、执行摘要标题条 |
| 主色浅 | `#60a5fa` | 英文标签、进度条底色 |
| 浅底色 | `#eff6ff` | 执行摘要、KPI 卡、分析师注背景 |
| 浅边框 | `#bfdbfe` | 表格边框、KPI 卡边框 |
| 高亮色 | `#dbeafe` | 蓝底高亮起始色 |
| 高亮渐变终色 | `#bfdbfe` | 蓝底高亮结束色 |
| 标题色 | `#0f172a` | 文章标题、章节标题、子标题 |
| 正文色 | `#334155` | 正文段落 |
| 辅助文字色 | `#475569` | 副标题、说明、日期 |
| 弱文字色 | `#64748b` | 元信息、图注（≥13px） |
| 分割线色 | `#e2e8f0` | 报告页眉线、表格行线 |
| 下划线色 | `#93c5fd` | 关键词下划线 |
| 深底白字背景 | `#1e40af` | 表头、CTA、进度条 |
| 等宽字体 | `'SF Mono','Consolas','Menlo',monospace` | 报告编号、数据 |
| 正文字体 | `-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif` | 正文 |

### Type Scale（本模板）

| 场景 | 字号 | 行高 |
|------|------|------|
| 报告编号（等宽） | 12px | 1.5 |
| 报告标题 | 24px | 1.4 |
| 章节标题 | 19px | 1.4 |
| 子标题 | 17px | 1.5 |
| 正文 | 16px | 1.9 |
| KPI 数值 | 28px | 1.2 |
| 表格文字 | 14px | 1.5 |
| 图注/脚注 | 12px | 1.6 |

---

## 二、各组件完整 HTML

### 1. 全局容器

```html
<section style="max-width:677px;margin:0 auto;padding:20px 16px;">
<!-- 文章内容 -->
</section>
```

### 2. 报告页眉（编号 + 部门 + 日期 + 标题）

```html
<section style="margin:0 0 24px;">
<section style="display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid #1e40af;padding:0 0 10px;margin-bottom:16px;">
<p style="margin:0;line-height:1.5;font-size:12px;color:#2563eb;letter-spacing:1px;font-family:'SF Mono','Consolas','Menlo',monospace;"><span leaf="">RPT-2026-007</span></p>
<p style="margin:0;line-height:1.5;font-size:12px;color:#64748b;"><span leaf="">行业研究部 · 2026.01.07</span></p>
</section>
<p style="margin:0 0 12px;line-height:1.4;font-size:24px;font-weight:bold;color:#0f172a;"><span leaf="">2026 内容行业趋势研报</span></p>
<section style="display:flex;flex-wrap:wrap;">
<section style="margin:0 12px 6px 0;padding:2px 10px;background:#eff6ff;border-radius:10px;"><p style="margin:0;line-height:1.5;font-size:12px;color:#2563eb;font-weight:bold;"><span leaf="">行业洞察</span></p></section>
<section style="margin:0 12px 6px 0;padding:2px 10px;background:#f1f5f9;border-radius:10px;"><p style="margin:0;line-height:1.5;font-size:12px;color:#475569;"><span leaf="">数据驱动</span></p></section>
<section style="margin:0;padding:2px 10px;background:#f1f5f9;border-radius:10px;"><p style="margin:0;line-height:1.5;font-size:12px;color:#475569;"><span leaf="">12 页报告</span></p></section>
</section>
</section>
```

### 3. 执行摘要（Exec Summary）

```html
<section style="margin:0 0 28px;border:1px solid #bfdbfe;border-radius:8px;overflow:hidden;">
<section style="padding:10px 18px;background:#1e40af;">
<p style="margin:0;line-height:1.5;font-size:12px;font-weight:bold;color:#ffffff;letter-spacing:2px;"><span leaf="">EXECUTIVE SUMMARY · 执行摘要</span></p>
</section>
<section style="padding:16px 18px;background:#eff6ff;">
<p style="margin:0 0 8px;line-height:1.8;font-size:15px;color:#334155;"><span leaf="">核心结论一：行业增速保持两位数，头部集中度进一步提升。</span></p>
<p style="margin:0 0 8px;line-height:1.8;font-size:15px;color:#334155;"><span leaf="">核心结论二：AI 工具渗透率从 12% 升至 34%，成为最大变量。</span></p>
<p style="margin:0;line-height:1.8;font-size:15px;color:#334155;"><span leaf="">核心结论三：建议关注内容效率与合规成本两条主线。</span></p>
</section>
</section>
```

### 4. KPI 指标行（数字 + 涨跌）

```html
<section style="margin:0 0 28px;display:flex;border:1px solid #bfdbfe;border-radius:8px;overflow:hidden;">
<section style="flex:1;padding:16px 12px;text-align:center;border-right:1px solid #bfdbfe;">
<p style="margin:0 0 6px;line-height:1.2;font-size:28px;font-weight:bold;color:#2563eb;"><span leaf="">+32%</span></p>
<p style="margin:0;line-height:1.5;font-size:12px;color:#64748b;"><span leaf="">AI 渗透率</span></p>
</section>
<section style="flex:1;padding:16px 12px;text-align:center;border-right:1px solid #bfdbfe;">
<p style="margin:0 0 6px;line-height:1.2;font-size:28px;font-weight:bold;color:#2563eb;"><span leaf="">2.4亿</span></p>
<p style="margin:0;line-height:1.5;font-size:12px;color:#64748b;"><span leaf="">月活创作者</span></p>
</section>
<section style="flex:1;padding:16px 12px;text-align:center;">
<p style="margin:0 0 6px;line-height:1.2;font-size:28px;font-weight:bold;color:#2563eb;"><span leaf="">¥8.1w</span></p>
<p style="margin:0;line-height:1.5;font-size:12px;color:#64748b;"><span leaf="">头部账号年收入</span></p>
</section>
</section>
```

### 5. 进度条（KPI Progress Bar）

```html
<section style="margin:24px 0;">
<section style="margin:0 0 6px;display:flex;justify-content:space-between;">
<p style="margin:0;line-height:1.5;font-size:14px;color:#334155;"><span leaf="">AI 工具渗透率</span></p>
<p style="margin:0;line-height:1.5;font-size:14px;font-weight:bold;color:#2563eb;"><span leaf="">34%</span></p>
</section>
<section style="height:8px;background:#dbeafe;border-radius:4px;">
<section style="width:34%;height:8px;background:#2563eb;border-radius:4px;"></section>
</section>
</section>
```

> 多条进度条纵向排列，各自独立 `<section>`；数值可加同比箭头（↑/↓ 全角箭头或文字）。

### 6. 章节标题（小节编号 + 发丝线）

```html
<section style="margin:36px 0 16px;border-top:1px solid #e2e8f0;padding-top:16px;">
<section style="display:flex;align-items:baseline;">
<p style="margin:0 12px 0 0;line-height:1;font-size:16px;font-weight:bold;color:#60a5fa;font-family:'SF Mono','Consolas','Menlo',monospace;"><span leaf="">01</span></p>
<p style="margin:0;line-height:1.4;font-size:19px;font-weight:bold;color:#0f172a;"><span leaf="">市场概况</span></p>
</section>
</section>
```

### 7. 子标题

```html
<section style="margin:24px 0 12px;padding-left:12px;border-left:3px solid #60a5fa;">
<p style="margin:0;line-height:1.5;font-size:17px;font-weight:bold;color:#0f172a;"><span leaf="">子标题内容</span></p>
</section>
```

### 8. 正文段落

```html
<p style="margin:0 0 20px;line-height:1.9;font-size:16px;color:#334155;"><span leaf="">这是标准正文段落，行高 1.9，字号 16px。每个段落之间保持 20px 间距，确保阅读舒适。</span></p>
```

### 9. 关键词下划线

```html
<span leaf="" style="border-bottom:2px solid #93c5fd;">关键词</span>
```

段落内示例：

```html
<p style="margin:0 0 20px;line-height:1.9;font-size:16px;color:#334155;"><span leaf="">这段话里有一个<span leaf="" style="border-bottom:2px solid #93c5fd;">关键概念</span>需要读者注意。</span></p>
```

### 10. 加粗标记（锚点层，全文 ≤5 处）

```html
<span leaf="" style="color:#2563eb;font-weight:bold;">加粗文字</span>
```

### 11. 高亮标记

```html
<span leaf="" style="background:linear-gradient(to top,#dbeafe 0%,#bfdbfe 100%);padding:2px 4px;border-radius:3px;">高亮文字</span>
```

### 12. 荧光笔

```html
<span leaf="" style="background:linear-gradient(to top,#dbeafe 40%,transparent 40%);">荧光标记文字</span>
```

### 13. 分析师注（Analyst Note，左竖条浅底）

```html
<section style="margin:24px 0;padding:14px 18px;background:#eff6ff;border-left:3px solid #2563eb;border-radius:0 6px 6px 0;">
<p style="margin:0 0 6px;line-height:1.5;font-size:12px;color:#2563eb;letter-spacing:1px;"><span leaf="">分析师注</span></p>
<p style="margin:0;line-height:1.8;font-size:15px;color:#334155;"><span leaf="">引用块内容，用于补充数据口径、提示风险或给出判断依据。</span></p>
</section>
```

### 14. 数据表（斑马纹 + 深底表头）

```html
<section style="margin:24px 0;border:1px solid #bfdbfe;border-radius:8px;overflow:hidden;">
<section style="display:flex;background:#1e40af;">
<section style="flex:1;padding:12px 16px;"><p style="margin:0;line-height:1.5;font-size:14px;font-weight:bold;color:#ffffff;"><span leaf="">指标</span></p></section>
<section style="flex:1;padding:12px 16px;"><p style="margin:0;line-height:1.5;font-size:14px;font-weight:bold;color:#ffffff;"><span leaf="">2025</span></p></section>
<section style="flex:1;padding:12px 16px;"><p style="margin:0;line-height:1.5;font-size:14px;font-weight:bold;color:#ffffff;"><span leaf="">2026E</span></p></section>
</section>
<section style="display:flex;background:#eff6ff;">
<section style="flex:1;padding:12px 16px;"><p style="margin:0;line-height:1.5;font-size:14px;color:#334155;"><span leaf="">市场规模</span></p></section>
<section style="flex:1;padding:12px 16px;"><p style="margin:0;line-height:1.5;font-size:14px;color:#334155;"><span leaf="">¥2.1 万亿</span></p></section>
<section style="flex:1;padding:12px 16px;"><p style="margin:0;line-height:1.5;font-size:14px;color:#334155;"><span leaf="">¥2.8 万亿</span></p></section>
</section>
<section style="display:flex;">
<section style="flex:1;padding:12px 16px;"><p style="margin:0;line-height:1.5;font-size:14px;color:#334155;"><span leaf="">渗透率</span></p></section>
<section style="flex:1;padding:12px 16px;"><p style="margin:0;line-height:1.5;font-size:14px;color:#334155;"><span leaf="">12%</span></p></section>
<section style="flex:1;padding:12px 16px;"><p style="margin:0;line-height:1.5;font-size:14px;color:#334155;"><span leaf="">34%</span></p></section>
</section>
</section>
```

### 15. 对比结论框（Conclusion Box）

```html
<section style="margin:32px 0 0;padding:20px;background:#eff6ff;border-radius:8px;">
<p style="margin:0 0 10px;line-height:1.5;font-size:12px;font-weight:bold;color:#2563eb;letter-spacing:2px;"><span leaf="">CONCLUSION · 结论</span></p>
<p style="margin:0;line-height:1.9;font-size:16px;color:#0f172a;"><span leaf="">综合来看，行业处于加速分化期，把握 AI 工具红利与合规底线的企业将获得结构性优势。</span></p>
</section>
```

### 16. 分割线（浅色短线）

```html
<section style="margin:32px 0;height:1px;background:#e2e8f0;"></section>
```

### 17. 脚注 / 数据来源（等宽小字）

```html
<section style="margin:24px 0;padding-top:12px;border-top:1px solid #e2e8f0;">
<p style="margin:0 0 4px;line-height:1.6;font-size:12px;color:#64748b;"><span leaf="">数据来源：行业白皮书、上市公司年报、抽样调研（n=1,286）。</span></p>
<p style="margin:0;line-height:1.6;font-size:12px;color:#64748b;"><span leaf="">口径说明：渗透率按月活跃设备计算；2026E 为预测值。</span></p>
</section>
```

### 18. 作者签名区／CTA

```html
<section style="margin:40px 0 0;padding:24px;background:#eff6ff;border-left:4px solid #2563eb;border-radius:0 8px 8px 0;text-align:center;">
<p style="margin:0 0 8px;line-height:1.6;font-size:15px;color:#334155;"><span leaf="">本报告由 {{作者名}} 团队撰写</span></p>
<p style="margin:0 0 16px;line-height:1.6;font-size:15px;color:#334155;"><span leaf="">如需完整数据底稿，欢迎留言获取</span></p>
<section style="display:inline-block;padding:6px 20px;background:#2563eb;border-radius:20px;">
<p style="margin:0;line-height:1.5;font-size:14px;font-weight:bold;color:#ffffff;"><span leaf="">{{作者名}}</span></p>
</section>
</section>
```

### 19. 产品徽章

```html
<section style="display:inline-block;padding:3px 10px;background:#eff6ff;border:1px solid #bfdbfe;border-radius:4px;">
<p style="margin:0;line-height:1.5;font-size:13px;color:#2563eb;font-weight:bold;"><span leaf="">产品名</span></p>
</section>
```

---

## 三、完整文章模板骨架（Report）

```
全局容器
 ├─ 报告页眉（编号 + 部门 + 日期 + 标签）
 ├─ 执行摘要
 ├─ KPI 指标行
 ├─ 〔 章节标题（小节编号 + 发丝线）    ← 循环 N 次
 │    ├─ 子标题（左竖条）
 │    ├─ 正文段落（下划线／加粗／高亮／荧光笔）
 │    ├─ 进度条（按需）
 │    ├─ 分析师注（按需）
 │    ├─ 数据表（按需）
 │    └─ 对比结论框（按需）〕
 ├─ 分割线
 ├─ 脚注 / 数据来源
 └─ 作者签名区／CTA
```

---

## 四、文章类型 → 组件组合配方表

| 文章类型 | 核心组件组合 |
|---------|------------|
| 企业／产品发布 | 页眉→执行摘要→KPI→章节→数据表→产品徽章→CTA→签名 |
| 行业／科技分析 | 页眉→执行摘要→KPI→章节→进度条→分析师注→结论框→脚注→签名 |
| 金融／数据报告 | 页眉→执行摘要→KPI→数据表→进度条→脚注→签名 |
| 商业／案例研究 | 页眉→执行摘要→章节→正文→数据表→分析师注→结论框→签名 |

---

## 五、Markdown → 组件映射规则表

| Markdown 元素 | 映射组件 |
|--------------|---------|
| `# 标题` | 报告页眉（等宽编号 + 部门 + 日期 + 标签） |
| `> 引言（开头）` | 执行摘要（EXECUTIVE SUMMARY） |
| `## 标题` | 章节标题（等宽编号 01/02/03 + 发丝线） |
| `### 标题` | 子标题（左竖条） |
| 正文段落 | 正文段落（每段主动加 1-3 个关键词下划线） |
| `**文字**` | 加粗标记（锚点层，全文 ≤5 处） |
| `==文字==` | 高亮标记 |
| `<u>文字</u>` | 关键词下划线 |
| `> 引用（非开头）` | 分析师注 |
| `` \| 表格 \| `` | 数据表（斑马纹 + 深底表头） |
| `- 项` / `1. 项` | 转为带缩进的正文段落（无序列表前缀「·」） |
| 数值 + 百分比语义 | 进度条 / KPI 指标行 |
| `` `code` `` | 通用库行内代码（主色替换 `#2563eb`） |
| ` ``` 围栏 ``` ` | 通用库代码块（主色替换 `#2563eb`） |
| `![说明](url)` | 通用库图片组件（有说明文字才加说明） |
