# lidar — 激光雷达

## 能力
获取当前激光雷达扫描数据：最近障碍物距离、扫描范围、光束数等。

## 启动
```bash
ros2launch xrrobot_bringup xrrobot_lidar.launch.py
```
启动后提供话题：`/scan`

## 调用
```bash
{baseDir}/scripts/rosx {baseDir}/scripts/xr-call scan --timeout 1.0
```
返回 `closest_range`（最近障碍物）、`beam_count`、`angle_span_deg` 等。
或直接用 ros2 看原始数据：
```bash
ros2 topic echo /scan --once --no-arr
```

## 依赖
| 需求 | 说明 |
|------|------|
| 节点 | `/scan` 有 publisher |
| launch | `xrrobot_lidar.launch.py` |
| 前置 | 无 |

## 兼容性
| 可共存 | 说明 |
|--------|------|
| ✅ base | 独立 |
| ✅ camera | 独立 |
| ✅ yolo | 独立 |
| ✅ grasp | 独立 |

⚠️ navigation 和 mapping 自带 lidar，不需要单独启动。
