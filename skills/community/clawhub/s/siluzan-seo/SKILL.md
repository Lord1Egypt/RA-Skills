---
name: seo-content-generator
description: >-
  工业 B2B 海外 SEO **网页结构化 JSON** 生成（非通用写稿）：按各子目录 schemas/output.json 输出
  引流页矩阵 / Blog SEO 包 / 外链 SEO 包（TDK、模块字段、密度自检等）。
  仅当用户明确要 SEO landing page JSON、批量引流页 schema、官网 Blog 结构化上线包、
  guest post JSON、TDK+output.json 交付时使用；先加载 siluzan-cso 做 RAG，再 Read 本子 Skill 路由。
  **不是** siluzan-cso 替代：口播/公众号/短视频/平台运营文案/无 schema 的普通写稿 → 只用 siluzan-cso。
---

# SEO 网页 Schema 生成（总 Skill）

本套件产出的是 **符合 `schemas/output.json` 的 JSON 网页物料**（引流页 `pages[]`、Blog/外链的 TDK + 正文字段 + 审计字段），供建站/CMS 灌入——**不是** CSO 三库口播/公众号等通用写稿流程。

工业 B2B 事实来源仍走 **siluzan-cso RAG**；本 Skill 只负责 **SEO 结构化 schema 生成与校验**。

## 一键安装

如果 CLI 尚未安装，直接帮用户执行对应平台的安装脚本：

- **macOS / Linux / WSL：**
  ```bash
  bash <(curl -fsSL https://unpkg.com/siluzan-seo-cli@latest/dist/skill/scripts/install.sh)
  ```
- **Windows PowerShell：**
  ```powershell
  irm https://unpkg.com/siluzan-seo-cli@latest/dist/skill/scripts/install.ps1 | iex
  ```

