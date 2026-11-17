# Lint（健康检查）

> Karpathy 三大操作之二。完整覆盖知识库的"健康体检"。
> 核心理念：**通过定期检查防止 wiki 衰败**，类比代码世界的 `eslint`。

## 1. 4 类标准检查

| 检查 | 内容 | 触发频率 |
|------|------|---------|
| **结构检查** | 文件夹散落、空文件夹、文件错放 | 每周 1 次 |
| **矛盾检查** | 不同导览对同一概念说法冲突 | 每月 1 次 |
| **孤立检查** | 导览未被任何文件引用 | 每月 1 次 |
| **过期检查** | 低 confidence + 长期未更新 | 每月 1 次 |

详见 [maintenance.md 第 6.5 节](maintenance.md)

## 2. 触发条件

| 触发词 | 行为 |
|--------|------|
| "检查知识库" / "知识库体检" | 完整 4 类检查 |
| "审查标签" / "整理标签" | 仅标签审查（属于结构检查的子集） |
| "健康检查" | 完整 4 类检查 |

## 3. 结构检查（Structure）

### 3.1 检查项

| 项目 | 检查方法 | 输出 |
|------|---------|------|
| 散落文件 | `get_knowledge_list` 不带 `folder_id`，找 `parent_folder_id == ROOT` 的文件 | 文件清单 |
| 空文件夹 | `get_knowledge_list` 找 `media_type=99` 且子项为空的文件夹 | 文件夹清单 |
| 文件错放 | LLM 比对文件标签和文件夹主题 | 错放文件清单 |

详见 [folder-organization.md](folder-organization.md)

### 3.2 自动建议

```
检测到 35 个散落文件
推荐归类：
- AkShare/BaoStock... → 数据工具与入门/
- 情绪... → 金融情绪分析/
- AI 量化... → AI 量化与深度学习/
```

## 4. 矛盾检查（Contradiction）

### 4.1 检查项

- 不同导览对同一概念说法冲突
- 同一文件夹内文件观点冲突

### 4.2 检查方法

```python
def check_contradictions(guides):
    """LLM 读取多个导览，识别冲突"""
    # 1. 提取所有导览的"核心思想"和"关键论断"
    claims_by_guide = {}
    for guide in guides:
        claims_by_guide[guide.id] = extract_key_claims(guide)

    # 2. LLM 配对比较
    contradictions = []
    guide_ids = list(claims_by_guide.keys())
    for i, id_a in enumerate(guide_ids):
        for id_b in guide_ids[i+1:]:
            pair_contradictions = llm_compare_claims(
                claims_by_guide[id_a],
                claims_by_guide[id_b]
            )
            contradictions.extend(pair_contradictions)

    return contradictions


def llm_compare_claims(claims_a, claims_b):
    prompt = f"""比较以下两组论断，识别直接冲突的项。

导览 A 的论断：
{format_claims(claims_a)}

导览 B 的论断：
{format_claims(claims_b)}

如果存在直接矛盾（同一概念，结论互斥），返回：
{{
  "topic": "<冲突的概念>",
  "claim_a": "<导览 A 的说法>",
  "claim_b": "<导览 B 的说法>",
  "severity": "high | medium | low",
  "suggestion": "<如何解决>"
}}

如果没有冲突，返回 {{"topic": null}}"""
    # 调用 LLM...
```

### 4.3 示例

```
矛盾：关于"因子有效性衰减"
- 导览 A（因子与资产定价 v2.3）: "Fama-French 三因子模型在 A 股市场有效性较弱"
- 导览 B（量化策略 v1.5）: "Fama-French 三因子在 A 股仍有显著 alpha"
- 严重度: medium
- 建议: 检查两份资料的发表时间和市场环境，可能需要分时段讨论
```

## 5. 孤立检查（Orphan）

### 5.1 检查项

| 维度 | 检查内容 |
|------|---------|
| 孤立导览 | 该导览的 `related_guides[]` 为空，且没有文件在 sources[] 中 |
| 孤立文件 | 文件未被任何导览的 sources[] 引用 |
| 孤立章节 | 导览某个章节只有 1 篇文章 |

### 5.2 检查方法

```python
def check_orphans(kb_id, all_guides, all_files):
    orphans = {"guides": [], "files": []}

    # 1. 找出被任何导览引用的文件
    referenced_files = set()
    for guide in all_guides:
        for src in guide.sources:
            referenced_files.add(src.media_id)

    # 2. 找出孤立文件（未被任何导览引用）
    for file in all_files:
        if file.media_id not in referenced_files:
            orphans["files"].append(file)

    # 3. 找出孤立导览（没有 related_guides[]，也没有任何 sources 引用）
    for guide in all_guides:
        if not guide.related_guides and not any(
            f for f in all_files if any(src.media_id == f.media_id for src in guide.sources)
        ):
            orphans["guides"].append(guide)

    return orphans
```

