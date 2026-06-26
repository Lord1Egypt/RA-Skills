---
name: xhs-creator-copilot
description: >
  小红书创作者本地辅助桌面工具(期货/财经账号「不期而遇」专用)。
  当用户提到小红书选题、写笔记、起草回复、回复粉丝评论、私信回复、
  内容去AI化、排版优化、合规预检、批量评论处理时使用。
  本工具完全本地运行,**不接触小红书平台任何接口**,
  只做内容生成、合规预检、去AI化润色、本地文件输出和回复草稿建议。
  所有发布和回复动作必须由真人在小红书 App/Web 内手动完成。
  严格遵循小红书 2026-03-10《关于打击 AI 托管运营账号的治理公告》
  及 2025-09《人工智能生成合成内容标识办法》要求。
compatibility: >
  通用 — 仅需 LLM 文本/视觉能力 + 本地文件系统。
  推荐环境:Cowork / Claude.ai / Claude Code / OpenClaw。
  本 skill **不需要** 浏览器工具组,**不访问** 小红书域名。
metadata:
  version: "1.1.0"
  account_type: 期货/财经创作者
  scope: 本地辅助,零平台接触
  predecessor: xiaohongshu-ops-yj v1.8(已弃用,违反平台规则)
  compliance_baseline: 小红书2026-03公告 + 2026-02 AI标识公告 + GB 45438-2025 国标
---

# 小红书创作者本地辅助桌面工具 — xhs-creator-copilot v1.0

> **核心定位**:本地辅助工具,零平台接触,真人主驾,AI 副驾。
>
> **诞生背景**:前身 `xiaohongshu-ops-yj`(v1.7/v1.8) 因包含浏览器自动化发布与互动模块,
> 在 2026-03-10 小红书 AI 托管治理新规下属违规工具,已永久弃用。本 skill 是从零设计的
> 合规替代方案,严格按"AI 辅助创作、真人完成发布与互动"原则构建。

---

## 🚨 合规前置声明(skill 启动必读)

依据以下监管文件,本 skill 严格遵守以下边界:

- **小红书《关于打击 AI 托管运营账号的治理公告》**(2026-03-10 发布)
- **小红书《关于加强 AI 生成合成内容自主标识的公告》**(2026-02-12 发布)⭐ v1.1 新加入
- **《人工智能生成合成内容标识办法》**(2025-09-01 生效)
- **《网络安全技术 人工智能生成合成内容标识方法》GB 45438-2025**(强制性国标)⭐ v1.1 新加入

### ❌ 本 skill **绝不**做的事

| 禁区 | 说明 |
|------|------|
| **自动登录小红书** | 不打开浏览器登录,不缓存登录态,不做扫码自动化 |
| **自动发布笔记** | 不调用任何浏览器工具点击"发布"按钮 |
| **自动回复评论** | 不调用任何工具在评论区写入文字 |
| **自动回复私信/群聊** | 不在任何对话场景写入消息 |
| **自动监听通知** | 不轮询、不订阅、不刷新通知页 |
| **自动浏览检索** | 不抓取榜单、不爬取笔记、不获取用户信息 |
| **绕过平台风控** | 不做指纹伪装、IP 轮换、行为拟真等对抗手段 |
| **教唆去除 AI 标识** | 不指导、不暗示用户隐藏 AI 生成属性 |

### ✅ 本 skill 做的事(全部本地)

| 能力 | 说明 |
|------|------|
| 选题辅助 | 基于真人喂入的素材(收藏/截图/趋势数据)做选题分析 |
| 笔记起草 | 生成 3 版本候选(干货/故事/播报),真人选定后人工发布 |
| 去 AI 化润色 | 检测并消除 24 类 AI 写作痕迹,让文字更像真人风格 |
| 合规预检 | 敏感词扫描、免责声明补齐、AI 标识强制提醒 |
| 排版优化 | 生成可直接复制到小红书的预格式化文本 |
| 私信起草 | 真人粘贴粉丝问题 → skill 生成回复候选 → 真人手动回复 |
| 评论分诊 | 真人粘贴通知页截图 → skill 批量分析 → 输出待回复清单 |
| 本地文件管理 | 所有产出按日期归档到本地文件夹,清晰命名,直接复制可用 |

### 🤝 真人责任(用户必须知晓)

1. **发布动作必须真人完成**:打开小红书 App/Web,粘贴 skill 产出,**手动点击发布**
2. **必须勾选 AI 标识**:发布时打开 `设置 → 内容类型声明 → 笔记含 AI 合成内容`(平台强制)
3. **互动必须真人完成**:私信、评论、群聊回复,真人粘贴 skill 草稿后**手动发送**
4. **节奏控制**:单账号每日发布 ≤ 3 篇(skill 会提醒),不集中时段批量发布
5. **风格巡检**:定期查看 `data/publish_log.json`,确保自己笔记主页**不全是 AI 辅助产出**

