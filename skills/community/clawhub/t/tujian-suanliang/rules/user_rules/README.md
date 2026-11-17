# 用户新增规则

把用户确认过的规则放在本目录。文件名不能以 `_` 开头。

规则是 JSON，顶层字段可以这样：

```json
{
  "beam_rules": [
    {
      "id": "my-rule-id",
      "enabled": true,
      "kind": "expression",
      "name": "规则名称",
      "applies_to": ["KL"],
      "required_inputs": ["section_h_mm", "seismic_level"],
      "formula": "max(k * section_h_mm, min_mm)",
      "params": {
        "seismic_level": {
          "一级": {"k": 2.0, "min_mm": 500}
        }
      },
      "source": "图纸指定图集编号",
      "source_page": "填写正式页码",
      "uncertainty": "复核说明"
    }
  ]
}
```

公式使用白名单表达式，不允许执行任意代码。
