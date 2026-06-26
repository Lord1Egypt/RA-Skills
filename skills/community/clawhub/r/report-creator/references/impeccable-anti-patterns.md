# Impeccable 反模式整合

基于 [impeccable.style](https://impeccable.style/) 的 37 条反模式，整合到 report-creator 的规则体系。

## 已有覆盖清单

以下反模式已被 report-creator 现有规则覆盖，无需额外处理：

| Impeccable 反模式 | report-creator 已有对应规则 |
|---|---|
| AI color palette (紫色渐变/青色暗色) | `design-quality.md` §4 Forbidden Patterns + §1 90/8/2 Color Law |
| Defaulting to dark mode for safety | Content-Type → Theme Routing（默认浅色主题） |
| Dark mode with glowing accents | 同上 + shared.css 暗色主题约束 |
| Flat type hierarchy (字体大小太接近) | §2 Typography: 10:1 Scale Ratio（最小/最大字号强制阶梯） |
| Overused font (Inter, Roboto, Arial) | §4 Forbidden Patterns: `Inter as body font` |
| Single font for everything | 已有 heading/body 字体栈区分 |
| Wrapping everything in cards | §4 Forbidden Patterns: 禁止每节一个卡片 |
| Identical card grids | §3 KPI Grid Column Rules（根据数量自适应列数） |
| Monotonous spacing | 视觉节奏规则：prose → component → prose 交替 |
| Low contrast text | §7 Pre-Output Self-Check |
| Tight line height (<1.3x) | shared.css 已有 line-height 定义 |
| Tiny body text (<12px) | §2 Typography min body 15px |
| Generic section headings | review-checklist.md §1.3 Anti-Template Section Headings |
| Prose walls | review-checklist.md §1.4 Prose Wall Detection |
| Rounded rectangles with generic drop shadows | shared.css 圆角/阴影定义 |
| Border accent on rounded element | shared.css accent 实现方式 |
| Side-tab accent border | 同上 |
| Redundant information | BLUF Opening 规则（§1.1） |
| Every button is a primary button | shared.css 按钮样式 |
| Gradient text | 已在禁止列表中 |
| Hero metric layout | 视觉节奏规则（不强制每个页面都有大数字） |

## 需补充的反模式

### 排版类

| # | 反模式 | 描述 | 补充位置 |
|---|---|---|---|
| T1 | **Line length too long** | 文本行超过 ~75 个字符导致阅读疲劳 | `design-quality.md` §7 self-check |
| T2 | **Wide letter-spacing on body text** | 正文 letter-spacing > 0.05em 降低阅读速度 | `design-quality.md` §2 Typography 增加上限 |
| T3 | **Justified text** | 两端对齐产生河流状空白 | `design-quality.md` §4 Forbidden Patterns |
| T4 | **All-caps body text** | 全大写正文破坏词形识别 | `design-quality.md` §4 Forbidden Patterns |
| T5 | **Monospace as technical shorthand** | 用等宽字体"装技术感" | `design-quality.md` §4 Forbidden Patterns |

### 颜色与对比度类

| # | 反模式 | 描述 | 补充位置 |
|---|---|---|---|
| C1 | **Pure black background (#000)** | 纯黑背景生硬、不自然 | `design-quality.md` §7 self-check |
| C2 | **Gray text on colored background** | 彩色背景上放灰色文字导致对比度不足 | `design-quality.md` §7 self-check |
| C3 | **Gradient text** | 装饰性渐变文字 | 已有，加强到 self-check |

### 布局与空间类

| # | 反模式 | 描述 | 补充位置 |
|---|---|---|---|
| L1 | **Nested cards** | 卡片嵌套卡片产生视觉噪声 | `design-quality.md` §4 Forbidden Patterns |
| L2 | **Everything centered** | 默认居中对齐缺乏层次感 | `design-quality.md` §4 Forbidden Patterns |
| L3 | **Cramped padding** | 内容离卡片边缘太近 | `shared.css` 最小 padding 约束 |
| L4 | **Glassmorphism everywhere** | 模糊效果当装饰 | `design-quality.md` §4 Forbidden Patterns |

### 视觉细节类

| # | 反模式 | 描述 | 补充位置 |
|---|---|---|---|
| V1 | **Sparklines as decoration** | 无意义的小图表装饰 | `rendering-rules.md` chart 规则 |
| V2 | **Icon tile stacked above heading** | 标题上方小圆角方块图标 | `design-quality.md` §4 Forbidden Patterns |
| V3 | **Reaching for modals by reflex** | 弹窗打断用户流程 | 报告场景不适用，跳过 |
| V4 | **Bounce or elastic easing** | 过时弹跳动画 | `html-shell-template.md` 动画约束 |

### 响应式

| # | 反模式 | 描述 | 补充位置 |
|---|---|---|---|
| R1 | **Amputating features on mobile** | 移动端隐藏关键功能 | `html-shell-template.md` 响应式规则 |

## 检测方法分类

参考 Impeccable 的三种检测方式，将现有和新增规则分类：

| 类型 | 规则编号 | 说明 |
|---|---|---|
| CLI (确定性，可机器扫描) | T1, T2, T3, C1, C3, L3, V4 | 可通过 CSS/grep 直接检测 |
| Browser (需真实布局渲染) | L2, C2, L1 | 需查看渲染后效果判断 |
| LLM-only (需语义理解) | T4, T5, V1, V2, R1 | 需 AI 判断内容是否合理 |

**执行策略：** CLI 类规则在 `--generate` 预写验证阶段自动扫描；Browser 类在 review 阶段通过 HTML 结构分析；LLM 类在生成时作为约束、review 时作为建议。

## 实施计划

| 优先级 | 变更 | 影响文件 | 耗时 |
|---|---|---|---|
| P0 | 增加 5 条自检查规则 | `design-quality.md` §7 | 5 分钟 |
| P0 | 增加 6 条禁止模式 | `design-quality.md` §4 | 5 分钟 |
| P0 | 增加 letter-spacing 上限 | `design-quality.md` §2 | 2 分钟 |
| P1 | shared.css 最小 padding/line-height 约束 | `templates/themes/shared.css` | 5 分钟 |
| P1 | 动画 easing 约束 | `references/html-shell-template.md` | 2 分钟 |
| P2 | chart sparklines 约束 | `references/rendering-rules.md` | 2 分钟 |
| P2 | 响应式功能隐藏约束 | `references/html-shell-template.md` | 2 分钟 |
