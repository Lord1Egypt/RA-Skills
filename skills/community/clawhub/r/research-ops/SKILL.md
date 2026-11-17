---
name: research-ops
description: 科研项目工作区通用方法论（跨项目 / 跨机，零项目专有路径）。把「本地文件 + Zotero + Obsidian + 飞书」四层按「每类内容一个真源」组织：项目 ID 命名、本地目录模板（README/STATE/scripts/data/results/output + chats + buffer）、组级 INDEX 登记表、跨机同步纪律、同步操作「双端确认」。当用户要"新建/整理科研项目、搭建组目录、登记项目索引、把项目映射到 Zotero/Obsidian/飞书、导出对话存档、处理 buffer、检查跨机同步"时使用。本 skill 只给通用规则与参数化脚本；**具体组名/路径/collection/文件夹由各项目 AGENTS.md 特化**（见 §8）。
version: 1.0.1
---

# research-ops — 科研项目工作区通用方法论

> **本 skill 只给通用规则 + 参数化脚本，零项目专有路径。**
> 具体「组名 / 本地路径 / Zotero collection / Obsidian 文件夹 / 飞书文件夹 / 同步端点」一律由**各项目的 `AGENTS.md` 特化**（§8）。
> 配合：`obsidian-ops`（笔记）、`zotero-ops`（文献）、`lark-*`（飞书）。

---

## 1. 四层真源模型（SSOT：每类内容只有一个真源）

| 内容 | 真源工具 | 组织维度 |
|------|----------|----------|
| 论文 / 引用 | **Zotero**（→ `zotero-ops`） | collection = 组/项目 |
| 笔记 / 组会 / 想法 | **Obsidian**（→ `obsidian-ops`） | 文件夹 = 组/项目 |
| 共享 / 交付（**脱敏**） | **飞书云文档**（→ `lark-drive`/`lark-doc`/`lark-base`） | 文件夹 = 组/项目 |
| 代码 / 原始数据 / 产物 | **本地文件** | `<组根>/…` |
| 项目索引 | **本地 `INDEX.md`** | 组级 |

**流动规则**：跨工具只**单向派生**——Zotero→Obsidian；本地→飞书。**原始/敏感数据永不出本地。**

---

## 2. 项目身份（ID）

`<组码>-<项目slug>`，例：`als-intronic`、`jl-cadgen`。四处命名对齐（Zotero collection / Obsidian 文件夹 / 飞书文件夹 / 本地目录）。

---

## 3. 本地目录模板

```
<组根>/
├── AGENTS.md              # ★ 特化：本组映射（§8）
├── INDEX.md               # ★ 登记表（§4）
├── projects/<项目>/       # 或小项目平铺在组根，用 INDEX 登记
│   ├── README.md  STATE.md    # 是什么 / ★当前基线
│   ├── scripts/ data/ results/ output/   # （非 git 项目 output/versions/<时间戳>/ 快照）
│   ├── handoff/               # 每轮交接单（人机协作）
│   ├── tmp/                   # 仅临时中间件；用完即清
│   └── chats/                 # 会话存档（也可放组根）
├── shared/                    # 跨项目只读（★ registry/ = 唯一事实源，可写）
├── archive/
├── buffer/                    # ★ 扁平：人 ⇄ AI 文件直接放这里（无 inbox/outbox）
├── chats/
└── .trash/                    # 软删除（压缩包 + _index.json；见 project-organization §六）
```

- **`STATE.md` = 当前基线**（AI 接手先读，只写"现在以什么为准"）。
- 删除走 `.trash/` 软删除；硬删前按全局 AGENTS「文件删除铁律」列清单并确认。

---

## 4. 组级 INDEX.md（登记表）

| 项目ID | 本地目录 | Zotero collection | Obsidian 笔记夹 | 飞书文件夹 |
|--------|----------|-------------------|-----------------|-----------|
| `jl-cadgen` | `CAD-Generation/` | `JiaLi/CAD-Generation` | `Jia Li/CAD-Generation/` | … |

机器可读版可选：`research.config.json`（组根），脚本读它以免参数散落。

---

## 5. buffer 协议（人 ⇄ AI 的**唯一交换口**）

