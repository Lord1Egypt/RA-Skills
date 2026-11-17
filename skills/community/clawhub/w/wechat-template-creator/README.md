# wechat-template-creator 📝

微信公众号文章排版模板创作技能（WorkBuddy Skill）。采用向导式交互，提供 **行业模板模式** 和 **完全自定义模式** 两种创作路径，产出微信编辑器兼容的内联样式 HTML 模板。

> **定位**：模板工厂 —— 产出排版结构，模板中保留 `{{占位符}}`，由下游写作 skill 在生成具体文章时填充内容。

## ✨ 特性

- 🏭 **模板工厂定位**：只负责排版骨架，不填充内容，占位符原样保留供下游消费
- 📱 **移动优先**：正文默认 17px、列表 `padding-left ≥ 32px`、全局 `box-sizing:border-box`，专为手机阅读优化
- ✅ **公众号规范兼容**：全部通过《公众号 HTML 代码规范》校验（详见下文「规范约束」）
- 🧭 **向导式交互**：逐项引导、支持回退修改、实时预览

## 🎨 两种创作模式

### 模式一：行业模板模式

7 套预设行业模板，即选即用：

| 编号 | 行业 | 风格关键词 | 配色 |
|------|------|-----------|------|
| 1 | 科技互联网 | 极简科技、现代理性 | 蓝 `#1a73e8` + 青 `#00bcd4` |
| 2 | 教育培训 | 温暖学术、知识亲和 | 橙 `#ff9800` + 琥珀 `#ffc107` |
| 3 | 金融理财 | 专业稳健、数据严谨 | 深蓝 `#1a237e` + 金 `#c8a45a` |
| 4 | 健康医疗 | 清新关怀、自然疗愈 | 绿 `#2e7d32` + 青绿 `#26a69a` |
| 5 | 美食生活 | 暖意烟火、生活美学 | 暖橙 `#e65100` + 砖红 `#d84315` |
| 6 | 文艺情感 | 素雅诗意、留白呼吸 | 灰 `#757575` + 玫红 `#e91e63` |
| 7 | 商业咨询 | 权威洞察、理性商业 | 深灰 `#263238` + 钢蓝 `#546e7a` |

每个模板包含完整的排版结构：头部（标题 + 作者/日期）、二级标题装饰、正文段落、引用块、划重点、列表、代码块、表格、分隔线、底部关注区（二维码 + 免责声明）。

### 模式二：完全自定义模式

逐项配置 10 大类排版要素：

1. **正文字体及大小** —— 5 种预设，默认 17px
2. **二级标题装饰** —— 色条 / 横线 / 色块 / 编号 / 图标 / 色带 / 双线
3. **段落间隔样式** —— 虚线 / 渐变线 / 三点 / SVG 波形 / 符号
4. **头部样式** —— 简约 / 装饰 / 卡片
5. **底部样式** —— 标准 / 卡片 / 左右布局 + 免责声明
6. **划重点样式** —— 荧光笔 / 加粗变色 / 背景色块 / 下划线
7. **引用块样式** —— 左色条 / 全边框 / 引号
8. **代码块样式** —— VS Code Dark / Monokai / 简约灰 / Dracula
9. **表格样式** —— 全边框 / 极简水平线
10. **列表样式** —— 圆点 / 方块 / 对勾 / 数字序号 / 中文数字 / 原生列表

## 📱 移动优先设计

公众号文章主要在移动端阅读，模板以移动端为首要考虑：

| 规则 | 说明 |
|------|------|
| 正文字号 17px | 在 375px 宽度的手机屏幕上清晰可读 |
| 列表 `padding-left ≥ 32px` | 编号/符号在移动端不被压缩截断 |
| 表格字号 ≥ 15px | 窄屏可读性 |
| 代码字号 ≥ 14px | 代码可读性 |
| `box-sizing:border-box` | 防止 padding 撑破容器宽度 |
| 表格 padding 竖大于横 | `14px 12px`，适配窄屏 |
| 图片 `max-width:100%` | 不超出屏幕宽度 |

## ✅ 公众号规范约束

所有模板和生成的 HTML 均强制遵守微信编辑器的限制：

**绝对禁止**：
- `<div>`（会被编辑器过滤，排版容器强制使用 `<section>`）
- `<script>`、`<style>` 标签及内联事件
- CSS 伪元素（`::before` / `::after`）
- `position:fixed/sticky`、`<iframe>`、Canvas、表单元素

**强制规范**：
- 所有样式内联 `style`，无 class / 外部 CSS
- 表格表头使用 `<td style="font-weight:600;">` 替代 `<th>`
- 图片添加 `display:block; max-width:100%; height:auto`
- 全局容器含标准 font-family、`word-break:break-all`、`box-sizing:border-box`
- 不使用 `colspan`/`rowspan`，不依赖 `counter-reset`

完整规范见 [`references/wechat-html-spec.md`](references/wechat-html-spec.md)。

## 📦 安装使用

### 作为 WorkBuddy 技能安装

将本仓库克隆或下载后，放到 WorkBuddy 技能目录：

```bash
git clone https://github.com/yourname/wechat-template-creator.git ~/.workbuddy/skills/wechat-template-creator
```

然后在对话中触发：

```
使用微信模板创作技能 / 帮我做一个公众号排版模板
```

### 使用流程

1. **选择模式**：行业模板（快速）或 完全自定义（精细）
2. **行业模式**：选行业 → 输出带占位符的模板 HTML
3. **自定义模式**：逐项配置 10 类要素 → 确认配色 → 组装输出
4. **产出**：`outputs/wechat-template.html`，保留 `{{占位符}}` 供下游写作 skill 填充

## 📁 目录结构

```
wechat-template-creator/
├── SKILL.md                    # 技能主文件（向导流程 + 强制规范）
├── assets/
│   └── templates/              # 7 个行业预设模板
│       ├── tech-internet.html      # 科技互联网
│       ├── education.html          # 教育培训
│       ├── finance.html            # 金融理财
│       ├── healthcare.html         # 健康医疗
│       ├── food-lifestyle.html     # 美食生活
│       ├── literary-emotional.html # 文艺情感
│       └── business-consulting.html# 商业咨询
├── references/
│   ├── custom-config.md        # 自定义模式 10 类要素 CSS 配置参考
│   └── wechat-html-spec.md     # 公众号 HTML 代码规范（权威约束）
└── LICENSE
```

## 🤝 与下游技能配合

本技能产出的模板是「骨架」，配合文章写作技能使用效果最佳：

```
wechat-template-creator 产出模板
        ↓ 保留 {{文章主标题}}、{{正文段落内容}} 等占位符
文章写作 skill 填充内容
        ↓
成品公众号文章 → 粘贴到微信编辑器发布
```

## 📄 License

详见 [LICENSE](LICENSE)。

---

作者：山观未来（43188540@qq.com）