Windows 注意：部分 Agent 客户端通过 PowerShell / cmd 代执行命令时存在兼容性问题。若上述命令异常失败，请先安装 [Git for Windows](https://git-scm.com/download/win)，然后在 Git Bash 中执行 macOS / Linux / WSL 的 Bash 安装命令。

脚本会自动完成 Node.js 检测/安装、`siluzan-seo-cli` 全局安装、`siluzan-seo init --global --force` 注册 Skill。**无需 login 或 API Key**。

---

## CLI 命令索引

| 命令 | 作用 | 详细文档 |
|------|------|----------|
| `siluzan-seo init` | Skill 文件初始化（写入 AI 助手目录） | [references/setup.md](references/setup.md) |
| `siluzan-seo update` | 升级 CLI 并刷新已安装 Skill 文件 | [references/setup.md](references/setup.md) |
| `siluzan-seo export -f <文件> -t docx\|pdf` | Markdown / 纯文本 / SEO JSON → Word 或 PDF | [references/export.md](references/export.md) |

---

## 与 siluzan-cso 的分工

| 用户意图 | 用哪个 |
| -------- | ------ |
| 口播稿、公众号、Blog 成稿（无 output.json）、改稿、人设、发布 | **siluzan-cso** |
| 批量引流页 JSON、SEO landing schema、Blog/外链 **结构化上线包**（含 TDK、seo_audit 等 schema 字段） | **本 Skill（+ siluzan-cso RAG）** |
| 只说「写 SEO 文章 / 写 Blog」但未要 JSON schema | **siluzan-cso**；若需 schema 再追问或转本 Skill |

## 导出 Word / PDF

要 Word/PDF/审阅稿 → Read [references/export.md](references/export.md)，执行 `siluzan-seo export -f <文件> -t docx|pdf`。勿自写 docx 脚本；仅加载子 skill 时同理。

## 子 Skill 路由

根据任务类型 **必须先 Read 对应子目录的 `SKILL.md`**，再按 prompts 与 **`schemas/output.json`** 执行：

| 场景 | 子目录 | 子 Skill 名 |
|------|--------|-------------|
| 批量引流页，N 个关键词 → N 个页面 JSON | [seo-traffic-page/SKILL.md](seo-traffic-page/SKILL.md) | `seo-traffic-page` |
| 单篇 Blog SEO 包（E-E-A-T / HCU / 上线字段） | [blog/SKILL.md](blog/SKILL.md) | `seo-blog-article` |
| 单篇外链 SEO 包（guest post JSON + backlink_notes） | [backlink-article/SKILL.md](backlink-article/SKILL.md) | `seo-backlink-article` |

**路由规则（按优先级）：**

0. 导出 Word/PDF → `siluzan-seo export`（见上）
1. 用户提供 **关键词数组** 或明确「批量引流页 / landing JSON / traffic page schema」→ `seo-traffic-page`
2. 用户明确「外链 JSON / guest post schema / backlink output.json」→ `backlink-article`
3. 用户提供 **title + keyword** 且要 **Blog SEO 结构化包**（含 seo_audit、publishing_recommendation 等 schema 字段）→ `blog`
4. 仅说「写 SEO 文章 / 博客」**未**要求 JSON schema → **不要**进本 Skill；用 **siluzan-cso**
5. 类型不明且用户确实要 schema 交付 → AskQuestion：批量页 JSON / Blog 包 / 外链包

## 共用约束（三子 Skill 均适用）

- **事实来源**：KB（经 siluzan-cso RAG）为唯一事实来源；KB 无依据的数据、认证、客户名不得编造
- **主关键词密度**：1%-3%（主词及核心拓展词次数 / 英文单词总数）
- **总关键词密度**：3%-10%（主词+辅助词+长尾及合理变体之和 / 英文单词总数）
- **TDK**：Title 45-55 英文字符（计空格）；Keywords 3-5 个；Description 145-155 英文字符（计空格）
- **输出**：合法 JSON，**严格符合**各子目录 `schemas/output.json`；正文纯文本，禁止 Markdown/HTML（表格等走 schema 独立字段）
- **语言**：正文英文；Blog/外链含中文字段见各子 schema

详细对比见 [README.md](README.md)。

## 执行流程

```
任务 Progress:
- [ ] 0. 确认用户要的是 JSON schema 交付（非普通写稿）；否则 siluzan-cso
- [ ] 1. 加载 siluzan-cso，按子 skill.yaml 做 RAG（若环境支持）
- [ ] 2. 判定子 Skill（上表）
- [ ] 3. Read 子目录 SKILL.md + schemas/output.json
- [ ] 4. Read 子目录 prompts/system.md、prompts/user.md
- [ ] 5. 收集必填入参（见子 SKILL.md）
- [ ] 6. 生成 JSON 并校验 schemas/output.json
- [ ] 7. 输出 keyword_density_check / SEO_Check 等自检字段
- [ ] 8. 若用户要 Word/PDF 审阅稿 → Read [references/export.md](references/export.md) 并执行 `siluzan-seo export`
```

## WorkBuddy 与 Cursor

- **WorkBuddy 运行时**：各子目录 `skill.yaml` 定义模型、inputs、RAG、prompt 路径
- **Cursor Agent**：以本文件 + 子 `SKILL.md` 为操作说明；无 RAG 时向用户索取 KB 摘要或关键产品资料

## 安装

手动安装与 `init` 平台列表见 [references/setup.md](references/setup.md)。一键安装见上文 **一键安装** 小节。

```bash
npm install -g siluzan-seo-cli
siluzan-seo init          # 写入 Cursor / Claude / DeerFlow 等 AI 助手 skill 目录
siluzan-seo update        # 升级 CLI 并刷新已安装 skill 文件
```

- **DeerFlow**：`siluzan-seo init --ai deerflow` → `skills/public/siluzan-seo/`
- **WorkBuddy**：也可将 `seo-traffic-page/`、`blog/`、`backlink-article/` 分别作为独立 Skill 安装
