# 内部控制属性映射

实际可用属性以 `deviceModels[device.model]` 为准。若属性未出现在能力定义中，不得下发。

## 开关

`open` 使用整数：`1` = 开，`0` = 关。

## 灯具

| 属性 | 范围 | 说明 |
| --- | --- | --- |
| `open` | `1` / `0` | 开/关 |
| `brightness` | 0–100 | 亮度 |
| `colorTemperature` | 2700–6500 | 色温，仅能力存在时使用 |
| `h` | 0–360 | 色相，仅彩光能力存在时使用 |
| `s` | 0–100 | 饱和度 |
| `l` | 0–100 | 明度 |

## 窗帘

| 属性 | 范围 | 说明 |
| --- | --- | --- |
| `open` | `true` / `false` | `true` = 全开，`false` = 全关（布尔值，非整数） |
| `position` | 0–100 | 开合度，0=全关，100=全开 |
| `shadePosition` | 0–100 | 遮光度，仅 `curtain_shade` 使用 |

注意：窗帘的 `open` 使用布尔值 `true`/`false`，与灯具/开关的整数 `1`/`0` 不同。也可以直接用 `position` 控制开合度。

一条 command 只放一个窗帘动作；多个动作拆成多条 command。

## 空调

| 属性 | 范围 | 说明 |
| --- | --- | --- |
| `open` | `1` / `0` | 开/关 |
| `targetTemp` | 16–30 | 设定温度 |
| `mode` | `auto` / `cool` / `heat` / `dry` / `fan` | 模式 |
| `fanSpeed` | `auto` / `low` / `medium` / `high` | 风速 |
| `tempDelta` | -14–14（非 0） | 温度增量 |
| `fanSpeedDelta` | -1 或 1 | 风速增量 |

绝对设置不能和增量设置放在同一条 command。`tempDelta` 和 `fanSpeedDelta` 也要拆成两条 command。

## 已有场景

使用同步结果中的场景 ID，`model` 固定为 `scene`，不要发送 `properties`。

## 翻译映射

空调模式：`auto`=自动、`cool`=制冷、`heat`=制热、`dry`=除湿、`fan`=送风。

风速：`auto`=自动风、`low`=低风、`medium`=中风、`high`=高风。
