# roborock-cli 命令完整规格

## 目录

1. [auth — 交互式认证](#auth)
2. [devices — 列出设备](#devices)
3. [status — 设备状态](#status)
4. [map — 获取地图](#map)
5. [routines — 智能场景列表](#routines)
6. [start-clean — 开始清洁](#start-clean)
7. [stop-clean — 停止清洁](#stop-clean)
8. [pause-clean — 暂停清洁](#pause-clean)
9. [resume-clean — 恢复清洁](#resume-clean)
10. [go-home — 回充电座](#go-home)
11. [find-robot — 寻找机器人](#find-robot)
12. [dock-action — 基座操作](#dock-action)
13. [set-volume — 设置音量](#set-volume)
14. [set-dnd — 设置勿扰模式](#set-dnd)
15. [execute-routine — 执行场景](#execute-routine)

---

## auth

交互式认证，需要 TTY 终端。

```
roborock-cli auth [-h]
```

| 参数 | 说明 |
|------|------|
| `-h` | 显示帮助 |

无 JSON 输出（交互式命令）。

---

## devices

列出所有设备。不需要 `-d` 参数，不需要 V1 协议。

```
roborock-cli devices [-h]
```

**输出字段**：

| 字段 | 类型 | 说明 | 下游用途 |
|------|------|------|----------|
| `count` | int | 设备总数 | — |
| `devices[].name` | string | 设备名称 | → 所有命令的 `-d` 参数 |
| `devices[].duid` | string | 设备唯一 ID | — |
| `devices[].model` | string\|null | 设备型号 | — |
| `devices[].firmware` | string\|null | 固件版本 | — |

**输出示例**：
```json
{
  "count": 1,
  "devices": [
    {
      "name": "Pearl Plus V5",
      "duid": "1Nky7XEsNJn75gTGWtxiIs",
      "model": "roborock.vacuum.a86v5",
      "firmware": "02.34.02"
    }
  ]
}
```

---

## status

获取设备完整状态。并行刷新 8 个 trait，某个失败不影响其他。

```
roborock-cli status [-h] [-d DEVICE]
```

| 参数 | 说明 |
|------|------|
| `-d DEVICE` | 设备名称（模糊匹配） |

**输出字段分组**：

### 基本信息
| 字段 | 类型 | 说明 |
|------|------|------|
| `device_name` | string | 设备名称（唯一不含 value/description 包装的字段） |

### status trait（23 个字段）
| 字段 | 值类型 | 说明 |
|------|--------|------|
| `battery` | int | 电池电量 (%) |
| `charge_status` | int | 充电状态 (0=未充电, 1=充电中, 2=完成) |
| `clean_percent` | int | 清洁完成百分比 (%) |
| `in_cleaning` | string | 清洁状态 (complete/global_clean_not_complete/zone_clean_not_complete/segment_clean_not_complete) |
| `in_returning` | int | 是否返回途中 (0/1) |
| `avoid_count` | int | 当前任务避障次数 |
| `repeat` | int | 当前任务重复遍数 |
| `map_present` | int | 是否有地图 (0/1) |
| `dock_type` | string | 基座类型 (no_dock/auto_empty_dock/empty_wash_fill_dock/p10_pro_dock 等) |
| `dock_error_status` | string | 基座错误 (ok/duct_blockage/water_empty/waste_water_tank_full 等) |
| `dust_collection_status` | int | 集尘状态 (0=未集尘, 1=集尘中) |
| `auto_dust_collection` | int | 自动集尘开关 (0/1) |
| `wash_status` | int | 洗拖布状态 (0=空闲, 1=洗涤中) |
| `wash_phase` | int | 洗拖布阶段 (0=空闲) |
| `wash_ready` | int | 准备好洗拖布 (0/1) |
| `dry_status` | int | 烘干状态 (0=关闭, 1=烘干中) |
| `water_box_status` | int | 水箱安装 (0/1) |
| `water_box_carriage_status` | int | 水箱托架状态 |
| `water_shortage_status` | int | 缺水状态 |
| `is_locating` | int | 是否定位中 (0/1) |
| `lock_status` | int | 童锁 (0/1) |
| `mop_forbidden_enable` | int | 拖地禁区 (0/1) |
| `collision_avoid_status` | int | 避障功能 (0/1) |

### computed（7 个字段）
| 字段 | 值类型 | 说明 |
|------|--------|------|
| `state` | string | 设备状态（charging/idle/cleaning/error 等） |
| `error_code` | string | 错误状态（none=正常） |
| `clean_area_m2` | float | 清洁面积 (m²) |
| `clean_time_minutes` | float | 清洁时长（分钟） |
| `fan_speed_name` | string | 吸力档位 |
| `water_mode_name` | string | 拖布湿度 |
| `mop_route_name` | string | 拖地路线 |

### dss（3 个字段）
| 字段 | 值类型 | 说明 |
|------|--------|------|
| `clear_water_box_status` | string | 清水箱 (okay/out_of_water) |
| `dirty_water_box_status` | string | 污水箱 (okay/full) |
| `dust_bag_status` | string | 尘袋 (okay/full) |

### dnd trait（3 个字段）
| 字段 | 值类型 | 说明 |
|------|--------|------|
| `dnd_enabled` | bool | 勿扰模式开关 |
| `dnd_start_time` | string\|null | 勿扰开始 HH:MM（关闭时 null） |
| `dnd_end_time` | string\|null | 勿扰结束 HH:MM（关闭时 null） |

### clean_summary（5 个字段）
| 字段 | 值类型 | 说明 |
|------|--------|------|
| `total_clean_time_hours` | float | 累计清洁时长（小时） |
| `total_clean_area_m2` | float | 累计清洁面积 (m²) |
| `total_clean_count` | int | 累计清洁次数 |
| `last_clean_begin` | string | 最近清洁开始（ISO 8601）— 条件性字段 |
| `last_clean_end` | string | 最近清洁结束（ISO 8601）— 条件性字段 |

### sound_volume（1 个字段）
| 字段 | 值类型 | 说明 |
|------|--------|------|
| `volume` | int | 音量 (0-100) |

### rooms trait（2 个字段）
| 字段 | 值类型 | 说明 |
|------|--------|------|
| `room_count` | int | 房间数量 |
| `rooms` | array | `[{segment_id, iot_id, name}]` → segment_id 用于 start-clean -s |

### maps trait（2 个字段）
| 字段 | 值类型 | 说明 |
|------|--------|------|
| `current_map_flag` | int | 当前地图 ID |
| `maps` | array | `[{map_flag, name, is_current}]` |

### consumables（3 个字段）
| 字段 | 值类型 | 说明 |
|------|--------|------|
| `main_brush_hours` | float | 主刷使用时长（小时） |
| `side_brush_hours` | float | 边刷使用时长（小时） |
| `filter_hours` | float | 滤网使用时长（小时） |

> 每个字段格式统一为 `{"value": <值>, "description": "中文说明"}`，`device_name` 除外。

---

## map

获取地图元数据，可选保存 PNG。

```
roborock-cli map [-h] [-d DEVICE] [--save FILE]
```

| 参数 | 说明 |
|------|------|
| `-d DEVICE` | 设备名称 |
| `--save FILE` | 保存地图 PNG 到指定路径 |

**不含 `--save` 的输出字段**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `device_name` | string | 设备名称 |
| `image_size_bytes` | int | 图片大小 |
| `has_map_data` | bool | 是否有地图 |
| `vacuum_position.x/y` | int\|null | 扫地机位置（仅 has_map_data=true） |
| `charger_position.x/y` | int\|null | 充电座位置（仅 has_map_data=true） |

**含 `--save` 时**，输出包裹在 `{"saved": "路径", "metadata": {...}}` 中。

---

## routines

列出智能场景。

```
roborock-cli routines [-h] [-d DEVICE]
```

**输出字段**：

| 字段 | 类型 | 说明 | 下游用途 |
|------|------|------|----------|
| `device_name` | string | 设备名称 | — |
| `count` | int | 场景总数 | — |
| `routines[].id` | int | 场景 ID | → `execute-routine` 的参数 |
| `routines[].name` | string | 场景名称 | — |

---

## start-clean

开始清洁。

```
roborock-cli start-clean [-h] [-d DEVICE] [-s SEGMENTS [SEGMENTS ...]] [-r REPEAT]
```

| 参数 | 说明 |
|------|------|
| `-d DEVICE` | 设备名称 |
| `-s SEGMENTS [SEGMENTS ...]` | 房间 segment_id 列表（省略 = 全屋） |
| `-r REPEAT` | 清洁遍数（默认 1） |

**输出**：

- 全屋：`{"status": "ok", "action": "full_clean"}`
- 指定房间：`{"status": "ok", "action": "segment_clean", "segments": [16], "repeat": 2}`

**获取 segment_id**：`roborock-cli status -d DEV | jq '.rooms.value[].segment_id'`

---

## stop-clean

```
roborock-cli stop-clean [-h] [-d DEVICE]
```

输出：`{"status": "ok", "action": "stop"}`

---

## pause-clean

```
roborock-cli pause-clean [-h] [-d DEVICE]
```

输出：`{"status": "ok", "action": "pause"}`

---

## resume-clean

```
roborock-cli resume-clean [-h] [-d DEVICE]
```

输出：`{"status": "ok", "action": "resume"}`

> 底层发送 APP_START 命令，在暂停状态下等同于恢复当前任务。

---

## go-home

回充电座。

```
roborock-cli go-home [-h] [-d DEVICE]
```

输出：`{"status": "ok", "action": "go_home"}`

---

## find-robot

让扫地机发出"滴滴"提示音，帮助用户通过声音定位机器人。不返回位置坐标（位置坐标在 `map` 命令的 `vacuum_position` 中）。受 `set-volume` 影响——音量为 0 时听不到。

```
roborock-cli find-robot [-h] [-d DEVICE]
```

输出：`{"status": "ok", "action": "find_robot"}`

---

## dock-action

基座操作：集尘/洗拖布。

```
roborock-cli dock-action [-h] [-d DEVICE] {start_collect_dust,stop_collect_dust,start_wash,stop_wash}
```

| 参数 | 说明 |
|------|------|
| `action`（位置参数，必填） | 四选一：start_collect_dust / stop_collect_dust / start_wash / stop_wash |
| `-d DEVICE` | 设备名称 |

输出：`{"status": "ok", "action": "<所选动作>"}`

---

## set-volume

设置音量。

```
roborock-cli set-volume [-h] [-d DEVICE] volume
```

| 参数 | 说明 |
|------|------|
| `volume`（位置参数，必填） | 整数 0-100 |

输出：`{"status": "ok", "volume": 50}`

超出 0-100 范围 → exit_code=4。

---

## set-dnd

设置勿扰模式。

```
roborock-cli set-dnd [-h] [--start START] [--end END] [-d DEVICE] {enable,disable}
```

| 参数 | 说明 |
|------|------|
| `action`（位置参数，必填） | enable 或 disable |
| `--start START` | 开始时间 HH:MM（enable 时必需） |
| `--end END` | 结束时间 HH:MM（enable 时必需） |

**enable 示例**：
```bash
roborock-cli set-dnd enable --start 22:00 --end 08:00
```
输出：`{"status": "ok", "action": "enable", "time": "22:00-08:00"}`

**disable 示例**：
```bash
roborock-cli set-dnd disable
```
输出：`{"status": "ok", "action": "disable"}`

约束：enable 时 `--start` 和 `--end` 都必须提供，时间范围 0-23:0-59。

---

## execute-routine

执行智能场景。

```
roborock-cli execute-routine [-h] [-d DEVICE] routine_id
```

| 参数 | 说明 |
|------|------|
| `routine_id`（位置参数，必填） | 场景 ID（从 `routines` 命令获取） |

输出：`{"status": "ok", "routine_id": 13258044}`

**获取 routine_id**：`roborock-cli routines -d DEV | jq '.routines[].id'`
