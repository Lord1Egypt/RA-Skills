# Deck Studio 资源速查（Catalog）

> **目的**：deck-studio 子模块（html-ppt-skill）资源的快速查找手册
> **范围**：themes / layouts / animations / FX / full-deck 模板
> **数据快照**：基于本仓库当前下载的资源（36 themes / 31 single-page / 15 full-decks / 20 FX / 27 CSS animations）

## 1. 主题（36 themes）

按"使用场景"快速匹配。所有主题文件位于 `deck-studio/assets/themes/<name>.css`。

### 1.1 极简 / 商务

| 主题 | 适用场景 | 视觉特征 |
|---|---|---|
| `minimal-white` | 内部汇报、严肃话题 | 极简白，Inter，强文字层级 |
| `editorial-serif` | 品牌故事、长文演讲 | 杂志风 Playfair 衬线 + 奶油底 |
| `corporate-clean` | 董事会、B2B 销售 | 纯白 + 海军蓝 + Inter + 保守边框 |
| `pitch-deck-vc` | 融资路演、VC meeting | YC 风白底 + 蓝紫渐变 |
| `academic-paper` | 学术报告、会议论文 | 论文白 + 衬线 + 蓝链接 |
| `japanese-minimal` | 品牌升级、匠人故事 | 象牙白 + 朱红 + 极大留白 |

### 1.2 强调 / 视觉冲击

| 主题 | 适用场景 | 视觉特征 |
|---|---|---|
| `bauhaus` | 设计 talk、产品美学 | 几何 + 红黄蓝原色 |
| `memphis-pop` | 年轻、潮流、品牌合作 | 孟菲斯波普背景点 + 大字标题 |
| `magazine-bold` | 专栏文章、品牌月刊 | 奶油底 + 超大 Playfair + 橙色 spot |
| `midcentury` | 设计史、家居美学 | 奶油底 + 芥末/青/焦橙 |
| `neo-brutalism` | 设计系统、高辨识度 | 粗边框 + 高对比 + 硬阴影 |
| `sharp-mono` | 极简主义、黑白双色 | 锐利黑白 + 粗等宽字 |
| `sunset-warm` | 品牌故事、情感表达 | 暖色调橘/珊瑚/琥珀渐变 |
| `soft-pastel` | 生活分享、柔和调性 | 马卡龙粉蓝/淡紫/薄荷 |
| `rose-pine` | 创意、写作、浪漫 | 松木玫瑰低饱和度深色 |
| `retro-tv` | 怀旧、复古发布会 | 显像管圆角 + 扫描线 + 棕调 |
| `news-broadcast` | 新闻播报、官方信息 | 蓝底白色新闻频道风格 |
| `swiss-grid` | 极简主义、国际主义风格 | 瑞士网格 + 无衬线 + 严格对齐 |
| `glassmorphism` | Apple 发布会、产品特性 | 毛玻璃 + 多色光斑 |

### 1.3 暗色 / 开发者

| 主题 | 适用场景 | 视觉特征 |
|---|---|---|
| `catppuccin-mocha` | 开发者内部分享、长时间观看 | catppuccin 深色 |
| `dracula` | 代码密集的技术分享 | 经典 Dracula 紫红 |
| `gruvbox-dark` | Terminal / vim 社群 | 温暖复古深色 |
| `tokyo-night` | 开发者深夜分享、高颜值 | 东京夜蓝紫色深色 |
| `vaporwave` | 赛博美学、复古未来 | 蒸汽波动画渐变 |
| `terminal-green` | 黑客风、CLI demo | 绿屏终端 + CRT 效果 |
| `cyberpunk-neon` | 赛博朋克、发布 | 霓虹粉 + 青蓝 |

### 1.4 工程 / 文档

| 主题 | 适用场景 | 视觉特征 |
|---|---|---|
| `blueprint` | 系统架构、工程蓝图 | 蓝图工程 + 网格 + 蒙太奇 |
| `engineering-whiteprint` | API 文档、架构白皮书 | 白底 + 坐标纸 + 等宽字 |
| `solarized-light` | 学术、开源文档 | Solarized 浅色 + 科学感 |
| `arctic-cool` | 商业分析、金融 | 蓝/青/石板灰 |

### 1.5 氛围 / 渐变

