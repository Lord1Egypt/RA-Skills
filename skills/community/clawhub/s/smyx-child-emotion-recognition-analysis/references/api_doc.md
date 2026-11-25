# API 接口文档

此处用于存放儿童情绪波动识别（哭闹/暴躁/低落）API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动儿童情绪识别任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果与情绪分类
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史情绪记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_CHILD_EMOTION_RECOGNITION_ANALYSIS` - 儿童情绪波动识别（哭闹/暴躁/低落）

## 输入约束

- 推荐视频清晰展示儿童面部（正面或侧脸），帧率 ≥ 15 FPS
- 如需音频通道（哭声分析），上传带音频的 mp4/mov
- 摄像头建议覆盖家庭客厅、儿童房或幼儿园活动区

## 多模态特征

- 视觉：面部表情（眉眼形态、嘴角弧度）、肢体动作幅度（挥手 / 跺脚 / 蜷缩）
- 听觉（可选）：哭声音调、频率、持续时间
- 时序：情绪持续时长、波动频次

## 情绪类别枚举

- `happy` - 快乐
- `calm` - 平静
- `sad` - 悲伤 / 低落
- `angry` - 愤怒 / 暴躁
- `fear` - 恐惧 / 害怕
- `cry` - 哭闹
- `surprise` - 惊讶

## 输出字段（参考）

- `child_detected` - 是否检测到儿童
- `dominant_emotion` - 主导情绪类别
- `emotion_confidence` - 主导情绪置信度
- `emotion_intensity` - 情绪强度（low / medium / high）
- `secondary_emotions` - 其他次要情绪及概率
- `duration_sec` - 当前情绪持续秒数
- `negative_emotion_alert` - 负面情绪预警（愤怒/恐惧/悲伤/哭闹超阈值）
- `soothing_hint` - 安抚提示文案（如"宝宝看起来害怕，请抱抱他"）

> 仅输出基于多模态特征的情绪分类结果与安抚提示，不提供心理诊断或临床建议。
