---
name: sql_audit
slug: sql_audit
version: 1.0.2
description: SQL 语法与安全审核，它将真正执行，并返回执行的数据结果
metadata: {"clawdbot":{"emoji":"🐬"}}
---
# Skill: sql_audit

- Description: SQL 语法与安全审核 + 真实执行，返回查询数据结果。
- Inputs: [sql_output]（从 `skills/.workflow/sql_output.json` 读取）
- Outputs: [data, row_count, success]（写入 `skills/.workflow/audit_output.json`）
- ID: sql_audit

- Role: 质量与安全哨兵 + 执行引擎

- 功能描述：在 SQL 执行前进行静态扫描，确保语法正确；通过连接真实 StarRocks/Doris 执行 SQL 并返回结果。

- 输入参数（来自 sql_output.json）：
    - sql (string): 主候选 SQL
    - sql_candidates (list): 多候选 SQL（重试用）
    - query (string): 用户原始问题
    - indicator_metric (list): 指标维度（重试时用于生成简化候选）

- 输出结果：
    - success (boolean): 执行是否成功。
    - data (list): 查询结果行（每行为 dict）。
    - row_count (int): 结果行数。
    - need_retry (boolean): 若结果为空，建议重新生成 SQL。
    - new_indicator_metrics (list): 简化后的候选指标（供重试时传给 sql_generator）。

- 拦截规则：拦截全表扫描（无 Where 条件）；拦截写操作；拦截跨库非法关联。

## 依赖（通过 `.env` 配置）

| 服务 | .env 配置键 |
|------|-------------|
| StarRocks/Doris | `DB_HOST` / `DB_PORT`（默认 9030）/ `DB_USER` / `DB_PASSWORD` / `DB_NAME` |
| Gemini（兜底候选生成） | `GEMINI_API_URL` / `GEMINI_API_KEY` / `GEMINI_TOKEN` |

## 独立运行说明

```bash
# 前置：先运行前四步
python ../rewrite-question/rewrite_question.py --query "今天汉河店的成交额"
python ../recognize-intent/recognize_intent.py
python ../mult-call/multi_call.py
python ../sql-generator/sql_generator.py

# 运行 SQL 审核执行（从 .workflow/sql_output.json 自动读取）
python sql_audit.py

# 带清理（清除本步输出）
python sql_audit.py --clean
```

这是整条链路的最后一步，执行完毕后可查看 `skills/.workflow/audit_output.json` 获得最终结果。
