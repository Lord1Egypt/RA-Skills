# 通用增量组件库（所有公众号主题共用）

> 代码块、图片/GIF、小标签标题这三类组件所有主题共用，套用当前主题主色即可。
> 优先级：**先查主题库映射规则表**——该主题有等价语义组件就用主题库版本；主题库没有时才用本库。

## 使用规则

- 所有组件的 `{{主色}}` / `{{浅底色}}` / `{{下划线色}}` 占位符替换为当前主题的设计变量值
- 所有文字节点必须用 `<span leaf="">` 包裹
- 代码块每行一个 `<p style="margin:0">`，**绝不用 `white-space:pre`**
- 缩进用全角空格 `　`，行距靠 `line-height`

---

## 1. 代码块

### 1a. 深色代码块

```html
<section style="margin:20px 0;padding:16px 20px;background:#1e293b;border-radius:8px;overflow-x:auto;">
<p style="margin:0;line-height:1.6;font-size:14px;color:#e2e8f0;font-family:'SF Mono','Consolas','Monaco',monospace;"><span leaf=""><span leaf="" style="color:#93c5fd;">pip</span> install openai</span></p>
<p style="margin:0;line-height:1.6;font-size:14px;color:#e2e8f0;font-family:'SF Mono','Consolas','Monaco',monospace;"><span leaf=""><span leaf="" style="color:#6ee7b7;">from</span> openai <span leaf="" style="color:#6ee7b7;">import</span> OpenAI</span></p>
</section>
```

### 1b. 浅色代码块

```html
<section style="margin:20px 0;padding:16px 20px;background:#f1f5f9;border-radius:8px;border-left:3px solid {{主色}};overflow-x:auto;">
<p style="margin:0;line-height:1.6;font-size:14px;color:#334155;font-family:'SF Mono','Consolas','Monaco',monospace;"><span leaf="">npm create vite@latest my-app</span></p>
<p style="margin:0;line-height:1.6;font-size:14px;color:#334155;font-family:'SF Mono','Consolas','Monaco',monospace;"><span leaf="">cd my-app && npm install</span></p>
</section>
```

### 1c. 行内代码

```html
<span leaf="" style="background:#f1f5f9;color:#059669;padding:2px 6px;border-radius:4px;font-size:0.9em;font-family:'SF Mono','Consolas','Monaco',monospace;">`代码内容`</span>
```

行内代码示例（实际使用时去掉反引号，直接写代码内容）：

```html
<p style="margin:0;line-height:1.9;color:#374151;font-size:16px;"><span leaf="">运行命令 <span leaf="" style="background:#f1f5f9;color:#059669;padding:2px 6px;border-radius:4px;font-size:14px;font-family:'SF Mono','Consolas','Monaco',monospace;">npm run dev</span> 启动开发服务器</span></p>
```

---

## 2. 图片与 GIF

### 2a. 带说明的图片

```html
<section style="margin:24px 0;text-align:center;">
<img src="图片URL" style="max-width:100%;height:auto;display:block;margin:0 auto;border-radius:8px;" />
<p style="margin:8px 0 0;line-height:1.6;color:#9ca3af;font-size:13px;"><span leaf="">图片说明文字</span></p>
</section>
```

### 2b. GIF（带动图角标）

```html
<section style="margin:24px 0;text-align:center;position:relative;">
<img src="GIF的URL" style="max-width:100%;height:auto;display:block;margin:0 auto;border-radius:8px;" />
<section style="display:inline-block;margin-top:8px;padding:3px 10px;background:#f3f4f6;border-radius:12px;font-size:12px;color:#6b7280;"><span leaf="">GIF</span></section>
</section>
```

### 2c. 居中素材占位板块（待补素材用）

```html
<section style="margin:24px 0;padding:32px 20px;background:#f9fafb;border:2px dashed #d1d5db;border-radius:8px;text-align:center;">
<p style="margin:0;line-height:1.8;color:#9ca3af;font-size:14px;"><span leaf="">待补充素材</span></p>
<p style="margin:4px 0 0;line-height:1.6;color:#d1d5db;font-size:13px;"><span leaf="">在此处插入截图 / GIF / 成果图</span></p>
</section>
```

> 注意：此居中占位块使用 `dashed` 虚线框是被允许的——它是居中的素材占位组件，不是正文强调。正文强调用 3a-3e 的小标签。

---

## 3. 小标签与强调组件

