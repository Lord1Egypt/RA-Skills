# mapping — 激光建图

## 能力
使用 Cartographer 进行激光 SLAM 建图，生成地图供后续导航使用。

## 启动
```bash
ros2launch xrrobot_bringup xrrobot_map_slam.launch.py
```

## 调用
```bash
# 保存当前建图结果
ros2launch xrrobot_bringup xrrobot_save_map.launch.py
```
保存后会生成 `.pgm` + `.yaml` 地图文件。

## 依赖
| 需求 | 说明 |
|------|------|
| launch | `xrrobot_map_slam.launch.py` |
| 前置 | 无（首次建图不需要已有地图） |
| 含底盘 | 本 launch 已包含 base + lidar，**不需要单独起** |

## 兼容性
| 可共存 | 说明 |
|--------|------|
| ✅ camera | 建图时也可以看画面 |

⚠️ 自身已包含 base + lidar，**不要重复启动**。
⚠️ 建图完成后记得 `save`，否则地图不写盘。
⚠️ 与 navigation 互斥——建图模式不能同时导航。
