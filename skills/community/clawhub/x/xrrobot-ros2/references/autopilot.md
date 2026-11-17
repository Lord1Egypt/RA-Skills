# autopilot — 视觉自动驾驶

## 能力
使用神经网络模型进行视觉自动驾驶（端到端），在跑道上自动循迹行驶。

## 启动
```bash
# 三轮车流程
# 1. 采集数据
ros2launch xrrobot_autopilot xrrobot_autopilot_collect.launch.py
# 2. 训练模型（耗时取决于主机计算性能）
ros2launch xrrobot_autopilot xrrobot_autopilot_train.launch.py
# 3. 自动驾驶运行
ros2launch xrrobot_autopilot xrrobot_autopilot_drive.launch.py
```

已有预训练模型位置：
```
~/xrrobot_autopilot/models/default/autopilot_model.keras
```

## 调用
直接启动 drive launch 即可，机器人自动在跑道上跑圈。

## 依赖
| 需求 | 说明 |
|------|------|
| launch | `xrrobot_autopilot_drive.launch.py` |
| 前置 | 需要已有训练好的模型 |
| 含 | 摄像头、底盘（全包） |

## 兼容性
| 可共存 | 说明 |
|--------|------|
| ❌ 任何其他 | 自动驾驶独占底盘+摄像头资源 |

⚠️ 独占模式，不能与其他能力共存。先 `ros2kill` 再启动。