### 3a. 左竖条小标题

```html
<section style="margin:24px 0;padding:8px 0 8px 14px;border-left:3px solid {{主色}};">
<p style="margin:0;line-height:1.6;font-size:17px;font-weight:bold;color:#1f2937;"><span leaf="">小标题文字</span></p>
</section>
```

### 3b. 药丸标签

```html
<section style="margin:16px 0 8px;">
<section style="display:inline-block;padding:4px 12px;background:{{浅底色}};border-radius:20px;">
<p style="margin:0;line-height:1.5;font-size:13px;color:{{主色}};font-weight:bold;"><span leaf="">标签文字</span></p>
</section>
</section>
```

### 3c. 步骤标签（Step Label）

```html
<section style="margin:20px 0;display:flex;align-items:center;">
<section style="flex-shrink:0;width:28px;height:28px;background:{{主色}};border-radius:50%;display:flex;align-items:center;justify-content:center;">
<p style="margin:0;line-height:1;font-size:14px;color:#ffffff;font-weight:bold;"><span leaf="">1</span></p>
</section>
<p style="margin:0 0 0 10px;line-height:1.6;font-size:16px;font-weight:bold;color:#1f2937;"><span leaf="">步骤标题</span></p>
</section>
```

### 3d. 左竖条金句/提示块

```html
<section style="margin:20px 0;padding:12px 16px;background:{{浅底色}};border-left:3px solid {{主色}};border-radius:0 6px 6px 0;">
<p style="margin:0;line-height:1.8;font-size:15px;color:#374151;"><span leaf="">这里是一段需要突出的金句或提示内容。</span></p>
</section>
```

### 3e. 居中金句

```html
<section style="margin:28px 0;padding:20px;text-align:center;">
<p style="margin:0;line-height:1.8;font-size:18px;font-weight:bold;color:#1f2937;letter-spacing:1px;"><span leaf="">核心金句内容</span></p>
<section style="margin:12px auto 0;width:40px;height:3px;background:{{主色}};border-radius:2px;"></section>
</section>
```

---

## 4. 版权脚注（所有产物必带）

固定版权行，**每个排版产物的正文末尾必须追加**。样式固定、不随主题变化，文字一字不差：

```html
<section style="margin:32px 0 0;padding-top:16px;border-top:1px solid #e5e7eb;text-align:center;">
<p style="margin:0;line-height:1.6;font-size:12px;color:#9ca3af;"><span leaf="">©2026 Qomob.AI 由WeChatLayout微信公众号排版引擎驱动</span></p>
</section>
```

> 版权行是完成判据的一部分，遗漏 = 产物不合格。文字必须精确为「©2026 Qomob.AI 由WeChatLayout微信公众号排版引擎驱动」。

---

## 5. 高频内容组件

> 以下组件覆盖教程、案例、发布、访谈等高频公众号场景，所有主题共用。
> 使用 `{{主色}}` / `{{浅底色}}` / `{{下划线色}}` 占位符自动适配当前主题。

### 5a. 时间线（Timeline）

适用：案例复盘、产品迭代史、成长历程。每个节点为一条目，纵向排列。

```html
<section style="margin:24px 0;">
<section style="margin:0 0 20px;display:flex;align-items:flex-start;">
<section style="flex-shrink:0;width:20px;margin-right:12px;display:flex;flex-direction:column;align-items:center;">
<section style="width:10px;height:10px;background:{{主色}};border-radius:50%;"></section>
<section style="width:2px;flex:1;background:{{下划线色}};margin-top:4px;min-height:40px;"></section>
</section>
<section style="flex:1;">
<p style="margin:0 0 4px;line-height:1.5;font-size:13px;color:#6b7280;"><span leaf="">2024年3月</span></p>
<p style="margin:0;line-height:1.7;font-size:15px;color:#1f2937;font-weight:bold;"><span leaf="">项目启动，确定方向</span></p>
<p style="margin:4px 0 0;line-height:1.7;font-size:14px;color:#4b5563;"><span leaf="">完成了需求调研和技术选型，团队从3人扩展到8人。</span></p>
</section>
</section>
<section style="margin:0;display:flex;align-items:flex-start;">
<section style="flex-shrink:0;width:20px;margin-right:12px;display:flex;flex-direction:column;align-items:center;">
<section style="width:10px;height:10px;background:{{主色}};border-radius:50%;"></section>
</section>
<section style="flex:1;">
<p style="margin:0 0 4px;line-height:1.5;font-size:13px;color:#6b7280;"><span leaf="">2024年6月</span></p>
<p style="margin:0;line-height:1.7;font-size:15px;color:#1f2937;font-weight:bold;"><span leaf="">MVP上线，首批用户测试</span></p>
<p style="margin:4px 0 0;line-height:1.7;font-size:14px;color:#4b5563;"><span leaf="">核心功能跑通，收集到200位种子用户反馈。</span></p>
</section>
</section>
</section>
```

