## 语义拆分示例

**输入**: "帮我用公司模板做一份关于钛合金马扎的演示 PPT，下周之前要交给客户"

**输出**:
```json
{
  "pipeline_summary": {
    "b_layers": ["regex"],
    "a_layers": ["regex", "embedding", "rerank"],
    "c_method": "agent_reasoning"
  },
  "steps": [
    {"name": "收集需求", "action": "确认PPT用途和受众", "milestone": true},
    {"name": "设计大纲", "action": "规划结构", "depends_on": ["s1"]},
    {"name": "制作内容", "action": "按照公司模板制作", "depends_on": ["s2"]}
  ]
}
```

## 模板扫描示例

**输入**: python scripts/json_manager.py scan --keywords 制作 PPT 产品

**输出**:
```json
[
  {"id": "make_ppt_v1", "name": "制作PPT", "score": 0.92, "steps": "..."},
  {"id": "design_report_v1", "name": "设计报告", "score": 0.45, "steps": "..."}
]
```
