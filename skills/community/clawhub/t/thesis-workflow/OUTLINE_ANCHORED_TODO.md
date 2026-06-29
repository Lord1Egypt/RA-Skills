# Outline-Anchored 重构待办项

> 记录 feature/outline-anchored 分支的重构计划和进度
> 分支: `feature/outline-anchored`，基于 `main` 分支

---

## ✅ 已完成

- [x] Step 1: 目录解析器 `outline_parser.py` + 状态管理器 `state_manager_v2.py`
- [x] Step 2: ContextBuilder `context_builder.py`
- [x] Step 3: NodeWriter 节点写作器 v1.0
- [x] Step 4: Reviewer 评审器 v1.0
- [x] Step 5: Orchestrator V2 全链路联调 v1.0
- [x] Step 6: Phase 边界重定义 + Phase3 用户修改支持
- [x] Step 7: 增强项2 — AI 标题匹配归因（`_llm_match_proposal_headings`）

---

## 🔲 待开发

### 增强项1: 跨父节点 Bridge — 章节摘要节点

**问题**：`2.1` 找不到 `1.2` 的 key_conclusion，bridge 断裂。

**方案（方案C — 章节摘要节点）**：
- 在每个一级章节末尾自动插入虚拟 `__chN_summary__` 节点
- 该节点吸收本章所有 L2/L3 的 `key_conclusion`，生成章节级摘要
- 下一章节的 bridge 可引用前一章节的摘要节点

**触发时机**：
- **时机A（自动）**：章节末尾最后一个 L2/L3 节点完成 → 自动触发章节摘要生成
- **时机B（补充）**：用户在 Phase 1.3 自定义分析维度时填的"本章核心问题"，作为摘要生成的补充参考

**状态**：待开发

---

### 增强项3: content_hint 生成

**问题**：Phase 1.3 用户填写"分析重点"时为空，需要从零填写，体验差。

**方案**：
1. `extract_proposal_content()` 时同步提取每个节点的前 1-2 句作为 `content_hint`
2. 存入节点的 `content_hint` 字段（新增字段）
3. Phase 1.3 展示时预填这些方向提示，用户可查看、修改、新增

**状态**：待开发

---

### 增强项4: 写作前信息检查

**问题**：节点写作前如果完全没有外部信息（content_hint 为空）需暂停让用户确认。

**方案**：
- 节点写作前检查 `content_hint` 是否为空
- 为空 → 暂停，询问用户是否补充或让 AI 自行生成
- 用户不补充 → AI 基于已有信息自行生成

**状态**：待开发

---

### Step 8: Orchestrator Phase 1.3 集成

将 `extract_proposal_content()` 接入 Orchestrator Phase 1.3：
- 用户上传开题报告 docx
- 自动提取内容 → 匹配到目录节点
- 展示归因结果，用户确认

**状态**：待开发

---

### Step 9: 全流程测试 + 提交

- 所有单元测试通过
- 全链路集成测试
- 提交本地分支，等待确认后 push

---

## 执行计划（小步快跑）

```
Step 7 ✅  — 增强项2 AI标题匹配（已完成）
Step 8    — 增强项3 content_hint 生成
Step 9    — 增强项1 跨父节点 Bridge（章节摘要节点）
Step 10   — 增强项4 写作前信息检查
Step 11   — Orchestrator Phase 1.3 集成
Step 12   — 全流程测试 + 提交
```
