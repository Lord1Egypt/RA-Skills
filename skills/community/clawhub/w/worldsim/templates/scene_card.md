# scene_card.md 模板

创建新场景时复制此模板，用实际内容替换方括号与示例。

| 字段 | 内容 |
|------|------|
| 场景ID | [SXX，递增] (例: S02) |
| 场景名 | [中文名] (例: 档案室) |
| 区域 | [regions/ 完整路径·引擎层·目录树同名节点必配] (例: regions/Westworld Park 1/Mesa Hub/Welcome Center/REGION.md) |
| 类型(INT/EXT) | [INT = 室内 / EXT = 室外] (例: INT) |
| 基准时间 | [第N日 HH:MM] (例: 第1日 08:00) |
| 出场角色 | [具名角色名(PC/状态)，逗号分隔] (例: Guest(PC), Angela, Sheriff(背景角色)) |
| 焦外/在场 | [具名焦外角色及其位置；REGION.常驻NPC 按当前时刻时间线命中本场者必列此处或出场角色；仅无 CHAR_.md 的纯背景可不列] (例: Robert Ford(Mesa Hub 办公室·未出场)) |
| 场景目标 | [一句话目标] (例: Angela 完成灰帽游客的过渡引导) |
| 前情钩子 | [为什么角色来到这里] (例: Guest 刚走完入境流程——Welcome to Westworld) |

存入 `{世界名}/scenes/{场景ID}-{场景名}/scene_card.md`。
