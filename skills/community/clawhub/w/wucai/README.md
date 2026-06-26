# 五彩 (WuCai / WuCai Highlight) Skill for OpenClaw

[](https://www.google.com/search?q=%5Bhttps://opensource.org/licenses/MIT-0%5D\(https://opensource.org/licenses/MIT-0\))

**五彩 (WuCai)** - 专业的网页划线批注、全文剪藏与个人知识库管理工具。  
**WuCai Highlight** - Web highlighter, annotation, full-text clipping, and personal knowledge base manager.

-----

## 🚀 快速安装 (Quick Installation)

你可以通过以下任意一种方式完成安装：

**方式一：对话安装 (推荐)**
直接在 OpenClaw 对话框中对 AI 说：

> `Install wucai skill from ClawHub`

**方式二：指令安装**
在对话框中输入以下指令：

```bash
/install https://raw.githubusercontent.com/makediff/wucai-openclaw/main/SKILL.md
```

-----

## 🔑 核心配置流程 (Critical Setup Guide)

**⚠️ 必须完成以下 3 步，AI 才能正常访问您的五彩数据。**

### 第一步：确认您的账号区域 (Confirm Your Region)

五彩各区域（CN/EU/US）数据**物理隔离且不互通**。请根据您的注册区域，直接对 AI 发送指令：

| 您的账号区域 | 请直接对 AI 说： |
| :--- | :--- |
| **中国/亚洲 (CN)** | `帮我配置五彩，我在中国区域` |
| **欧洲 (EU)** | `Help me configure WuCai, I'm in EU region` |
| **美国 (US)** | `Help me configure WuCai, I'm in US region` |

### 第二步：获取 OpenClaw 专用 Token

AI 会根据区域回复您对应的获取链接。您也可以手动访问（需登录对应区域账号）：

  - **CN (中国区)**: [https://marker.dotalk.cn/\#/personSetting/openapi](https://marker.dotalk.cn/#/personSetting/openapi)
  - **EU (欧洲区)**: [https://eu.wucainote.com/\#/personSetting/openapi](https://eu.wucainote.com/#/personSetting/openapi)
  - **US (美国区)**: [https://us.wucainote.com/\#/personSetting/openapi](https://us.wucainote.com/#/personSetting/openapi)

> **注意**：请拷贝页面中以 **`wct-`** 开头的 **OpenClaw 专用 Token**，不要错拷贝成普通 API Key。

### 第三步：绑定与验证 (Bind & Verify)

1.  将拷贝的 Token 发送给 AI 完成绑定。
2.  **验证连接**：发送指令 `“看看今天的五彩划线”`。如果 AI 能够正常读出内容，即表示配置成功！

-----

## ✨ 核心能力 (Core Capabilities)

| 能力 (Capability) | 对应函数 (Function) | 说明 (Description) |
| :--- | :--- | :--- |
| **🔍 跨区域语义搜索** | `search_highlights`, `search_articles` | 跨文章精准定位标题、划线文本或个人批注。 |
| **📅 时间区间追溯** | `list_highlights`, `list_diary` | 支持快捷键或自定义日期，回顾过去 **14 天内** 的知识增量。 |
| **✍️ 每日复盘与记录** | `append_diary`, `list_diary` | 快速向五彩日记追加灵感，或调取历史心路进行每日复盘。 |
| **🎯 精准内容问答** | `get_article_details` | 通过 URL 或 ID 获取划线上下文，实现基于私有笔记的深度问答。 |
| **📥 知识流状态管理** | `list_articles`, `set_article_status` | 管理剪藏库的生命周期（Inbox, Later, Archive）。 |

-----

## 📋 常见问题 (FAQ)

  - **为什么提示 Token 无效？** 请确认 Token 是否以 `wct-` 开头。如果是从普通 API 页面拷贝的 Key 将无法在 OpenClaw 中使用。
  - **搜不到较早之前的划线？** 出于性能与隐私平衡，单次查询的最大时间跨度限制为 **14 天**。如需查询更久之前的内容，请指定具体日期（如：“看下 2025-11-20 的划线”）。
  - **区域设置错了怎么办？** 随时对 AI 说 `“将五彩区域切换为 eu”`（或 cn/us），AI 会自动更新请求域名并引导您重新获取该区域的 Token。

-----

## 🔐 安全与隐私 (Security & Privacy)

  - **隐私隔离**: 笔记和日记是私密数据，AI 仅在您的明确指令下才会读取或搜索相关内容。
  - **零依赖执行**: 核心脚本 `scripts/wucai_api.py` 采用 Python 原生 `urllib` 实现，**无 requests 等第三方库依赖**，确保执行环境安全纯净。
  - **本地运行**: 所有 API 请求均在您的 OpenClaw 本地环境触发，具备 15s 超时保护。

-----

## 📜 相关链接 (Links)

  - **官方网站 (Official)**:
      - 中文: [https://doc.wucai.site/](https://doc.wucai.site/)
      - Global: [https://wucainote.com/](https://wucainote.com/)
  - **问题反馈 (Feedback)**: [https://github.com/makediff/wucai-openclaw/issues](https://github.com/makediff/wucai-openclaw/issues)
  - **许可证 (License)**: MIT-0

-----

## License

MIT-0 (MIT No Attribution) · Published on [ClawHub](https://clawhub.ai)

-----