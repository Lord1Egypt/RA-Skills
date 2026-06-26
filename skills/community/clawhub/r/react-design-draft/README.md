# React Design Draft Generator v5.3.0

> 从内容生成信息密度高、审美在线的 React 设计稿四件套

[![版本](https://img.shields.io/badge/version-5.3.0-blue)](https://github.com/EdwardWason/react-design-draft)
[![License](https://img.shields.io/badge/license-MIT--0-green)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-react--design--draft-orange)](https://clawhub.ai/skills/react-design-draft)

## 功能

- **三维组合系统**：25种布局 × 23种风格 × 12种配色，自动匹配内容结构
- **React 四件套输出**：design-tokens.css + data.js + components/*.jsx + App.jsx
- **信息密度量化**：5维度25分制评分，≥16分及格，10条反模式红线
- **前置适配建议**：生成前强制展示风格/布局/比例推荐，用户确认后才生成
- **生成后编辑指南**：文件树 + 快捷编辑地图 + 组件层级树，体现 React 可定向修改优势
- **本地字体优先**：7种字体预设 + 11个本地CJK字体注册表，Local-first 策略
- **29个快捷预设**：知识卡片、对比分析、信息图、纸墨风等一键触发
- **Kami 纸墨风格**：10条不变量规则，仓耳今楷02 + 羊皮纸配色

## 快速开始

```bash
# ClawHub 安装
clawhub install react-design-draft

# 或手动安装
git clone https://github.com/EdwardWason/react-design-draft.git
```

## 使用方式

在 TRAE / Claude Code / 任何 Agent 平台中，提供内容即可触发：

```
帮我把这篇文章做成高密度信息图
```

```
用纸墨风格做一个知识卡片
```

```
对比分析 A 和 B，生成设计稿
```

### 关键词触发

| 关键词 | 触发预设 |
|--------|---------|
| 知识卡片 / 干货 / 要点 | knowledge-card |
| 对比 / PK / 优劣 | versus |
| 信息图 / 可视化 | infographic |
| 纸墨风 / Kami / 雅致 | kami-report |
| 高密度信息大图 | dense-info |
| 杂志风 / 排版 | magazine |

### 自定义覆盖

```
用赛博朋克风格做知识卡片 → --style cyberpunk-neon
高密度信息图，用暗色方案 → --palette dark
```

## 执行流程

```
内容输入 → Step 1: Parse & Match → Step 2: Confirm & Advise → Step 3: Generate → Step 4: Post-Generation Guide
```

1. **Parse & Match**：解析内容结构，自动匹配 Layout × Style × Palette
2. **Confirm & Advise**：展示推荐方案 + 适配建议，等待用户确认
3. **Generate**：输出 React 四件套（design-tokens.css / data.js / components/*.jsx / App.jsx）
4. **Post-Generation Guide**：输出编辑指南（文件树 + 快捷编辑 + 组件层级）

## 配置

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| Layout | 自动匹配 | 25种布局模式 |
| Style | 自动匹配 | 23种视觉风格 |
| Palette | 自动匹配 | 12种配色方案 |
| Density Threshold | 16/25 | 最低信息密度分数 |
| Font Strategy | local-first | 本地字体优先，Web字体回退 |

## 文档

| 文档 | 说明 |
|------|------|
| [内容布局映射](references/content-layout-mapping.md) | 三维组合系统 + 25种布局 + 关键词映射 |
| [美学指南](references/aesthetics-guide.md) | 23种风格 + 12种配色 + 7种字体预设 + 反模式 |
| [密度标准](references/density-standards.md) | 5维度评分 + 10条反模式红线 |
| [输出规范](references/react-output-spec.md) | React四件套规范 + 交互编辑指南 |
| [风格预设](references/style-presets.md) | 29个快捷预设 + 关键词触发映射 |

## License

MIT-0 © 2026

---

# React Design Draft Generator v5.3.0

> Generate information-dense, visually refined React design drafts (4-piece set) from content

[![Version](https://img.shields.io/badge/version-4.0.0-blue)](https://github.com/EdwardWason/react-design-draft)
[![License](https://img.shields.io/badge/license-MIT--0-green)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-react--design--draft-orange)](https://clawhub.ai/skills/react-design-draft)

## Features

- **Three-dimension system**: 25 layouts × 23 styles × 12 palettes, auto-matched to content
- **React 4-piece output**: design-tokens.css + data.js + components/*.jsx + App.jsx
- **Density quantification**: 5-dimension 25-point scoring, ≥16 pass, 10 anti-pattern red lines
- **Pre-generation consultation**: Mandatory style/layout/ratio recommendation before generating
- **Post-generation edit guide**: File tree + quick edit map + component hierarchy tree
- **Local-first fonts**: 7 font presets + 11 local CJK font registry
- **29 quick presets**: Knowledge card, comparison, infographic, Kami editorial, etc.
- **Kami editorial style**: 10 invariants, TsangerJinKai02 + parchment palette

## Quick Start

```bash
clawhub install react-design-draft
```

## Usage

Provide content in any Agent platform:

```
Turn this article into a high-density infographic
```

```
Create a knowledge card in Kami editorial style
```

## Execution Flow

```
Content → Step 1: Parse & Match → Step 2: Confirm & Advise → Step 3: Generate → Step 4: Post-Generation Guide
```

## Documentation

| Document | Description |
|----------|-------------|
| [Content Layout Mapping](references/content-layout-mapping.md) | Three-dimension system + 25 layouts + keyword mapping |
| [Aesthetics Guide](references/aesthetics-guide.md) | 23 styles + 12 palettes + 7 font presets + anti-patterns |
| [Density Standards](references/density-standards.md) | 5-dimension scoring + 10 anti-pattern red lines |
| [React Output Spec](references/react-output-spec.md) | React 4-piece spec + interactive edit guide |
| [Style Presets](references/style-presets.md) | 29 quick presets + keyword trigger mapping |

## License

MIT-0 © 2026