> **值钱在哪**：用户**不用学任何东西**——丢文件 + 说一句「读取 buffer」即可；**双向 · 可追溯 · 不硬删**。**越简单越好。**

1. 用户把文件丢进 `buffer/`（扁平）；
2. 对 AI 说「**读取 buffer**」→ AI 列清单 + **归属方案**（源→目标）；
3. **等用户确认**（移动铁律）；
4. 确认后归位、记账；AI 的交付物也放 `buffer/`。

**三条硬规则**：① **TTL 2 天 = 强制清理**（超期一律清掉；buffer 只做中转）；② **buffer 里每项必须在 `projects/`（或 `shared/`/`archive/`）有归宿**（**不当唯一副本**）；③ **同一交付物只留最新一版**（旧版自动进暂存；`buffer.py tidy --apply`）。

---

## 6. chats 协议（对话存档）

- `opencode export <ses_id> > chats/<YYYYMMDD>_<主题>.json`
- **`opencode.db` 本身（本机数十 GB）永不进同步、永不迁移**——只沉淀导出的存档。

---

## 7. 跨机同步纪律（不同同步方式 + 双端确认）

| 内容 | 同步方式 | 库/端点 |
|------|----------|---------|
| 本地文件 | **Syncthing** | 各机 `THU` 等文件夹 |
| 笔记 | **Obsidian LiveSync** | 自建 CouchDB 库 |
| 文献 | **Zotero 同步**（可自建，如 altero） | 服务端 URL |

铁律：
1. **一个文件只走一条同步管道**（`opencode.db`、Obsidian vault 都不进 Syncthing）。
2. **同步类操作要「双端确认」**：本地端 + 远端（NAS）各查一次，别只看一端。
3. 脚本**禁止写死绝对路径**（换机失效）；路径/端点由参数或项目 `AGENTS.md` 提供。
4. 涉及远端访问一律走 **`ssh-mesh`**（`mesh_run.py`），不自拼 ssh。

---

## 8. 特化机制（各项目 `AGENTS.md` 写什么）

> 通用规则在本 skill；**本组的"值"写在项目 `AGENTS.md`**。模板：

```markdown
## 科研工作区特化（research-ops）
- 组码：<als | jl>
- 组根：<本地路径>
- 项目索引：本目录 INDEX.md
- 适用通用 skill：research-ops / obsidian-ops / zotero-ops（飞书走 lark-*）
- 映射：见 INDEX.md（项目ID ↔ Zotero collection ↔ Obsidian 文件夹 ↔ 飞书文件夹）
- 同步：本地 Syncthing 文件夹=<名>；笔记 LiveSync 库=<db>；文献同步=<URL>
- 会话入口：本 AGENTS.md → INDEX.md → 目标项目 AGENTS.md → STATE.md
```

---

## 9. 脚本

### scripts/new_subproject.py
用途：在任意组根下新建子项目骨架（README/STATE/各目录/chats），可选登记进 INDEX。
| 参数 | 说明 | 必填 |
|------|------|------|
| `--root DIR` | 组根或 `projects/` 父目录（**显式传入，零硬编码**） | ✅ |
| `--name SLUG` | 项目 slug | ✅ |
| `--title` | 人类可读标题（写进 README/STATE） | 否 |
| `--in-projects` | 放到 `<root>/projects/<name>/`（默认直接放 `<root>/<name>/`） | 否 |
| `--force` / `--dry-run` | 复用已存在 / 只预演 | 否 |
示例：`python scripts/new_subproject.py --root <组根> --name agent-ppt --in-projects`
输出：`{"status":"ok","project":...,"created":[...]}`

### scripts/doctor.py
用途：检查一个组根是否符合本规范（缺 README/STATE、根目录散落物、缓冲非空、INDEX 缺失）。
| 参数 | 说明 | 必填 |
|------|------|------|
| `--root DIR` | 组根 | ✅ |
| `--strict` | 有 high 级发现则退出码 1 | 否 |
示例：`python scripts/doctor.py --root <组根>`
输出：`{"status":"ok","summary":{...},"issues":[...]}`

---

## 最新版

本技能**开源**，**最新版以这两处为准**：

- **GitHub**：https://github.com/TOMUIV/research-ops-skill
- **ClawHub**：`research-ops`（`clawhub install research-ops`）
