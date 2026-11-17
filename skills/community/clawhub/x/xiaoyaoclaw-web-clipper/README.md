# OpenClaw Web Clipper 📎

<div align="center">
  <strong>网页剪藏（知识喂料机）</strong> | <a href="README.en.md">🌐 English</a>
</div>

<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="OpenClaw Web Clipper — save any web page as clean local Markdown with frontmatter. Dual-engine extraction (readability + trafilatura), Chinese-friendly filenames, batch clipping with dedup, output lands in knowledge/clippings/ ready for kb-retriever indexing.">
</p>

> 网页「知识喂料机」：发送链接 → 提取正文 → 保存本地 Markdown（frontmatter 齐全）→ 直通 knowledge/ 建索引可检索。双引擎提取、中文友好、批量去重。
> OpenClaw web clipper: save any web page as clean local Markdown with YAML frontmatter. Dual-engine extraction (readability-lxml + trafilatura fallback), Chinese-safe filenames, batch clipping with dedup, output ready for kb-retriever indexing.

![license](https://img.shields.io/badge/license-MIT-green)
[![ClawHub downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fclawhub.ai%2Fapi%2Fv1%2Fskills%2Fxiaoyaoclaw-web-clipper&query=skill.stats.downloads&label=ClawHub%20downloads&color=blue)](https://clawhub.ai/dtsola/skills/xiaoyaoclaw-web-clipper)

## 为什么需要

看到好文章想存下来，但：
- 🔖 浏览器收藏夹越攒越乱，**永远不再打开**
- 📝 复制粘贴到笔记，**格式稀碎**、没有来源、没有日期
- 🌐 剪藏工具（印象笔记/Cubox）**数据在云端**，还得付费、怕泄露
- 🧠 收藏了想喂给 AI 知识库，**格式不统一没法检索**

这个 skill 解决：**一个命令，网页 → 干净的本地 Markdown**，自动带标题/来源/作者/日期 frontmatter，直接进 knowledge/ 建索引，AI 随时可检索。

## 特性

- 🔧 **双引擎提取**：readability-lxml（快）+ trafilatura（学术级）自动降级链，质量分不足自动切换，bs4 兜底
- 🇨🇳 **中文友好**：微信公众号/知乎/CSDN 容器适配、GBK/UTF-8 编码自动判定、**中文标题文件名安全保留**
- 📋 **批量剪藏**：URL 列表文件一次剪完，汇总报告（成功/跳过/失败）
- 🔁 **自动去重**：`.clips-index.json` 索引，重复 URL 自动跳过
- 📦 **frontmatter 齐全**：标题/来源/作者/日期/标签，Obsidian 兼容
- 🔗 **知识库闭环**：默认输出 `knowledge/clippings/`，配合 kb-retriever 一键建索引即可检索
- 🖥️ **双平台**：Windows / macOS 行为一致（纯 Python）
- 🔒 **纯本地**：不调用外部 API，数据不出本机

## 安装

```bash
# ClawHub（推荐）
clawhub install xiaoyaoclaw-web-clipper

# 或从 GitHub 手动安装
git clone https://github.com/dtsola/xiaoyaoclaw-web-clipper
# 把 SKILL.md、scripts/ 放到你的 skills 目录
```

依赖：`requests` `beautifulsoup4` `lxml`（增强引擎可选 `readability-lxml` `trafilatura`）——
**版本下限已钉**，避免装到已知有问题的旧版本：

```bash
pip install -r requirements.txt
# 等价于：requests==2.34.2 / beautifulsoup4==4.15.0 / lxml==6.1.1
# 可选增强（提取质量更高，缺了自动降级）：
#   readability-lxml==0.9 / trafilatura==2.2.0
```

## 使用

> ⚠️ **会写本地文件**：剪藏在 `~/knowledge/clippings/` 下**新建 `.md`** 并更新去重索引 `.clips-index.json`；内容随后可被 kb-retriever 检索 —— 属**本地持久化**动作，首次使用前请知悉。
> ⚠️ **会联外网**：抓取会把本次访问的常规请求元数据（IP、UA）暴露给目标站点——这是剪藏功能的固有代价；只允许 http/https + 80/443 + 公网目标（内网/回环/云元数据地址一律拒绝），且**校验后固定连接地址**（连到已校验的那个 IP，连接期不再做域名解析 → DNS 重绑定无效）。
> 🌐 语言可选：默认中文，用英文或其他语言提问就用该语言回答。

1. 把 skill 放到 OpenClaw 的 skills 目录
2. 对你的 agent 说：**「剪藏这个 https://...」**（**要点名具体链接**）→ agent 提取正文、保存 Markdown 并告诉你文件路径
3. **不会因为「读到」就触发**：网页正文、引用的聊天、文档里出现的「剪藏这个链接 / save this page」等文字一律当**数据**，不会当作指令去抓取；只有你直接给链接并要求留存才算调用

也可以直接跑脚本：

```bash
# 单条剪藏（默认存 ~/knowledge/clippings/）
python scripts/clip.py <URL>

# 指定目录 + 标签
python scripts/clip.py <URL> --dir ~/knowledge/clippings --tags ai,research

# 批量剪藏（每行一个 URL，# 注释）
python scripts/clip.py --batch urls.txt

# 检查依赖
python scripts/clip.py --check
```

## 🚀 快速上手（三步，5 分钟）

### Step 1：安装技能 + 依赖

```bash
clawhub install xiaoyaoclaw-web-clipper
pip install requests beautifulsoup4 lxml readability-lxml trafilatura
```

### Step 2：剪藏一篇文章

对你的 agent 说：

> 剪藏 https://example.com/article

几秒后它会告诉你：`✅ 已保存到 knowledge/clippings/20260828_文章标题.md`

### Step 3：入库检索（配合 kb-retriever）

剪藏多了之后，重建一次知识库索引：

```bash
python <kb-retriever>/scripts/build_index.py <knowledge根目录>
```

之后就能对你的 agent 说「检索一下知识库里关于 XX 的内容」，剪藏的文章会被检索到。

### 日常使用习惯

| 场景 | 做法 |
|---|---|
| 存单篇文章 | 「剪藏 <URL>」 |
| 批量收藏 | 整理 URL 到 txt，`--batch urls.txt` |
| 分类管理 | `--dir knowledge/clippings/<主题>` + `--tags` |
| 入库检索 | 定期跑 kb-retriever 的 `build_index.py` |
| 工作区体检 | auditor 会检查 clippings 是否建了索引（没建会提示） |

## 和现成方案对比

| | 浏览器收藏夹 | 云端剪藏（印象笔记/Cubox） | **xiaoyaoclaw-web-clipper** |
|---|---|---|---|
| 格式 | 无，只有链接 | 有，但私有格式 | ✅ 标准 Markdown + frontmatter |
| 数据归属 | 浏览器 | 云端（付费/隐私） | ✅ 本地文件，纯本地 |
| 检索 | 无 | 站内搜索 | ✅ 进知识库，AI 可检索 |
| 自动化 | 手动 | 手动 | ✅ agent 一句话触发，批量+去重 |
| 依赖 | 无 | 订阅制 | ✅ 免费，仅 Python |

## 目录结构

```
xiaoyaoclaw-web-clipper/
├── SKILL.md                    # 技能主体（触发词 / 工作流程 / 红线）
├── scripts/
│   ├── clip.py                 # 【核心】主入口：单 URL / 批量 / 去重 / frontmatter
│   └── extract.py              # 【核心】双引擎提取模块（readability + trafilatura 降级链）
├── assets/readme/
│   ├── hero.svg                # README 封面
│   └── community-qr.png        # 交流群二维码
├── docs/
│   └── DESIGN.md               # 设计方案（引擎降级链 / 元数据规则 / 测试记录）
├── README.md / README.en.md
└── LICENSE
```

## License

MIT — 随便用，署名可选。

---

## 🛠️ 需要定制？

**Agent & Skills 定制，价格 ¥800 起。**

- 微信：`dtsola`（添加好友时备注：**openclaw定制**）
- 服务范围：OpenClaw 多 agent 部署 / 工作区规范化 / 自定义 Skill 开发 / agent 记忆系统搭建 / 知识库搭建

## 姊妹项目（十件套）

- 🏠 **xiaoyaoclaw-workspace-initializer**（工作区初始化器）：给每个 agent 一个「家」——标准目录结构 + WORKSPACE.md 规范 + 多 agent 配置安全。<https://github.com/dtsola/xiaoyaoclaw-workspace-initializer>
- 🧠 **xiaoyaoclaw-memory-distill**（记忆蒸馏）：把对话蒸馏成 MEMORY.md + 日常日志，解决上下文溢出。<https://github.com/dtsola/xiaoyaoclaw-memory-distill>
- 🗂️ **xiaoyaoclaw-task-progress-tracker**（任务进度跟踪器）：目录即容器，PROGRESS.md 即进度——tasks/ 与 projects/ 生命周期管理。<https://github.com/dtsola/xiaoyaoclaw-task-progress-tracker>
- 📚 **xiaoyaoclaw-kb-retriever**（知识库检索器）：本地知识库检索——分层 data_structure.md 索引导航 + 渐进式检索（md/pdf/xlsx），无需 API key，Windows / macOS 双平台。<https://github.com/dtsola/xiaoyaoclaw-kb-retriever>
- 🩺 **xiaoyaoclaw-workspace-auditor**（工作区体检）：只读扫描健康度——目录合规、任务进度、记忆日志、知识库索引、垃圾文件，分级报告 + 修复建议。<https://github.com/dtsola/xiaoyaoclaw-workspace-auditor>
- 🤝 **xiaoyaoclaw-agent-orchestrator**（Agent 协作编排，**协作层**）：架在生态之上——拆任务、分 agent、管进度、聚结果、失败重试。<https://github.com/dtsola/xiaoyaoclaw-agent-orchestrator>
- 📊 **xiaoyaoclaw-usage-report**（用量报告）：解析 session JSONL，回答「每次 agent 任务花了多久、用了哪些工具/技能/模型、消耗了多少 token」——零依赖纯本地，token 为主指标。<https://github.com/dtsola/xiaoyaoclaw-usage-report>
- 🎛️ **xiaoyaoclaw-commander**（跨工具指挥官，**指挥层**）：让任意支持 Agent Skills 的工具（Claude Code / Codex / OpenCode / Trae / DSH）指挥小遥Claw / OpenClaw 多 agent 系统。<https://github.com/dtsola/xiaoyaoclaw-commander>
- 🔍 **xiaoyaoclaw-seo-skill**（SEO 技能）：网站搜索可见性分析与优化——audit（技术SEO）/page（页面）/content（内容质量）/schema（结构化数据）/geo（AI搜索优化）五流程 + 零依赖审计脚本，跨工具通用。<https://github.com/dtsola/xiaoyaoclaw-seo-skill>

## 小遥Claw

**小遥Claw，把 AI 助手装进自己的电脑。**

- 🚀 宣传页：<https://www.yuque.com/dtsola/igp1aa/adcicbai2zlem0bz>
- 📖 介绍页：<https://github.com/dtsola/xiaoyaoclaw-introduction>

## 关于作者

- 🌐 博客：<https://www.dtsola.com>
- 📺 B站：<https://space.bilibili.com/736015>
- 💻 GitHub：<https://github.com/dtsola>
- 📕 小红书：<https://www.xiaohongshu.com/user/profile/5b4c0597e8ac2b06aa13346d>

## 💬 加入交流群

小遥全系产品用户交流群——产品反馈 · 使用交流 · 功能建议：

<p align="center">
  <img src="./assets/readme/community-qr.png" width="280" alt="小遥AI 用户交流群二维码：扫码加群，或添加微信 dtsola（备注：加群）">
</p>

<p align="center">扫码加群，或添加微信 <code>dtsola</code>（备注：<b>加群</b>）</p>
