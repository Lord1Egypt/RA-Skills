# OKF v0.1 Spec Summary

> 本文件是 [OKF v0.1 Spec](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) 的关键要点摘要，供 Agent 快速参考。完整规范以原文为准。

## Section 2: 术语
- **Knowledge Bundle**: 自包含的层级知识文档集合，分发单元
- **Concept**: bundle 中的单个知识单元，一个 markdown 文件
- **Concept ID**: 文件路径去掉 .md 后缀（如 `tables/users.md` → `tables/users`）
- **Frontmatter**: 文件开头的 YAML 元数据块，用 `---` 分隔
- **Link**: concept 间的标准 markdown 链接
- **Citation**: concept 到外部来源的链接

## Section 3: Bundle 结构
- 目录树结构，组织方式由 producer 决定
- 保留文件名：`index.md`（§6）、`log.md`（§7）
- 可作为 git 仓库、tarball 或子目录分发

## Section 4: Concept 文档
### Frontmatter（§4.1）
必填：
- `type`: concept 类型字符串（如 `BigQuery Table`, `Entity`, `Concept`），producer 自定义，consumer 容忍未知类型

推荐（优先级排序）：
- `title`: 显示名称
- `description`: 一句话摘要
- `resource`: 底层资产的 URI
- `tags`: YAML 标签列表
- `timestamp`: ISO 8601 最后修改时间

扩展：producer 可添加任意额外字段，consumer 应保留未知字段

### Body（§4.2）
标准 markdown，推荐结构化（标题、列表、表格、代码块）
约定标题：
- `# Schema`: 资产字段结构
- `# Examples`: 使用示例
- `# Citations`: 外部来源（§8）

## Section 5: 交叉链接
- 标准 markdown 链接
- 绝对路径（bundle-relative，以 `/` 开头）：推荐，文件移动时稳定
- 相对路径（`./other.md`）：允许
- 链接语义由周围文本表达，链接本身无类型
- Consumer 必须容忍断链（代表未编写知识）

## Section 6: Index 文件
- `index.md` 可出现在任意目录（含 bundle 根）
- 无 frontmatter（§6），但 bundle-root index.md 可含 `okf_version`（§11 唯一例外）
- 目录列表格式，支持渐进式披露
- 条目应包含链接 concept 的 description

## Section 7: Log 文件
- `log.md` 可出现在任意层级
- 日期分组条目，最新在前
- 日期标题用 ISO 8601 `YYYY-MM-DD`
- 条目为散文，前置粗体词（`**Update**`、`**Creation**` 等）为约定

## Section 8: Citations
- concept 正文引用外部来源时，在底部用 `# Citations` 标题列出
- 编号格式：`[1] [标题](URL)`
- 链接可为绝对 URL、bundle-relative 路径或 references/ 子目录路径

## Section 9: Conformance
bundle 符合 OKF v0.1 当且仅当：
1. 每个非保留 .md 文件含可解析的 YAML frontmatter
2. 每个 frontmatter 含非空 `type` 字段
3. 保留文件名（index.md, log.md）存在时遵循 §6/§7 结构

Consumer 应将其他约束视为软指导，不得因以下原因拒绝 bundle：
- 缺少可选 frontmatter 字段
- 未知 type 值
- 未知额外 frontmatter 键
- 断链
- 缺少 index.md
**Conformance 检查是报告性的，不是拒绝性的。**

## Section 11: 版本
- 当前版本：OKF 0.1
- minor 版本：向后兼容的新增（新可选字段、新约定标题）
- major 版本：可能破坏性变更（重命名必填字段、改保留文件名）
- Bundle 可在 bundle-root index.md frontmatter 中声明 `okf_version: "0.1"`（index.md 唯一允许的 frontmatter 位置）
- Consumer 不识别版本时应 best-effort 消费，而非拒绝
