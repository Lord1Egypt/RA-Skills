# 语义颜色角色参考表

本表基于 GitHub Primer 的角色划分方式，规定每个颜色**用在哪里**以及**禁止用在哪里**，不包含具体色值。

## 核心 17 个角色

| 组别 | 角色变量 | 用在哪里 | 禁止 / 注意事项 |
| :--- | :--- | :--- | :--- |
| 背景 | `bgColor.default` | 页面主背景、画布底色 | 禁止在上面放置未达标的浅灰正文 |
| 背景 | `bgColor.muted` | 次级面板、卡片底、表头 | 暗色下与主底对比度低时，须用 `borderColor.muted` 兜边 |
| 背景 | `bgColor.accent.emphasis` | 主按钮、刊头、整块强调平涂 | 一屏只保留一个强调色相；其上文字必须用 `fgColor.onEmphasis` |
| 背景 | `bgColor.deep` | 深色图版、封面、深色 Banner | 亮暗两主题均保持深底，其上文字必须用 `fgColor.onDeep` |
| 文字 | `fgColor.default` | 主标题、正文、核心标签 | 需达到 ≥ 7:1（AAA）对比度 |
| 文字 | `fgColor.muted` | 时间、摘要、辅助说明 | 避免用于大段正文阅读 |
| 文字 | `fgColor.disabled` | 禁用态文字与图标 | 必须配合不可交互状态与文案/位置提示，不能单独表义 |
| 文字 | `fgColor.accent` | 链接、可交互文字与图标 | 仅代表可点击交互，不做纯装饰使用 |
| 文字 | `fgColor.accentHover` | 链接与文本按钮 Hover 态 | 与 `fgColor.accent` 同色相，仅改变亮度 |
| 文字 | `fgColor.onEmphasis` | 强调实底上的反白文字 | 禁止写死 `#fff`，必须与 `bgColor.accent.emphasis` 成对使用 |
| 文字 | `fgColor.onDeep` | 深色图版上的亮字 | 必须与 `bgColor.deep` 成对使用 |
| 文字 | `fgColor.danger` | 错误提示、破坏性操作文字 | 必须搭配图标或文字冗余，不能只靠颜色区分 |
| 边框 | `borderColor.default` | 输入框、按钮等交互控件边框 | 需达到 ≥ 3:1 非文字对比度 |
| 边框 | `borderColor.muted` | 列表分割线、卡片发丝线 | 不用于强调交互态 |
| 边框 | `borderColor.emphasis` | 强结构分界线 | 克制使用，避免页面线条过重 |
| 边框 | `borderColor.accent` | 选中态边框 | 只用于表示当前选中，不用于普通 Hover |
| 焦点 | `focus.outlineColor` | 键盘 Tab 焦点环 | 独立可访问性角色，建议 `2px solid` |

## 可选扩展异色（默认开启）

用于界面状态反馈，色相已自动与主品牌色保持分离：
- `fgColor.success` / `bgColor.success.muted` / `bgColor.success.emphasis`（成功 / 完成）
- `fgColor.warning` / `bgColor.warning.muted` / `bgColor.warning.emphasis`（警告 / 注意）
- `fgColor.info` / `bgColor.info.muted` / `bgColor.info.emphasis`（信息 / 引导）
- `bgColor.danger.muted` / `bgColor.danger.emphasis`（危险提示底 / 危险实底）
