# vision — 视觉面板（MediaPipe）

## 能力
通过 MediaPipe 和 OpenCV 提供多种视觉功能：
- 人体骨架/姿态检测
- 手部跟随
- 人脸关键点检测
- ArUco 码识别
- 边缘检测
- HSV 调参
- 颜色识别追踪
- 人脸追踪

## 启动
```bash
ros2launch xrrobot_vision vision_dashboard.launch.py
```

## 调用
Web 界面：浏览器访问 `http://<机器人IP>:8792`
顶部菜单切换不同视觉模式。

## 依赖
| 需求 | 说明 |
|------|------|
| launch | `vision_dashboard.launch.py` |
| 前置 | 需要摄像头在线 |

## 兼容性
| 可共存 | 说明 |
|--------|------|
| ✅ 任何不独占摄像头的 | 视觉面板只是上层分析，不控制底层 |
