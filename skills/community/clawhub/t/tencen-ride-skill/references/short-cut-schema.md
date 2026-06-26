# 快捷叫车文件 `~/.config/tms-takecar/short-cut.json`

用于保存快捷叫车场景配置。

## 1. 文件结构

顶层必须是 JSON object，key 为归一化场景键：

```json
{
  "回家": {
    "preferred_car_type": "便宜点的，最近的司机",
    "userPreferLabels": [1],
    "from": "公司",
    "to": "家"
  },
  "去公司": {
    "preferred_car_type": "",
    "userPreferLabels": [],
    "from": "家",
    "to": "公司"
  }
}
```

## 2. 字段约束

| 字段 | 含义 | 约束 |
| --- | --- | --- |
| `preferred_car_type` | 偏好车型描述 | 可为空字符串；其余情况下必须是用户确认后的完整偏好描述 |
| `userPreferLabels` | 下单阶段偏好标签 | 必填，必须是整数数组；无偏好时传空数组 `[]` |
| `from` | 起点地址别名 | 必填，且必须能在 `addr.json` 中命中 |
| `to` | 终点地址别名 | 必填，且必须能在 `addr.json` 中命中 |

## 3. `userPreferLabels` 枚举说明

| 枚举值 | 含义 | 触发关键词示例 |
| --- | --- | --- |
| `1` | 接驾距离更近 | "附近的"、"近一点"、"最近的" |
| `2` | 接驾最快 | "最快的"、"快点来"、"尽快"、"5分钟内接驾" |
| `3` | 电车 | "电车"、"新能源"、"纯电" |
| `4` | 油车 | "油车"、"燃油车" |

约束：

- 可多选，无偏好时必须保存为空数组 `[]`。
- 仅保存枚举值，不保存自然语言描述。
- 禁止给用户透出标签编号，只在内部作为 `create-order --user-prefer-labels` 的参数来源。

## 4. 场景键规则

- key 必须是归一化后的场景键，例如 `回家`、`去公司`、`接孩子`。
- 同一场景键全局唯一，禁止重复。
- 未命中场景键时，必须进入快捷场景设置流程，禁止猜测。

## 5. 读写规则

1. 快捷叫车主流程必须先读取本文件，再按 `from` / `to` 到 `addr.json` 查找对应地址对象。
2. 新增或更新场景时，必须保证 `from` 与 `to` 在 `addr.json` 中都已存在。
3. 允许单独更新 `preferred_car_type` 或 `userPreferLabels`；若修改 `from` 或 `to`，必须按整条场景记录覆盖。
4. `userPreferLabels` 的值必须与 [打车主流程中的 `userPreferLabels` 定义](./takecar-workflow.md#userpreferlabels-参数说明) 保持一致。
5. 禁止将 `poi.name`、自然语言地址文本或经纬度直接写入本文件；本文件只保存地址别名引用和快捷偏好配置。
