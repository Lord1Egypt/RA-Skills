---
name: word-knowledge-map
description: >-
  输入英文单词时使用：经 Knowledge IR 生成手绘涂鸦教学海报风格单词知识地图（卡通小人+粗弯箭头；禁止 Soft UI/扁平 App 风）。适用于看一眼就会的单词、单词知识地图等场景；含弱词族兜底版式。
---
# Word Knowledge Map Skill v1.2.0

配套：`templates/knowledge-schema.json`、`templates/infographic-prompt.md`、`templates/style-guide.md`、`templates/layout-modes.md`、`references/style-target-care.png`、`examples/care.json`

## 目标

输入英文单词 → Knowledge IR → **手绘涂鸦教学海报**（对齐参考图）。关系优先；禁止做成干净 Soft UI / 扁平 App。

## Pipeline（每阶段必须产出；禁止跳过 IR）

| 阶段 | 必须产出 | 何时停下问用户 |
|------|----------|----------------|
| 1. 解析 | 目标词、可选学段覆盖 | 输入不是英文词/短语，或一次多个互不相关的词 |
| 2. 学段 | audience（默认：小学高年级+初中） | 用户点名高中/考纲且与默认冲突 |
| 3. 知识构建 | 完整 IR JSON（符合 schema） | — |
| 4. 筛选 | `layout_plan`：版式模式 + 上图条目（见下） | — |
| 5. 内容 QA | 通过/打回：无编造派生、拼写正确、例句自然、P1 齐全 | 关键词义拿不准且会影响主图时，可一句确认 |
| 6. Layout | 选定 layout mode + 卡面标题与箭头文案 | — |
| 7. 成图 | 16:9 图（对齐 style-guide + infographic-prompt） | — |
| 8. 视觉 QA | 对照反例锁；失败则重做，不对用户甩 JSON | — |

## 学段

默认小学高年级+初中。P1 必显，P3 默认可删；主图优先 priority≥4。

## IR 全量 vs 成图取用（分流）

- **IR 全量收集**：schema 必填字段都填（含 `word_forms`、`common_mistakes` 等），供记忆线索与后续复用。
- **成图只取**：`layout_plan` 里选中的条目；默认 priority≥4，且能进当前版式模块的字段。
- **禁止**为填满 schema 或填满四象限而编造冷门义项、假派生词、假词族。
- `word_forms`（三单/过去式等）默认**不上主图**，除非用户点名要语法变位图，或该词几乎没有搭配/词族可讲。

## 知识规则

- 主图搭配 priority≥4；区分词形变化 vs 派生词族。
- 完整词族时象限优先：短语 → 形容词 → 副词 → 名词（见 layout `full-family`）。
- 例句短自然；目标词在成图中高亮。
- 无真实派生时：空着对应模块，改用弱词族版式，**绝不编造**。

## 版式模式（弱词族兜底）

详见 `templates/layout-modes.md`。筛选阶段必须写入 `layout_plan.mode`：

1. **`full-family`**：有清晰「短语 + 形/副/名」链（如 care）→ 中央 + 四象限 + 底链。
2. **`phrasal-hub`**：多义/多短语、派生弱（如 get、run）→ 中央 + 用法/短语卡 + 可选「易混/注意」卡；底链改为真实关系，不套假派生链。
3. **`function-word`**：虚词/限定词（如 the、a、of）→ 用法对比 + 正反例 + 固定说法；禁止硬凑形/副派生。
4. **`compact-three`**：内容不足以撑四卡 → 中央 + 三卡，留白宁空勿假。

底链文案必须反映真实关系；禁止在链条不存在时套用「词根→短语→形→副→名」。

## 视觉（风格锁）

必须：奶油纸细微纸感（不要响亮点阵网格）、马卡龙色、手写标题、粗弯手绘箭头、卡通小孩场景、卡片可微倾。

禁止：Soft UI、细直线连接、极简线性 icon 当主视觉、数字产品完美对齐风、硬偏移 sticker 阴影。

偏 Soft UI = 失败重做。详见 style-guide 反例锁与 `references/style-diff-notes.md`。

## 成图

优先：参考图锚定的涂鸦气质 + IR 文字校对；文生图必须带上 `infographic-prompt.md` 中的 positive/negative 锚点。或 HTML 文字层 + 卡通插画嵌入（HTML 更易滑向 Soft UI，视觉 QA 更严）。

## 对用户输出

- 成功：一句话导语 + 图 + 可选记忆线索（可来自 IR `memory_tip`）。
- **不暴露** JSON、schema、QA 术语、layout mode 内部名。
- 视觉失败重做时只说：**「风格有点偏，我按手绘海报参考图重做一版。」**
- 内容失败重做时只说：**「知识点我再收紧一版，马上重出图。」**

## 输出检查（执行者自用，不对用户念）

- [ ] 已生成 IR 且未跳过
- [ ] 已选 layout mode，无编造派生
- [ ] 成图文字 ⊆ IR / layout_plan
- [ ] 视觉未触反例锁
