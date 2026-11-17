# Unified-Research-Finder

**[简体中文](#简体中文) | [English](#english)**

## 目录 / Table of Contents

- [简体中文](#简体中文)
  - [1. 简介](#1-简介)
  - [2. 安装与使用](#2-安装与使用)
  - [3. 技术原理](#3-技术原理)
  - [4. 致谢](#4-致谢)
- [English](#english)
  - [1. Introduction](#1-introduction)
  - [2. Install & Use](#2-install--use)
  - [3. How It Works](#3-how-it-works)
  - [4. Acknowledgements](#4-acknowledgements)

---

# 简体中文

## 1. 简介

**Unified-Research-Finder** 是一个用于 WorkBuddy / 兼容 SkillHub 的「学术文献一站式检索」技能。它把两套最常用的学术搜索引擎合二为一：

- **PubMed**（生物医学权威数据库）——走官方 E-utilities API，返回真实 PMID、摘要、DOI。
- **Google Scholar 及其镜像站**——覆盖「KipHub学术」「烂番薯学术」「学术搜索Pro」「灯塔学术」「Google Scholar 香港镜像」「Google Scholar 官方站」**六个源**，按「kiphub → 烂番薯 → 学术搜索Pro → 灯塔 → 香港 → 官方」优先级自动回退。

默认开启 **PubMed + Scholar 跨库合并去重**：同一篇论文不会在两库里重复出现。所有结果均来自真实网络响应，**找不到就是找不到，绝不编造**。

## 2. 安装与使用

> 给电脑小白的话：别慌，这东西不需要你懂编程，跟着点就行。

**第一步：拿到文件**
把本仓库（文件夹 `Unified-Research-Finder`）整个下载下来，放到你电脑里 WorkBuddy 的技能目录：
- Windows：`C:\Users\你的用户名\.workbuddy\skills\Unified-Research-Finder\`
- macOS / Linux：`~/.workbuddy/skills/Unified-Research-Finder/`

（你也可以直接把仓库里的 `Unified-Research-Finder` 文件夹复制过去。）

**第二步：开始用**
在 WorkBuddy 对话框里直接说人话就行，例如：
- 「帮我找 CRISPR 基因编辑 的最新文献」
- 「在 PubMed 上搜 二甲双胍 和 2 型糖尿病」
- 「用灯塔学术查 大语言模型 综述」

技能会自动同时检索两库、合并去重，并告诉你「已开启多库去重，可手动关闭」。
如果你不想去重，说一句「不用去重」，它会保留重复项。

> 进阶（可选）：脚本是纯 Python 标准库写的，装好 Python 3.8+ 即可直接在命令行跑：
> ```bash
> python scripts/unified_search.py --query "CRISPR gene editing" --num 10
> ```

**项目结构 / Project Structure：**

```
Unified-Research-Finder/
├── SKILL.md                # 技能说明（触发词、检索流程、输出模板）
├── CHANGELOG.md            # 更新日志
├── LICENSE                 # MIT-0 开源协议
├── README.md               # 本说明文件（中英双语）
├── .gitignore              # 忽略 Python 缓存等无关文件
├── scripts/
│   ├── unified_search.py   # 双库合并去重入口（默认推荐）
│   ├── pubmed_search.py    # PubMed 官方 API 检索
│   └── scholar_search.py   # Google Scholar 及镜像站检索
└── references/
    ├── scholar-sources.md       # 四个 Scholar 源的技术细节
    ├── pubmed-query-syntax.md   # PubMed 检索语法
    └── register-api-key.md      # 免费注册 NCBI API key 引导
```

（运行时自动生成的 `__pycache__` 等缓存已被 `.gitignore` 排除，不会进入仓库。）

## 3. 技术原理

- **纯标准库、零依赖**：所有脚本只用 Python 自带模块（`urllib` / `json` / `re` / `subprocess`），无需 `pip install`，启动快、内存低。
- **PubMed**：直接调用 NCBI 官方 `esearch` + `efetch` 接口，拿到结构化 JSON（PMID、标题、作者、期刊、摘要、DOI），真实可验证。
- **Scholar 多源回退**：优先用「灯塔学术」的 JSON API（最快最省内存）；若被限流，自动退回「烂番薯」服务端渲染 HTML（带 Referer 解析）；再不行试香港镜像与官方站。任一源被拦截（403 / 验证码 / 超时）即跳下一源。
- **跨库合并去重**：`unified_search.py` 用子进程并行调用上面两个脚本，把结果统一字段后，以 **DOI 或归一化标题** 为键去重——同一篇论文在 PubMed 和 Scholar 都出现时只保留一条。
- **浏览器兜底（可选）**：当所有 HTTP 方式都被拦，可装 Playwright 用 `--browser` 模式做无头渲染；该模式较重，仅按需启用，不常驻。

## 4. 致谢

本技能最初是作为 [`paper-finder`](https://clawhub.ai/wangjinhongmy-pixel/skills/paper-finder) 的升级案例而构思的。`paper-finder` 提供了「只返回真实文献、绝不编造」的优良第一原则，以及清晰的技能结构范式，本项目的 PubMed 网页检索思路也受其启发。在此对 `paper-finder` 的作者表达诚挚感谢。

---

# English

## 1. Introduction

**Unified-Research-Finder** is an all-in-one academic literature search skill for WorkBuddy / SkillHub-compatible agents. It unifies two of the most-used scholarly search engines:

- **PubMed** (the authoritative biomedical database) — powered by the official NCBI E-utilities API, returning real PMIDs, abstracts, and DOIs.
- **Google Scholar and its mirrors** — covering "KipHub", "Lanfanshu", "Scholar Pro", "Dotaindex", the Google Scholar Hong Kong mirror, and the official Google Scholar site — **six sources** with auto fallback in priority order.

Cross-database **merge + deduplication (PubMed + Scholar) is on by default**: the same paper never appears twice. Every result comes from a real network response — **if nothing is found, we say so; we never fabricate.**

## 2. Install & Use

> Plain-English version for non-technical users: don't panic, you don't need to know any coding.

**Step 1 — Get the files**
Download this repository (the `Unified-Research-Finder` folder) and drop it into your WorkBuddy skills directory:
- Windows: `C:\Users\YourName\.workbuddy\skills\Unified-Research-Finder\`
- macOS / Linux: `~/.workbuddy/skills/Unified-Research-Finder/`

(You can simply copy the `Unified-Research-Finder` folder from the repo.)

**Step 2 — Start using**
Just talk to WorkBuddy in plain language, e.g.:
- "Find me the latest papers on CRISPR gene editing"
- "Search PubMed for metformin and type 2 diabetes"
- "Use Dotaindex to look up large language model surveys"

The skill searches both databases, merges and deduplicates, and tells you "cross-database deduplication is on; you can turn it off." If you don't want deduplication, just say so and it keeps the duplicates.

> Advanced (optional): the scripts use only the Python standard library. With Python 3.8+ you can run them directly from the command line:
> ```bash
> python scripts/unified_search.py --query "CRISPR gene editing" --num 10
> ```

**Project Structure:**

```
Unified-Research-Finder/
├── SKILL.md                # Skill manifest (triggers, search flows, output templates)
├── CHANGELOG.md            # Changelog
├── LICENSE                 # MIT-0 license
├── README.md               # This file (bilingual)
├── .gitignore              # Excludes Python caches and unrelated files
├── scripts/
│   ├── unified_search.py   # Dual-database merge + dedup entry point (recommended)
│   ├── pubmed_search.py    # PubMed official API search
│   └── scholar_search.py   # Google Scholar & mirrors search
└── references/
    ├── scholar-sources.md       # Technical details of the four Scholar sources
    ├── pubmed-query-syntax.md   # PubMed query syntax
    └── register-api-key.md      # Guide to register a free NCBI API key
```

(Runtime-generated caches such as `__pycache__` are excluded by `.gitignore` and never enter the repository.)

## 3. How It Works

- **Standard library only, zero dependencies**: every script uses only Python built-ins (`urllib` / `json` / `re` / `subprocess`) — no `pip install` needed; fast startup, low memory.
- **PubMed**: calls the official NCBI `esearch` + `efetch` endpoints and gets structured JSON (PMID, title, authors, journal, abstract, DOI) — verifiable and real.
- **Scholar multi-source fallback**: prefers the "Dotaindex" JSON API (fastest, lowest memory); if rate-limited, falls back to "Lanfanshu" server-rendered HTML (parsed with a `Referer` header); then the HK mirror and the official site. Any blocked source (403 / CAPTCHA / timeout) triggers the next one.
- **Cross-database merge + dedup**: `unified_search.py` invokes the two scripts as subprocesses, normalizes their fields, then deduplicates by **DOI or normalized title** — so a paper present in both PubMed and Scholar is kept only once.
- **Browser fallback (optional)**: when every HTTP path is blocked, install Playwright and use `--browser` for headless rendering; this mode is heavy and only used on demand, never resident.

## 4. Acknowledgements

This skill was originally conceived as an upgraded case study of [`paper-finder`](https://clawhub.ai/wangjinhongmy-pixel/skills/paper-finder). `paper-finder` established the excellent first principle of "return only real literature, never fabricate" and a clean skill structure; its approach to PubMed web search was also an inspiration. Sincere thanks to the author of `paper-finder`.
