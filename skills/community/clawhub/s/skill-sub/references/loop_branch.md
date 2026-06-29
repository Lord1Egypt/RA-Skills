# 循环与分支编排

> 本文档是 SKILL.md 的渐进式补充，包含循环与分支编排的完整示例。

---

## for-each 循环

在调用链 JSON 中，将某步骤的  设为 ，并定义  对象：

```json
{
  "type": "loop",
  "step_name": "批量处理文件",
  "loop": {
    "mode": "for_each",
    "items": "{{file_list}}",
    "loop_variable": "f",
    "max_iterations": 10,
    "steps": [
      {"type": "skill", "skill_name": "file-ops", "step_name": "处理单个文件", "action": "处理 {{f}}"}
    ]
  }
}
```

## while 循环

```json
{
  "type": "loop",
  "step_name": "重试直到成功",
  "loop": {
    "mode": "while",
    "while_condition": "{{retry_count}} < 3 and {{last_result}} != 'success'",
    "max_iterations": 3,
    "steps": [
      {"type": "skill", "skill_name": "api-call", "step_name": "调用接口", "action": "重试第 {{retry_count}} 次"}
    ]
  }
}
```

## if-else 分支

```json
{
  "type": "branch",
  "step_name": "按环境部署",
  "branch": {
    "condition": "{{env}} == 'prod'",
    "if_steps": [
      {"type": "skill", "skill_name": "deploy", "step_name": "生产部署", "action": "部署到生产环境"}
    ],
    "else_steps": [
      {"type": "skill", "skill_name": "deploy", "step_name": "预发部署", "action": "部署到预发环境"}
    ]
  }
}
```

---

> 完整 schema 详见 `references/chain_schema.md`
