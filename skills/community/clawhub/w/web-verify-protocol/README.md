# web-verify-protocol：三轮联网搜索验证协议

让"AI 联网搜出来的数据"达到可发布、可引用的可信度。单次搜索只能抓住约 70% 的错误，第二轮到 90%，三轮独立验证接近 100%。这不是建议，是结构性门槛——不满足就禁止输出。

AI 搜数据最大的问题不是搜不到，是搜到的不可信：媒体互相抄、老数据当新的、夸大数字四处传。这个协议用 S/A/B/C 四级信源分级加三轮硬性核实，把"据 XX 报道"的翻车风险压到最低。

## 适合谁用

- 公众号/文章要引用具体数字（营收、出货量、市占率）的写作者
- 拿爆料/新闻要点需要联网核实真伪的内容团队
- 做研报拆解、商业分析、信息图的数据研究者
- 任何"AI 出数据"且强调可靠性的场景

## 快速开始

零依赖，直接按 SKILL.md 执行。核心流程：

```text
信源分级(S/A/B/C) → R1 S级升级(≥3次搜索) → R2 独立交叉验证(≥3次) → R3 叙事审查(≥2次) → 阻塞门报告 → 输出
```

每次核实结束，先打印三轮核实报告再输出文件，这是用户验证"三轮真的跑了"的唯一方式。

## 文件说明

| 文件 | 作用 |
|------|------|
| `SKILL.md` | 完整协议：信源分级表、三轮硬性下限、阻塞门报告、红旗清单、冲突解决 |

## 核心机制

- **四级信源分级**：S（官方公告/监管文件/央媒）> A（权威证券媒体/IDC）> B（36Kr/虎嗅）> C（自媒体，永不作唯一来源）
- **R1 S级升级**：≥3 次新角度搜索，找更好的来源而不是复查旧的
- **R2 独立交叉验证**：≥3 次搜索找第二个独立来源，抓媒体互相抄的连锁错误
- **R3 叙事审查**：≥2 次搜索只查"讲故事的数字"（X 倍/最高级/前后对比）
- **阻塞门报告**：输出文件前必须打印，任一环节不达标禁止输出
- **红旗清单**：最高级说法、过于整齐的整数、"业内人士透露"、两个 B 级来源数据打架

## 推荐流程

1. 收集数据 → 按 S/A/B/C 分级标注来源
2. 跑 R1/R2/R3 三轮硬性核实
3. 打印三轮核实报告，门通过才输出
4. 输出带来源级别的最终版本

---

# web-verify-protocol: three-round web verification protocol

Make "AI-researched data" trustworthy enough to publish and cite. A single search catches about 70% of errors; a second round reaches 90%; three independent rounds approach 100%. This is not a suggestion — it's a structural gate. Fail it and output is forbidden.

The biggest problem with AI research isn't finding data, it's trusting data: media copy each other, stale numbers get passed off as new, exaggerations spread everywhere. This protocol combines S/A/B/C source grading with three hard verification rounds to minimize the risk of "according to reports" disasters.

## Who it's for

- Writers citing specific numbers (revenue, shipments, market share) in articles
- Content teams that need to verify leaked news before using it
- Data researchers doing report breakdowns, business analysis, infographics
- Any scenario where "AI produced the data" and reliability matters

## Quick start

Zero dependencies — just follow SKILL.md. Core flow:

```text
Source grading (S/A/B/C) → R1 S-grade upgrade (≥3 searches) → R2 independent cross-check (≥3) → R3 narrative review (≥2) → block-gate report → output
```

Always print the three-round report before outputting files — it's the only way the user can verify the three rounds actually ran.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Full protocol: source grading table, three-round hard minimums, block-gate report, red flags, conflict resolution |

## Core mechanisms

- **Four-level source grading**: S (official announcements/regulatory filings/state media) > A (authoritative financial media/IDC) > B (36Kr/Huxiu) > C (self-media, never the sole source)
- **R1 S-grade upgrade**: ≥3 searches from new angles — find better sources, don't recheck old ones
- **R2 independent cross-verification**: ≥3 searches for a second independent source, catching media-mirroring chain errors
- **R3 narrative review**: ≥2 searches only for "storytelling numbers" (X-times, superlatives, before/after comparisons)
- **Block-gate report**: must be printed before any file output; any round failing blocks output
- **Red-flag list**: superlatives, too-round integers, "industry insiders say", conflicting B-grade sources

## Recommended workflow

1. Collect data → grade sources S/A/B/C
2. Run the R1/R2/R3 hard verification rounds
3. Print the three-round report; output only if the gate passes
4. Output the final version with source grades
