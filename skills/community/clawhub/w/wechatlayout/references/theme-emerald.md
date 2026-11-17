# Blueprint 蓝图 · 科技知识行业模板（theme-emerald）

> **行业**：科技知识（教程/测评/清单/工具盘点/数据复盘/产品发布）
> **设计语言**：对标 Linear / Stripe / Raycast 的产品文档美学——等宽字体点缀、左对齐、连接线步骤时间轴、信息密度高、克制单色。
> **与通用库的关系**：本模板自带正文骨架与行业专属组件（步骤连接线/清单核对框/API 参数表/关键要点框）；代码块/图片/GIF 等仍用 [`common-components.md`](./common-components.md)，套用本表色值。
> **克制原则**：主色 `#059669` 只在锚点出现（全文 ≤5 处），大面积白底＋灰阶，彩色只做点缀。

---

## 一、设计变量速查表

| 变量 | 色值 | 用途 |
|------|------|------|
| 主色 | `#059669` | 连接线节点、清单勾选框、加粗锚点（≤5 处） |
| 主色深 | `#065f46` | 深底 CTA、表头、终端代码块标题栏 |
| 主色浅 | `#10b981` | 英文标签、子标题竖条、装饰点 |
| 浅底色 | `#ecfdf5` | 引言卡、要点框、数据卡背景 |
| 浅边框 | `#d1fae5` | 表格边框、核对框边框 |
| 高亮色 | `#fef08a` | 黄底高亮起始色 |
| 高亮渐变终色 | `#fde68a` | 黄底高亮结束色 |
| 标题色 | `#1f2937` | 文章标题、章节标题、子标题 |
| 正文色 | `#374151` | 正文段落 |
| 辅助文字色 | `#4b5563` | 副标题、元信息、日期 |
| 弱文字色 | `#6b7280` | 元信息标签、图注（≥13px 可读） |
| 分割线色 | `#e5e7eb` | 封面分隔、发丝线 |
| 下划线色 | `#6ee7b7` | 关键词下划线 |
| 等宽强调色 | `#0f766e` | 等宽 Kicker、代码行内关键词 |
| 深底白字背景 | `#065f46` | 关键要点框头、CTA、表头 |
| 等宽字体 | `'SF Mono','Consolas','Menlo',monospace` | Kicker、版本药丸、代码 |
| 正文字体 | `-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif` | 正文 |

### Type Scale（本模板）

| 场景 | 字号 | 行高 |
|------|------|------|
| 等宽 Kicker | 12px | 1.5 |
| 文章标题 | 24px | 1.4 |
| 章节大编号 | 18px | 1 |
| 章节标题 | 19px | 1.4 |
| 子标题 | 17px | 1.5 |
| 正文 | 16px | 1.9 |
| 说明/要点 | 14px | 1.7 |
| 元信息 | 13px | 1.5 |

---

## 二、各组件完整 HTML

### 1. 全局容器

```html
<section style="max-width:677px;margin:0 auto;padding:20px 16px;">
<!-- 文章内容 -->
</section>
```

### 2. 封面（等宽 Kicker + 版本药丸 + 元信息条）

```html
<section style="margin:0 0 28px;">
<section style="margin:0 0 14px;display:flex;align-items:center;">
<p style="margin:0 0 0 2px;line-height:1.5;font-size:12px;color:#0f766e;letter-spacing:2px;font-family:'SF Mono','Consolas','Menlo',monospace;"><span leaf="">TUTORIAL · PYTHON</span></p>
<section style="margin-left:12px;padding:2px 10px;background:#ecfdf5;border-radius:10px;"><p style="margin:0;line-height:1.5;font-size:12px;color:#059669;font-weight:bold;font-family:'SF Mono','Consolas','Menlo',monospace;"><span leaf="">v2.4</span></p></section>
</section>
<p style="margin:0 0 10px;line-height:1.4;font-size:24px;font-weight:bold;color:#1f2937;"><span leaf="">用 Python 做数据分析：从零到实战</span></p>
<section style="margin:0 0 18px;display:flex;flex-wrap:wrap;">
<section style="margin:0 16px 6px 0;"><p style="margin:0;line-height:1.5;font-size:13px;color:#6b7280;"><span leaf="">📖 阅读 8 分钟</span></p></section>
<section style="margin:0 16px 6px 0;"><p style="margin:0;line-height:1.5;font-size:13px;color:#6b7280;"><span leaf="">🎯 难度 入门</span></p></section>
<section style="margin:0 16px 6px 0;"><p style="margin:0;line-height:1.5;font-size:13px;color:#6b7280;"><span leaf="">🛠 工具 pandas</span></p></section>
</section>
<section style="height:1px;background:#e5e7eb;"></section>
</section>
```

