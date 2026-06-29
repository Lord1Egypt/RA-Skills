---
name: stuff-skill
description: "Stuff Skill - 秩。告诉 AI 你想管理什么,它给你生成一个专属 App。"
---

# Stuff Skill - 秩

> 告诉 AI 你想管理什么,它给你生成一个专属 App,直接能在手机上用。

**核心理念:Agent 是设计师,不是模板替换器。**

从自然语言描述生成个人数据管理 PWA。Skill 提供设计约束和数据引擎(硬规则、数据层 JS 模式、主题色彩系统),Agent 负责根据场景**自由设计 UI 布局、卡片样式、交互细节**——让每个应用看起来像它该有的样子,而不是同一个模板换张皮。

**两种模式:**
- **本地模式(默认)**:零依赖,双击 `index.html` 即可用,数据存浏览器里。
- **云模式**:部署到 Cloudflare Pages + D1,多设备同步。也可换 Vercel+Turso / Netlify+Supabase 等(自行适配 API 层)。

## 适用 / 不适用 / 能力圈

**适用:** 个人收藏/库存管理、记录追踪(训练/补剂/观影)、清单管理、任何需要搜索/筛选/排序的个人数据。

**不适用:** 多人协作/认证/第三方 API、复杂关系型数据(多表关联)、实时数据流/支付/审批等后端业务逻辑。

**能力圈:** 强势=个人数据管理全品类;需用户配合=带图片、复杂计算字段;不做=多用户系统、>10000 条数据。

## 必读 References

- `references/inspiration.md` — 场景灵感 + 能力边界(用户不知道做什么时给他看)
- `references/field-inference.md` — 字段类型推断规则
- `references/design-proposal.md` — **设计提案规范 + 主题系统 + 布局映射 + 审美原则**(第 4 步必读)
- `references/components.md` — 主题 CSS 变量体系 + UI 组件完整规范
- `references/deploy-guide.md` — Cloudflare 部署全流程 + 给用户的部署指南
- `references/validation.md` — 校验规则 R1-R7

## 种子模板(参考,不是规范)

`assets/` 里的种子模板和 `references/components.md` 都是**参考实现**,不是强制规范。

- **数据层 JS 模式**(localStorage CRUD、Smart Select、导入导出)→ 必须复用,这是硬规则
- **UI 组件**(卡片、色条/色点、布局、信息层次)→ 自由设计,components.md 只是"一种可能的做法"
- Agent 可以用色点代替色条、分组代替扁平列表、时间线代替卡片——只要符合场景气质

| 文件 | Agent 用它做什么 |
|------|-----------------|
| `template-app-local.js` | 学习本地 localStorage CRUD、Smart Select、导入导出 |
| `template-app.js` | 学习云模式 API CRUD、离线 fallback |
| `template-api.js` | 学习 Workers D1 绑定、CORS |
| `template-sw.js` | 直接复用(SW 不需要设计) |
| `template-styles.css` | 提取当前主题的 CSS 变量,不复制选择器 |
| `template-app.html` | 了解必要元素(dialog、FAB、chips),结构自己设计 |

## 工作流

0. **环境检查** — 检测 Node/wrangler/Cloudflare 登录:全通过→云模式;任一缺失→本地模式;用户可覆盖。
1. **Intake** — 抓住三件事:管什么、谁在用、怎么用。读 `references/field-inference.md` 推断一套合理字段,一次确认,**不逐字段追问**。有用户画像则据此调字段/主题/设计语言;没有则走通用默认。
2. **Schema 设计** — 生成字段元数据 JSON。硬规则:必须有一个 `display:"title"` 字段、至少一个 `type:"enum"` 字段(状态筛选);Smart Select/Date/Number/Textarea 按规则分配。
3. **选择主题** — 从 4 套预设主题选一套(详见 `references/design-proposal.md`)。
4. **🔥 设计提案** — 工作流最重要的一步。按 `references/design-proposal.md` 提出布局/卡片/交互/配色概念,给用户一个视觉提案,**一次确认**。
5. **视觉 Mockup(可选但建议)** — 有渲染能力就生成 2-3 张假数据卡片的 HTML mockup;没有就用 ASCII 线框图。
6. **生成应用** — ⚠️ 不复制种子模板的 HTML/CSS,只复用数据层 JS 模式。HTML/CSS 从头写、自由设计;数据层(load/save/CRUD/filter/sort/export/import)+ Smart Select 三件套保持与种子模板兼容。本地模式 4 文件;云模式额外加 functions/ + schema.sql + sw.js + 多尺寸图标。**必做 PWA 图标**(详见硬规则)。
7. **预览 → 部署 → 交付** — 先给用户看,再问要不要校验;交付含数据导入导出说明(部署见 `references/deploy-guide.md`)。

## 硬规则(Non-Negotiables)

**设计自由,功能不自由。以下规则必须遵守,不管 UI 怎么设计。**

### 数据层(不可妥协)
- **数据必须持久化** — localStorage 或 D1。
- **导入/导出必须有** — JSON 格式,数据安全底线。
- **Smart Select 三件套不可少** — select + hidden input + custom input。
- **Smart Select 必须带管理功能** — 每个 smart-select 字段旁有 ⚙ 管理按钮,支持改名(批量更新)和删除(清空使用该值记录的对应字段)。模板已内置(`template-app.js` 的 `openSmartSelectManager` + `template-app.html` 的 `#smartSelectManager` + `template-styles.css` 的 `.smart-manage-btn`/`.smart-manager-*`)。

### 组件约束(不可妥协)
- **Editor 必须是 `<dialog>` 模态框** — 不用路由跳转,不用侧边栏。
- **FAB 必须有 safe-area 适配** — `bottom: calc(24px + env(safe-area-inset-bottom, 0px))`。
- **状态必须有视觉区分** — 色条/标签/颜色,形式 Agent 定,但必须一眼能区分。

### 主题约束(不可妥协)
- **优先用 4 套预设主题** — 允许微调强调色和字体,但背景明暗层级必须一致。
- **至少一个 enum 字段用于筛选。**

### 本地模式额外
- **双击即用** — 不依赖服务器/npm/Node。
- **不用 `type="module"`** — file:// 协议下有 CORS 问题。

### PWA 图标(不可妥协)
- **每个应用必须有设计感图标** — 不允许纯文字/默认图标。
- **图标 = 主题渐变背景 + 场景代表性扁平图形**(咖啡豆/哑铃/线轴/胶囊等)。
- **尺寸:** 至少 192/512,iOS 额外 180。manifest.json 必须含 icons 数组,`<head>` 必须有 `<link rel="apple-touch-icon" href="./icon-180.png" />`。
- **风格:** iOS squircle 造型,主题渐变底 + 白色/主题色图形,扁平,不加文字不加阴影。

### 云模式额外
- **离线 fallback** — Service Worker + localStorage。
- **API 带 CORS。**
- **从项目根目录部署,不是 public/ 子目录。**

## 迭代

- 增减字段 → 改 HTML 表单 + app.js 字段列表
- 换主题 → 换 CSS 变量值
- 换布局 → **大改动,重新走设计提案流程**
- 本地→云模式升级 → 加 API 层 + D1 + SW

## 设计哲学

> 好的设计是"这应用就该长这样"。CrossFit 日记不该看起来像图书馆,图书馆不该看起来像咖啡豆仓。
>
> 种子模板是乐高积木的说明书,不是乐高成品。Agent 读说明书,搭自己的东西。
