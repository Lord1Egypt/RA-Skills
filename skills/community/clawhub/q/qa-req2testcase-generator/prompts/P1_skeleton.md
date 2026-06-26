---
id: P1_skeleton
name: P1模块功能点骨架生成
version: "4.8.9"
last_updated: "2026-05-22"
---

# P1 模块与功能点骨架

基于输入的 P0 需求结构化数据，生成完整的**模块→功能点**树骨架。**本次只生成结构和描述，不需要生成场景（scenarios）。**

---

## 输出格式

```json
{
  "feature_tree": {
    "children": [
      {
        "name": "模块名",
        "id": "M01",
        "type": "module",
        "description": "模块描述（≤80字）",
        "children": [
          {
            "name": "功能点名",
            "id": "M01-F01",
            "type": "feature",
            "description": "功能点描述（≤80字）",
            "children": []
          }
        ]
      }
    ]
  },
  "coverage_check": {
    "operations_missing": [],
    "business_rules_unmapped": [],
    "module_mapping": {"模块名": ["M01"]}
  }
}
```

## 规则

1. **不得少拆**：P0 中每个 `operation` 必须在功能点树中有对应 feature
2. **不得多拆**：不得自行发明 P0 中没有的功能点
3. **场景占位**：每个 feature 的 `children` 必须为空数组 `[]`，场景将在后续步骤中逐 feature 填充
4. **模块命名**：按业务域聚合，模块数 ≤ 8 个
5. **功能点命名**：`{操作对象}{操作动作}`，如"新增分润规则""删除分润规则"
6. **描述必填**：module 和 feature 的 `description` 必填，不得为空
7. **输出纯 JSON**：不得在 JSON 前后添加任何解释性文字
8. **coverage_check**：`operations_missing` 必须为空

---

现在基于输入数据生成 P1 骨架 JSON。
