# Alias Normalization Matrix

用于快速说明 `wotohub-automation` 当前字段命名的三层关系：
- 请求层 canonical
- skill 内部运行时 canonical
- compatibility aliases only

目标不是保留多套名字长期并存，而是让兼容入口在进入 skill 后尽快归一。

---

## 1. Request-layer canonical（推荐宿主这样传）

- `hostAnalysis`
- `productSummary`
- `hostDrafts`
- `replyModelAnalysis`
- campaign draft delivery: `host_drafts_per_cycle`

说明：
- 这是宿主向 skill 注入结构化结果时的推荐写法。
- 新接入、新文档、新示例都应优先使用这些字段。

---

## 2. Internal runtime canonical（skill 内部归一后主要使用）

- `modelAnalysis`
- `productSummary`
- `hostDrafts`
- `replyModelAnalysis`
- campaign cycle output field: `host_drafts_per_cycle`

说明：
- `hostAnalysis` 在 upper-layer / context normalization 后，通常会进入 `modelAnalysis`。
- `productSummary / hostDrafts / replyModelAnalysis` 归一后仍沿用同名。
- campaign 周期草稿产物的 canonical write-back field 仍是 `host_drafts_per_cycle`。

---

## 3. Compatibility aliases only（可接收，但不应扩散）

### Understanding / analysis
- `understanding` -> `hostAnalysis` -> `modelAnalysis`
- `conversationAnalysis` -> `replyModelAnalysis`

### Drafts
- `hostEmailDrafts` -> `hostDrafts`
- `emailModelDrafts` -> `hostDrafts`
- `hostDraftsPerCycle` -> `host_drafts_per_cycle`
- `hostDrafts` / `emailModelDrafts` -> `host_drafts_per_cycle`（仅限部分 campaign delivery contract 吸收）

### Summary
- `hostProductSummary` -> `productSummary`

---

## 4. Deprecation guidance

### Keep as compatibility for now
以下字段仍建议保留一段时间的兼容吸收能力，因为已经出现在历史 brief / tests / bridge payload 中：
- `understanding`
- `conversationAnalysis`
- `hostEmailDrafts`
- `emailModelDrafts`
- `hostProductSummary`
- `hostDraftsPerCycle`

### Do not use in new examples or new host integrations
- `understanding`
- `conversationAnalysis`
- `hostEmailDrafts`
- `emailModelDrafts`
- `hostProductSummary`

### Future deprecate first candidates
如果后续要正式缩减 alias 面，可以优先考虑从文档和新桥接 payload 中彻底退出这些名字：
1. `hostEmailDrafts`
2. `emailModelDrafts`
3. `conversationAnalysis`
4. `hostProductSummary`

`understanding` 是否淘汰应最后决定，因为它仍承担一部分“统一语义入口”的历史角色。

---

## 5. Practical rule

一句话规则：

**新接入只写 canonical，旧入口允许 alias，skill 内部一律尽快归一。**
