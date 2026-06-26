# 会话状态

> `~/.config/tms-delivery/session.json` —— 防止接口参数因 chat 截断而丢失。

## 约束

1. **只存接口会丢的字段**（sender/receiver/estimatePriceRecordId/skuMap/selectedSkuId/orderCode）
2. **禁止泄露到用户端**（详见 [SKILL.md §4](../SKILL.md#output-leak-firewall)）
3. **禁止 read_file/cat 直接访问**，只能通过 `state` 子命令

## Schema（v3）

```
sender/receiver:
  name / phone / address: { name, longitude, latitude, poiid }

estimatePriceRecordId   询价缓存Key
estimate_at             询价时间戳（自动写入）
skuMap                  序号→skuId 映射
selectedSkuId           用户选中的 skuId
orderCode               订单编码
```

## 常用命令

```bash
state get [path]                    # 读取
state set <path> <json_value>       # 写入（有 WRITE_GUARD）
state next                          # FSM 驱动器
state show                          # 快照诊断（手机号脱敏）
state reconcile <going_json>        # §0 校准（bootstrap 已内嵌）
state clear                         # 释放
state init                          # 初始化空快照
```

## 清理时机

| 场景 | 动作 |
|------|------|
| §0 reconcile | 自动 init 或 keep |
| 修改地址 | 清空 estimatePriceRecordId/skuMap/selectedSkuId |
| 用户退出/支付成功/取消成功 | state clear |