### 5b. 语义提示框（Callout）

四色语义固定色，**不随主题变化**（颜色代表含义而非品牌）。

```html
<!-- ℹ️ 提示 Tip -->
<section style="margin:20px 0;padding:12px 16px;background:#eff6ff;border-left:3px solid #3b82f6;border-radius:0 6px 6px 0;">
<p style="margin:0;line-height:1.7;font-size:14px;color:#1e40af;"><span leaf="">💡 提示：开启 HTTPS 可避免混合内容警告。</span></p>
</section>

<!-- ⚠️ 注意 Warning -->
<section style="margin:20px 0;padding:12px 16px;background:#fffbeb;border-left:3px solid #f59e0b;border-radius:0 6px 6px 0;">
<p style="margin:0;line-height:1.7;font-size:14px;color:#92400e;"><span leaf="">⚠️ 注意：API Key 切勿提交到公开仓库。</span></p>
</section>

<!-- ✅ 成功 Success -->
<section style="margin:20px 0;padding:12px 16px;background:#ecfdf5;border-left:3px solid #10b981;border-radius:0 6px 6px 0;">
<p style="margin:0;line-height:1.7;font-size:14px;color:#065f46;"><span leaf="">✅ 部署成功，可通过 https://yourapp.com 访问。</span></p>
</section>

<!-- ❌ 错误 Danger -->
<section style="margin:20px 0;padding:12px 16px;background:#fef2f2;border-left:3px solid #ef4444;border-radius:0 6px 6px 0;">
<p style="margin:0;line-height:1.7;font-size:14px;color:#991b1b;"><span leaf="">❌ 报错：数据库连接超时，请检查安全组配置。</span></p>
</section>
```

### 5c. 统计数据行（Stats Row）

适用：数据成果展示、核心指标。flex 横排，2-4 列自适应。

```html
<section style="margin:24px 0;display:flex;justify-content:space-around;text-align:center;">
<section style="flex:1;">
<p style="margin:0;line-height:1.2;font-size:28px;font-weight:bold;color:{{主色}};"><span leaf="">10万+</span></p>
<p style="margin:6px 0 0;line-height:1.5;font-size:13px;color:#6b7280;"><span leaf="">累计用户</span></p>
</section>
<section style="flex:1;">
<p style="margin:0;line-height:1.2;font-size:28px;font-weight:bold;color:{{主色}};"><span leaf="">99.9%</span></p>
<p style="margin:6px 0 0;line-height:1.5;font-size:13px;color:#6b7280;"><span leaf="">可用性</span></p>
</section>
<section style="flex:1;">
<p style="margin:0;line-height:1.2;font-size:28px;font-weight:bold;color:{{主色}};"><span leaf="">50ms</span></p>
<p style="margin:6px 0 0;line-height:1.5;font-size:13px;color:#6b7280;"><span leaf="">平均响应</span></p>
</section>
</section>
```

### 5d. 问答对（Q&A）

适用：FAQ、访谈记录。问句带主色标记，答句为正文色。

```html
<section style="margin:20px 0;">
<p style="margin:0 0 8px;line-height:1.7;font-size:16px;font-weight:bold;color:#1f2937;"><span leaf="" style="color:{{主色}};">Q：</span><span leaf="">这个服务收费吗？</span></p>
<p style="margin:0 0 0 20px;line-height:1.8;font-size:15px;color:#4b5563;"><span leaf="">A：个人用户完全免费，团队版按席位收费，详见定价页。</span></p>
</section>
```

### 5e. 特性网格（Feature Grid）

适用：产品发布、工具盘点。2×2 卡片，每张含图标 + 标题 + 描述。

