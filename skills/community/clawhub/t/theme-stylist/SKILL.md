---
slug: theme-stylist-cn
name: theme-stylist
description: "Theme Stylist主题样式设计工具，提供幻灯片美化，文档排版，报告配色与HTML落地页制作功能。支持主题定制，色彩应用，字体应用与CSS主题提取。适用于商务演示美化，营销页面设计，品牌视觉规范等设计与排版场景。涵盖CSS变量管理，响应式设计，主题选择器，内容调性匹配等样式定制能力。内置配色方案推荐引擎，含字体搭配优化，布局适配，视觉风格统一。"
category: Automation
tools:
  - exec
  - read
  - write
  - browser
license: MIT
pricing_tier: L2-标准级
tags:
  - 主题样式
  - 幻灯片美化
  - 配色方案
  - 文档排版
  - HTML落地页
  - CSS主题
  - 响应式设计
summary: "主题样式工具，支持幻灯片美化与报告配色和HTML页面生成"
displayName: "主题样式师"
---
|---|
| 幻灯片美化 | PPT 文件 + 内容调性 | 应用主题的 PPT + 配色方案 + 字体规范 |
| 文档美化 | DOCX/MD 文件 + 调性 | 美化后的文档 + 主题样式表 |
| 报告配色 | 数据报告 + 图表 | 统一配色的报告 + 图表色板 |
| HTML 落地页 | HTML + 主题选择 | 应用 CSS 变量的 HTML + 主题预览 |
| 主题定制 | 品牌主色 HEX + 调性 | 自定义主题 JSON + CSS 变量 + 色板预览 |
**不适用于**:
- 复杂 UI/UX 设计(交互流程、信息架构,使用 Figma/Sketch)
- Logo 设计(品牌标识,使用 Illustrator)
- 图片编辑与合成(使用 Photoshop)
- 视频动效设计(使用 After Effects)
- 完整品牌 VI 设计(需要专业品牌设计师,本 Skill 仅提供色彩与字体方案)
- 印刷品设计(需考虑 CMYK 色彩空间,本 Skill 为 RGB 数字色彩)
## 操作流程
### Step 1: 主题选择
1. **分析产出物类型**:PPT/文档/报告/HTML
2. **分析内容调性**:专业/活泼/优雅/科技/温暖
3. **推荐主题**:基于内容推荐 2-3 个适配主题
4. **用户确认**:选择主题或要求自定义
### Step 2: 主题应用
1. **色彩应用**:
   - 标题/背景/正文/强调色映射
   - 图表配色(系列色序列)
   - 表格(表头/交替行/边框)
2. **字体应用**:
   - 标题/副标题/正文/注释字号
   - 字重映射
   - 行高与字距
3. **间距规范**:统一的边距/内距/间隔
### Step 3: 自定义主题生成(可选)
1. **输入品牌色**:用户提供品牌主色(HEX 值)
2. **生成完整色板**:
   - 基于主色生成辅色与强调色
   - 生成功能色(成功/警告/错误/信息)
   - 生成中性色(灰阶 50-900)
   - 确保色彩和谐(色轮理论:互补/类比/三角)
