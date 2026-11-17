# Evidence Grading — 证据分级体系

**加载时机：** 📍 Pass 2 Extract 执行知识提取时加载；Pass 6 Layer B 契约验证时加载。

---

## 设计哲学

从多源内容（PDF/视频/网页/图片）提取的知识，可信度并不相同。原文直引、模型转述、编译器推断——这三类知识如果在 skill 中被同等对待，会导致用户把"推测"当成"事实"使用。

本体系为每条知识打上证据等级，让 skill 的消费者（AI agent + 人类用户）知道"这条结论多可靠"。核心原则：**矛盾的信息不强行统一，而是保留并标注**——人本来就前后不一致，强制洗白会丢失真实信号。

---

## 三级证据体系

| 等级 | 标签 | 含义 | 典型来源 |
|------|------|------|---------|
| **L1** | `primary` | 原文直引，可直接溯源到原始载体 | PDF 文本层、字幕原文、网页正文、代码注释 |
| **L2** | `secondary` | 经过一次模型转述，存在转述损失 | OCR 结果、whisper 转写、视觉理解描述、摘要 |
| **L3** | `inferred` | 编译器从上下文推断，原始载体未直接陈述 | 隐含假设、跨段推理、模式归纳 |

### 判定规则

| 内容形态 | 等级 | 理由 |
|---------|------|------|
| 引号内的原文 | `primary` | 可逐字核对 |
| 代码块 | `primary` | 机器可验证 |
| 表格数据 | `primary` | 结构化事实 |
| OCR 提取的文字 | `secondary` | 可能有字符错误 |
| 语音转写 | `secondary` | 可能有同音错误 |
| "这意味着..." 的解读 | `inferred` | 推断而非原文 |
| 从多个案例归纳的规律 | `inferred` | 归纳推理 |
| 图表的结构化描述 | `secondary` | 视觉理解转述 |

---

## 在 Pass 2 中的应用

### 提取时标注

Pass 2 Extract 从 `structured_content`（Pass I 产出）提取知识时，**每条知识必须带 `evidence` 字段**：

```json
{
  "content": "所有 API 响应必须包含 request_id 字段",
  "source": "spec.pdf:p47",
  "evidence": "primary",
  "confidence": 0.98
}
```

### 默认值继承

- 若 Pass I 为整份内容设定了默认 `evidence_grade`，Pass 2 提取的单条知识默认继承此等级
- 但 Pass 2 可**逐条覆盖**：如从 `secondary` 内容中识别出一段原文直引，可升级为 `primary`

### confidence 字段

`confidence`（0-1）补充 `evidence` 的细粒度：
- `primary` + `confidence: 0.95` = 高可信原文
- `secondary` + `confidence: 0.6` = 低质量转写，需人工复核
- `inferred` + `confidence: 0.7` = 中等把握的推断

来源：OCR 置信度、whisper 置信度、或编译器对推断的自评。

---

## 冲突保留规则

**核心原则：** 当多个来源对同一事实给出矛盾表述时，**不强行统一，保留所有版本并标注冲突**。

### 冲突检测

Pass 2 提取时，若两条知识描述同一实体但内容矛盾：

```json
{
  "conflicts": [
    {
      "id": "C-001",
      "topic": "API 限流策略",
      "status": "open",
      "versions": [
        { "content": "每分钟 100 次", "source": "doc-v1.md", "evidence": "primary", "confidence": 0.95 },
        { "content": "每分钟 1000 次", "source": "doc-v2.md", "evidence": "primary", "confidence": 0.95 }
      ],
      "resolution": null,
      "resolved_by": null,
      "resolved_at": null,
      "note": "两个版本表述不一致，保留待用户裁决"
    }
  ]
}
```

### 冲突状态机

```
open ──────────────────────────────► resolved
  │                                     │
  ├──► wontfix（不影响核心功能）         ├── resolution: prefer_higher_evidence
  │                                     ├── resolution: prefer_newer
  └──► deprecated（源已过期）            ├── resolution: merged
                                        ├── resolution: user_override
                                        └── resolved_by: user | compiler | cross_reference
```

| 状态 | 含义 | 终态？ |
|------|------|--------|
| `open` | 新发现冲突，待处理 | 否 |
| `resolved` | 已裁决，标注了 resolution 和 resolved_by | 是 |
| `wontfix` | 不影响核心功能，保留但不处理 | 是 |
| `deprecated` | 冲突源已不再适用 | 是 |

### 冲突处理策略

| 策略 | 适用场景 |
|------|---------|
| `prefer_higher_evidence` | 一方 primary 一方 inferred，采用 primary |
| `prefer_newer` | 来源有时间戳且差异显著，采用较新版本（需标注理由） |
| `flag_for_user` | 矛盾影响 skill 核心功能，必须用户裁决 |
| `merged` | 两版本可合并为更完整的表述 |
| `user_override` | 用户明确选择了某一版本 |

**禁止操作：** 静默丢弃任一版本、强行取平均值、随机选择一方。

### 冲突在生成 skill 中的呈现

冲突不隐藏，写入生成的 skill 的 `references/gotchas.md` 或 `references/conflicts.md`：

```markdown
## 已知冲突

### API 限流策略
- 来源 A（doc-v1.md）称"每分钟 100 次"
- 来源 B（doc-v2.md）称"每分钟 1000 次"
- 状态：未裁决。使用前请核实当前版本。
```

---

## 在 Pass 6 中的应用

### Layer B 契约验证新增检查

| # | 检查项 | PASS 标准 | 严重度 |
|---|--------|-----------|--------|
| B9 | evidence 字段完整性 | 所有 knowledge_inventory 条目都有 evidence 字段 | 🟠 High |
| B10 | inferred 条目有标注 | evidence=inferred 的条目在生成文件中明确标注为"推断" | 🟡 Medium |
| B11 | 冲突未被静默丢弃 | IR 中 conflicts 数组的每个条目在生成文件中都有对应呈现 | 🟠 High |

### 诚实性原则

生成的 skill 不应把 `inferred` 知识当作 `primary` 事实陈述。Pass 6 Layer A 检查：

> reference 文件中，推断性结论是否使用了"可能"、"推测"、"建议核实"等限定词，而非确定性表述。

---

## 与 Ingestion 阶段的衔接

| Pass I 产出 | Pass 2 继承 |
|------------|-------------|
| `evidence_grade: primary`（默认） | 单条知识默认 primary，可被覆盖 |
| `evidence_grade: secondary`（OCR/转写） | 单条知识默认 secondary |
| `extraction_warnings: [OCR 置信度低]` | 相关段落 confidence 降至 0.6 以下 |
| `provenance: [{source, extractor, confidence}]` | 每条知识的 source 字段溯源到此 |
