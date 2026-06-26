# API 接口文档

此处用于存放婴幼儿哭声原因分类 API 的接口文档，待后续补充。

## 接口规范

- 基础地址：由 smyx_common 配置统一管理
- 认证方式：API Key 鉴权
- 响应格式：JSON

## 主要接口

1. `/web/health-analysis/v2/start-health-analysis` - 启动婴儿哭声原因分类任务
2. `/web/health-analysis/v2/get-health-analysis-result` - 获取分析结果与最可能原因
3. `/web/health-analysis/page-health-analysis-result` - 分页查询历史哭声分析记录
4. `/health/order/api/getReportDetailExport?id={id}` - 导出完整报告

## 场景代码

- `SMYX_INFANT_CRY_CAUSE_CLASSIFICATION_ANALYSIS` - 婴幼儿哭声原因分类

## 输入约束

- 推荐采样率 ≥ 16 kHz、单声道 PCM/AAC，时长建议 3-30 秒
- 支持 wav / mp3 / m4a / aac / opus 等常见音频格式，也支持带音频的 mp4/mov
- 录音环境建议尽量减少背景噪音（电视、对话等）

## 提取的声学特征

- 基频（F0 / pitch）
- 共振峰（formant F1-F3）
- 能量包络（energy envelope）
- 哭声/停顿持续时间
- 节奏与间隔模式（rhythm / interval pattern）
- 谱质心 / MFCC 等

## 哭声原因类别

- `hunger` - 饥饿
- `sleepy` - 困倦
- `pain_discomfort` - 疼痛 / 不适（如尿布湿、肚子胀）
- `boredom_need_attention` - 无聊 / 需要安抚
- `fear` - 恐惧
- `colic` - 肠绞痛（特殊高频长哭）
- `unknown` - 不明（置信度偏低时）

## 输出字段（参考）

- `cry_detected` - 是否检测到婴儿哭声（与非哭声噪音区分）
- `dominant_cause` - 最可能的哭声原因类别
- `confidence` - 主原因置信度
- `secondary_causes` - 次要原因及概率列表
- `cry_duration_sec` - 哭声持续秒数
- `audio_features_summary` - 关键声学特征摘要
- `suggestion_hint` - 行动建议提示（如"宝宝可能是饿了，建议喂奶"）

> 仅输出基于声学特征的分类结果与方向性安抚提示，不提供医疗诊断或临床建议。若婴儿持续哭闹超过常态或伴随发热、呕吐等症状，请及时就医。
