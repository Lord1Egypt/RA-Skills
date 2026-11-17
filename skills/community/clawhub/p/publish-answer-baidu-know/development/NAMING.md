# 技能 slug 命名规范（verb-noun-platform）

> 本文是匠厂**新业务 skill** 的 slug / Git 仓库名 / 目录名命名权威说明。复制 `skill-template` 出去开发新技能前**必读**；Agent 在开发者询问命名或 slug 时也应先读本文。

---

## 1. 适用范围

| 范围 | 说明 |
|------|------|
| ✅ **适用** | 从 `skill-template` **复制出去的新技能** |
| ❌ **不追溯** | 已上线历史技能（如 `account-manager`、`reconcile-finance`、`scrape-contacts-lianjia` 等）保持不动 |
| ❌ **不修改** | 其他仓库（尤其 `account-manager`）不在本文约束范围内 |
| ✅ **模板占位** | 模板本体的 `your-skill-slug` 占位必须继续通过全部测试 |

**新技能勿仿**历史 2 段无平台形态（如 `reconcile-finance`）或不符合 verb-noun-platform 的旧 repo 名；校验器对历史 repo **不追溯**，但规范中明确标注为反模式。

---

## 2. 命名格式

标准形态（约 95% 新技能）：

```text
{verb}-{noun-phrase}-{platform}
```