### 3. 引言卡（浅底 + 等宽角标）

```html
<section style="margin:0 0 24px;padding:18px 20px;background:#ecfdf5;border-radius:8px;">
<p style="margin:0 0 10px;line-height:1.5;font-size:12px;color:#0f766e;letter-spacing:2px;font-family:'SF Mono','Consolas','Menlo',monospace;"><span leaf="">// INTRO</span></p>
<p style="margin:0;line-height:1.8;font-size:15px;color:#374151;"><span leaf="">这是一段引言或导读文字，用浅底卡片突出文章核心价值，帮助读者快速判断是否继续阅读。</span></p>
</section>
```

### 4. 清单式目录（Checklist TOC）

```html
<section style="margin:0 0 28px;padding:20px 24px;background:#f9fafb;border-radius:8px;">
<p style="margin:0 0 14px;line-height:1.5;font-size:13px;color:#6b7280;letter-spacing:1px;"><span leaf="">本文导航</span></p>
<section style="margin:0 0 12px;display:flex;align-items:center;">
<section style="flex-shrink:0;width:16px;height:16px;border:2px solid #059669;border-radius:4px;margin-right:10px;"></section>
<p style="margin:0;line-height:1.6;font-size:15px;color:#374151;"><span leaf="">准备工作：环境搭建与验证</span></p>
</section>
<section style="margin:0 0 12px;display:flex;align-items:center;">
<section style="flex-shrink:0;width:16px;height:16px;border:2px solid #059669;border-radius:4px;margin-right:10px;"></section>
<p style="margin:0;line-height:1.6;font-size:15px;color:#374151;"><span leaf="">读取与清洗：看结构、补缺失、去重复</span></p>
</section>
<section style="margin:0;display:flex;align-items:center;">
<section style="flex-shrink:0;width:16px;height:16px;border:2px solid #059669;border-radius:4px;margin-right:10px;"></section>
<p style="margin:0;line-height:1.6;font-size:15px;color:#374151;"><span leaf="">可视化与结论：让数据自己说话</span></p>
</section>
</section>
```

### 5. 章节标题（连接线步骤节点）

编号节点 + 垂直连接线贯穿下方正文，形成"步骤感"。

```html
<section style="margin:36px 0 0;display:flex;align-items:flex-start;">
<section style="flex-shrink:0;width:34px;display:flex;flex-direction:column;align-items:center;margin-right:14px;">
<section style="width:30px;height:30px;background:#059669;border-radius:6px;display:flex;align-items:center;justify-content:center;"><p style="margin:0;line-height:1;font-size:14px;color:#ffffff;font-weight:bold;font-family:'SF Mono','Consolas','Menlo',monospace;"><span leaf="">01</span></p></section>
<section style="width:2px;flex:1;background:#d1fae5;margin-top:6px;min-height:24px;"></section>
</section>
<section style="flex:1;padding-top:2px;">
<p style="margin:0 0 4px;line-height:1.4;font-size:19px;font-weight:bold;color:#1f2937;"><span leaf="">准备工作</span></p>
<p style="margin:0;line-height:1.4;font-size:12px;color:#10b981;letter-spacing:2px;font-family:'SF Mono','Consolas','Menlo',monospace;"><span leaf="">SETUP</span></p>
</section>
</section>
```

> 正文段落接在节点下方，连接线随内容自然延伸；下一个章节标题重复本结构（编号递增 02/03…）。末章为结语时编号用 `∞`。

### 6. 子标题（等宽箭头前缀）

