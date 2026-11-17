---
# ══════════════════════════════════════════════════════════════════════
#  ▍技能骨架模板 — 技能生成器 / templates
#
#  用法（两条路，优先第一条）：
#    A. 自动生成：python scripts/new_skill.py <skill-name> --desc "..." \
#                    --desc-zh "..." --desc-en "..." --triggers a,b,c
#    B. 手工复制：把本文件拷成 <技能目录>/SKILL.md，逐项替换占位值后，
#                 删掉本 frontmatter 内所有 # 注释行，再跑体检。
#
#  ⚠️ 本文件首行必须是 ---（frontmatter 起始）。若在文件最上方加 HTML 注释块，
#     体检会直接判 P0「缺 frontmatter」——这是最容易被忽略的坑。
#
#  字段依据技能市场分发规范（YAML frontmatter + Markdown 正文）。
#  [必填] 缺一个就上架失败；[建议] 只影响展示；[可选] 用不到直接删行。
# ══════════════════════════════════════════════════════════════════════

# ── 标识 ────────────────────────────────────────────────────────────
# [必填] 小写字母+数字+连字符，必须与目录名一致；平台用 name 生成 slug
name: your-skill-name
# [建议] 平台的发布 CLI 必填，与 name 保持一致
slug: your-skill-name
# [建议] WorkBuddy 本机展示名，可以带「 · 功能列举」
display_name: 你的技能展示名
# [建议] 英文展示名
display_name_en: Your Skill Name
# [必填] 平台（SkillHub）的商店展示名，**只认驼峰 displayName**，
#        不认下划线 display_name —— 缺了商店里直接显示英文 slug
displayName: 你的技能

# ── 描述：一律写成单行 ──────────────────────────────────────────────
# ⚠️ 平台自带的解析器只认「key: 值」这一行，且不认行尾 # 注释：
#      `>-` 折叠块会被读成字面量 ">-"；多行列表会被读空；行尾注释会被拼进值里。
#      长文本折成一行即可（对完整 YAML 解析器同样合法，两边都安全）。
# [必填] 给模型看：做什么 / 何时触发 / 触发词
description: "一句话说清这个技能解决什么问题。当用户提到「触发词A」「触发词B」或出现「具体场景」时使用。"
# [必填] 给中文用户看，30 字以内，别照抄 description
description_zh: "一句话中文介绍"
# [必填] 给英文用户看，首字母大写、结尾不加句号
description_en: "One-line English introduction"
# [建议] 商店列表摘要，一般直接复用 description_zh
summary: "一句话中文介绍"
# [建议] 商店标签，用内联列表写法（多行 `- 项` 平台同样读不到）
tags: [标签一, 标签二]

# ── 元信息 ──────────────────────────────────────────────────────────
# [建议] 分类须落在平台 13 个枚举内，否则上架后显示「未分类」：
#   office-efficiency / content-creation / dev-programming / data-analysis /
#   design-media / ai-agent / knowledge-management / business-ops / education /
#   professional / it-ops-security / life-service / pay-skill
category: dev-programming
# [必填] 语义化版本，改动后必须递增
version: 1.0.0
# [建议] 个人或团队/公司名，别留机器默认值
author: 你的署名

# ── 可选开关（用不到就删）───────────────────────────────────────────
allowed-tools: Read, Write, Bash
disable-model-invocation: false
user-invocable: true

# ── WorkBuddy 本机扩展 ──────────────────────────────────────────────
agent_created: true
trigger:
  - 触发词A
  - 触发词B
---

# 技能展示名 (your-skill-name)

一句话说明它替用户省掉了什么。

## 何时使用

- 用户提到「触发词A」时
- 场景二

## 运行前提

- 依赖：列出第三方包 / 外部可执行文件；有第三方包必须配 `scripts/setup.py`
- 配置：真实值放 `~/.workbuddy/<name>_config.json`，对外只留 `config/settings.example.json` 空模板
- 首次配置：`python scripts/setup.py`

## 执行步骤

当用户需要 <做什么> 时，按以下步骤执行：

1. **<步骤名>** — 具体命令与判断条件。
   ```bash
   python scripts/<脚本>.py --参数 <值>
   ```
2. **<步骤名>** — 说明输入、输出、失败时的行为（缺依赖 / 缺配置 / 无网络）。
3. **<步骤名>** — 产出交付给用户，并说明输出文件放在哪。

## 目录说明

- `scripts/` — 执行逻辑
- `references/` — 按需加载的参考文档
- `templates/` — 可复制的骨架 / 报告模板
- `config/` — 只放 `*.example.*` 空模板

> 只保留真实存在的目录条目；写了不存在的文件会被体检判成「引用缺失」。

## 参考资料

- `references/<文档>.md` —— 什么时候需要读它（按需加载，不要默认全读）

## 常见坑

1. <踩过的坑 + 规避方式> —— 这一节是技能最值钱的部分，务必写

<!--
  写完后跑：
    python scripts/audit_skill.py "<技能目录>" --market     # 体检
    python scripts/pack_skill.py  "<技能目录>" --install    # 打包 + 装到本机

  注意：本注释块是文件末尾的说明，不要挪到文件开头。
-->
