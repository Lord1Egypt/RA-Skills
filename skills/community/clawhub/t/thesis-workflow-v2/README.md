# MBA/学术论文 多Agent协作工作流（v2 新框架）

📝 多Agent协作完成MBA/学术论文写作的完整工作流，支持大纲解析、逐节点写作、深度审核、整合终审、Word输出。

适用于开题报告到毕业论文的全流程。

---

## ⚠️ 当前项目双版本并行

本仓库包含 **两条独立版本线**，互不干扰、并行发布：

| 版本线 | ClawHub Slug | 当前 latest | 状态 | 文档 |
|--------|--------------|-------------|------|------|
| **v1.x**（稳定） | `thesis-workflow` | **v1.7.3** | 长期维护，仅兼容性修复 | [CHANGELOG-v1.md](./CHANGELOG-v1.md) |
| **v2.x**（新框架） | `thesis-workflow-v2` | **v2.0.14** | ⚠️ 测试版，outline-anchored + 9 HIL + 多工具检索 | [CHANGELOG-v2.md](./CHANGELOG-v2.md) |

### 选型指南

- **生产环境 / 已有 v1 用户** → `thesis-workflow` (v1.7.3，稳定)
- **新框架 / outline-anchored / 9 HIL 体验** → `thesis-workflow-v2` (v2.0.14，测试)
- **同时跑多篇论文** → 两个都装，**可共存**

### 怎么装两个？

```bash
# v1 稳定版（不依赖本仓库）
openclaw skills install thesis-workflow

# v2 测试版
openclaw skills install thesis-workflow-v2
```

两者安装路径、状态文件、依赖互不冲突。

详见 [`references/git-workflow.md`](./references/git-workflow.md) 和 [CHANGELOG.md](./CHANGELOG.md) 索引。

---

## 核心功能（v2 框架）

- **outline-anchored 写作**：以大纲为锚点，逐节点生成内容，节点间自动承接
- **BGE-small-zh 向量标题匹配**：Phase 1.3 开题归因加速 30-90s → 2-5s
- **多工具并行检索**：4工具（Tavily/arXiv/OpenAlex/web_search）同时搜索，去重排序
- **Phase 3.5 深度学术评审**：P0/P1/P2 分级问题清单，自动修复 + 重审闭环
- **RuntimeLLM**：零硬编码，自动复用当前 session 模型配置
- **9 个 HIL 节点**：human-in-the-loop 检查点，关键决策不跳过
- **Guardrails 自检**：10 项自动化规范检查（章节完整性/字数/引用/表格格式等）
- **Loop 架构**：Orchestrator Loop / 内部自检 Loop / 审核 Loop / Verification Loop
- **Phase 5 Word输出**：md2docx_strict.py 合规脚本（三线表/分页/字体/行距）

## 适用场景TODO_SPLIT

- MBA毕业论文（战略管理/企业分析类）
- 学术研究报告（竞争战略/行业分析类）
- 需要多轮审核、多版本整合的正式长文

## 工作流程

```
用户 → Phase 1（大纲确认 + 开题归因）→ Phase 2（逐节点写作）→ Phase 2.5（用户确认）
     → Phase 3（整合）→ Phase 3.5（深度学术评审 → P0修复循环）
     → Phase 4（修复）→ Phase 5（终审 + Word输出）
```

## v2.0.x 版本历史（详见 [CHANGELOG-v2.md](./CHANGELOG-v2.md)）

| 版本 | 亮点 |
|------|------|
| 2.0.12-beta | Phase 3.5 大纲锚定章节拆分（替代硬编码正则）+ P0/P1 修复（F1-F6）|
| 2.0.11-beta | 清理 v1 残留 + clawhubignore 排除 |
| 2.0.10-beta | Phase 3.5/4/5 实现 + requirements.txt + lazy BGE |
| 2.0.9-beta | BGE-small-zh 向量标题匹配（Layer 2） |
| 2.0.8-beta | multi-search并行引擎 + RuntimeLLM 零硬编码 |
| 2.0.7 | outline_parser 引擎切换 B→A 单向降级 |
| 2.0.6 | 双版本独立发布 + enforcement + 真实入口 CLI |
| 2.0.5 | B-2 状态同步修复 |
| 2.0.4 | B-1 HIL 死循环修复 |
| 2.0.3 | P2 代码清理 |
| 2.0.2 | P0/P1 修复 |
| 2.0.1 | 方案 C 端到端验证 |
| 2.0.0 | outline-anchored feature complete |

## Agent 角色体系

| Agent | 调用方式 | 主责 |
|-------|---------|------|
| **Orchestrator** | 当前 session | 调度 / 推进 / 决策 |
| **NodeWriter** | `sessions_spawn` | 逐节点内容生成 |
| **Reviewer** | `sessions_spawn` | Phase 3/5 规则型审核 |
| **DeepReviewer** | `sessions_spawn` | Phase 3.5 学术深度评审 |
| **Integrator** | `sessions_spawn` | Phase 4 整合方案 |
| **WordAgent** | `exec python3` | md2docx执行 + 格式校验 |

## 版本说明

| 文件命名 | 说明 |
|---------|------|
| `论文_xxx.md` | 论文正稿 |
| `_orchestrate_state.json` | 流程状态（自动管理） |
| `_outline_state.json` | 大纲状态（自动管理） |

## 写作规范

- **引用格式**：GB/T 7714 作者年制（作者, 年）
- **正文字数**：≥3.5万字
- **写作语法**：正文段落禁止 `**加粗**` 强调术语
- **中文字体**：宋体12磅，行距20磅
- **英文字体**：Times New Roman
- **标题字体**：黑体16磅/14磅/13磅

## 技术栈

- OpenClaw subagent (sessions_spawn)
- BGE-small-zh 中文向量模型（Layer 2 标题匹配）
- Tavily / arXiv / OpenAlex 多工具并行检索
- md2docx_strict.py（Word 合规转换）
- Guardrails loop_self_check.py（10 项自动化校验）

## License

MIT-0 — Free to use, modify, and distribute without attribution

## Author

GitHub: [hehe973781230](https://github.com/hehe973781230)

---

*If this skill is helpful to you, please give it a ⭐*