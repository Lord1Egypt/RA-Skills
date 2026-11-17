# INDEX.md 模板

场景索引表。状态值：COMPLETED / ACTIVE / LOCKED。

> **状态列仅为展示**——当前场景唯一权威源是 `world_state.yaml` 顶层第一行 `焦点场景`（短 ID，如 `S04`）。
> 场景切换时必须同步：world_state.焦点场景（权威）+ 本表 ACTIVE 行（展示）。validate 会核对两者一致。

| ID | 场景名称 | 类型 | 基准时间 | 出场 | 状态 |
|----|------|------|------|------|------|
| [SXX，递增] (例: S01) | [场景名] (例: Welcome Center) | [INT/EXT] (例: INT) | [第N日 HH:MM] (例: 第1日 07:20) | [角色名，逗号分隔] (例: Guest, Angela) | [COMPLETED/ACTIVE/LOCKED] (例: COMPLETED) |
| [SXX] (例: S02) | [场景名] (例: 甜水镇主街) | [INT/EXT] (例: EXT) | [第N日 HH:MM] (例: 第1日 09:00) | [角色名，逗号分隔] (例: Dolores, Teddy) | [COMPLETED/ACTIVE/LOCKED] (例: ACTIVE) |

存入 `{世界名}/scenes/INDEX.md`。
