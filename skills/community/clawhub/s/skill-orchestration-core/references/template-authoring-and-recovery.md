# 模板编写与跨会话恢复

## 1. 新建工作流模板的验证流程

每个 DESIGN.md 模板完成后，**必须**跑三个验证：

```bash
# 1) 解析验证 — 阶段/skills/tasks/outputs 非空
python3 scripts/workflow_orchestrator.py parse templates/<name>/DESIGN.md

# 2) 输出验证（需在项目目录里有对应文件）
python3 scripts/output_validator.py validate-all templates/<name>/

# 3) 端到端测试（仅 example-project 做，其他模板无项目文件）
python3 scripts/test_e2e.py
```

解析验证最容易暴露的问题：
- 加粗列表标题导致 `_extract_list` 返回空 → 陷阱 #7
- 上下文/验证 YAML 缩进不一致 → 解析失败
- 阶段标题没用 `### 阶段 N:` 或 `### Stage N:` → 正则不匹配

## 2. 跨会话恢复迭代工作

skill-orchestration-core 的迭代跨了 6月10-13号 共 4+ 个 session。
恢复方法：

1. `session_search(limit=5, sort="newest")` 浏览最近 session
2. 找到标题提及当前任务的 session，`session_search(session_id=...)` 读全文
3. 定位最后的 TODO 列表（`todo` tool output），找到 `status=in_progress` 或 `status=pending`
4. 从最后一个未完成项继续，**不要**从头重做已验证通过的步骤

关键信号：
- session 标题含 "迭代改进" / "完成" → 可能已做完
- 用户输入 "?" 后中断 → 上一个 tool call 可能执行完了但结果没被整理
- TODO 里的 completed 项不需要重跑

## 3. 模板目录约定

```
templates/<name>/
├── DESIGN.md           # 必需 — 编排指南
└── (可选) 其他输出文件   # 仅 example-project 需要
```

新增模板后，同步更新：
- SKILL.md 的「工作流模板」表格
- SKILL.md 的项目结构树
- templates/README.md

## 4. 已有模板清单 (v2.1.0)

| 模板 | 阶段 | Skills | 适用 |
|------|------|--------|------|
| example-project | 4 | writing-plans, tdd, subagent, requesting-code-review | 学习/测试 |
| web-fullstack | 5 | writing-plans, tdd, subagent, requesting-code-review | React+FastAPI |
| data-analysis | 5 | writing-plans, tdd, subagent, requesting-code-review | 数据采集/建模/报告 |
| api-product | 4 | writing-plans, api-product-planning, tdd, subagent, requesting-code-review, enterprise-web-deployment | API组合产品 |
