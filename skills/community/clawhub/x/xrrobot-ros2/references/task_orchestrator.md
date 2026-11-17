# task_orchestrator — 任务编排器

## 能力
可视化多步任务工作流编排。支持导航→识别→抓取→放置等组合工序。

## 启动
```bash
# 需要先启动导航+底盘作为基础环境
ros2launch xrrobot_bringup xrrobot_map_navigation.launch.py
ros2launch xrrobot_bringup xrrobot_base.launch.py

# 另开终端启动编排器
ros2launch xrrobot_task_orchestrator xrrobot_task_orchestrator.launch.py
```

## 调用
Web 界面：浏览器访问 `http://<机器人IP>:8796`
- 左侧：编辑导航点位（将机器人驱动到目标点→读取位置→保存）
- 中间：工作流编辑器，拖拽编排步骤
- 右侧：播放/测试/实机运行工作流

## 依赖
| 需求 | 说明 |
|------|------|
| launch | `xrrobot_task_orchestrator.launch.py` |
| 前置 | 导航 + 抓取 都需要提前启动 |
| 需要 | 已有建图好的地图 |

## 兼容性
| 可共存 | 说明 |
|--------|------|
| ✅ navigation | 编排器依赖导航 |
| ✅ base | 编排器需要底盘 |
| ✅ grasp | 编排器可以调度抓取 |
| ✅ camera | 编排器需要视觉反馈 |
