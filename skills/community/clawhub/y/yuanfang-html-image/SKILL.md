---
name: yuanfang-html-image
description: |
  HTML方案生成社交媒体配图。给定文字或URL，自动提取内容，选择模板风格，生成全平台多尺寸精美图片（小红书3:4、朋友圈1:1、微博16:9、公众号封面2.35:1、OG卡片1.9:1）。
  相比AI生图，HTML方案100%可控：文字精确、像素级布局、零API成本、可批量。
当用户提到"配图"、"图片"、"封面"、"海报"、"发小红书"、"发朋友圈"、"多平台配图"时考虑使用此技能。
---

# yuanfang-html-image — HTML方案社交媒体配图生成

## 依赖

本 skill 依赖同仓库 `yuanfang-design/` 共享设计库：
- `../yuanfang-design/base.css` — token CSS 变量
- `../yuanfang-design/themes/*.css` — 12 个主题
- `../yuanfang-design/layout-types/cover.html` — 布局块

如需独立部署，需复制整个 `yuanfang-skills/` 仓库。

---

## Step 0: 提取品牌资产 (URL → logo + 主题色)

**第一步永远是品牌**, 因为它决定了"这套图属于谁". 用户给了 URL, 就自动把品牌资产全抓出来; 给了纯文本, 跳过这步.

### URL 输入 → 自动抓品牌 (建议值, 不是终值)

| 资产 | 来源 | 用途 |
|---|---|---|
| **logo 图片** | `<link rel="apple-touch-icon">` → `og:image` → favicon | 建议值, **Step 2 询问后用户决定** |
| **品牌名** | `og:site_name` → 域名 | 仅供参考 |
| **主题色** | `<meta name="theme-color">`, 兜底: logo 主色 | 建议值, **Step 2 询问后用户决定** |
| **字体** | 页面 `@font-face` / Google Fonts link | 标题/正文字体建议 |

### 抓取结果只作"建议", 用户始终有最终决定权

**Step 0 抓到的东西不是终点, 是"默认值建议"**. Step 2 必须问用户:

1. **logo** (不管抓没抓到都问):
   - 抓到了: "抓到 logo: `data:image/png;...` 或 `<URL>`, 要展示吗? 用这个, 还是换 URL?"
   - 没抓到: "要展示 logo 吗? 给个图片 URL/data URL, 或不要"
   - 不用 logo → 左下角**完全空**, 不用文字兜底 (干净的图片)

2. **品牌色** (不管抓没抓到都问):
   - 抓到了: "抓到主题色: `#4B43E4`, 用这个, 还是换其他颜色?"
   - 没抓到: "要替换主题色吗? 给个 hex (如 `#E11D48`), 或保持主题默认"
   - 不用 → 主题默认色, 右 24% 块 = 主题 indigo

**核心原则**: 自动提取是方便, **最终用户说了算**. 不静默 fallback, 不文字兜底.

### 实现

```bash
node scripts/extract-brand.js "https://example.com/article"
# → 写入 ./.yuanfang/brand-specs/<domain>.json
```

### 缓存策略

`./.yuanfang/brand-specs/<domain>.json` 自动缓存, TTL 7 天, `--refresh-brand` 强制刷新。**没有全局缓存** — 品牌是项目资产, 团队通过 git 共享。

### 文本输入 / 无输入

跳过 Step 0 (没东西可抓), 进 Step 2 时**仍然要主动问 logo 和颜色**。

### Step 0 抓取后的展示 (仅供参考)

```
我从 https://... 抓到了:
  logo: ✓ 抓到 (256×256 PNG)  → 存到 ./.yuanfang/brand-specs/yuanfang.skills.json
  品牌名: Yuanfang
  主题色: #5856E9 (indigo)
  字体: Outfit / Inter

(这些是建议值, 后面 Step 2 你可以改)
```

### [等待用户确认] 展示以上结果给用户，等用户确认后才能进 Step 1

用户确认 → 进 Step 1 (内容).

---

## Step 1: 提取内容 (URL 或文本 → 标题/正文/要点)

**用户不该被问"标题是什么"** — 应该自动从 URL 或文本提取, 然后给用户改.

### 来源

- **URL** — 已在 Step 0 抓过页面, 复用 HTML 提取 title/body/points
- **纯文本** — agent 调 `extract.js --text` 解析首行/段落/bullet
- **已有 content.json** — 直接用, 跳过提取

### 提取字段

