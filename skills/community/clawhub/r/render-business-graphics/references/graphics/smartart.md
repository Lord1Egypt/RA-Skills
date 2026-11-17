# SmartArt

## ID 和数量

| ID | 意图 | 数据形状 | 数量 |
| --- | --- | --- | --- |
| `smartart.process` | 有序流程 | 项目数组 | 2–6 |
| `smartart.vertical-detail` | 纵向详细条目 | 项目数组 | 2–6 |
| `smartart.cycle` | 循环闭环 | 项目数组 | 2–6 |
| `smartart.radial` | 中心和周边维度 | 项目数组 | 2–6 |
| `smartart.petal-radial` | 六维分类 | 项目数组 | 恰好 6 |
| `smartart.pyramid` | 分层体系 | 项目数组 | 3–5 |
| `smartart.relationship` | 多方围绕中心关系 | 项目数组 | 3–5 |
| `smartart.comparison` | 两个方案按指标对比 | 对比对象 | 2–5 行 |
| `smartart.key-points` | 关键保障或要点 | 项目数组 | 3–6 |

## 普通项目

```json
{
  "kind": "smartart",
  "variant": "process",
  "title": "项目实施总体流程",
  "data": [
    {"title": "需求调研", "note": "梳理建设目标"},
    {"title": "方案设计", "note": "形成实施方案"}
  ]
}
```

项目也可以直接写标题字符串。对象必须有 `title`，可选 `note` 和图标 `cross`、`circle`、`curve`、`card`、`nodes`、`gear`。

`direction` 只用于 `smartart.process`；`center` 只用于 `cycle`、`radial`、`petal-radial`、`relationship`。除 `petal-radial` 外使用 A4 竖版，`petal-radial` 必须使用 A4 横版。

## 对比结构

```json
{
  "kind": "smartart",
  "variant": "comparison",
  "data": {
    "columns": ["方案一", "方案二"],
    "rows": [
      {"label": "建设周期", "values": ["较短", "较长"]}
    ]
  }
}
```

必须恰好两个 `columns`，每行恰好两个 `values`。数值为主时改用 `chart.comparison`。标题建议 14 个字符以内，解释放 `note`，建议 36 个字符以内。