```html
<section style="margin:24px 0 12px;display:flex;align-items:baseline;">
<p style="margin:0 8px 0 0;line-height:1.5;font-size:14px;color:#0f766e;font-family:'SF Mono','Consolas','Menlo',monospace;"><span leaf="">▸</span></p>
<p style="margin:0;line-height:1.5;font-size:17px;font-weight:bold;color:#1f2937;"><span leaf="">子标题内容</span></p>
</section>
```

### 7. 正文段落

```html
<p style="margin:0 0 20px;line-height:1.9;font-size:16px;color:#374151;"><span leaf="">这是标准正文段落，行高 1.9，字号 16px。每个段落之间保持 20px 间距，确保阅读舒适。</span></p>
```

### 8. 关键词下划线

```html
<span leaf="" style="border-bottom:2px solid #6ee7b7;">关键词</span>
```

段落内示例：

```html
<p style="margin:0 0 20px;line-height:1.9;font-size:16px;color:#374151;"><span leaf="">这段话里有一个<span leaf="" style="border-bottom:2px solid #6ee7b7;">关键概念</span>需要读者注意。</span></p>
```

### 9. 加粗标记（锚点层，全文 ≤5 处）

```html
<span leaf="" style="color:#059669;font-weight:bold;">加粗文字</span>
```

### 10. 高亮标记

```html
<span leaf="" style="background:linear-gradient(to top,#fef08a 0%,#fde68a 100%);padding:2px 4px;border-radius:3px;">高亮文字</span>
```

### 11. 荧光笔

```html
<span leaf="" style="background:linear-gradient(to top,#fef08a 40%,transparent 40%);">荧光标记文字</span>
```

### 12. 引用块（左竖条 + 等宽角标）

```html
<section style="margin:24px 0;padding:14px 18px;background:#ecfdf5;border-left:3px solid #059669;border-radius:0 6px 6px 0;">
<p style="margin:0 0 6px;line-height:1.5;font-size:12px;color:#0f766e;letter-spacing:1px;font-family:'SF Mono','Consolas','Menlo',monospace;"><span leaf="">NOTE</span></p>
<p style="margin:0;line-height:1.8;font-size:15px;color:#374151;"><span leaf="">引用块内容，用于强调重要观点或补充说明。</span></p>
</section>
```

### 13. 清单核对框（Checklist）

适用：操作清单、验收清单、踩坑自查。

```html
<section style="margin:24px 0;padding:16px 20px;border:1px solid #d1fae5;border-radius:8px;background:#f9fafb;">
<p style="margin:0 0 12px;line-height:1.5;font-size:13px;font-weight:bold;color:#059669;"><span leaf="">☑ 操作清单</span></p>
<section style="margin:0 0 10px;display:flex;align-items:flex-start;">
<section style="flex-shrink:0;width:16px;height:16px;background:#059669;border-radius:4px;margin:2px 10px 0 0;display:flex;align-items:center;justify-content:center;"><p style="margin:0;line-height:1;font-size:10px;color:#ffffff;"><span leaf="">✓</span></p></section>
<p style="margin:0;line-height:1.7;font-size:15px;color:#374151;"><span leaf="">用虚拟环境隔离依赖</span></p>
</section>
<section style="margin:0 0 10px;display:flex;align-items:flex-start;">
<section style="flex-shrink:0;width:16px;height:16px;background:#059669;border-radius:4px;margin:2px 10px 0 0;display:flex;align-items:center;justify-content:center;"><p style="margin:0;line-height:1;font-size:10px;color:#ffffff;"><span leaf="">✓</span></p></section>
<p style="margin:0;line-height:1.7;font-size:15px;color:#374151;"><span leaf="">先看数据结构再动手分析</span></p>
</section>
<section style="margin:0;display:flex;align-items:flex-start;">
<section style="flex-shrink:0;width:16px;height:16px;background:#059669;border-radius:4px;margin:2px 10px 0 0;display:flex;align-items:center;justify-content:center;"><p style="margin:0;line-height:1;font-size:10px;color:#ffffff;"><span leaf="">✓</span></p></section>
<p style="margin:0;line-height:1.7;font-size:15px;color:#374151;"><span leaf="">处理缺失值与重复订单</span></p>
</section>
</section>
```

### 14. API / 参数表（等宽参数名）

