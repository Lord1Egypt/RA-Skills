# xbot-camera-qc-pro
xbot.coffee Lite 无人咖啡机 · 视觉质检专业技能

## Overview
本技能适用于 OpenClaw / ClawBot 智能体，用于对 xbot.coffee Lite 无人咖啡机的摄像头抓拍图片进行**自动化异常检测**，输出标准化 JSON 结果，可直接对接业务系统、告警平台与运维 API。

## 检测范围
- 饮品容量与出品质量（偏少、溢出、异物、杯外泼洒）
- 主屏幕运行状态（亮屏 / 黑屏关机）
- 工作台清洁度（泼洒、水渍、咖啡渍、垃圾）
- 双机械臂姿态与运行状态
- 设备外观污损、残留
- 整体环境整洁度
- 虫害检测（老鼠、蟑螂）

## 输出格式
返回**纯英文结构化 JSON**，无多余文本，便于后端直接解析、判断异常与推送告警。

```json
{
  "drink_status": "normal|insufficient|overflow|foreign_object|spill_outside",
  "screen_status": "normal|off",
  "table_clean": "normal|dirty",
  "robot_arm": "normal|abnormal",
  "equipment_dirty": "normal|dirty",
  "environment_clean": "normal|messy",
  "pest": "none|found",
  "has_anomaly": true|false,
  "alert_msg": "string"
}
```

## 适用场景
- 200+ 台设备规模化巡检
- 每日大批量图片自动质检
- 异常实时告警与运维派单
- API 对接、数据上报、可视化大屏

## 使用方式
1. 在 OpenClaw 中安装本技能
2. 传入咖啡机摄像头抓拍图片
3. 技能自动分析并返回 JSON 结果
4. 后端根据 `has_anomaly` 触发告警或业务逻辑

## License
MIT