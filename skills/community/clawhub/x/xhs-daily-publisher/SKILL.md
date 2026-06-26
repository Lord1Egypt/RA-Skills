---
name: xhs-auto-publisher
description: 小红书自动化内容生产与发布助手。通过对话收集账号定位（领域/人设/视觉偏好/发布节奏），自动完成「热点选题 → 9 图文案 → HTML 视觉模板 → 高清图片渲染 → 浏览器自动发布 → 定时任务调度」全链路，最终保留"用户手动点发布"一步防封号。支持随时通过对话调整视觉风格、文案语气、选题方向。触发关键词：小红书、xhs、自动发布、自媒体、日更、9 图、数字人、每日速报、起号、作品集、批量生产、账号运营、图文生成。
agent_created: true
---

# 小红书自动化内容生产与发布助手

## 这个 Skill 是什么

**一套端到端的小红书日更自动化工作流。** 不是单点工具，是把「选题 → 内容 → 发布 → 优化」4 个环节打通成可循环运行的流水线。用户只需给出账号定位，Skill 会自动生成可发布的 9 图图文包，并在本机用浏览器自动打开发布页等用户点最后一下。

**关键设计哲学**：
- **先跑通再扩能力**：不追求一次性完美，先建最小闭环（选题+文案+图+半自动发布），再扩展视频、抖音、数据回流
- **半自动发布**：最后"点发布"必须人工，降低封号风险（尤其新号前 7 天）
- **持久化 profile + cookies**：首次扫码后永久免登
- **视觉模板化**：HTML + Puppeteer 渲染，一次写好 CSS，每天只换文字就能出 9 图

## 何时使用此 Skill

当用户表达以下意图时，主动调用：
- "我想做小红书自媒体 / 起号 / 日更"
- "帮我自动发小红书"
- "做一个 AI 内容账号 / 资讯号 / 速报号"
- "我想通过 AI 做自媒体作品集 / 简历素材"
- "每天自动生成小红书内容"
- 已有类似项目要接手优化

**不适用**：
- 只做抖音 / B站 / 公众号（本 skill 聚焦小红书，但架构可迁移）
- 需要真人出镜的"生活 vlog"类内容（不适合全 AI 生产）
- 超高垂直专业领域需要人工写稿审稿（本 skill 面向资讯/工具/速报类）

## 完整执行流程（7 步）

### Step 1｜收集定位（对话式）

通过 AskUserQuestion 收集 6 个关键字段，没有的字段给默认值，别卡住用户：

| 字段 | 问题 | 默认值 |
|---|---|---|
| 领域 | 你想做什么领域的账号？ | 「AI 资讯」 |
| 频道名/昵称 | 账号叫什么？ | 让用户自定 |
| 受众 | 写给谁看？新手/进阶/专业人士？ | 「泛关注 AI 的打工人」 |
| 发布节奏 | 日更/周 3/周 5？每天几点发？ | 每日早 8:35 |
| 视觉风格 | 严肃研究风 / 爽文资讯风 / 简约极客风？ | 研究风（Aki 风：黑底白卡+宋体+红竖线+黄高亮） |
| 数据源 | 中文国内源 / 英文外网 / 中英混合？ | 国内中文源（机器之心、36kr、CSDN、腾讯新闻） |

**收集后必须确认一次**：把字段做成摘要给用户确认，不要直接开跑。

### Step 2｜初始化项目目录

```
{workspace}/
  ├─ output/               # 每日内容包
  │   └─ YYYY-MM-DD/
  │       ├─ digest.md           # 选题+文案
  │       ├─ slides.html         # 9 图源 HTML
  │       └─ images/             # 9 张 jpg
  ├─ scripts/
  │   ├─ render_slides.js        # HTML→图渲染器
  │   └─ publish_xhs.js          # 发布机器人
  ├─ templates/
  │   ├─ slides_template.html    # 视觉模板（可复用）
  │   └─ config.json             # 定位配置
  ├─ .auth/                # 登录态 + 持久 profile（不进 git）
  │   ├─ xhs_cookies.json
  │   └─ chrome_profile/
  └─ README.md             # 给用户看的 3 分钟上手指南
```

把模板文件从 skill 目录复制过去：
- `templates/slides_template.html` → 用户 output 目录
- `scripts/render_slides.js`, `scripts/publish_xhs.js` → 用户 scripts 目录

### Step 3｜选题生成

调用 WebSearch 抓取当日所选领域热点（5-8 条候选），按"热度 + 争议度 + 算法友好度"3 维打分，选出：
- 1 条主 topic（做 9 图深度版）
- 1-2 条快讯（点缀在 06 海外线 或 07 时事速览页）

**红线硬编码**（Skill 里留给用户自定义补充列表）：
- 避开与用户所在公司冲突的产品
- 避开用户在职客户真名
- 新号前 7 天避 A 股上市公司敏感话题

输出 `output/YYYY-MM-DD/digest.md`（含选题打分表 + 小红书标题 + 正文 800 字 + 10 标签 + 9 图文案）。

### Step 4｜生成 HTML 模板

根据 Step 1 选定的视觉风格，从 `templates/slides_template.html` 生成当日 `slides.html`。9 页结构：

1. 封面（标题/副标/日期/插图）
2. 导语（引文/背景铺垫）
3. 01 主角（核心事件）
4. 02 对照组（对比细节）
5. 03 为什么重要（意义解读）
6. 04 海外线 / 快讯（点缀）
7. 05 读图方式（辅助理解）
8. 06 记住这句话（金句）
9. 07 关注 CTA（@用户名 + 明日预告）