```html
<section style="margin:24px 0;border:1px solid #d1fae5;border-radius:8px;overflow:hidden;">
<section style="display:flex;background:#065f46;">
<section style="flex:1;padding:10px 14px;"><p style="margin:0;line-height:1.5;font-size:13px;font-weight:bold;color:#ffffff;"><span leaf="">参数</span></p></section>
<section style="flex:2;padding:10px 14px;"><p style="margin:0;line-height:1.5;font-size:13px;font-weight:bold;color:#ffffff;"><span leaf="">说明</span></p></section>
</section>
<section style="display:flex;background:#f9fafb;">
<section style="flex:1;padding:10px 14px;"><p style="margin:0;line-height:1.6;font-size:13px;color:#0f766e;font-family:'SF Mono','Consolas','Menlo',monospace;"><span leaf="">df.head()</span></p></section>
<section style="flex:2;padding:10px 14px;"><p style="margin:0;line-height:1.6;font-size:13px;color:#374151;"><span leaf="">查看数据前几行结构</span></p></section>
</section>
<section style="display:flex;">
<section style="flex:1;padding:10px 14px;"><p style="margin:0;line-height:1.6;font-size:13px;color:#0f766e;font-family:'SF Mono','Consolas','Menlo',monospace;"><span leaf="">df.isna()</span></p></section>
<section style="flex:2;padding:10px 14px;"><p style="margin:0;line-height:1.6;font-size:13px;color:#374151;"><span leaf="">定位缺失值位置</span></p></section>
</section>
</section>
```

### 15. 数据卡

```html
<section style="margin:24px 0;padding:24px;background:#ecfdf5;border-radius:8px;text-align:center;">
<p style="margin:0 0 6px;line-height:1;font-size:36px;font-weight:bold;color:#059669;"><span leaf="">98%</span></p>
<p style="margin:0;line-height:1.6;font-size:14px;color:#4b5563;"><span leaf="">数据说明文字</span></p>
</section>
```

### 16. 表格（斑马纹 + 深底表头）

```html
<section style="margin:24px 0;border:1px solid #d1fae5;border-radius:8px;overflow:hidden;">
<section style="display:flex;background:#065f46;">
<section style="flex:1;padding:12px 16px;"><p style="margin:0;line-height:1.5;font-size:14px;font-weight:bold;color:#ffffff;"><span leaf="">列标题A</span></p></section>
<section style="flex:1;padding:12px 16px;"><p style="margin:0;line-height:1.5;font-size:14px;font-weight:bold;color:#ffffff;"><span leaf="">列标题B</span></p></section>
</section>
<section style="display:flex;background:#f9fafb;">
<section style="flex:1;padding:12px 16px;"><p style="margin:0;line-height:1.5;font-size:14px;color:#374151;"><span leaf="">数据A1</span></p></section>
<section style="flex:1;padding:12px 16px;"><p style="margin:0;line-height:1.5;font-size:14px;color:#374151;"><span leaf="">数据B1</span></p></section>
</section>
<section style="display:flex;">
<section style="flex:1;padding:12px 16px;"><p style="margin:0;line-height:1.5;font-size:14px;color:#374151;"><span leaf="">数据A2</span></p></section>
<section style="flex:1;padding:12px 16px;"><p style="margin:0;line-height:1.5;font-size:14px;color:#374151;"><span leaf="">数据B2</span></p></section>
</section>
</section>
```

### 17. 分割线（等宽样式）

```html
<section style="margin:32px 0;text-align:center;">
<p style="margin:0;line-height:1;font-size:12px;color:#10b981;letter-spacing:6px;font-family:'SF Mono','Consolas','Menlo',monospace;"><span leaf="">• • •</span></p>
</section>
```

### 18. 关键要点框（Key Takeaways，文末）

```html
<section style="margin:36px 0 0;border-radius:8px;overflow:hidden;">
<section style="padding:10px 20px;background:#065f46;">
<p style="margin:0;line-height:1.5;font-size:13px;font-weight:bold;color:#ffffff;letter-spacing:1px;"><span leaf="">✓ KEY TAKEAWAYS</span></p>
</section>
<section style="padding:16px 20px;background:#ecfdf5;">
<p style="margin:0 0 8px;line-height:1.7;font-size:15px;color:#374151;"><span leaf="">要点一：先看结构再分析，缺失值先处理。</span></p>
<p style="margin:0 0 8px;line-height:1.7;font-size:15px;color:#374151;"><span leaf="">要点二：重复订单去重，避免统计虚高。</span></p>
<p style="margin:0;line-height:1.7;font-size:15px;color:#374151;"><span leaf="">要点三：结论先行，让图表自己说话。</span></p>
</section>
</section>
```