| 部分 | 规则 |
|------|------|
| **verb** | 1 个词，来自 [动词白名单](#5-动词白名单) |
| **noun-phrase** | 1～3 个词（按 `-` 分段），描述业务对象 |
| **platform** | 1 个词，来自 [平台白名单](#6-平台白名单)；可含连字符（如 `single-window`） |

**展示层分工不变：**

| 字段 | 语言 | 示例 |
|------|------|------|
| slug / repo / 目录 / `SKILL_SLUG` / DB 文件名 | **英文** kebab-case | `download-settlement-report-amazon` |
| `SKILL.md` 的 `name`、`description`、根 `README.md` | **中文** | `亚马逊结算报表下载` |

---

## 3. 硬约束（新技能强制校验）

| 约束 | 值 |
|------|-----|
| 格式 | `{verb}-{noun-phrase}-{platform}`（标准型，默认） |
| 总段数（按 `-` 分割） | **3～5 段**（标准型）；scope 型见 [§4](#4-三类合法形态) |
| 总长度 | **≤ 48 字符** |
| 字符集 | 小写字母、数字、连字符；kebab-case |
| 禁止 | 中文 slug、下划线、**平台放最前**（如 `amazon-download-xxx`） |

实现校验见 `scripts/util/slug_naming.py`；`scripts/db/display_metadata_validator.py` 在 `SKILL.md` frontmatter 自检时调用。

---

## 4. 三类合法形态

### 4.1 标准型（95%）

`verb-noun-platform` 或 `verb-noun-noun-platform`（3～5 段）

- 第 1 段 ∈ 动词白名单
- 最后 1 段（或 hyphenated 平台的最后 2 段）∈ 平台白名单
- 中间为 noun-phrase（1～3 段）

示例：

- `download-settlement-report-amazon`
- `add-product-shopee`
- `enter-sales-receipt-kingdee`
- `fill-export-declaration-single-window`

### 4.2 scope 型（少见）

`verb-noun-scope`

- 最后 1 段 ∈ scope 白名单：`all` | `batch` | `multi` | `default`
- 第 1 段 ∈ 动词白名单
- 总段数 3～5

示例：`generate-article-all`

> 说明：`geo-generate-article-all` 若作为新技能且不在豁免表、首段 `geo` 不在动词表，应写为 `generate-article-all`。

### 4.3 历史豁免（不校验语义）

以下 slug 跳过 verb/platform 语义校验（见 `LEGACY_EXEMPT_SLUGS`）：

- `account-manager`
- `skill-template`
- `your-skill-slug` / `your_skill_slug`（模板占位）

---

## 5. 动词白名单

词表文件：[`assets/naming/verbs.txt`](../assets/naming/verbs.txt)（每行一词，便于后续扩展）

| 动词 | 动词 | 动词 | 动词 |
|------|------|------|------|
| scrape | receive | download | export |
| add | fill | enter | bind |
| withdraw | reconcile | verify | submit |
| query | process | reply | generate |
| draft | review | confirm | track |
| upload | match | triage | ship |
| reprice | | | |

---

## 6. 平台白名单

词表文件：[`assets/naming/platforms.txt`](../assets/naming/platforms.txt)

| 平台 | 平台 | 平台 |
|------|------|------|
| amazon | shopee | xinghang |
| alibaba | kingdee | icbc |
| pingpong | worldfirst | paypal |
| lianlian | single-window | export-rebate |
| etax | | |

scope 词表：[`assets/naming/scopes.txt`](../assets/naming/scopes.txt) — `all`、`batch`、`multi`、`default`

---

## 7. slug 与展示字段分工

```yaml
---
name: 亚马逊结算报表下载          # 中文，用户可见
description: "从卖家中心下载结算报表并入库"  # 中文说明
metadata:
  openclaw:
    slug: download-settlement-report-amazon   # 英文机器标识
---
```

同步修改：

- 目录名
- `metadata.openclaw.slug`
- `scripts/util/constants.py` 中的 `SKILL_SLUG`
- 默认数据库路径 `{slug}/{slug}.db`

三者必须一致。

---

## 8. 与 account-manager 的关系

slug **末段 platform** 与 `account-manager` 中的 `platform_key` **语义对应**，但**不要求字符串完全相等**。

| slug 末段 (platform) | account-manager platform_key（示例） |
|----------------------|--------------------------------------|
| amazon | `amazon_sim` / `amazon` |
| shopee | `shopee` |
| kingdee | `kingdee` |

新技能若需账号下发，在 `REQUIREMENTS.md` §0 填写拟用的 `platform_key`，并与兄弟技能调用参数对齐。

---

## 9. 复制新技能流程

1. **先定 slug** — 按本文规范拟定 `{verb}-{noun-phrase}-{platform}`，确认在白名单内且 ≤ 48 字符
2. **复制目录** — **推荐** [`tools/scaffold_skill.ps1`](../tools/scaffold_skill.ps1)（`-Slug` 与目录名一致）；勿整包复制带走 `.git`
2.5. **清理 Git（若未用 scaffold）** — 删除 `.git`、`.openclaw-skill-template`、`.pytest_cache`；再 `git init` 与 `git remote add origin`
3. **全局替换** — `your-skill-slug` → 新 slug；更新 `SKILL.md`、`constants.py`、文档中的占位
4. **填写 REQUIREMENTS** — 完成 [`REQUIREMENTS.md`](REQUIREMENTS.md) §0 技能标识
5. **开发 & 自检** — `python tests/run_tests.py -v`，含 slug 语义测试；`git remote -v` 确认非 template

---

## 10. 正例 / 反例

### ✅ 正例

| slug | 说明 |
|------|------|
| `download-settlement-report-amazon` | 标准型，4 段 |
| `add-product-shopee` | 标准型，3 段 |
| `enter-sales-receipt-kingdee` | 标准型 |
| `fill-export-declaration-single-window` | 标准型，平台含连字符 |
| `generate-article-all` | scope 型 |

### ❌ 反例

| slug | 原因 |
|------|------|
| `amazon-download-settlement-report` | 平台在最前 |
| `enter-cross-border-sales-receipt-voucher-kingdee` | 过长、noun 臃肿 |
| `reconcile-finance` | 新技能禁止 2 段无平台 |
| `download_settlement_amazon` | 非 kebab-case（下划线） |

---

## 11. 反模式

- **平台前置**：`amazon-download-...`、`shopee-add-...`
- **英文占位 name**：复制后仍保留 `My Skill` 或纯英文 slug 风格名称
- **只改目录名**：`SKILL.md` slug 与 `constants.SKILL_SLUG` 未同步
- **noun 堆砌**：中间段过多导致超 48 字符或难以阅读
- **仿历史 2 段 repo**：`reconcile-finance`、`content-manager` 等

---

## 12. 演进说明（当前不启用）

当技能库规模 **> 200** 时，可再评估引入 `{domain}-verb-noun-platform` 前缀形态。**当前不启用**，新技能一律使用本文 verb-noun-platform 标准型或 scope 型。

---

## 13. 历史形态说明

以下为代表性**历史 repo**，新技能**勿仿**：

| 历史 slug | 说明 |
|-----------|------|
| `account-manager` | 跨平台账号管理，非 verb-noun-platform |
| `reconcile-finance` | 2 段无 platform |
| `scrape-contacts-lianjia` | 平台名不在当前白名单（链家） |
| `skill-template` | 模板仓库本身 |

校验器通过 `LEGACY_EXEMPT_SLUGS` 对模板占位与少数豁免 slug 跳过语义检查；**新复制出去的业务 skill 不在豁免表内**，必须满足 §3 硬约束。

---

## 14. 相关文档

| 文档 | 内容 |
|------|------|
| [`DEVELOPMENT.md`](DEVELOPMENT.md) | 复制模板步骤、发布前检查清单 |
| [`REQUIREMENTS.md`](REQUIREMENTS.md) | §0 技能标识必填项 |
| [`../references/SCHEMA.md`](../references/SCHEMA.md) | kebab-case 与数据库路径 |
| [`../SKILL.md`](../SKILL.md) | frontmatter 命名摘要 |
