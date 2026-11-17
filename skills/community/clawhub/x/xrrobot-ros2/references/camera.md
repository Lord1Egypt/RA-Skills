# camera — 摄像头拍照

## 能力
拍摄当前画面并返回 JPEG 图像，供我（agent）分析画面中的物体、障碍物、环境等信息。

## 启动
```bash
ros2launch xrrobot_bringup xrrobot_camera.launch.py
```
启动后提供话题：`/camera/color/image_raw`

## 调用
```bash
# 先确认话题存在 publisher
{baseDir}/scripts/rosx ros2 topic info /camera/color/image_raw

# 再确认能收到一帧图像
timeout 2s {baseDir}/scripts/rosx ros2 topic echo /camera/color/image_raw --once

# 最后执行拍照验证
{baseDir}/scripts/rosx {baseDir}/scripts/xr-call capture --timeout 2.0
```
返回 base64 JPEG + 宽高 + 时效信息。

## 依赖
| 需求 | 说明 |
|------|------|
| 节点 | `/camera/color/image_raw` 有 publisher |
| launch | `xrrobot_camera.launch.py` |
| 前置 | 无（不依赖底盘、不依赖雷达） |

## 兼容性
| 可共存 | 说明 |
|--------|------|
| ✅ lidar | 不同节点，完全独立 |
| ✅ base | 可同时开底盘驱动 |
| ✅ navigation | 导航通常也需要看画面 |
| ✅ yolo | YOLO Studio 同用摄像头 |
| ✅ grasp | 视觉抓取需要摄像头 |

无互斥项。