### 19. 作者签名区／CTA

```html
<section style="margin:40px 0 0;padding:24px;background:#065f46;border-radius:8px;text-align:center;">
<p style="margin:0 0 8px;line-height:1.6;font-size:15px;color:#ffffff;"><span leaf="">如果这篇文章对你有帮助</span></p>
<p style="margin:0 0 16px;line-height:1.6;font-size:15px;color:#ffffff;"><span leaf="">欢迎点赞、在看、转发分享</span></p>
<section style="display:inline-block;padding:6px 20px;background:#ffffff;border-radius:20px;">
<p style="margin:0;line-height:1.5;font-size:14px;font-weight:bold;color:#065f46;"><span leaf="">{{作者名}}</span></p>
</section>
</section>
```

### 20. 产品徽章

```html
<section style="display:inline-block;padding:3px 10px;background:#ecfdf5;border:1px solid #d1fae5;border-radius:4px;">
<p style="margin:0;line-height:1.5;font-size:13px;color:#059669;font-weight:bold;"><span leaf="">产品名</span></p>
</section>
```

---

## 三、完整文章模板骨架（Blueprint）

```
全局容器
 ├─ 封面（等宽 Kicker + 版本药丸 + 元信息条）
 ├─ 引言卡
 ├─ 清单式目录
 ├─ 〔 章节标题（连接线步骤节点）    ← 循环 N 次
 │    ├─ 子标题（按需，等宽 ▸ 前缀）
 │    ├─ 正文段落（关键词下划线／加粗／高亮／荧光笔）
 │    ├─ 引用块 NOTE（按需）
 │    ├─ 清单核对框（按需）
 │    ├─ API 参数表（按需）
 │    ├─ 数据卡（按需）
 │    ├─ 表格（按需）
 │    └─ 通用库：代码块／图片（按需）〕
 ├─ 分割线
 ├─ 关键要点框
 └─ 作者签名区／CTA
```

---

## 四、文章类型 → 组件组合配方表

| 文章类型 | 核心组件组合 |
|---------|------------|
| 教程／操作指南 | 封面→引言→清单目录→步骤节点章节→代码块→NOTE 引用→清单核对框→关键要点框→签名 |
| 测评／对比 | 封面→引言→表格（对比）→正文→数据卡→API 参数表→关键要点框→签名 |
| 工具盘点／清单 | 封面→清单目录→产品徽章→清单核对框→表格→数据卡→关键要点框→签名 |
| 数据复盘／报告 | 封面→引言→清单目录→数据卡→表格→正文→关键要点框→签名 |

---

## 五、Markdown → 组件映射规则表

| Markdown 元素 | 映射组件 |
|--------------|---------|
| `# 标题` | 封面（自动生成等宽 Kicker + 元信息条） |
| `> 引言（开头）` | 引言卡（等宽 `// INTRO` 角标） |
| `## 标题` | 章节标题（连接线步骤节点 01/02/03，末章 `∞`） |
| `### 标题` | 子标题（等宽 `▸` 前缀） |
| 正文段落 | 正文段落（每段主动加 1-3 个关键词下划线） |
| `**文字**` | 加粗标记（锚点层，全文 ≤5 处） |
| `==文字==` | 高亮标记 |
| `<u>文字</u>` | 关键词下划线 |
| `> 引用（非开头）` | 引用块（`NOTE` 角标） |
| `- [ ] 项` | 清单核对框 |
| `` \| 表格 \| `` | 表格（斑马纹）或 API 参数表（含等宽参数名列时） |
| `- 项` / `1. 项` | 转为带缩进的正文段落（无序列表前缀「·」） |
| `` `code` `` | 通用库行内代码（等宽 `#0f766e` 关键字） |
| ` ``` 围栏 ``` ` | 通用库代码块（浅色版套主色） |
| `![说明](url)` | 通用库图片组件（有说明文字才加说明） |