**视觉风格预设**（skill 内置 3 套，用户选一套或自定义）：
- **研究风（默认）**：黑背板 + 白卡片 + 思源宋体 Black + 红色左竖线 + 黄色马克笔高亮 + 灰底引用框
- **爽文风**：纯色大色块 + 思源黑体 Black + 大号中文数字 + 红/黄反差
- **极客风**：白底 + 等宽字体 + 单色（#111/#e63946）+ 代码块风格引用

### Step 5｜渲染图片

```bash
node scripts/render_slides.js
```

用 Puppeteer 无头模式把 HTML 渲染为 2160×2880 jpg（deviceScaleFactor=2），输出到 `output/YYYY-MM-DD/images/`。

### Step 6｜更新并启动发布脚本

- 修改 `scripts/publish_xhs.js` 的 IMAGES_DIR / POST_TITLE / POST_BODY 为当日内容
- 启动脚本（非阻塞）：用户本机弹出 Chromium → 自动跳发布页 → 上传 9 图 → 填标题 → 填正文 → 停在发布页
- 告知用户："内容已填好，请在浏览器里点『发布』"

**关键技术细节**（必须这么做，踩过的坑）：
- `userDataDir: .auth/chrome_profile` 持久化，权限永久记住
- `context.overridePermissions` 预授权 notifications/clipboard，屏蔽弹窗
- 真实 UA + `ignoreDefaultArgs: ['--enable-automation']` 绕风控
- 监听 SIGINT/SIGTERM/SIGHUP + `browser.on('disconnected')` 优雅退出
- 30s setInterval keep-alive 防 macOS 杀僵尸进程
- 首次扫码成功后 saveCookies 到 `.auth/xhs_cookies.json`

### Step 7｜调度定时任务

调用 `automation_update` 创建 recurring automation：
- 频率：用户在 Step 1 选定
- RRULE 示例：`FREQ=DAILY;BYHOUR=8;BYMINUTE=35;BYSECOND=0`
- prompt 内容：让明日自动化按 Step 3-6 执行，最终把浏览器停在发布页

### Step 8（可选）｜优化循环

发布 48 小时后，引导用户：
1. 回到这里说"看下昨天数据"
2. Skill 询问笔记链接或手动输入关键指标（播放、点赞、评论、粉丝增长）
3. 根据数据给建议：
   - 完播率 < 30%：前 3 页钩子太弱，下一期强化封面冲突
   - 互动率 < 2%：结尾 CTA 不够，优化第 9 页
   - 无粉丝增长但有流量：简介/昵称不匹配当下内容

## 用户交互模式

Skill 触发后按顺序：

1. **第 1 轮**：简短自我介绍 + AskUserQuestion 收集 6 字段（一次问完，不要来回问）
2. **第 2 轮**：展示配置摘要，请用户确认
3. **第 3 轮**：一次性完成"建目录 + 复制模板 + 跑 Step 3-6"，最终告知"浏览器已在等你点发布"
4. **后续轮次**：按用户需求微调（改风格/改选题/看数据），不要每次都重跑全流程

**交互原则**：
- 能用默认值不问用户
- 用户说"换风格"时，只重渲染图片，不重跑选题
- 用户说"不满意文案"时，只重生成 digest，不重跑视觉

## 资源文件清单

本 skill 目录下包含：
- `SKILL.md`（本文件）
- `templates/slides_template.html`：默认视觉模板（研究风）
- `scripts/render_slides.js`：渲染器
- `scripts/publish_xhs.js`：发布机器人（v3 持久 profile 版）
- `templates/config.schema.json`：定位配置 schema
- `assets/style-research.html`：研究风完整示例
- `assets/style-punchy.html`：爽文风完整示例
- `assets/style-geek.html`：极客风完整示例

## 技术依赖

- Node.js ≥ 22（用户环境自带 managed 版本）
- Puppeteer（一般已在 node workspace 里）
- 系统：macOS（Linux/Windows 需改路径）
- Chromium：Puppeteer 安装时附带

## 合规与安全

- 发布最后一步必须人工点击（新号前 7 天硬规则）
- cookies 和 profile 保存在用户项目的 .auth/ 目录，不上传云端、不进 git
- 不代表用户发任何内容，所有发布动作由用户最终确认
- 视觉模板不抄袭任何具体博主，风格为"风格类别"层级（研究风/爽文风/极客风）

## 常见问题

**Q: 用户说"我不会写代码"怎么办？**
A: 本 skill 设计前提就是用户不写代码，所有命令由 skill 调用 Bash 执行。用户只需要：① 对话回答 6 个问题 ② 扫码 1 次 ③ 每天点一下"发布"。

**Q: 视觉风格用户不满意？**
A: 别换 HTML 架构，只调 CSS 颜色/字体/间距。改完让 skill 重跑 render_slides.js 即可。

**Q: 如何扩展到抖音？**
A: 基于本 skill 的文案生成部分，增加 TTS 生成 + 数字人视频合成 + 抖音浏览器自动化。这是本 skill 的 V2 路线，当前 V1 专注小红书。

**Q: 封号风险？**
A: 保留人工点发布 + 持久 profile + 真实 UA + 发布时间带轻微随机 ±5 分钟，综合下来与真人操作难以区分。
