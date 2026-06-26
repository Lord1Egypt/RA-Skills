# 封面图设计指南

## 五维度选择体系

封面图由 5 个独立维度交叉定义。每个维度独立选择，通过兼容矩阵确保组合合理。

```
文章内容 → 自动推荐五维度组合 → 老板确认/调整 → 组装 prompt → 生成
```

---

### 维度 1：构图类型（Type）

| 类型 | 构图方式 | 视觉区占比 | 适用文章 |
|------|---------|-----------|---------|
| `hero` | 大视觉冲击 + 标题覆盖，戏剧性构图 | 视觉 60-70% | 产品分析、重磅发布 |
| `conceptual` | 抽象概念可视化，信息分区，干净 | 视觉 50% | 技术架构、方法论 |
| `typography` | 文字为主体元素（40%+面积），极少视觉 | 文字 60% | 观点文、金句、声明 |
| `metaphor` | 具象物体隐喻抽象概念，符号化 | 视觉 60% | 成长、转型、哲理 |
| `split` | 左右或上下对比分屏，强烈视觉对照 | 各 50% | 对比文、before/after |
| `minimal` | 单一焦点 + 大量留白（60%+） | 视觉 30% | 极简核心概念、禅意 |

### 维度 2：配色方案（Palette）

| 配色 | 色值 | 视觉感受 | 适用 |
|------|------|---------|------|
| `tech-blue` | #1a1f5c → #7c3aed | 科技/紫蓝渐变 | AI产品、技术拆解 |
| `insight-blue` | #1e3a5f → #3b82f6 | 理性/深蓝 | 方法论、框架思考 |
| `action-orange` | #f97316 → #eab308 | 活力/橙黄 | 效率提升、实战 |
| `solution-green` | #10b981 → #f97316 | 解决方案/绿橙 | 场景方案、破局 |
| `trend-cyan` | #0891b2 → #06b6d4 | 趋势/蓝绿 | 行业观察、前沿 |
| `mono` | #1A1A1A + #F5F5F5 | 极简/黑白灰 | 哲理、极简、金句 |
| `warm` | #F5E6D0 + #D4956A + #7BA3A8 | 温暖/莫兰迪 | 个人故事、感悟 |
| `dark` | #0F172A + #3B82F6 + #06B6D4 | 高级/深色 | 电影感、高级观点 |

### 维度 3：渲染风格（Rendering）

| 渲染 | 视觉特征 | Prompt 关键词 |
|------|---------|-------------|
| `3d-icon` | 现代3D图标、光效、微渐变 | modern 3D style icons, subtle glow, depth |
| `flat-vector` | 扁平矢量、干净线条、无阴影 | flat vector, clean lines, no shadows, solid colors |
| `hand-drawn` | 手绘马克笔、不均匀线条 | hand-drawn marker style, uneven strokes, sketch quality |
| `painterly` | 水彩/油画质感、柔和边缘、艺术感 | watercolor soft edges, painterly brushstrokes, dreamy artistic |
| `digital` | 数据可视化、仪表盘风、打磨感 | polished digital render, data dashboard aesthetic, clean gradients |
| `screen-print` | 丝网印刷、半色调、2-4色 | screen print poster art, halftone dots, 2-4 flat colors, stencil-cut |
| `chalk` | 黑板粉笔、教学感、粗糙质感 | chalkboard style, chalk texture, rough hand-lettering, dark background |

### 维度 4：文字密度（Text）

| 级别 | 文字内容 | 适用 |
|------|---------|------|
| `none` | 纯视觉，无文字 | 抽象概念封面（少用） |
| `title-only` | 仅主标题（**默认**） | 大多数文章 |
| `title-subtitle` | 主标题 + 副标题/系列名 | 系列文章、教程 |
| `text-rich` | 标题 + 副标题 + 2-4 关键词标签 | 公告、多要点文章 |

### 维度 5：视觉强度（Mood）

| 级别 | 效果 | 量化调整 | 适用 |
|------|------|---------|------|
| `subtle` | 低对比、柔和、专业克制 | 对比度 -20~30%，饱和度 -20~30%，线条更细 | 方法论、学术类 |
| `balanced` | 中等对比（**默认**） | 标准 | 大多数文章 |
| `bold` | 高对比、强冲击、饱和色 | 对比度 +20~30%，饱和度 +20~30%，线条更粗 | 重磅观点、争议话题 |

### 维度 6：字体风格（Font）← 新增