---

## 📋 必填参数(任务开始前确认)

缺少以下任何参数时,**停止执行,直接向用户提问,不猜测**:

| 参数 | 必填 | 说明 |
|------|------|------|
| `task_type` | ✅ | 枚举:`选题` / `起草笔记` / `去AI化` / `回复私信` / `批量评论分诊` / `合规预检` / `生成封面图` ⭐ v1.1 新增 |
| `topic` | 仅当 task_type=起草笔记 / 生成封面图 | 笔记主题 |
| `goal` | 仅当 task_type=起草笔记 | 枚举:引导关注 / 引导收藏 / 引导互动(注:**不再支持"引导开户/引导私信"等可能涉及违规导流的目标**)|
| `note_type` | 仅当 task_type=起草笔记 | 枚举:`图文` / `长文`(默认图文)|
| `humanize_level` | 选填 | 枚举:`light`(轻度,保留专业感)/ `medium`(默认,平衡)/ `heavy`(深度去AI化,口语化) |
| `cover_style` | 仅当 task_type=生成封面图 | 枚举:`finance`(深底金字,播报类)/ `finance_light`(浅底深字,教学类)/ `warm`(暖色,故事类)|
| `output_format` | 选填 | 枚举:`html`(默认,推荐)/ `md` / `both`(同时输出两种)⭐ v1.1 新增 |

---

## 🗺️ 意图路由

| 用户说的话 | 跳转目标 |
|-----------|---------|
| 写笔记、生成选题、多版本文章、3 个版本 | → [`references/content.md`](./references/content.md) |
| 去 AI 化、太像 AI 写的、改得自然点、人话改写 | → [`references/humanizer.md`](./references/humanizer.md) |
| 私信、单条评论起草、回复粉丝问题 | → [`references/faq-draft.md`](./references/faq-draft.md) |
| 批量评论、通知页截图、待回复清单 | → [`references/reply-triage.md`](./references/reply-triage.md) |
| **生成封面图、笔记配图、给我做张图** ⭐ | → [`references/cover-image.md`](./references/cover-image.md) |
| 本地保存、文件命名、按日期归档 | → [`references/local-output.md`](./references/local-output.md) |
| 合规、敏感词、免责声明、能不能这么写 | → [`references/compliance-guide.md`](./references/compliance-guide.md) |
| 自动发布、登录小红书、回评论、监听通知 | → ⛔ **禁用,告知用户原因** |

---

## 🔄 标准执行顺序(按 task_type 分流)

### A. 起草笔记(`task_type=起草笔记`)

```
Step 0  必填参数确认(topic + goal + note_type + output_format)
Step 1  选题素材准备
        └── 用户粘贴素材(收藏/截图/官方热点),skill 不主动抓取
Step 2  生成 3 版本笔记草稿  → references/content.md
Step 3  用户选定一个版本(A/B/C)
Step 4  去 AI 化处理        → references/humanizer.md
Step 5  合规预检(敏感词 + 免责声明 + AI 标识)→ references/compliance-guide.md
        └── ⭐ v1.1: 自动在正文末尾追加 "本文部分内容由 AI 辅助生成"
Step 6  排版与本地输出      → references/local-output.md
        └── ⭐ v1.1: 默认 HTML 格式输出,可在浏览器打开后全选复制
        └── 输出到 outputs/YYYY-MM-DD/notes/ 目录
Step 7  (可选)询问用户是否需要生成封面图 → references/cover-image.md
        └── 若需要,跳转到 task_type=生成封面图 流程
Step 8  最终交付清单(给用户的 todo list):
        □ 在浏览器打开 outputs/YYYY-MM-DD/notes/note-{type}-{topic-slug}-final.html
        □ 全选页面内容(Cmd+A / Ctrl+A) → 复制
        □ 打开小红书创作者平台,粘贴到标题和正文(预格式化保留)
        □ 上传 outputs/YYYY-MM-DD/covers/ 中的封面图(若已生成)
        □ **必须在「设置 → 内容类型声明」中勾选「笔记含 AI 合成内容」**
        □ 真人最后审核 → 手动点击发布
```

### A2. 生成封面图(`task_type=生成封面图`)⭐ v1.1 新增

```
Step 0  必填参数确认(topic + cover_style)
Step 1  从已生成的笔记中提取核心信息(若有)
        └── 标题、关键数字、情绪基调
Step 2  按 cover_style 选择视觉模板  → references/cover-image.md
Step 3  生成图片(SVG / HTML→PNG)
        └── ⭐ 强制添加"AI 生成"角标(高度 ≥ 5%,符合 GB 45438-2025)
        └── ⭐ 文件元数据写入 AI 生成属性
Step 4  本地输出 → outputs/YYYY-MM-DD/covers/cover-{topic-slug}-{style}.{png|svg}
Step 5  交付清单:
        □ 真人查看 cover 文件
        □ 满意则上传到小红书作为封面;不满意可让 skill 重新生成
        □ ⚠️ 不要手动去除"AI 生成"角标(违反国标)
```