| 主题 | 适用场景 | 视觉特征 |
|---|---|---|
| `aurora` | 封面 / CTA / 结语页 | 极光渐变 + blur + saturate |
| `nord` | 北欧、冷静专业 | 北欧蓝灰色系 |
| `rainbow-gradient` | 多彩发布会、创意展示 | 彩虹渐变点缀 + 亮色 |
| `y2k-chrome` | 千禧科技、金属质感 | 银色铬金属 + 反光 |
| `xiaohongshu-white` | 小红书图文、种草 | 白底高级感 + 柔色标签 |
| `catppuccin-latte` | 开发者友好的浅色 | catppuccin 浅 |

> ✅ 全部 36 个主题已从上游仓库下载完成。Agent 可直接使用任意主题。**36 个主题清单见上文各表。**

## 2. 布局（28 single-page templates）

所有布局位于 `deck-studio/templates/single-page/<name>.html`，每个都是带示例数据的独立可运行页。

### 2.1 开场与过渡

| 文件 | 用途 |
|---|---|
| `cover.html` | Deck 封面。Kicker + 巨型标题 + lede + pill 行 |
| `toc.html` | 目录。2×3 编号卡片网格 |
| `section-divider.html` | 大字号章节分隔（"02 · Theme"） |
| `thanks.html` | 结尾 "Thanks" 页 + 五彩纸屑 |

### 2.2 文本为中心

| 文件 | 用途 |
|---|---|
| `bullets.html` | 经典 bullet 列表，card 包裹项 |
| `two-column.html` | 概念 + 示例并排 |
| `three-column.html` | 三个等宽 pillar + 图标 |
| `big-quote.html` | 全幅 pull quote，editorial-serif 风格 |
| `comparison.html` | Before / After 双面板 |
| `pros-cons.html` | 优缺点双卡 |
| `todo-checklist.html` | 清单（已勾/未勾状态） |

### 2.3 数字与数据

| 文件 | 用途 |
|---|---|
| `stat-highlight.html` | 一个巨型数字 + 副标题（用 `.counter` 动画） |
| `kpi-grid.html` | 4 个 KPI 一行 + 涨跌 delta |
| `table.html` | 数据表 + hover + 数字右对齐 |
| `chart-bar.html` | Chart.js 柱状图（主题感知） |
| `chart-line.html` | Chart.js 双折线 + 填充区 |
| `chart-pie.html` | Chart.js 环形图 + takeaways 卡片 |
| `chart-radar.html` | Chart.js 雷达图，2 个产品 × 6 维度 |

### 2.4 代码与终端

| 文件 | 用途 |
|---|---|
| `code.html` | highlight.js 语法高亮（JS 示例） |
| `diff.html` | 手写 +/- diff 视图 |
| `terminal.html` | 终端窗口 mock + 红黄绿按钮 |

### 2.5 图表与流程

| 文件 | 用途 |
|---|---|
| `flow-diagram.html` | 5 节点流水线 + 箭头 + 1 个高亮节点 |
| `arch-diagram.html` | 3 层架构网格 |
| `process-steps.html` | 4 编号步骤卡片 |
| `mindmap.html` | 放射状思维导图 + SVG 路径动画 |
| `timeline.html` | 5 点水平时间轴 + 圆点 |
| `roadmap.html` | 4 列 NOW / NEXT / LATER / VISION |
| `gantt.html` | 12 周甘特图 + 5 个并行轨道 |

### 2.6 视觉

| 文件 | 用途 |
|---|---|
| `image-hero.html` | 全幅 hero + Ken Burns 渐变背景 |
| `image-grid.html` | 7 格 bento 网格 + 渐变占位 |

### 2.7 行动

| 文件 | 用途 |
|---|---|
| `cta.html` | CTA，大渐变标题 + 按钮 |

## 3. 完整 deck 模板（15 full-decks）

位于 `deck-studio/templates/full-decks/<name>/`，每个是自包含的目录（带 scoped `style.css` + `README.md`）。

