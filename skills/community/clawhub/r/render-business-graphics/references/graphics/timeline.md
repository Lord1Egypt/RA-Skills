# 时间轴

## 版式 ID

| ID | 视觉意图 |
| --- | --- |
| `timeline.milestone` | 标准横向里程碑，事件卡片上下交替 |
| `timeline.wave` | 波浪曲线 |
| `timeline.path` | 曲线路径和定位点 |
| `timeline.ribbon` | 箭头色带 |
| `timeline.blocks` | 上下交替色块 |
| `timeline.loop` | 双轨回环 |
| `timeline.staircase` | 立体阶梯递进 |
| `timeline.vertical-spine` | 纵向主轴和左右卡片 |
| `timeline.icon-ribbon` | 图标、箭头带和信息分栏 |

所有版式使用同一事件数据，variant 只改变视觉表达。

## 请求结构

```json
{
  "kind": "timeline",
  "variant": "milestone",
  "title": "项目发展历程",
  "data": [
    {"ref":"A","date":"2023","title":"项目启动","position":"bottom","icon":"briefcase"},
    {"ref":"B","date":"2024","title":"方案确定","position":"top","icon":"handshake"},
    {"ref":"C","date":"2025","title":"成果交付","position":"bottom","icon":"trophy"}
  ]
}
```

事件必须有唯一 `ref`、`date`、`title`；`description`、`position`、`icon` 可选。`position` 为 `top` 或 `bottom`，省略时自动交替。图标只能使用 `briefcase`、`handshake`、`trophy`、`chart`、`clock`、`globe`、`flag`。

## 限制和文字

事件数量为 2–8，默认 A4 横版。保持源内容的时间顺序，服务不会替 Agent 解析日期并重排。事件标题建议 14 个字符以内，说明建议 32 个字符以内。