```html
<section style="margin:24px 0;display:flex;flex-wrap:wrap;gap:12px;">
<section style="flex:1 1 40%;min-width:140px;padding:16px;background:{{浅底色}};border-radius:8px;">
<p style="margin:0 0 6px;line-height:1.5;font-size:20px;"><span leaf="">⚡</span></p>
<p style="margin:0 0 4px;line-height:1.5;font-size:15px;font-weight:bold;color:#1f2937;"><span leaf="">极速启动</span></p>
<p style="margin:0;line-height:1.6;font-size:13px;color:#6b7280;"><span leaf="">冷启动 < 200ms</span></p>
</section>
<section style="flex:1 1 40%;min-width:140px;padding:16px;background:{{浅底色}};border-radius:8px;">
<p style="margin:0 0 6px;line-height:1.5;font-size:20px;"><span leaf="">🔒</span></p>
<p style="margin:0 0 4px;line-height:1.5;font-size:15px;font-weight:bold;color:#1f2937;"><span leaf="">安全合规</span></p>
<p style="margin:0;line-height:1.6;font-size:13px;color:#6b7280;"><span leaf="">SOC2 + GDPR</span></p>
</section>
<section style="flex:1 1 40%;min-width:140px;padding:16px;background:{{浅底色}};border-radius:8px;">
<p style="margin:0 0 6px;line-height:1.5;font-size:20px;"><span leaf="">🌐</span></p>
<p style="margin:0 0 4px;line-height:1.5;font-size:15px;font-weight:bold;color:#1f2937;"><span leaf="">全球加速</span></p>
<p style="margin:0;line-height:1.6;font-size:13px;color:#6b7280;"><span leaf="">200+ 边缘节点</span></p>
</section>
<section style="flex:1 1 40%;min-width:140px;padding:16px;background:{{浅底色}};border-radius:8px;">
<p style="margin:0 0 6px;line-height:1.5;font-size:20px;"><span leaf="">📊</span></p>
<p style="margin:0 0 4px;line-height:1.5;font-size:15px;font-weight:bold;color:#1f2937;"><span leaf="">数据看板</span></p>
<p style="margin:0;line-height:1.6;font-size:13px;color:#6b7280;"><span leaf="">实时可视化分析</span></p>
</section>
</section>
```

### 5f. 图片网格（Image Grid）

适用：美食、旅行、穿搭。双图或三图横排，每图带简短说明。

```html
<!-- 双图 -->
<section style="margin:24px 0;display:flex;gap:8px;">
<section style="flex:1;">
<img src="图片1URL" style="width:100%;height:auto;display:block;border-radius:8px;" />
<p style="margin:6px 0 0;line-height:1.5;font-size:12px;color:#6b7280;text-align:center;"><span leaf="">场景一</span></p>
</section>
<section style="flex:1;">
<img src="图片2URL" style="width:100%;height:auto;display:block;border-radius:8px;" />
<p style="margin:6px 0 0;line-height:1.5;font-size:12px;color:#6b7280;text-align:center;"><span leaf="">场景二</span></p>
</section>
</section>

<!-- 三图 -->
<section style="margin:24px 0;display:flex;gap:6px;">
<section style="flex:1;">
<img src="图片1URL" style="width:100%;height:auto;display:block;border-radius:6px;" />
<p style="margin:4px 0 0;line-height:1.5;font-size:11px;color:#6b7280;text-align:center;"><span leaf="">步骤一</span></p>
</section>
<section style="flex:1;">
<img src="图片2URL" style="width:100%;height:auto;display:block;border-radius:6px;" />
<p style="margin:4px 0 0;line-height:1.5;font-size:11px;color:#6b7280;text-align:center;"><span leaf="">步骤二</span></p>
</section>
<section style="flex:1;">
<img src="图片3URL" style="width:100%;height:auto;display:block;border-radius:6px;" />
<p style="margin:4px 0 0;line-height:1.5;font-size:11px;color:#6b7280;text-align:center;"><span leaf="">步骤三</span></p>
</section>
</section>
```

---

## 换色规则

通用库组件用到主色时，替换为当前主题的对应变量：

| 占位符 | emerald | graphite | sunset | ocean | rose |
|--------|---------|---------|--------|-------|------|
| `{{主色}}` | `#059669` | `#374151` | `#ea580c` | `#2563eb` | `#e11d48` |
| `{{浅底色}}` | `#ecfdf5` | `#f3f4f6` | `#fff7ed` | `#eff6ff` | `#fff1f2` |
| `{{下划线色}}` | `#6ee7b7` | `#9ca3af` | `#fb923c` | `#93c5fd` | `#fb7185` |