### 5.3 修复建议

```
孤立文件：
- 《文章A》.pdf — 未被任何导览引用
  - 建议：纳入"主题导览：XXX"（相关度 0.85）
  - 或：新建独立导览（如果内容丰富）

孤立导览：
- 📖 主题导览：XXX — 没有相关导览也没有引用文件
  - 建议：补充 related_guides[]，加入交叉引用
```

## 6. 过期检查（Freshness）

### 6.1 检查项

| 项目 | 阈值 | 标记 |
|------|------|------|
| 低 confidence 导览 | confidence == "low" | 待更新 |
| 长期未更新（medium） | updated > 30 天前 AND confidence == "medium" | 可能过时 |
| 关键文章已更新但导览未跟进 | 文件 updated > 导览 updated | 待同步 |

### 6.2 检查方法

```python
def check_freshness(guides, files):
    from datetime import datetime, timedelta

    today = datetime.now()
    stale = []

    for guide in guides:
        days_since_update = (today - guide.updated).days

        # 规则 1: 低 confidence
        if guide.confidence == "low":
            stale.append((guide, "low_confidence", "高优先级"))

        # 规则 2: medium + 长期未更新
        elif guide.confidence == "medium" and days_since_update > 30:
            stale.append((guide, "stale_medium", "中优先级"))

        # 规则 3: 关键文章已更新但导览未跟进
        guide_files = [f for f in files if any(
            src.media_id == f.media_id for src in guide.sources
        )]
        newer_files = [f for f in guide_files if f.updated > guide.updated]
        if newer_files:
            stale.append((guide, "files_updated_guide_stale", "高优先级"))

    return stale
```

## 7. Lint 输出：标准报告

### 7.1 报告路径

```
outputs/lint-YYYY-MM-DD.md
```

例如：`outputs/lint-2026-09-28.md`

### 7.2 报告模板

```markdown
# Wiki 健康检查报告

**生成时间**：2026-09-28
**知识库**：[知识库名称] (kb_id: ...)
**检查导览数**：X 个
**检查文件数**：Y 个

## 总体评分

| 维度 | 评分 | 状态 |
|------|:----:|:----:|
| 结构 | ⭐⭐⭐⭐ | 良好 |
| 矛盾 | ⭐⭐⭐ | 一般 |
| 孤立 | ⭐⭐⭐⭐ | 良好 |
| 过期 | ⭐⭐⭐ | 一般 |
| **综合** | **⭐⭐⭐⭐** | **良好** |

## 1. 结构检查

- 散落文件：X 个
- 空文件夹：X 个
- 文件错放：X 个

**修复建议**：
- [P1] 调用 `move_knowledge` 把 X 个散落文件归类
- [P2] 删除/重组 X 个空文件夹

## 2. 矛盾检查

- 矛盾论断对：X 对

**示例**：
- [导览A] vs [导览B] 对 "XXX" 概念说法冲突
  - A: ...
  - B: ...
  - 建议: ...

## 3. 孤立检查

- 孤立导览：X 个
  - [导览1]: 建议补充交叉引用
- 孤立文件：X 个
  - [文件1]: 建议纳入相关导览

## 4. 过期检查

- 低 confidence 导览：X 个
- 长期未更新（medium）：X 个
- 关键文章已更新但导览未跟进：X 个

**修复建议**：
- [P0] 更新低 confidence 导览：XXX
- [P1] 跟进已更新但导览未更新的：YYY

## 总体改进建议

按优先级排序：
1. [P0] ...
2. [P1] ...
3. [P2] ...
```

## 8. 自动 Lint 调度（可选）

### 8.1 每周定时

```bash
# 每周日 0 点跑 Lint，输出到 outputs/lint-YYYY-MM-DD.md
0 0 * * 0 cd /workspace && \
  python3 lint.py --kb_id <kb_id> --output outputs/lint-$(date +%Y-%m-%d).md
```

### 8.2 历史对比

```bash
# 比较最近 4 周的 Lint 报告
diff outputs/lint-2026-09-07.md outputs/lint-2026-09-28.md
```

跟踪指标：
- 散落文件数变化（应持续下降）
- 矛盾数变化（应 < 5）
- 孤立文件率变化（应 < 20%）

## 9. 与 Ingest 的协同

| Lint 发现 | 触发 Ingest |
|---------|------------|
| 低 confidence 导览 | 自动增量更新（带 confidence 提升） |
| 孤立文件 | 建议纳入相关导览 |
| 文件错放 | 调用 `move_knowledge` 归类 |
| 矛盾论断 | 用户确认后增量更新相关导览 |

**核心理念**：Lint 不只是发现问题，而是**驱动 Ingest 解决问题**。
