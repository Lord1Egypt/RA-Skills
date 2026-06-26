# Assembly Workflow

## Goal

输出单文件 HTML 演示文稿，优先高质量和稳定性，兼顾低 token 和移动端体验。

## Workflow

### 1. Confirm The Runtime

先读 `references/runtime.md`。

默认使用自定义单文件 HTML 演示运行时，不依赖特定模型或外部演示引擎。

### 2. Pick One Theme

先读 `references/theme-catalog.md`，只加载最匹配的单主题文件。

不要一次读取多个主题文件，避免无效占用 token。

优先使用脚本快速路由：

- `node scripts/get-theme-bundle.mjs --scene investor-pitch`
- `node scripts/recommend-deck.mjs --scene investor-pitch --density medium`

### 3. Pick 6-10 Layouts

从 `references/layout-system.md` 中选择适合的布局原型。

避免：

- 每页都不同
- 同套 deck 同时出现两种相互冲突的页面语言

### 4. Build A Slide Outline

先出大纲，再写 HTML。推荐格式：

1. 封面
2. 目录或开场观点
3. 章节页
4. 内容页
5. 数据页
6. 结尾页

如果需要快速拿结构化脚手架，运行：

- `node scripts/scaffold-deck.mjs --scene ai-product-launch --title "你的标题"`

如果已经有结构化内容，直接按 `references/content-schema.md` 准备 JSON 文件。

如果用户先给的是 markdown 提纲，优先转换：

- `node scripts/markdown-to-content.mjs --input examples/investor-pitch.md --output examples/investor-pitch.json --scene investor-pitch --mobile`

生成前可先校验：

- `node scripts/validate-content.mjs examples/investor-pitch.json`
- `node scripts/smoke-test.mjs`
- `node scripts/qa-deck.mjs --content examples/investor-pitch.json`

### 5. Generate HTML

规则：

- CSS 尽量内嵌
- 主题 token 用 CSS 变量统一管理
- 布局用可复用 class，不要每页写大量内联样式
- 动画只保留必要部分

如果只需要快速生成一个单文件 HTML 成品骨架，优先运行：

- `node scripts/generate-slide-html.mjs --scene investor-pitch --title "Investor Pitch" --out dist/investor-pitch.html`

如果已经有内容 JSON，优先运行：

- `node scripts/generate-slide-html.mjs --content examples/investor-pitch.json --out dist/investor-pitch.html`

生成后可做质量检查：

- `node scripts/qa-deck.mjs --content examples/investor-pitch.json --html dist/investor-pitch.html`

如果要导出首屏预览图：

- `node scripts/render-preview.mjs --input dist/investor-pitch.html --output dist/investor-pitch.png`
- `node scripts/build-preview-gallery.mjs`

### 6. Self Review

对照 `references/quality-bar.md` 自检：

- 是否有高级感
- 是否有信息层次
- 是否足够稳
- 是否移动端友好

## Token Discipline

### Keep In Main Context

- 当前用户需求
- 主 `SKILL.md`
- 1 个主题文件
- `layout-system.md`
- `quality-bar.md`

### Load Only If Needed

- 其他主题文件
- 具体单主题设计说明

## Implementation Hint

如果要做进一步工程化，可让脚本先根据场景输出：

- 推荐主题
- 推荐布局序列
- 推荐内容密度

然后再写最终 HTML，减少路由阶段的 token 消耗。