| 字体 | 视觉感受 | Prompt 关键词 | 适用 |
|------|---------|-------------|------|
| `clean` | 无衬线、现代、干净（**默认**） | clean sans-serif typography | 技术、产品、大多数文章 |
| `handwritten` | 手写体、亲和、个人感 | handwritten casual font style | 个人故事、生活感悟 |
| `serif` | 衬线体、经典、学术感 | classic serif editorial typography | 深度长文、学术、书评 |
| `display` | 粗重装饰体、冲击力 | bold decorative display font | 公告、事件、促销类 |

---

## 构图核心原则（融合 baoyu-cover-image Base Prompt）

每次生成封面图，prompt 末尾必须附加以下构图约束：

```
Composition rules:
- Generous whitespace: maintain 40-60% breathing room, avoid cluttered layouts
- Visual anchor: main element centered or offset left (reserve right side for title area if title included)
- Information hierarchy: one dominant focal point, 1-2 supporting elements, decorative accents
- Clean backgrounds: solid colors or subtle gradients, no complex textures or patterns
- Characters: simplified silhouettes only, NO realistic human faces or bodies
- Icon vocabulary: use simple recognizable icons to represent concepts (see table below)
- Chinese text must be clearly readable, text and visuals must not overlap
- No emoji (renders as color blocks in browser screenshots)
```

### 图标词汇表速查

| 类别 | 图标 |
|------|------|
| 技术 | 代码窗口、齿轮、电路、云、锁、API 括号 |
| 创意 | 灯泡、火箭、靶心、拼图、钥匙、放大镜 |
| 沟通 | 对话气泡、聊天点、喇叭、信封 |
| 成长 | 植物/幼苗、树、箭头、图表、山 |
| 工具 | 扳手、铅笔、画笔、清单、时钟 |
| 抽象概念 | 无穷≡、太极、螺旋、层叠/堆叠、桥、门/传送门、镜子/倒影 |

### 图标组合模式

通过组合图标创建视觉比喻：

| 组合 | 表达 |
|------|------|
| 灯泡 + 齿轮 | 创新工程 |
| 植物 + 代码 | 有机技术增长 |
| 火箭 + 靶心 | 精准加速 |
| 钥匙 + 锁 | 安全解决方案 |
| 桥 + 人物 | 团队连接 |
| 放大镜 + 数据 | 分析洞察 |

### 渲染风格与图标处理

| Rendering | 图标风格 |
|-----------|----------|
| `3d-icon` | 立体感、微渐变、光影 |
| `flat-vector` | 几何化、简单形状、均匀填充 |
| `hand-drawn` | 涂鸦感、有机线条、手绘质感 |
| `painterly` | 柔和边缘、笔触感 |
| `digital` | 精确、微渐变、打磨 |
| `screen-print` | 模板切割、单色块、半色调 |
| `chalk` | 粗糙、粉笔质感、网格对齐 |

---

## Rendering 详细定义

每种渲染风格的线条/纹理/深度/元素规范，prompt 中引用对应条目：

| Rendering | Lines | Texture | Depth | Prompt 特征词 |
|-----------|-------|---------|-------|---------------|
| `3d-icon` | 干净圆滑 | 微光泰效果 | 有立体感和阴影 | modern 3D icons, subtle glow, soft shadows, depth layers |
| `flat-vector` | 均匀精确、无变化 | 无纹理、纯色填充 | 完全扁平 | flat vector, clean uniform lines, solid fills, no shadows, no gradients |
| `hand-drawn` | 不均匀、略有抖动 | 马克笔/铅笔质感 | 最小深度 | hand-drawn marker sketch, slightly shaky lines, paper texture, doodle quality |
| `painterly` | 柔和笔触、模糊边缘 | 水彩/油画质感 | 柔和边缘、光影渗透 | watercolor soft washes, visible brushstrokes, dreamy blending, artistic texture |
| `digital` | 精确干净、圆滑 | 微光泰效果 | 微层次感 | polished digital render, clean gradients, dashboard aesthetic, subtle depth |
| `screen-print` | 模板切割、粗犷 | 半色调点/色块边缘 | 扁平、无深度 | screen print poster, halftone dots, 2-4 flat colors, stencil-cut edges, bold contrast |
| `chalk` | 粗糙手写、不均匀 | 粉笔飞粉感 | 扁平 | chalkboard style, chalk dust texture, rough hand-lettering, dark background, educational feel |

