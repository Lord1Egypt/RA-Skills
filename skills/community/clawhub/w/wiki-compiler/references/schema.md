# Schema（契约）

> Karpathy 模式的灵魂：**没有 schema，LLM 会天马行空；有了 schema，LLM 才守纪律**。
> 类比代码世界的 `eslint` 配置 + TypeScript 类型定义。

## 1. 主题导览 frontmatter（强制）

每篇主题导览笔记**必须**有如下 frontmatter：

```yaml
---
title: 📖 主题导览：[主题名称]      # 必填
type: guide                          # 必填，固定值
confidence: high | medium | low      # 必填（Karpathy 特色）
created: YYYY-MM-DD                  # 必填
updated: YYYY-MM-DD                  # 必填
version: 1.0                         # 必填（语义化版本）
changelog:                           # 必填（变更历史）
  - v1.0: 初始版本
sources:                             # 必填（可追溯到 raw）
  - [《文章1》](URL)
  - [《文章2》](URL)
related_guides:                      # 推荐（交叉引用）
  - [《另一导览》](URL)
---
```

## 2. 字段详解

### 2.1 `title`（必填）

格式：`📖 主题导览：[主题名称]`

示例：`📖 主题导览：因子与资产定价`

**意义**：
- emoji `📖` 视觉上突出主题导览
- "主题导览：" 前缀方便 `search_note` 按标题定位

### 2.2 `type: guide`（必填）

固定值 `guide`，用于：
- Lint 快速识别"这是导览，不是普通笔记"
- Cascade 算法快速筛选
- 知识库类型元数据

### 2.3 `confidence`（必填，Karpathy 特色）

| 值 | 含义 | 何时使用 |
|----|------|---------|
| **high** | 多源交叉验证，LLM 高度确信 | 5+ 篇相关文章相互印证 |
| **medium** | 单一权威来源，或部分验证 | 1-4 篇相关文章 |
| **low** | 单源或推断，LLM 不确定 | 仅 1 篇文章，或基于推测 |

**自动计算（LLM）**：
```python
def calc_confidence(article_count, cross_validated):
    if article_count >= 5 and cross_validated:
        return "high"
    elif article_count >= 1:
        return "medium"
    else:
        return "low"
```

**用途**：
- Lint 优先检查 low confidence 导览
- Cascade 时考虑 confidence（low 的导览谨慎级联）
- 用户决策：是否信任这个导览

### 2.4 `created` / `updated`（必填）

- `created`: 首次创建日期（YYYY-MM-DD）
- `updated`: 最近更新日期

**Lint 用途**：判断"过期检查"中的天数。

### 2.5 `version`（必填）

语义化版本号（SemVer）：
- `1.0.0` 初始版本
- `1.0.1` 仅增删文章
- `1.1.0` 修改关键要素
- `2.0.0` 核心概念结构变化

详见 [versioning.md](versioning.md) 第 2 节

### 2.6 `changelog`（必填）

变更历史，每行一条：

```yaml
changelog:
  - v2.3: [Ingest 2026-08-01] 自动级联，新增 2 篇遗传算法文章
  - v2.2: [Manual 2026-07-15] 修正置信度评估
  - v2.1: [Ingest 2026-07-01] 新增 5 篇相关文章
  - v2.0: 重构核心概念划分
  - v1.0: 初始版本
```

**意义**：审计追踪，每个论断何时被加进来、基于哪些资料。

### 2.7 `sources`（必填，Karpathy 核心）

**强制要求**：每篇导览必须列出引用的所有文章。

**格式**：
```yaml
sources:
  - [《文章标题1》](URL)            # type 2/6 用 URL
  - 《文章标题2》                    # type 7/11 用纯文本（保留书名号）
  - 《文章标题3》— 请在知识库查看    # 其他类型
```

**意义**：
- Karpathy 强调："每个论断都能追到 raw"
- 防止 LLM 幻觉污染
- 维护时一目了然"这个导览引用了哪些资料"

### 2.8 `related_guides`（推荐）

**推荐使用**：体现 wiki 是"网"不是"树"。