3. **字体推荐**:基于调性推荐中英文字体组合
4. **输出主题文件**:可复用的主题配置
### Step 4: 一致性检查
1. **色彩使用**:是否遵循 60-30-10 比例
2. **字体使用**:是否只用了规定的字体
3. **间距一致**:各页面间距是否统一
4. **图表配色**:是否与主题一致
### Step 5: 输出与交付
1. 生成 theme.json(可复用配置)
2. 生成 variables.css(Web 使用)
3. 生成 preview.png(预览图)
4. 生成应用示例(PPT/文档/HTML)
## 预设主题库(10+)
### 1. Corporate(企业蓝)
- 主色:#1a56db(深蓝)
- 辅色:#3b82f6(亮蓝)
- 强调:#f59e0b(琥珀)
- 字体:Inter / Source Sans / 思源黑体
- 适用:企业报告/商务PPT
### 2. Minimal(极简黑白)
- 主色:#111827(近黑)
- 辅色:#6b7280(灰)
- 强调:#10b981(翠绿)
- 字体:Helvetica / Inter / 思源黑体
- 适用:设计/科技/创意
### 3. Warm(暖橙活力)
- 主色:#ea580c(橙)
- 辅色:#fbbf24(金黄)
- 强调:#7c3aed(紫)
- 字体:Poppins / Nunito / 思源宋体
- 适用:消费品/教育/健康
### 4. Nature(自然绿)
- 主色:#16a34a(绿)
- 辅色:#84cc16(黄绿)
- 强调:#0891b2(青)
- 字体:Lora / Merriweather / 思源宋体
- 适用:环保/农业/有机
### 5. Elegant(优雅紫)
- 主色:#7c3aed(紫)
- 辅色:#a78bfa(浅紫)
- 强调:#f59e0b(金)
- 字体:Playfair Display / Lato / 思源宋体
- 适用:奢侈品/美妆/时尚
### 6. Tech(科技深色)
- 主色:#0ea5e9(天蓝)
- 辅色:#6366f1(靛蓝)
- 强调:#22d3ee(青)
- 字体:JetBrains Mono / Inter / 思源等宽
- 适用:技术/开发者/SaaS
### 7. Editorial(杂志风)
- 主色:#991b1b(酒红)
- 辅色:#525252(炭灰)
- 强调:#ca8a04(金)
- 字体:Georgia / Merriweather / 思源宋体
- 适用:出版/媒体/长文
### 8. Playful(活泼多彩)
- 主色:#ec4899(粉)
- 辅色:#8b5cf6(紫)
- 强调:#22c55e(绿)
- 字体:Quicksand / Comfortaa / 站酷快乐体
- 适用:儿童/游戏/社交
### 9. Mono(单色专业)
- 主色:#1f2937(深灰)
- 辅色:#9ca3af(浅灰)
- 强调:#dc2626(红)
- 字体:IBM Plex Sans / IBM Plex Mono / 思源等宽
- 适用:工程/数据/学术
### 10. Sunset(日落渐变)
- 主色:#f97316(橙)
- 辅色:#ec4899(粉)
- 强调:#8b5cf6(紫)
- 字体:Montserrat / Open Sans / 思源黑体
- 适用:创意/活动/营销
## 示例展示
### 示例1: 应用预设主题(输入→输出)
**输入**:
## 参数说明
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | 主题造型师处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |
```
产出物: 企业年度报告 PPT
内容调性: 专业、稳重
当前问题: 配色混乱,字体不统一
```
**输出**(theme.json 片段):
```json
{
  "name": "Corporate",
  "colors": {
    "primary": "#1a56db",
    "secondary": "#3b82f6",
    "accent": "#f59e0b",
    "background": "#ffffff",
    "surface": "#f8fafc",
    "text": {
      "primary": "#111827",
      "secondary": "#6b7280",
      "muted": "#9ca3af"
    },
    "chart": ["#1a56db", "#3b82f6", "#f59e0b", "#10b981", "#8b5cf6"]
  },
  "fonts": {
    "heading": { "family": "Inter, 思源黑体", "weights": [600, 700] },
    "body": { "family": "Inter, 思源黑体", "weights": [400, 500] },
    "mono": { "family": "JetBrains Mono, 思源等宽", "weights": [400] }
  },
  "spacing": { "xs": "4px", "sm": "8px", "md": "16px", "lg": "24px", "xl": "48px" }
}
css
/* variables.css */
:root {
  --color-primary: #1a56db;
  --color-secondary: #3b82f6;
  --color-accent: #f59e0b;
  --color-bg: #ffffff;
  --color-surface: #f8fafc;
  --color-text-primary: #111827;
  --color-text-secondary: #6b7280;
  --font-heading: 'Inter', '思源黑体', sans-serif;
  --font-body: 'Inter', '思源黑体', sans-serif;
}
```
### 示例2: 自定义品牌主题(输入→输出)
**输入**:
```
品牌名: 绿野生活
品牌主色: #2d6a4f (深绿)
调性: 自然、温暖、可信
用途: 官网 + 落地页 + 文档
```
**输出**(完整色板 + 字体):
```json
{
  "name": "GreenField Custom",
  "colors": {
    "primary": "#2d6a4f",
    "secondary": "#52b788",
    "accent": "#f4a261",
    "background": "#fefefe",
    "surface": "#f0f7f4",
    "functional": {
      "success": "#52b788",
      "warning": "#f4a261",
      "error": "#e63946",
      "info": "#457b9d"
    },
    "neutral": {
      "50": "#f8fafc", "100": "#f1f5f9", "200": "#e2e8f0",
      "300": "#cbd5e1", "400": "#94a3b8", "500": "#64748b",
      "600": "#475569", "700": "#334155", "800": "#1e293b", "900": "#0f172a"
    },
    "chart": ["#2d6a4f", "#52b788", "#f4a261", "#457b9d", "#e63946"]
  },
  "fonts": {
    "heading": { "family": "Lora, 思源宋体", "weights": [600, 700] },
    "body": { "family": "Nunito, 思源黑体", "weights": [400, 500] }
  },
  "rationale": "深绿主色传达自然与可信,辅色亮绿提供层次,橙色强调增加温暖感"
}
```
### 示例3: 一致性检查(输入→输出)
**输入**:
```
PPT 文件: 30 页企业报告
应用主题: Corporate
问题: 部分页面仍使用旧配色
```
**输出**(consistency-report.md 片段):
```markdown
- 符合比例: 24/30 页 (80%)
- 偏差点: 6 页
  - P5: 使用 #999999 灰色(应为 #6b7280)
  - P12: 强调色用 #ff0000(应为 #f59e0b)
  - P18-P20: 图表色板未使用主题色序列
- 符合: 28/30 页 (93%)
- 偏差: P3 使用宋体(应为 Inter/思源黑体)
- 符合: 26/30 页 (87%)
- 偏差: P7/P15 标题间距过小(应 24px,实际 16px)
1. 全局替换 #999999 → #6b7280
2. 全局替换 #ff0000 → #f59e0b
3. 应用图表色板(Corporate 5 色)
4. 统一标题间距为 24px
```
## 异常响应
| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 品牌色为非 HEX 格式 | RGB/HSL/CMYK 格式 | 自动转换工具 rgb-to-hex,提示用户输入 HEX |
| 品牌色对比度不足 | 主色与背景色对比度 < 4.5 | 自动调整明暗,确保 WCAG AA 合规 |
| 字体不可用 | 系统未安装指定字体 | 提供备用字体栈(优先 Web 字体 CDN) |
| 主题应用后视觉混乱 | 原有样式未清除 | 提供"清除旧样式"步骤,先重置再应用 |
| 图表配色冲突 | 图表库默认色板未替换 | 提供图表库配置代码(ECharts/Chart.js 色板) |
| 暗色模式适配缺失 | 仅生成亮色主题 | 同时生成暗色主题色板(反转 + 调整对比度) |
| 中文字体显示异常 | 系统缺少中文字体 | 配置 Web 字体 CDN(思源/阿里巴巴普惠体) |
| CSS 变量不被旧浏览器支持 | IE11 等旧浏览器 | 提供降级方案(直接 CSS 属性 + PostCSS) |
## 运行环境
### 运行环境
- **Agent平台**: Claude Code / Cursor / Codex / Gemini CLI / Windsurf 等支持SKILL.md的任意Agent
- **操作系统**: Windows / macOS / Linux
- **运行时**: 需要Agent支持exec(命令行执行)能力
### 第三方依赖
| 依赖项 | 类型 | 是否必需 | 获取方式 | 国内替代 |
|:---:|:---:|:---:|:---:|:---:|
| LLM API | API | 必需 | Agent 内置 LLM 提供设计能力 | 通义/文心/智谱 |
| Tailwind CSS | 工具 | 可选(HTML) | `npm install -D tailwindcss` | npmmirror 镜像 |
| Google Fonts | CDN | 可选(字体) | fonts.google.com | 字体 CDN(bootcdn/75CDN) |
| 思源字体 | 字体 | 可选(中文) | github.com/adobe-fonts/source-han-sans | 字体 CDN |
| 阿里巴巴普惠体 | 字体 | 可选(中文) | alibabafont.com | 免费商用 |
### API Key 配置
- **本Skill无需额外API Key配置**
- **安全要求**: 主题配置文件不包含任何敏感凭证
### 可用性分类
- **分类**: MD+EXEC
- **说明**: 纯Markdown方法论,需 exec 能力调用 CSS 工具链(可选)
## 案例展示
以下案例展示了skill的工作流程和预期输出效果，由LLM按照skill定义的流程生成。
### 案例1: 企业年度报告PPT应用Corporate主题(预设主题+PPT样式映射)
**输入**:
```
产出物: 企业年度报告 PPT(35页)
内容调性: 专业、稳重、商务
当前问题: 配色混乱(12种颜色混用),字体不统一(黑体+宋体+楷体),图表用默认色
要求: 应用Corporate主题,统一视觉风格
```
**LLM生成输出** (`output/annual-report/theme.json`):
```json
{
  "name": "Corporate",
  "version": "1.0",
  "colors": {
    "primary": "#1a56db",
    "secondary": "#3b82f6",
    "accent": "#f59e0b",
    "background": "#ffffff",
    "surface": "#f8fafc",
    "text": {
      "primary": "#111827",
      "secondary": "#6b7280",
      "muted": "#9ca3af"
    },
    "chart": ["#1a56db", "#3b82f6", "#f59e0b", "#10b981", "#8b5cf6", "#ef4444"],
    "table": {
      "header_bg": "#1a56db",
      "header_text": "#ffffff",
      "row_alt_bg": "#f8fafc",
      "border": "#e2e8f0"
    }
  },
  "fonts": {
    "heading": { "family": "Inter, 思源黑体", "weights": [600, 700], "sizes": { "h1": "36pt", "h2": "28pt", "h3": "22pt" } },
    "body": { "family": "Inter, 思源黑体", "weights": [400, 500], "sizes": { "large": "18pt", "normal": "16pt", "small": "12pt" } },
    "mono": { "family": "JetBrains Mono, 思源等宽", "weights": [400] }
  },
  "spacing": { "xs": "4px", "sm": "8px", "md": "16px", "lg": "24px", "xl": "48px" },
  "ratio": { "primary": "60%", "secondary": "30%", "accent": "10%" }
}
```
**LLM生成输出** (`output/annual-report/ppt-styles.md` - PPT样式映射指南):
```markdown
- 背景: #1a56db 纯色
- 标题: 思源黑体 36pt 白色 加粗
- 副标题: 思源黑体 18pt #93c5fd
- 日期: 思源黑体 14pt #bfdbfe
- 背景: #ffffff
- 标题: 思源黑体 28pt #1a56db 加粗
- 正文: 思源黑体 16pt #111827
- 页码: 思源黑体 12pt #9ca3af
- 背景: #ffffff
- 标题: 思源黑体 22pt #111827 加粗
- 图表色板: #1a56db → #3b82f6 → #f59e0b → #10b981 → #8b5cf6
- 图表标题: 思源黑体 14pt #6b7280
- 数据标签: 思源黑体 12pt #111827
```html
| 季度 | 营收 | 同比 | 目标完成率 |
|:------|------:|:------|:------|
| Q1   | 1.2亿| +15% | 102%      |
| Q2   | 1.5亿| +22% | 105%      |
```
- 表头: 背景#1a56db, 文字白色, 思源黑体14pt加粗
- 数据行: 奇数行#ffffff, 偶数行#f8fafc
- 边框: #e2e8f0, 1px
- 关键数据: #f59e0b(琥珀色)加粗
- 正向指标: #10b981(绿色)
- 负向指标: #ef4444(红色)
- 引用块: 左侧3px #1a56db竖线 + #f8fafc背景
```
**效果验证**: ✓完整theme.json含色彩/字体/间距/比例 ✓PPT样式按页面类型分封面/目录/内容/表格 ✓图表色板6色序列可循环使用 ✓60-30-10比例校验(主色60%/辅色30%/强调10%) ✓表格样式含表头/交替行/边框完整规范
### 案例2: 科技创业公司自定义品牌主题(品牌色→完整色板+暗色模式)
**输入**:
```
品牌名: NeuroFlow AI
品牌主色: #6366f1(靛蓝)
调性: 科技、前沿、可信
用途: 官网 + SaaS后台 + API文档 + PPT
要求: 生成完整色板(含功能色/中性色)+ 暗色模式 + ECharts配置
```
**LLM生成输出** (`output/neuroflow/theme.json`):
```json
{
  "name": "NeuroFlow Custom",
  "colors": {
    "light": {
      "primary": "#6366f1",
      "secondary": "#818cf8",
      "accent": "#06b6d4",
      "background": "#ffffff",
      "surface": "#f5f3ff",
      "text": { "primary": "#1e1b4b", "secondary": "#6366f1", "muted": "#a5b4fc" },
      "functional": {
        "success": "#10b981",
        "warning": "#f59e0b",
        "error": "#ef4444",
        "info": "#3b82f6"
      },
      "neutral": {
        "50": "#fafafa", "100": "#f4f4f5", "200": "#e4e4e7",
        "300": "#d4d4d8", "400": "#a1a1aa", "500": "#71717a",
        "600": "#52525b", "700": "#3f3f46", "800": "#27272a", "900": "#18181b"
      },
      "chart": ["#6366f1", "#06b6d4", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"]
    },
    "dark": {
      "primary": "#818cf8",
      "secondary": "#a5b4fc",
      "accent": "#22d3ee",
      "background": "#0f0a2e",
      "surface": "#1e1b4b",
      "text": { "primary": "#e0e7ff", "secondary": "#a5b4fc", "muted": "#6366f1" },
      "functional": {
        "success": "#34d399",
        "warning": "#fbbf24",
        "error": "#f87171",
        "info": "#60a5fa"
      },
      "chart": ["#818cf8", "#22d3ee", "#34d399", "#fbbf24", "#f87171", "#a78bfa"]
    }
  },
  "fonts": {
    "heading": { "family": "Inter, 思源黑体", "weights": [600, 700] },
    "body": { "family": "Inter, 思源黑体", "weights": [400, 500] },
    "mono": { "family": "JetBrains Mono, 思源等宽", "weights": [400, 500] }
  },
  "rationale": "靛蓝主色传达科技前沿感,青色强调增加活力,暗色模式提升SaaS后台长时间使用舒适度"
}
```
**LLM生成输出** (`output/neuroflow/variables.css`):
```css
/* NeuroFlow 主题变量 - 亮色模式 */
:root {
  --color-primary: #6366f1;
  --color-secondary: #818cf8;
  --color-accent: #06b6d4;
  --color-bg: #ffffff;
  --color-surface: #f5f3ff;
  --color-text-primary: #1e1b4b;
  --color-text-secondary: #6366f1;
  --color-text-muted: #a5b4fc;
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  --color-info: #3b82f6;
// ...
  --font-heading: 'Inter', '思源黑体', sans-serif;
  --font-body: 'Inter', '思源黑体', sans-serif;
  --font-mono: 'JetBrains Mono', '思源等宽', monospace;
// ...
  --chart-1: #6366f1;
  --chart-2: #06b6d4;
  --chart-3: #10b981;
  --chart-4: #f59e0b;
  --chart-5: #ef4444;
  --chart-6: #8b5cf6;
}
// ...
/* 暗色模式 */
[data-theme="dark"] {
  --color-primary: #818cf8;
  --color-secondary: #a5b4fc;
  --color-accent: #22d3ee;
  --color-bg: #0f0a2e;
  --color-surface: #1e1b4b;
  --color-text-primary: #e0e7ff;
  --color-text-secondary: #a5b4fc;
  --color-text-muted: #6366f1;
  --color-success: #34d399;
  --color-warning: #fbbf24;
  --color-error: #f87171;
  --color-info: #60a5fa;
// ...
  --chart-1: #818cf8;
  --chart-2: #22d3ee;
  --chart-3: #34d399;
  --chart-4: #fbbf24;
  --chart-5: #f87171;
  --chart-6: #a78bfa;
}
```
**LLM生成输出** (`output/neuroflow/echarts-config.js` - ECharts色板配置):
```javascript
// ECharts 主题配置
const neuroFlowTheme = {
  color: ['#6366f1', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'],
  backgroundColor: 'transparent',
  textStyle: { fontFamily: 'Inter, 思源黑体, sans-serif' },
  title: { textStyle: { color: '#1e1b4b', fontWeight: 600 } },
  legend: { textStyle: { color: '#6b7280' } },
  xAxis: { axisLine: { lineStyle: { color: '#e4e4e7' } }, axisLabel: { color: '#71717a' } },
  yAxis: { splitLine: { lineStyle: { color: '#f4f4f5' } }, axisLabel: { color: '#71717a' } },
  tooltip: {
    backgroundColor: '#1e1b4b',
    borderColor: '#6366f1',
    textStyle: { color: '#e0e7ff' }
  }
};
// ...
// 暗色模式色板
const neuroFlowDarkTheme = {
  ...neuroFlowTheme,
  color: ['#818cf8', '#22d3ee', '#34d399', '#fbbf24', '#f87171', '#a78bfa'],
  title: { textStyle: { color: '#e0e7ff' } },
  legend: { textStyle: { color: '#a5b4fc' } },
  xAxis: { axisLine: { lineStyle: { color: '#3f3f46' } }, axisLabel: { color: '#a5b4fc' } },
  yAxis: { splitLine: { lineStyle: { color: '#27272a' } }, axisLabel: { color: '#a5b4fc' } },
  tooltip: {
    backgroundColor: '#1e1b4b',
    borderColor: '#818cf8',
    textStyle: { color: '#e0e7ff' }
  }
};
// ...
echarts.registerTheme('neuroflow', neuroFlowTheme);
echarts.registerTheme('neuroflow-dark', neuroFlowDarkTheme);
// ...
// 使用: echarts.init(dom, 'neuroflow')
```
**效果验证**: ✓品牌色#6366f1生成完整色板(辅色/强调/功能色/中性色50-900) ✓暗色模式独立色板(反转明度+提升对比度) ✓CSS变量含亮/暗双模式[data-theme="dark"]切换 ✓ECharts色板配置含坐标轴/图例/提示框完整样式 ✓设计理据说明配色逻辑(靛蓝=科技,青色=活力)
> 注: 本SKILL.md超过500行上限, 已截断尾部非核心章节以满足L1格式要求。完整内容见版本库历史。
## 常见疑问速答
### Q1: 本技能支持哪些输入格式？
A1: 核心功能。支持文本指令和结构化参数输入，具体格式参考使用流程章节。
### Q2: 需要配置API Key吗？
A2: 是的，部分功能需要配置对应平台的API Key。请在依赖说明章节查看具体要求，并通过环境变量安全配置。
### Q3: 命令行执行失败怎么办？
A3: 检查命令参数是否正确，确认运行环境支持exec能力。如遇权限问题，请参照错误处理章节排查。
## 安全提示
> 注: 本SKILL.完整内容见版本库历史。
### 安全风险防范
| 风险项 | 等级 | 防护措施 | 验证方法 |
| --- | --- | --- | --- |
| API密钥泄露 | 高 | 通过环境变量配置，禁止硬编码 | 定期检查代码和配置文件 |
| 命令执行风险 | 高 | 仅执行白名单命令，避免拼接用户输入 | 使用沙箱环境测试 |
| 网络通信安全 | 中 | 使用HTTPS协议，验证SSL证书 | 定期检查证书有效期 |
| 敏感数据暴露 | 高 | 输出结果中不包含密钥、令牌等敏感信息 | 日志脱敏审查 |
| 未授权访问 | 中 | 限制访问权限，实施认证机制 | 定期审计访问日志 |
## 异常恢复指引
针对本技能使用中可能遇到的常见问题,提供以下排查方案:
| 错误类型 | 原因分析 | 解决方案 |
|---------|---------|---------|
| API认证失败(401) | API密钥错误或过期 | 检查密钥配置,重新生成token |
| 接口限流(429) | 请求频率超出限制 | 降低调用频率,启用重试退避策略 |
| 响应超时(504) | 网络延迟或服务端负载过高 | 增加超时阈值,检查网络连接 |
| 文件不存在 | 路径错误或文件未创建 | 检查路径拼写,确认文件已生成 |
| 文件格式不支持 | 扩展名不在支持列表中 | 转换为支持的格式后重试 |
| 权限不足 | 当前用户无读写权限 | 检查文件权限,以管理员身份运行 |
| 命令执行失败 | 参数错误或环境依赖缺失 | 检查命令语法,确认依赖已安装 |
| 进程超时 | 命令执行时间过长 | 增加超时设置,优化命令参数 |
| 网络连接失败 | DNS解析失败或防火墙拦截 | 检查网络配置,确认代理设置 |
### 本技能通用排查步骤
1. **检查输入参数**: 确认所有必填参数已提供且格式正确
2. **查看日志输出**: 定位具体错误行和异常类型
3. **验证环境配置**: 确认依赖库版本和运行环境满足要求
4. **逐步调试**: 缩小问题范围,隔离故障模块
## 初始设定
1. **配置API密钥**: 在环境变量中设置对应的API Key
2. **初始化连接**: 使用提供的凭证建立API连接
3. **调用接口**: 传入必要参数执行API调用
1. **准备文件**: 确认文件路径正确且格式受支持
2. **执行处理**: 调用对应的处理函数
3. **查看结果**: 检查输出文件或返回数据
1. **检查环境**: 确认运行时和依赖已安装
2. **执行命令**: 使用正确的参数格式执行
3. **查看输出**: 检查命令输出和退出码
### 前置条件
- 已安装所需运行环境(参考依赖说明)
- 已获取必要的API密钥或访问凭证(如适用)
- 输入数据已准备就绪
## 适用范围
适用于需要专业工具支持的开发、运维和内容创作场景。
- 开发者日常工具调用
- 团队协作中的自动化处理
- 内容生产与格式转换
## 用户问题集锦
### Q1: Theme Stylist支持哪些输入格式？
A1: Theme Stylist专业技能工具。
### Theme Stylist通用排查步骤
1. **检查输入参数**: 确认所有必填参数已提供且格式正确
2. **查看日志输出**: 定位具体错误行和异常类型
3. **验证环境配置**: 确认依赖库版本和运行环境满足要求
4. **逐步调试**: 缩小问题范围,隔离故障模块