# Theme Catalog

## Usage

先根据用户场景和调性选主题，再读取对应单主题文件。

优先选择最贴合的一个主题，不要同时加载多个主题文档。

## 12 Flagship Themes

| Theme | Best For | Tone |
|---|---|---|
| `cyber-grid` | AI、云、科技发布、行业峰会 | 强科技、未来感、深色 |
| `executive-dark` | 董事会、高管汇报、战略复盘 | 沉稳、高端、压场 |
| `executive-light` | 咨询方案、客户提案、项目汇报 | 明亮、专业、整洁 |
| `glass-future` | 创新实验室、AIGC、概念展示 | 轻未来、玻璃质感 |
| `data-intelligence` | BI、经营分析、年度复盘 | 数据导向、理性、精准 |
| `startup-pitch` | 融资路演、创业 BP、商业模式 | 进攻感、增长感、品牌化 |
| `product-launch` | 新品发布、路线图、功能介绍 | 舞台感、产品感、现代 |
| `dev-summit` | 技术分享、架构演讲、开发者大会 | 工程感、清晰、可信 |
| `luxury-black-gold` | 高端品牌、管理层演示、重磅发布 | 奢雅、权威、仪式感 |
| `editorial-serif` | 白皮书、研究报告、教育内容 | 编辑感、知识感、耐读 |
| `neo-minimal` | 极简品牌提案、设计复盘、作品陈述 | 克制、留白、高级极简 |
| `creative-motion` | 品牌活动、营销 campaign、创意提案 | 张力、动态、视觉冲击 |

## Scene To Theme Mapping

| Scene | Preferred Theme | Backup Theme |
|---|---|---|
| AI 产品发布 | `cyber-grid` | `glass-future` |
| 企业战略汇报 | `executive-dark` | `executive-light` |
| 咨询项目提案 | `executive-light` | `neo-minimal` |
| 融资路演 | `startup-pitch` | `luxury-black-gold` |
| 数据分析报告 | `data-intelligence` | `executive-light` |
| 技术大会演讲 | `dev-summit` | `cyber-grid` |
| 新品发布会 | `product-launch` | `glass-future` |
| 高端品牌发布 | `luxury-black-gold` | `neo-minimal` |
| 白皮书 / 研究报告 | `editorial-serif` | `neo-minimal` |
| 极简设计提案 | `neo-minimal` | `executive-light` |
| 创意营销案 | `creative-motion` | `product-launch` |
| 创新概念展示 | `glass-future` | `creative-motion` |

## Density Guidance

| Density | Recommended Themes |
|---|---|
| 轻内容 | `product-launch`, `glass-future`, `creative-motion`, `luxury-black-gold` |
| 中内容 | `cyber-grid`, `startup-pitch`, `dev-summit`, `neo-minimal` |
| 重内容 | `executive-light`, `executive-dark`, `data-intelligence`, `editorial-serif` |

## Mobile Guidance

移动端优先级最高的主题：

1. `executive-light`
2. `neo-minimal`
3. `data-intelligence`
4. `startup-pitch`

这些主题更适合小屏下保持标题清晰、卡片整洁、信息层次稳定。