**格式**：
```yaml
related_guides:
  - [《主题导览：相关主题1》](URL)
  - [《主题导览：相关主题2》](URL)
```

**自动生成（LLM）**：
```python
def suggest_related_guides(current_guide, all_guides):
    """LLM 推荐相关导览"""
    suggestions = []
    for guide in all_guides:
        if guide.id == current_guide.id:
            continue
        relevance = compute_relevance(current_guide, guide)
        if 0.5 < relevance < 0.9:  # 强相关但不重复
            suggestions.append((guide, relevance))
    return sorted(suggestions, key=lambda x: -x[1])[:3]  # 最多 3 个
```

## 3. 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 主题导览标题 | `📖 主题导览：[主题名称]` | 📖 主题导览：因子与资产定价 |
| 文件夹名 | 语义化（避免"其他"等兜底） | AI 量化与深度学习/ |
| 标签 | `类型-XXX` | `主题-机器学习`、`状态-已编译` |
| Lint 报告 | `outputs/lint-YYYY-MM-DD.md` | outputs/lint-2026-09-28.md |

## 4. 链接规范

详见 [link-handling.md](link-handling.md) 第 2 节

| media_type | 写法 |
|-----------|------|
| 2/6（网页/公众号） | `[《标题》](URL)` |
| 7/11（Markdown/笔记） | `《标题》` |
| 1/3/4/5/9/12-21（其他） | `《标题》— 请在知识库查看` |

## 5. 版本号规范

详见 [versioning.md](versioning.md)

| 变更 | 版本号变化 |
|------|---------|
| 仅增删文章 | patch +0.0.1 |
| 修改关键要素 | minor +0.1 |
| 核心概念结构变化 | major +1.0 |

## 6. 不符合 schema 的后果

| 情况 | 后果 |
|------|------|
| 缺少 `type: guide` | LLM 无法识别为导览，Cascade 不会选中 |
| `confidence` 缺失 | Lint 默认视为 low，标记为待检查 |
| `sources[]` 为空 | 知识复利中断，无法追溯 |
| `related_guides[]` 为空 | Lint 标记为孤立候选 |
| `changelog` 缺失 | 审计追踪丢失 |
| 标题不含"主题导览" | search_note 找不到 |

## 7. Schema 验证脚本（可选）

```python
def validate_guide_schema(guide):
    """验证导览是否符合 schema"""
    required_fields = ["title", "type", "confidence", "created", "updated", "version", "changelog", "sources"]

    issues = []
    for field in required_fields:
        if field not in guide.frontmatter:
            issues.append(f"缺少必填字段: {field}")

    if guide.frontmatter.get("type") != "guide":
        issues.append(f"type 字段必须是 'guide'，当前是 '{guide.frontmatter.get('type')}'")

    if guide.frontmatter.get("confidence") not in ["high", "medium", "low"]:
        issues.append(f"confidence 必须是 high/medium/low，当前是 '{guide.frontmatter.get('confidence')}'")

    if not guide.frontmatter.get("sources"):
        issues.append("sources[] 为空，无法追溯到原始资料")

    return issues
```

## 8. Schema 演进追踪

IMA 平台知识库能力可能变化，schema 也会演进。

**当前版本**：v1.0（2026-09-28）

**演进原则**：
- 新增字段 → minor 版本 +0.1
- 删除字段 → major 版本 +1.0
- 字段重命名 → major 版本 +1.0
- 字段含义调整 → minor 版本 +0.1

## 9. 与 Karpathy 的对应

| Karpathy 原始模式 | wiki-compiler v5.0 实现 |
|------------------|----------------------|
| `CLAUDE.md` 模式核心 | `references/schema.md` |
| frontmatter 约定 | 强制 frontmatter 字段 |
| `[[wikilinks]]` 引用 | `related_guides[]` 数组 |
| `git log` 审计 | `changelog[]` 数组 |
| 资料溯源 | `sources[]` 数组 |
| LLM 把握度 | `confidence` 字段 |

> wiki-compiler 不复制 Karpathy 的所有机制，但保留他的**核心设计哲学**：schema 是模式的灵魂。