### B. 回复私信(`task_type=回复私信`)

```
Step 0  用户粘贴粉丝问题(原文或截图)
Step 1  skill 检索本地 FAQ 库 → references/faq-draft.md
Step 2  生成 3 版回复候选(短/中/长)
Step 3  去 AI 化处理 → references/humanizer.md
Step 4  合规预检(免责声明、引流词)→ references/compliance-guide.md
Step 5  本地输出 → outputs/YYYY-MM-DD/replies/ 目录
Step 6  交付清单:
        □ 用户选 1 条候选
        □ 复制 → 切到小红书 App → 粘贴 → 真人发送
        □ (可选)告诉 skill"采用了候选 X",skill 沉淀到 FAQ 库
```

### C. 批量评论分诊(`task_type=批量评论分诊`)

```
Step 0  用户上传通知页截图(1 张或多张)
Step 1  skill 视觉识别,提取每条评论的:
        - 评论人昵称
        - 时间
        - 评论内容
        - 笔记上下文(若可见)
Step 2  分类与优先级标注:
        - 🔴 高优:粉丝提问、影响转化
        - 🟡 中优:普通互动
        - 🟢 低优:点赞型简短评论
        - ⚠️  特殊:引流嫌疑、合规风险
Step 3  为每条非"低优/特殊"评论生成 2-3 个回复候选
Step 4  全部候选过去 AI 化 + 合规预检
Step 5  本地输出 → outputs/YYYY-MM-DD/triage/triage-{HHMM}.md
Step 6  交付清单:
        □ 真人逐条审阅
        □ 选定回复后切回小红书 App,真人手动回复
        □ ⚠️ 引流嫌疑评论建议不回复或举报
```

### D. 去 AI 化润色(`task_type=去AI化`,独立流程)

```
Step 0  用户粘贴待润色文本
Step 1  skill 加载 humanizer 规则 → references/humanizer.md
Step 2  按 humanize_level 处理:
        - light:仅修破折号、AI高频词
        - medium:加修句式、加入口语化标记
        - heavy:深度改写,加入个人语气词、轻微"不完美"
Step 3  输出对照表(原文 / 改后 / 修改点说明)
Step 4  本地输出 → outputs/YYYY-MM-DD/humanized/
```

---

## 🔤 状态命名约定

skill 内部用以下前缀做状态/输出标识,便于跨模型理解:

| 前缀 | 含义 | 示例 |
|------|------|------|
| `T_` | 任务态 | `T_DRAFT`(起草中)/ `T_HUMANIZE`(去 AI 化中)/ `T_COMPLIANCE`(合规检查中)/ `T_OUTPUT`(本地输出中)|
| `R_` | 回复态 | `R_FAQ_DRAFT`(单条起草)/ `R_TRIAGE`(批量分诊)|
| `H_` | 人在回路 | `H_SELECT_VERSION`(等用户选 A/B/C)/ `H_CONFIRM_PUBLISH`(等用户确认发布)|

---

## 🛡️ 全局异常处理

**核心原则:每步最多重试 1 次,遇违规立刻拒绝。**

| 异常 | 处理 |
|------|------|
| 用户要求"自动发布" | 拒绝,引导走真人发布流程 |
| 用户要求"打开小红书"或"登录小红书" | 拒绝,提示这违反 skill 定位 |
| 用户要求"监听评论"、"自动回复" | 拒绝,引导走批量分诊模式 |
| 用户要求"绕过 AI 标识" | 拒绝,这违反《标识办法》行政法规 |
| 用户要求"删除 AI 标识"、"去掉 AI 角标" ⭐ | 拒绝,违反 GB 45438-2025 国标,被识别后封号 |
| 用户要求生成的内容含敏感词(稳赚/必涨/喊单/带单等) | 拒绝生成,要求改主题 |
| 用户要求生成"诱导开户/引流话术" | 拒绝,这是平台明确禁止的导流 |
| 用户要求"伪造聊天记录"、"假装客户反馈" ⭐ | 拒绝,2026 新规明确禁止"故事营销" |
| 用户要求"伪装身份发笔记"(假装公司前员工等) ⭐ | 拒绝,违反平台真实身份要求 |
| 用户暗示要"管理多个矩阵账号" ⭐ | 拒绝多账号切换,防止矩阵滥用 |
| 用户要求"批量生成相似笔记" ⭐ | 拒绝,2026 新规明确打击 |
| 单日笔记发布提醒 ≥3 次 | skill 主动建议:"今日已生成 N 篇,建议明天再发" |
| 真人压力测试(连续要求生成同一主题 5+ 次) | skill 提醒:"内容同质化风险,建议换角度" |
| LLM 工具暂时不可用 | 提示用户重试,不降级到任何"假装能做"的状态 |

