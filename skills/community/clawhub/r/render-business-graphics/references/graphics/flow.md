# 流程图

## 稳定 ID

- `flow.sequence`：至少两个步骤的线性流程，由服务自动生成相邻连线。
- `flow.graph`：明确提供节点和连线，适用于分支、判断、反馈和非线性流程。

## 线性流程

```json
{
  "kind": "flow",
  "variant": "sequence",
  "title": "项目实施流程",
  "data": [
    "需求调研",
    {"text": "方案设计", "detail": "形成实施方案", "shape": "process"},
    "验收交付"
  ]
}
```

每个步骤可以是字符串，或包含必填 `text`、可选 `detail`/`shape` 的对象。

## 复杂流程

```json
{
  "kind": "flow",
  "variant": "graph",
  "data": {
    "nodes": [
      {"ref":"start","text":"提交申请","shape":"start"},
      {"ref":"check","text":"资料完整？","shape":"decision"},
      {"ref":"end","text":"完成","shape":"end"}
    ],
    "links": [
      {"from":"start","to":"check"},
      {"from":"check","to":"end","label":"是"}
    ]
  }
}
```

图模式节点必须有唯一 `ref` 和 `text`；连线的 `from`/`to` 必须引用已有 ref。`relation` 为 `main` 或 `feedback`，反馈关系使用虚线表现。节点 `shape` 支持 `start`、`end`、`process`、`decision`、`document`、`subprocess`，默认是 `process`。

## 自适应独立画布

只有 `flow.graph` 支持显式开启独立图片画布：

```json
"layoutPolicy": {
  "usage": "standalone-image",
  "canvas": "adaptive",
  "preserveDirection": true
}
```

启用后不能再传 `page`，服务会在受控范围内保留方向和文字。只有用户确实需要独立长图时才启用。

## 限制和文字

最多 80 个节点、160 条连线。节点标题建议 14 个字符以内，说明建议 28 个字符以内，连线标签尽量使用“是”“否”“通过”“退回”等短词。不能从自然语言自行推断缺失连线。