---

## 参考图处理流程

当提供参考图时（老板给了风格参考、竞品封面等）：

### 流程

1. **保存参考图**：复制到 `refs/ref-NN-{slug}.{ext}`
2. **深度分析**：提取具体、可复现的元素（不是“有个 logo”，而是“logo 用平行竖线拼 m”）
3. **分类用途**：
   - `direct`：参考图直接传给模型 `--ref`（需要复现人物/核心元素时）
   - `style`：只提取视觉风格（线条、纹理、构图）
   - `palette`：只提取配色方案（hex 色值）
4. **写入 prompt**：用 MUST/REQUIRED 前缀强制约束，不能只传 `--ref` 不写文字描述（模型经常忽略 ref 图片）

### 深度分析提取清单

| 分析维度 | 好的描述 | 差的描述 |
|----------|---------|----------|
| 配色 | “#2D4A3E 深青 + #F5F0E0 米白” | “有深色和浅色” |
| 线条 | “2px 均匀线条，圆角端点” | “有线条” |
| 布局 | “底部 30% 暗色横幅放品牌” | “有个横幅” |
| 字体 | “大写、宽字距、无衬线” | “有文字” |

### 优先级规则

- 参考图 **覆盖默认**：如果参考图风格与预设配色/渲染冲突，参考图优先
- 具体 > 模糊：提取具体元素，不要“干净风格”这种模糊描述
- 生成后检查：确认参考元素在产出中可见，不可见则加强 prompt 重试

---

## 兼容矩阵

### Type × Rendering

| Type \ Rendering | 3d-icon | flat-vector | hand-drawn | painterly | digital | screen-print | chalk |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `hero` | ✓✓ | ✓ | ✓ | ✓ | ✓✓ | ✓ | ✗ |
| `conceptual` | ✓✓ | ✓✓ | ✗ | ✗ | ✓✓ | ✓ | ✓ |
| `typography` | ✓ | ✓✓ | ✓ | ✗ | ✓ | ✓✓ | ✓✓ |
| `metaphor` | ✓ | ✓ | ✓✓ | ✓✓ | ✓ | ✓✓ | ✓ |
| `split` | ✓✓ | ✓✓ | ✓ | ✗ | ✓✓ | ✓ | ✗ |
| `minimal` | ✓ | ✓✓ | ✓ | ✓✓ | ✓ | ✓✓ | ✓ |

### Type × Mood

| Type \ Mood | subtle | balanced | bold |
|---|:---:|:---:|:---:|
| `hero` | ✓ | ✓✓ | ✓✓ |
| `conceptual` | ✓✓ | ✓✓ | ✓ |
| `typography` | ✓ | ✓✓ | ✓✓ |
| `metaphor` | ✓✓ | ✓✓ | ✓ |
| `split` | ✓ | ✓✓ | ✓✓ |
| `minimal` | ✓✓ | ✓✓ | ✗ |

### Palette × Rendering

| Palette \ Rendering | 3d-icon | flat-vector | hand-drawn | painterly | digital | screen-print | chalk |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `tech-blue` | ✓✓ | ✓ | ✗ | ✗ | ✓✓ | ✓ | ✗ |
| `insight-blue` | ✓✓ | ✓✓ | ✗ | ✗ | ✓✓ | ✓ | ✗ |
| `action-orange` | ✓✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| `solution-green` | ✓✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✗ |
| `trend-cyan` | ✓✓ | ✓✓ | ✗ | ✗ | ✓✓ | ✓ | ✗ |
| `mono` | ✓ | ✓✓ | ✓ | ✗ | ✓ | ✓✓ | ✓✓ |
| `warm` | ✓ | ✓ | ✓✓ | ✓✓ | ✓ | ✓ | ✗ |
| `dark` | ✓✓ | ✓ | ✗ | ✗ | ✓✓ | ✓✓ | ✓✓ |

> ✓✓ 强推荐 | ✓ 可用 | ✗ 不推荐

### Type × Text

| Type \ Text | none | title-only | title-subtitle | text-rich |
|---|:---:|:---:|:---:|:---:|
| `hero` | ✓ | ✓✓ | ✓✓ | ✓ |
| `conceptual` | ✓✓ | ✓✓ | ✓ | ✓ |
| `typography` | ✗ | ✓ | ✓✓ | ✓✓ |
| `metaphor` | ✓✓ | ✓ | ✓ | ✗ |
| `split` | ✓ | ✓✓ | ✓ | ✓ |
| `minimal` | ✓✓ | ✓✓ | ✓ | ✗ |

