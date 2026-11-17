# 组织架构图

## ID 和含义

稳定 ID：`organization`。只表达严格嵌套树，不能表达跨分支协同或任意网状关系。

## 请求结构

```json
{
  "kind": "organization",
  "title": "项目实施组织架构",
  "direction": "vertical",
  "data": {
    "name": "项目领导小组",
    "role": "重大事项决策",
    "children": [
      {
        "name": "项目经理部",
        "children": [{"name": "技术组", "headcount": 8}]
      }
    ]
  }
}
```

`kind` 和 `data` 必填。`direction` 为 `vertical` 或 `horizontal`。每个节点必须有 `name`，`role`、非负整数 `headcount` 和递归的 `children` 可选。服务会从树自动生成节点 ID 和连接线，不要在 V2 `data` 中发送 `id`、`parentId`、坐标或扁平节点数组。

## 限制和文字

最多 200 个节点、12 层。节点名称建议 12 个字符以内，职责建议 24 个字符以内。层级过密时可以按一级部门拆成多张图，但不能删除节点来强行适配。
