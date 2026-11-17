# lanekeeping — 车道保持/巡线

## 能力
基于 OpenCV 的 HSV 颜色识别巡线，在跑道地图中自动沿着车道行驶。

## 启动
```bash
ros2launch xrrobot_lanekeeping xrrobot_lanekeeping.launch.py
```

## 调用
Web 界面：浏览器访问 `http://<机器人IP>:8765`
1. 看 HSV 掩膜窗口是否显示正确（黑线为白色，其余黑色）
2. 如效果不佳，调整 HSV 滑块或点击"室内暗光/室外强光"补偿
3. 点击"开始跟线"

## 依赖
| 需求 | 说明 |
|------|------|
| launch | `xrrobot_lanekeeping.launch.py` |
| 前置 | 需要摄像头在线 |
| 含 | 底盘+摄像头（全包） |

## 兼容性
| 可共存 | 说明 |
|--------|------|
| ❌ 其他占用底盘的 | 巡线独占底盘控制 |

⚠️ 独占底盘，不能和 navigation、manual move 等同时用。