| 模板 | 类型 | 用途 | 适用场景 |
|---|---|---|---|
| `product-launch-bento/` | scenario | 产品发布会 deck | 9-15 页产品介绍 + demo + 路线图 |
| `agent-orchestration/` | scenario | Agent 编排演示 | AI Agent 工作流/编排展示 |
| `storybook-presentation/` | scenario | 叙事风格分享 | 故事化品牌叙事 |
| `tech-vision/` | scenario | 技术愿景宣讲 | 技术战略/赋能分享 |
| `full-deck-engine/` | scenario | 完整 deck 引擎 | 通用全页模板 |
| `xhs-white-editorial/` | extracted | 白底杂志风 | 小红书图文/观点输出 |
| `graphify-dark-graph/` | extracted | 暗底知识图谱 | AI/数据产品展示 |
| `knowledge-arch-blueprint/` | extracted | 奶油蓝图架构 | 架构设计/系统思考 |
| `hermes-cyber-terminal/` | extracted | 暗终端 cyber | 开发者工具/Agent demo |
| `obsidian-claude-gradient/` | extracted | GitHub 暗紫渐变 | 工具 walkthrough/LLM 产品 |
| `testing-safety-alert/` | extracted | 红琥珀警示 | 安全/测试/风险主题 |
| `xhs-pastel-card/` | extracted | 柔和马卡龙 | 生活方式/情感内容 |
| `xhs-post/` | scenario | 小红书 3:4 图文 | 小红书/IG 轮播 |
| `dir-key-nav-minimal/` | extracted | 方向键 8 色极简 | Keynote/单页概念 |
| `presenter-mode-reveal/` | scenario | 演讲者模式 + 逐字稿 | 技术分享/带演讲稿的 talk |

## 4. CSS 动画（27 named entry animations）

位于 `deck-studio/assets/animations/animations.css`。用法：

```html
<h1 class="anim-fade-up">标题</h1>
<ul class="anim-stagger-list">
  <li>...</li>
</ul>
<!-- 或用 data-anim，runtime.js 会在 slide 进入时重新触发 -->
<div data-anim="rise-in">...</div>
```

### 4.1 方向性淡入

| 名称 | 效果 | 用途 |
|---|---|---|
| `fade-up` | 从 +32px 升起 + 淡入 | 段落、card 默认入场 |
| `fade-down` | 从 -32px 落下 + 淡入 | 标题、横幅、警示 |
| `fade-left` | 从 -40px 滑入 | 双列布局的左列 |
| `fade-right` | 从 +40px 滑入 | 双列布局的右列 |

### 4.2 戏剧性入场

| 名称 | 效果 | 用途 |
|---|---|---|
| `rise-in` | +60px 升起 + blur 清除 | slide 标题、hero 标题 |
| `drop-in` | -60px 落下 + 微缩放 | 横幅、警示栏 |
| `zoom-pop` | scale 0.6→1.04→1 | 按钮、stat 数字、CTA |
| `blur-in` | 18px blur 清除 | 封面揭示 |
| `glitch-in` | clip-path 阶梯 + 抖动 | 科技 / 赛博 / 错误状态 |

### 4.3 文本效果

| 名称 | 效果 | 用途 |
|---|---|---|
| `typewriter` | 等宽逐字 | 一句话、slogan |
| `neon-glow` | 周期性 text-shadow 脉冲 | terminal-green / dracula |
| `shimmer-sweep` | 白色高光扫过 | 金属按钮、高级卡片 |
| `gradient-flow` | 无限横向渐变滑动 | 品牌字标 |

### 4.4 列表与数字

| 名称 | 效果 | 用途 |
|---|---|---|
| `stagger-list` | 子元素逐个 rise-in | 任何 `<ul>` / `.grid` |
| `counter-up` | 数字 0→target 跳动 | KPI、stat-highlight 页 |

### 4.5 SVG / 几何

| 名称 | 效果 | 用途 |
|---|---|---|
| `path-draw` | 线条自动绘制 | 线条、箭头、图表 |
| `morph-shape` | path `d` 形变 | 背景形状 |

### 4.6 3D 与透视

| 名称 | 效果 | 用途 |
|---|---|---|
| `parallax-tilt` | hover → 3D 倾斜 | hero 卡片、产品图 |
| `card-flip-3d` | Y 轴 90° 翻转 | Before/After 揭示 |
| `cube-rotate-3d` | 从立方体侧面旋入 | 章节分隔 |
| `page-turn-3d` | 左侧铰链翻页 | 编辑/故事流 |
| `perspective-zoom` | 从 -400 Z 拉近 | 封面开场 |

### 4.7 环境 / 持续

| 名称 | 效果 | 用途 |
|---|---|---|
| `marquee-scroll` | 无限横向滚动 | 客户 logo 滚动条 |
| `kenburns` | 14s 慢速缩放 | hero 背景 |
| `confetti-burst` | 伪元素火花爆发 | Thanks / 胜利页 |
| `spotlight` | 圆形 clip-path 揭示 | 重大揭示时刻 |
| `ripple-reveal` | 角落起点波纹揭示 | 章节过渡 |

## 5. 画布 FX（20 canvas effects）