### Font × Rendering

| Font \ Rendering | 3d-icon | flat-vector | hand-drawn | painterly | digital | screen-print | chalk |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `clean` | ✓✓ | ✓✓ | ✗ | ✗ | ✓✓ | ✓ | ✗ |
| `handwritten` | ✓ | ✓ | ✓✓ | ✓✓ | ✓ | ✗ | ✓✓ |
| `serif` | ✓ | ✓ | ✗ | ✓ | ✓✓ | ✓ | ✗ |
| `display` | ✓✓ | ✓✓ | ✓ | ✓ | ✓✓ | ✓✓ | ✓ |

**兼容检查**：选定六维度后，检查上方 5 张矩阵中是否有 ✗ 组合。有则提示调整。

---

## 内容信号自动推荐

**决策规则**（与小红书 presets.md 统一逻辑）：
1. 扫描文章关键词，匹配下表第一个命中行
2. 取推荐的六维度组合（或直接用预设快捷方式）
3. 用上方兼容矩阵校验组合无 ✗
4. 混合信号时取第一个匹配，不迭加多个维度推荐

公众号用「六维度」因为封面图是 AI 生图需要细粒度控制；小红书用「预设」因为预设已封装最佳组合。两套体系底层逻辑一致：内容信号 → 自动推荐 → 兼容校验 → 生成。

根据文章关键词自动推荐六维度组合：

| 文章关键词/类型 | Type | Palette | Rendering | Text | Mood |
|---------------|------|---------|-----------|------|------|
| AI、产品、工具、拆解、评测 | `hero` | `tech-blue` | `3d-icon` | title-only | balanced |
| 架构、框架、系统、分层、原理 | `conceptual` | `insight-blue` | `flat-vector` | title-only | subtle |
| 观点、趋势、判断、声明、预测 | `typography` | `mono` | `screen-print` | title-only | bold |
| 成长、转型、个人经历、反思 | `metaphor` | `warm` | `hand-drawn` | title-only | balanced |
| vs、对比、before/after、选型 | `split` | `tech-blue` | `3d-icon` | title-only | bold |
| 极简、核心、本质、一个概念 | `minimal` | `mono` | `flat-vector` | title-only | subtle |
| 效率、实战、工具实操 | `hero` | `action-orange` | `3d-icon` | title-subtitle | balanced |
| 行业、前沿、趋势报告 | `hero` | `trend-cyan` | `3d-icon` | title-only | balanced |
| 解决方案、破局、方法 | `hero` | `solution-green` | `3d-icon` | title-only | balanced |
| 电影感、高级、深度长文 | `typography` | `dark` | `screen-print` | title-only | bold |

---

## 预设快捷方式

常用组合一键选择：

| 预设名 | Type | Palette | Rendering | Font | 典型文章 |
|--------|------|---------|-----------|------|---------|
| `ai-product` | hero | tech-blue | 3d-icon | clean | AI产品拆解（**最常用**） |
| `methodology` | conceptual | insight-blue | flat-vector | clean | 方法论/框架文 |
| `bold-opinion` | typography | dark | screen-print | display | 观点输出/声明（mood=bold） |
| `pm-growth` | metaphor | warm | hand-drawn | handwritten | 个人成长/转型 |
| `versus` | split | tech-blue | 3d-icon | clean | 对比类文章 |
| `zen-core` | minimal | mono | flat-vector | serif | 极简深度文（mood=subtle） |
| `efficiency` | hero | action-orange | 3d-icon | clean | 效率/实战 |
| `trend-report` | hero | trend-cyan | digital | clean | 行业观察/数据 |
| `chalkboard` | conceptual | dark | chalk | handwritten | 教程/解释概念 |
| `watercolor` | metaphor | warm | painterly | serif | 文学/艺术/反思 |
| `cinematic` | hero | dark | screen-print | display | 电影感深度解读（mood=bold） |
| `dashboard` | conceptual | insight-blue | digital | clean | 数据分析/SaaS拆解 |

Text 默认 `title-only`，Mood 默认 `balanced`，除非预设标注（如 bold-opinion/cinematic → bold，zen-core → subtle）。

> ℹ️ 融合自 baoyu-cover-image v1.56.1 五维度体系 + Style Presets，适配公众号封面场景。

---

