# 时序图

## ID 和边界

稳定 ID：`sequence`。用于表达参与方之间的调用和返回，不要把它写成 `flow.sequence`。

## 请求结构

```json
{
  "kind": "sequence",
  "title": "业务请求调用时序",
  "data": {
    "participants": [
      {"ref":"user","name":"用户"},
      {"ref":"gateway","name":"网关服务"},
      {"ref":"service","name":"业务服务"}
    ],
    "messages": [
      {"from":"user","to":"gateway","message":"提交请求"},
      {"from":"gateway","to":"service","message":"转发请求"},
      {"from":"service","to":"gateway","message":"返回结果","kind":"return"}
    ],
    "notes": [{"participant":"service","text":"记录审计日志"}]
  }
}
```

参与方可以是字符串，也可以是必须包含 `ref` 和 `name` 的对象。参与方必须唯一，消息端点必须引用已有参与方。`kind` 为 `call` 或 `return`，默认 `call`；自调用是合法的。

## 限制和文字

2–6 个参与方、1–12 条消息、最多 4 条备注。参与方名称建议 14 个字符以内，消息建议 24 个字符以内，长报文应放到备注或拆图。