位于 `deck-studio/assets/animations/fx/<name>.js`，需要 `fx-runtime.js` 引导。

用法：

```html
<div data-fx="knowledge-graph"></div>
<script src="../assets/animations/fx-runtime.js"></script>
```

| 名称 | 视觉效果 | 适用场景 |
|---|---|---|
| `_util` | 共享工具 | — |
| `chain-react` | 节点反应式扩散 | 复杂系统、分布式架构 |
| `confetti-cannon` | 五彩纸屑大炮 | Thanks、庆祝、达成 |
| `constellation` | 星座连线 | 数据点聚类、关系图 |
| `counter-explosion` | 数字爆炸粒子 | KPI 揭示、目标达成 |
| `data-stream` | 流动数据流 | 监控、IoT、实时数据 |
| `firework` | 烟花 | Thanks、庆功、新年 |
| `galaxy-swirl` | 星系漩涡 | 宏观、探索、宇宙感 |
| `gradient-blob` | 渐变 blob 形变 | 抽象背景、封面 |
| `knowledge-graph` | 知识图谱 | AI、知识库、关系网络 |
| `letter-explode` | 字母爆炸 | 标题、slogan、宣言 |
| `magnetic-field` | 磁力场 | 物理、吸引、互动 |
| `matrix-rain` | 矩阵雨 | 赛博、黑客、复古 |
| `neural-net` | 神经网络 | AI、ML、深度学习 |
| `orbit-ring` | 轨道环 | 行星、循环、调度 |
| `particle-burst` | 粒子爆发 | 通用点击/触发效果 |
| `shockwave` | 冲击波 | 重要节点、影响范围 |
| `sparkle-trail` | 闪光轨迹 | 鼠标跟随、互动路径 |
| `starfield` | 星海 | 太空、深度、背景 |
| `typewriter-multi` | 多行打字机 | 故事化叙事、对话 |
| `word-cascade` | 文字瀑布 | 关键词墙、灵感迸发 |

## 6. 启动 deck 的最小骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>My Talk</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="../deck-studio/assets/base.css">
  <link rel="stylesheet" id="theme-link" href="../deck-studio/assets/themes/aurora.css">
  <link rel="stylesheet" href="../deck-studio/assets/fonts.css">
</head>
<body data-themes="aurora,dracula,catppuccin-mocha,japanese-minimal">

  <header class="deck-header">
    <span class="deck-title">My Talk</span>
    <span class="slide-number"></span>
  </header>

  <main class="deck">
    <section class="slide is-active" data-screen-label="01 Cover">
      <h1 class="anim-fade-up">标题</h1>
      <p class="anim-fade-up">副标题</p>
    </section>

    <section class="slide" data-screen-label="02 Content">
      <h1 class="anim-fade-up">第二页</h1>
      <ul class="anim-stagger-list">
        <li>要点 1</li>
        <li>要点 2</li>
      </ul>
    </section>

    <!-- 更多 slide -->
  </main>

  <div class="progress"></div>

  <script src="../deck-studio/assets/runtime.js"></script>

  <aside class="notes">
    <!-- 这一页的演讲稿（150-300 字，按 S 弹出） -->
  </aside>

</body>
</html>
```

## 7. 路由速查（给 Agent）

| 用户说 | 用 |
|---|---|
| "做一份 deck" | `deck-studio/templates/deck.html` 起步 |
| "做 pitch" | `deck-studio/templates/full-decks/pitch-deck/` |
| "做产品发布" | `deck-studio/templates/full-decks/product-launch/` |
| "技术分享" | `deck-studio/templates/full-decks/tech-sharing/` |
| "带演讲稿" | `deck-studio/templates/full-decks/tech-sharing/`（已含 speaker notes） |
| "周报" | `deck-studio/templates/full-decks/weekly-report/` |
| "课程" | `deck-studio/templates/full-decks/course-module/` |
| "小红书图文" | `deck-studio/templates/single-page/image-grid.html` |
| "KPI 大屏" | `deck-studio/templates/single-page/kpi-grid.html` |
| "架构图" | `deck-studio/templates/single-page/arch-diagram.html` |
| "流程图" | `deck-studio/templates/single-page/flow-diagram.html` |
| "数据图表" | `chart-bar.html` / `chart-line.html` / `chart-pie.html` |
| "代码讲解" | `deck-studio/templates/single-page/code.html` |
| "终端演示" | `deck-studio/templates/single-page/terminal.html` |
| "结尾感谢" | `deck-studio/templates/single-page/thanks.html` |