## 尺寸规范

| 用途 | 比例 | 生成尺寸 | 后处理 |
|------|------|---------|--------|
| 公众号封面 | 2.35:1 | `2560x1440`(16:9) | `sips -c 1090 2560` 裁剪 |
| 公众号次条 | 1:1 | `1920x1920` | 无 |
| 小红书封面 | 3:4 | `1680x2240` | 无 |

---

## Prompt 组装

### 步骤

1. **选定五维度**（自动推荐或手动选择）
2. **兼容矩阵校验**（检查 3 张矩阵无 ✗）
3. **存 prompt 文件**：`prompts/00-cover.md`（⛔ 先存后生）
4. **生成图片**
5. **裁剪**（如需 2.35:1）

### Prompt 模板

```markdown
---
type: [hero/conceptual/typography/metaphor/split/minimal]
palette: [配色名]
rendering: [渲染名]
text: [none/title-only/title-subtitle]
mood: [subtle/balanced/bold]
---

[渲染风格的 Prompt 关键词，从维度3表格中复制]

配色：[配色色值，从维度2表格中复制]

构图：[构图方式描述，从维度1表格中复制]

内容：
- 标题：「[中文标题]」
- 副标题：「[副标题，如有]」
- 视觉元素：[与文章主题相关的具象物体/抽象图形]

约束：
- 中文文字清晰可读
- 文字和视觉不重叠
- 不要 emoji
- 横版，高质量
```

### 生图调用

```bash
# 首选：idealab Chat API（团队AK免费）
<WORKSPACE>/scripts/generate-image.sh "[组装好的 prompt]" cover.jpg

# 降级：Seedream（idealab 不可用时）
<WORKSPACE>/scripts/seedream-generate.sh \
  "[组装好的 prompt]" \
  cover.jpg "2560x1440" 1

# 裁剪为 2.35:1
sips -c 1090 2560 cover.jpg
```

---

## 多方案选择

每次封面图出 **2-3 个方案**供老板选择：

```markdown
## 方案 A（推荐）
- 预设：ai-product（hero + tech-blue + 3d-icon）
- 视觉：[具体视觉元素描述]

## 方案 B
- 预设：bold-opinion（typography + dark + screen-print）
- 视觉：[具体视觉元素描述]

## 方案 C（可选）
- 预设：methodology（conceptual + insight-blue + flat-vector）
- 视觉：[具体视觉元素描述]
```

方案之间必须在 **Type 或 Rendering** 上有明显差异（不只是换配色）。

---

## 生图工具优先级

1. **idealab Chat API**（首选）：`<WORKSPACE>/scripts/generate-image.sh`，团队AK免费无额度压力，~25s/张
2. **Seedream 5.0 Lite**（降级）：`<WORKSPACE>/scripts/seedream-generate.sh`，0.22元/张，idealab不可用时
3. **DashScope qwen-image-2.0-pro**（中文文字专用）：当中文渲染失败时
4. **HTML 截图**（兜底）：typography 类型封面可用 HTML 精确控制文字

---

## 内容结构图（可选）

放在文章开头、封面图之后，帮读者一图看全文。

### 风格

Graphic Recording / Visual Thinking 手绘风格：
- 白纸背景，无横线
- 黑色细线笔轮廓 + 彩色标记（青色、橙色、柔和红色）
- 放射状布局，箭头连接
- 16:9 比例

### Prompt 模板

```
Create a hand-drawn sketch visual summary about [文章主题].
Clean white paper background, no lines.
Art style: graphic recording / visual thinking.
Black fine-tip pen for outlines and text.
Colored markers (cyan, orange, soft red) for emphasis.
Main title "[文章标题]" centered in a 3D rectangular box.
Surround with radially distributed simple doodles, icons, and diagrams:
- [要点1]
- [要点2]
- [要点3]
Connect ideas with arrows. Clear hand-written block letters.
Layout 16:9, high quality.
```

### 决策规则

- 文章 ≥ 3 个主要观点：建议生成
- 文章内容简单或时间紧迫：可跳过

---

## 质量检查

- [ ] 五维度组合通过兼容矩阵检查
- [ ] Prompt 已保存到 `prompts/00-cover.md`
- [ ] 中文文字清晰可读
- [ ] 颜色鲜明，吸引眼球
- [ ] 主题契合文章内容
- [ ] 视觉和文字不重叠
- [ ] 裁剪后比例正确（2.35:1）
