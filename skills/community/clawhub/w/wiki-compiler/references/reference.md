# Wiki 编译参考（v5.0.0 重构版）

> 索引页：基于 Karpathy 三大操作重新组织。从这里跳转到各专题详情。

## 🎯 核心理念

> "Human curates, LLM maintains" — 人类决定收录什么，LLM 维护导览
> **三大操作**：Ingest（摄取）/ Lint（健康检查）/ Schema（契约）

## 📚 Karpathy 三大操作文档

| 操作 | 文档 | 适用场景 |
|------|------|---------|
| **Ingest** | [ingest.md](ingest.md) | 资料入库、编译导览、自动级联 |
| **Lint** | [lint.md](lint.md) | 4 类标准检查（结构/矛盾/孤立/过期）|
| **Schema** | [schema.md](schema.md) | 强制 frontmatter 契约 |

## 📚 子流程文档

| 文档 | 适用场景 | 说明 |
|------|---------|------|
| [folder-organization.md](folder-organization.md) | Ingest 前置 | 知识库结构诊断 + 文件归类 |
| [tagging.md](tagging.md) | Ingest 子任务 | 标签设计 + 应用 + 审查 |
| [security.md](security.md) | 全流程 | 破坏性操作保护 |
| [api-reference.md](api-reference.md) | 全流程 | IMA OpenAPI 端点 + 错误码 |
| [guide-template.md](guide-template.md) | Ingest 子任务 | 主题导览 4 章节结构 + 写作规范 |
| [versioning.md](versioning.md) | Ingest 子任务 | 主题导览的版本控制 |
| [write-and-verify.md](write-and-verify.md) | Ingest 子任务 | 写入笔记 + 验证流程 |
| [link-handling.md](link-handling.md) | Ingest 子任务 | 链接特性预获取 + 链接策略 |
| [troubleshooting.md](troubleshooting.md) | 全流程 | 常见错误 + 解决方案 |
| [cases/quantitative-investing.md](cases/quantitative-investing.md) | 案例 | 量化投资知识库试跑经验 |

## 🎯 Karpathy 三大操作 vs wiki-compiler 7 阶段（v4.x）

| Karpathy 三大操作 | wiki-compiler v4.x 7 阶段 | v5.0.0 重构 |
|------------------|---------------------------|------------|
| Ingest（摄取）| 阶段 1+2+3+4+5 | 6 个子任务：Collect/Check/Link/Compile/Write/Cascade |
| Lint（健康检查）| 阶段 6（部分）| 4 类标准检查 |
| Schema（契约）| （软约束）| 强制 frontmatter |

## 🚀 快速跳转

- 不知道从哪开始？→ 看 SKILL.md 的"快速开始"章节
- 触发词困惑？→ SKILL.md "核心理念"章节
- 遇到错误？→ [troubleshooting.md](troubleshooting.md)
- 不知道 API 怎么调用？→ [api-reference.md](api-reference.md)
- 担心破坏性操作？→ [security.md](security.md)
- 想看实际案例？→ [cases/quantitative-investing.md](cases/quantitative-investing.md)
- 主题导览怎么写？→ [guide-template.md](guide-template.md) + [schema.md](schema.md)

## 📊 与 Karpathy 原始模式的对应

| Karpathy 原始模式 | wiki-compiler v5.0 实现 |
|------------------|----------------------|
| `CLAUDE.md` 模式核心 | `references/schema.md` |
| frontmatter 约定 | 强制 frontmatter 字段 |
| `[[wikilinks]]` 引用 | `related_guides[]` 数组 |
| `git log` 审计 | `changelog[]` 数组 |
| 资料溯源 | `sources[]` 数组 |
| LLM 把握度 | `confidence` 字段 |
| 三层架构（raw/wiki/CLAUDE.md）| IMA 知识库 / 主题导览 / Schema 文档 |
| 三大操作（Ingest/Query/Lint）| Ingest / 不归我管 / Lint |

## 🔄 Karpathy vs IMA 平台差异

| 维度 | Karpathy 原始 | IMA 平台 |
|------|--------------|---------|
| 存储 | 本地 Markdown 文件 | 云端笔记 + 知识库 |
| 触发 | 手动操作 UI | 自然语言触发词 |
| 版本控制 | Git 提交 | 笔记版本号 + changelog |
| 反向链接 | `[[wikilinks]]` 自动建立 | `related_guides[]` 手动维护 |
| 删除笔记 | 完全支持 | ❌ 不支持（需客户端） |
| 向量搜索 | LanceDB（可选） | 平台内置（不归我管）|

## 📖 核心理念速查

### 传统 RAG vs Karpathy LLM Wiki

| 特性 | Karpathy LLM Wiki | 传统 RAG |
|------|------------------|----------|
| **状态** | 有状态——知识持续积累 | 无状态——每次查询独立 |
| **基础设施** | 一堆 `.md` 文件 | 向量库 + embedding |
| **交叉引用** | 预建（`related_guides[]`）| 临时发现 |
| **可追溯性** | 强（每个论断追到 raw）| 弱（chunk 级引用） |
| **规模甜区** | < 100-200 个源 | 百万级文档 |

### 文件夹设计模式

详见 [folder-organization.md 第 6 节](folder-organization.md)

**模式 A：扁平**（中等规模）

```
知识库根
├── 文件夹 1
├── 文件夹 2
└── 文件夹 3
```

**模式 B：2 层嵌套**（复杂领域）

```
知识库根
├── 文件夹 1
├── 文件夹 2（复杂主题）
│   ├── 子文件夹 A
│   ├── 子文件夹 B
│   └── 子文件夹 C
└── 文件夹 3
```

### 标签与文件夹的协同

详见 [folder-organization.md 第 7 节](folder-organization.md) 和 [tagging.md](tagging.md)

| 维度 | 文件夹 | 标签 |
|------|:---:|:---:|
| 主导维度 | 主题分类 | 多维关联 |
| 结构 | 树状（一文件一父）| 网状（一文件多标签）|
| 人类友好 | 高（导览）| 低（API）|
| 机器友好 | 低 | 高 |

**核心原则**：
- 职责不重叠：文件夹负责"内容组织"，标签负责"维度标记"
- 互为补充：标签给文件夹扩展维度，文件夹给标签赋予语义
- 低耦合：任一失效，另一方仍可独立工作

## 📝 文档维护说明

**当前版本**：v5.0.0（2026-09-28）

**重构原则**：
- Karpathy 三大操作作为顶层架构
- 子流程文档按 Ingest 子任务组织
- Lint 和 Schema 各自独立

**演进原则**：
- 新增功能 → 在对应 Karpathy 操作下扩展
- 避免重新发明轮子（不归我管的由 IMA 处理）
