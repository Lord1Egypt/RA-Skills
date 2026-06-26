---
id: P1_feature_scenario
name: P1单功能点场景生成
version: "4.8.9"
last_updated: "2026-05-22"
---

# 为单个功能点生成测试场景

基于以下信息，为**一个**功能点生成 2-5 个测试场景。

---

## 当前功能点

```json
{{feature_context}}
```

## 相关业务规则

```json
{{related_rules}}
```

---

## 输出格式

```json
{
  "feature_id": "M01-F01",
  "page_path": "页面路径（如: 分润管理→员工配置）",
  "scenarios": [
    {
      "name": "场景名（≤50字）",
      "id": "M01-F01-S01",
      "type": "scenario",
      "scenario_type": "positive",
      "description": "场景描述（≤200字）",
      "test_point_hint": "测试要点（≤100字）",
      "precondition": "前置条件（如: 已登录CRM系统，具有XX权限）",
      "operations_chain": [
        {"action": "点击", "target": "分润管理", "expected": "进入分润管理页面"},
        {"action": "输入", "target": "员工姓名", "value": "张三", "expected": "输入框显示张三"},
        {"action": "点击", "target": "查询按钮", "expected": "显示查询结果列表"}
      ]
    }
  ]
}
```

## 规则

1. **至少 2 个** scenario：1 正向 + 1 异常（违反规则时使用），最多 5 个
2. **scenario_type**：`positive`（正向验证）、`negative`（异常/违反规则）、`boundary`（边界值）
3. **场景名简洁**：≤50 字
4. **描述聚焦**：≤200 字，只描述本场景的核心行为
5. **test_point_hint 简短**：≤100 字，提示测试关注点
6. **page_path 必填**：从 UI 导航路径提取，如 "分润管理→员工配置"，即使不完整也要填写
7. **precondition 必填**：列出执行本场景前必须满足的条件
8. 🔴 **operations_chain 必填**：每个 scenario 必须有 2-4 步操作链，每步含 action(点击/输入/选择/查询)、target(具体的按钮名/字段名/页面名)、expected(预期结果)。不得为空数组。
9. **输出纯 JSON**：不得添加解释性文字
10. **🔴 优先保证场景质量而非数量**：2 个高质量场景（正向+异常）优于 5 个凑数场景
