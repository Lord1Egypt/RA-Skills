# 第二步：确定收件地址 + 收件人信息

> **触发**：`next_state == step2-receiver-address`

流程与 [第一步](./step-1-sender.md) 完全一致（含 [§0 前置判断硬约束](./step-1-sender.md#0-调命令前的前置判断硬约束)），把 `sender` 换成 `receiver`：

```bash
python3 ./scripts/tms_delivery.py resolve-address receiver "<keyword>" "<region?>"
python3 ./scripts/tms_delivery.py pick-address receiver <序号>
python3 ./scripts/tms_delivery.py commit-contact receiver "<姓名>" "<手机号>"
```

`decision` / `status` / `next_state` 分支表同第一步。`next_state == "step3-estimate"` 即本步完成。

## 硬约束

- ✅ 本步只为 `receiver.*` 调地址搜索
- ❌ 禁止再次调 `sender.*`
- ❌ 禁止在此调询价（第三步的事）
- ❌ 禁止在用户未提收件地点时凭空捏造 `<keyword>`（见 [第一步 §0](./step-1-sender.md#0-调命令前的前置判断硬约束)）