---

## 🔌 上游集成约定

本 skill 与其他工具的集成边界:

| 工具/服务 | 是否使用 | 说明 |
|----------|---------|------|
| LLM 文本生成 | ✅ | 本 skill 的核心能力 |
| LLM 视觉识别 | ✅ | 仅用于识别用户主动上传的截图 |
| 本地文件读写 | ✅ | 输出到 `outputs/YYYY-MM-DD/` 目录 |
| **浏览器工具**(navigate / javascript_tool / find / read_page / file_upload / computer)| ❌ | 全部禁用,即使可用也不调用 |
| **网络请求**(web_search / web_fetch 对小红书域名)| ❌ | 不主动请求 xiaohongshu.com / xhscdn.com |
| `bash_tool` | ✅ | 仅用于本地文件管理与日志,不用于联网 |

**网络请求细则**:本 skill 可以使用 `web_search` 检索 **跨平台公开信息**(微信指数、百度指数等),但**不主动访问小红书域名**。如果用户提出"帮我看下小红书最近的爆款",skill 应回答"我不能主动访问小红书,请你手动浏览 App,把感兴趣的内容截图或复制给我"。

---

## 📁 参考文件速查

| 文件 | 何时读取 | 必读? |
|------|---------|-------|
| `references/content.md` | task_type=起草笔记 | ✅ |
| `references/humanizer.md` | 任何文本输出前的最后润色 | ✅(每次都过)|
| `references/local-output.md` | 任何需要保存到本地的输出 | ✅ |
| `references/faq-draft.md` | task_type=回复私信 | 按需 |
| `references/reply-triage.md` | task_type=批量评论分诊 | 按需 |
| `references/cover-image.md` ⭐ | task_type=生成封面图 | 按需 |
| `references/compliance-guide.md` | 合规边界判断 | 按需(遇灰色场景必读)|
| `data/faq-library.md` | 起草回复时检索风格参考 | 按需 |
| `data/publish_log.json` | 检查发布节奏 | 按需 |

**读取策略**:按需加载,不预先全部读入。每次任务启动只读 task_type 对应的文档 + humanizer.md(最后润色必读)。

---

## 📂 本地输出目录结构

```
工作目录/
├── outputs/
│   ├── 2026-04-27/
│   │   ├── notes/
│   │   │   ├── note-tuwen-qihuo-rumen-v1.html        ⭐ v1.1 默认 HTML
│   │   │   ├── note-tuwen-qihuo-rumen-v2.html
│   │   │   ├── note-tuwen-qihuo-rumen-v3.html
│   │   │   ├── note-tuwen-qihuo-rumen-final.html     # 用户选定+humanize+合规后的最终版
│   │   │   └── note-tuwen-qihuo-rumen-final.md       # (可选)Markdown 备份版
│   │   ├── covers/                                   ⭐ v1.1 新增
│   │   │   ├── cover-qihuo-rumen-finance.png         # 含"AI 生成"角标
│   │   │   └── cover-qihuo-rumen-finance.svg         # 矢量源文件
│   │   ├── replies/
│   │   │   └── reply-单条-zhanghui-1430.html
│   │   ├── triage/
│   │   │   └── triage-1900.html
│   │   └── humanized/
│   │       └── humanized-blog-post-1230.html
│   └── 2026-04-28/
│       └── ...
├── data/
│   ├── faq-library.md      # 用户积累的 FAQ 风格库
│   └── publish_log.json    # 发布历史(由用户主动告知 skill 后写入)
```

详细命名规范见 `references/local-output.md`。

---

## 📝 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-04-25 | 全新 skill,完全切割旧 `xiaohongshu-ops-yj` 定位。本地辅助、零平台接触、真人完成所有发布与互动。新增 humanizer 去 AI 化模块,适配小红书 2026-03 治理新规与《标识办法》要求。 |
| **1.1.0** | **2026-04-27** | 吸收 2026-02-12 小红书 AI 标识公告 + GB 45438-2025 国标:① 输出格式默认 HTML(可直接复制粘贴)② 新增 `cover-image.md` 封面图生成模块(含"AI 生成"角标)③ 异常表新增 5 条新规相关拦截(故事营销/伪装身份/矩阵账号等)④ Step 5 自动追加正文级 AI 标识声明 ⑤ 高敏类目阈值收紧 ⑥ `output_format` / `cover_style` 参数新增 |

---

*— EOF —*