| 字段 | 来源 | 用户可改 | 推荐长度 |
|------|------|---------|---------|
| `title` | `<h1>` / og:title / 文本首行 | ✓ | 10-20 字，不超过 30 字 |
| `body` | og:description / 第一段 / 文本摘要 | ✓ | 30-60 字，不超过 100 字（超长会被截断） |
| `points` | sub-headings / 文本 bullet / 自动归纳 | ✓ | 3-5 条，每条 10-20 字 |

### 实现

```bash
node scripts/extract.js --text "标题\n正文\n- 要点1\n- 要点2" > content.json
# URL 已经在 Step 0 抓过, 直接复用
```

### 展示给用户

```
我提取了内容:
  标题: AI 重塑内容创作
  正文: 从文案到配图, AI 正在重新定义创意的边界。
  要点: 效率提升 10 倍 / 零门槛创作 / AI 不是替代而是增强

要改吗? 没问题就继续.
```

注意：正文过长会撑满画面导致标题不可见，建议正文不超过 100 字，标题不超过 30 字。

### [等待用户确认] 展示以上内容给用户，等用户确认/修改后才能进 Step 2

---

## Step 2: 询问样式 (按优先级分轮)

### 第一轮 (必答)

- **主题** — 从 12 个主题中选 1 个。向用户展示完整信息（底色、主色、视觉特征、适合场景），参考「完整主题库」表格。
  - **如果 Step 0 抓到品牌主色**, 推荐色调最接近的 2-3 个主题, 让用户挑
  - **没抓品牌色**, 默认推荐 `minimal-white` (干净白底, 通用百搭)
- **平台** — 从 6+ 个尺寸中选 1-N 个 (允许多选)
  - 默认推荐: `xiaohongshu` 组 (覆盖小红书竖 + 方)
  - 用户说 "全平台" / "全选" → 选全部

### [等待用户确认] 等用户回答第一轮后才能继续第二轮

### 第二轮 (logo + 颜色, 都要问)

- **logo** — 左下角
  - **抓到 logo**: 展示给用户 (URL 或 data URL), 问 "用这个, 换 URL, 还是要?"
    - 用这个 → `content.brandImage = <extracted>`
    - 换 URL → `content.brandImage = <new url>`
    - 不要 → `content.brandImage = null` (左下角完全空)
  - **没抓到**: 问 "要加 logo 吗? 给个 URL/data URL, 或不要"
    - 给 URL → `content.brandImage = <url>`
    - 不要 → `content.brandImage = null`
- **品牌色** — `--accent` token
  - **抓到主题色**: 展示给用户 (`#xxx`), 问 "用这个, 换颜色, 还是要?"
    - 用这个 → `brand-spec.colors.primary = <extracted>`
    - 换颜色 → `brand-spec.colors.primary = <new hex>`
    - 不要 → `brand-spec.colors.primary = null` (主题默认)
  - **没抓到**: 问 "要替换主题色吗? 给个 hex, 或保持主题默认"

### [等待用户确认] 等用户回答第二轮后才能继续第三轮

### 第三轮 (可选, 答 "不用" 跳过)

- **分类标签 (badge)** — 顶部小字
  - 默认: 不渲染
  - 常见: `FEATURED` / `TRENDING` / `ESSENTIAL` / `EXCLUSIVE` / `HOT` / `NEW`
- **二维码 (qr)** — 中下角
  - 默认: 不渲染
  - **3 种提供方式** (任选一种):
    1. **URL** (推荐) — 传 `https://yuanfang.skills`, 渲染时自动生成 QR
    2. **图片 data URL** — 传 `data:image/png;base64,...` (用户已有现成 QR)
    3. **图片 URL** — 传 `https://x.com/qr.png` (有现成 QR 图)
  - 智能检测: 以 `data:image/` 开头或 `.png/.jpg` 结尾 → 当图片用; 否则当 URL 自动生成
  - 常见场景: 公众号文章链接、视频号主页、个人收款码

### 询问方式

- ✅ 有原生 UI 工具 (OpenCode `question` / Claude Code `AskUserQuestion`): 弹选项菜单
- ⚠️ 无 UI 工具: 打印带编号的选项列表, 等用户从 stdin 输入编号

### 内容类型 → 主题推荐

```
干货/教程 → minimal-white / data-infographic / list-ranking
重磅消息 → dark-gold / bold-poster / magazine-cover
深度分析 → editorial / eastern / magazine-cover
个人故事 → warm-handdrawn / minimal-white-editorial
科技资讯 → tech-modern / split-screen / minimal-white-editorial
```

---

## CLI

详见 [references/cli.md](references/cli.md)。核心命令：

```bash
node scripts/render.js --theme <theme> --layout cover --platforms <ids>
```

旧版 `--template 1-12` 仍兼容（映射到 12 个主题）。

---

[原 SKILL.md 内容继续...]

## 核心理念

**HTML + Playwright 截图 = 稳定、可控、精美的社交图片。**

| 对比 | HTML方案 | AI生图 |
|------|---------|--------|
| 文字准确度 | 100% | 可能出错 |
| 布局控制 | 像素级 | AI自由发挥 |
| 多尺寸输出 | 一键生成全部 | 逐张生成 |
| API成本 | 零 | 每次消耗 |
| 迭代速度 | 改CSS即刻重出 | 需要重新生成 |

## 工作流速览

```
用户提供 URL / 文本 / content.json
    ↓
Step 0: 提取品牌资产 (URL → logo + 主题色 + 字体)
  → 自动抓, 展示给用户
  → ⬋ 等用户确认后才能继续
  → 文本输入则跳过
    ↓
Step 1: 提取内容 (URL/文本 → 标题/正文/要点)
  → 自动提取, 展示给用户
  → ⬋ 等用户确认/修改后才能继续
    ↓
Step 2: 询问样式 (分三轮)
  → 第一轮 (必答): 主题 + 平台
  → ⬋ 等用户回答后才能继续
  → 第二轮 (必答): logo + 品牌色
  → ⬋ 等用户回答后才能继续
  → 第三轮 (可选): 分类标签 + 二维码
  → ⬋ 等用户回答后才能继续
    ↓
Step 3: 渲染 (按选的主题/平台批量生成)
    ↓
Step 4: 预览确认 / 迭代优化
```

**硬保护 (render.js hard gate)**：如果执行 render 时 content.json 没有 `brand` / `brandImage` 字段且没传 `--theme`，render.js 拒绝执行并打印明确错误（exit 1）。这是**跨 100% agent 平台**生效的兜底，不依赖 hook 机制。

---

---

## 详细参考文档

按需查阅，不要预先加载：

- **[references/cli.md](references/cli.md)** — render.js 完整 CLI 参数
- **[references/themes-catalog.md](references/themes-catalog.md)** — 12 主题详细视觉特征
- **[references/platforms.md](references/platforms.md)** — 12 平台 ID + 尺寸
- **[references/extract-api.md](references/extract-api.md)** — extract.js 内容提取 API
- **[references/template-vars.md](references/template-vars.md)** — `{{TOKEN}}` 变量系统 + 设计原则

---

## Step 3: 生成图片

```bash
# 从 content.json 生成
node scripts/render.js \
  --file /path/to/content.json \
  --theme <theme> \
  --layout cover \
  --platforms <ids>

# 调试（输出 HTML 不截图）
node scripts/render.js --preview --theme tech-modern --platforms xiaohongshu-v
```

更多参数和并行生成示例见 [references/cli.md](references/cli.md)。平台 ID 列表见 [references/platforms.md](references/platforms.md)。

---

### [等待用户确认] 等用户回答第三轮后才能执行渲染

---

## Step 4: 预览确认

### [等待用户确认] 展示图片给用户，等用户确认/要求修改后才能结束

检查项：
1. 文字内容完全正确？
2. 布局在不同比例下正常？
3. 色彩和风格符合预期？
4. 视觉层次清晰？（大字 > 中字 > 小字）

---

## 模板设计说明

旧模板在 `templates/[编号]-[名称]/` 下有 `template.json`（配色/字体/字号）+ `template.html`（HTML 布局 + `{{TOKEN}}`）。

**新代码应使用 `yuanfang-design/themes/*.css` + `yuanfang-design/layout-types/cover.html`，不要创建新模板目录**。

完整 `{{TOKEN}}` 变量系统（`{{COLOR__Axx}}` 透明度、`{{SIZE__PRINT}}` 打印缩放、配置优先级）见 [references/template-vars.md](references/template-vars.md)。

---

## 文件结构

```
yuanfang-html-image/
├── SKILL.md                    # 本文件
├── references/                 # 详细参考
│   ├── cli.md
│   ├── themes-catalog.md
│   ├── platforms.md
│   ├── extract-api.md
│   └── template-vars.md
├── scripts/
│   ├── render.js               # 核心渲染引擎
│   ├── extract.js              # 内容提取
│   └── extract-brand.js        # 品牌资产提取
├── .yuanfang/                  # 品牌资产缓存 (项目级)
│   ├── content-*.json          # content 草稿
│   └── brand-specs/            # 抓到的 brand specs
│       └── <domain>.json
└── templates/                  # 旧版模板目录 (兼容保留)
```

