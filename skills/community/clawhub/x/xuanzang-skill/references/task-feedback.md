# 任务完成反馈

> 本文件由 SKILL.md 引用。定义每次主要任务交付后的两步反馈收集与脱敏规则。

## 反馈流程

每次主要任务交付后，执行两步反馈收集，为自进化协议提供闭环数据。

### 第一步：紧箍咒体验评分

向用户发起单选询问：

```
AskUserQuestion:
  question: "本次紧箍咒体验如何？"
  options:
    - "紧箍咒到位 — 压力适中，有效推动了交付"
    - "一般 — 有感觉但没明显帮助"
    - "没感觉 — 紧箍咒形同虚设"
```

### 第二步：Session 分享确认

询问用户是否可将本次 session 脱敏后分享：

```
AskUserQuestion:
  question: "是否允许将本次 session 脱敏后上传？"
  options:
    - "是，脱敏后分享（仅保留任务类型和失败模式分类，不含具体代码/文件名）"
    - "否，不分享"
```

## 本地记录格式

反馈写入 `data/feedback.jsonl`（首次使用时自动创建）。session_id 使用 Python uuid4 或等价方法生成，格式为 32 位十六进制带连字符。

```json
{
  "timestamp": "ISO 8601 时间戳",
  "session_id": "<uuid4 生成的 UUID>",
  "role": "当前角色",
  "task_type": "Debug/构建/审查/调研/架构/其他",
  "rating": "到位|一般|没感觉",
  "share_consent": true|false,
  "pressure_level_peak": "L0-L4 峰值",
  "failure_count": 0,
  "task_completed": true|false
}
```

## 脱敏规则

- **保留**：任务类型分类、失败模式分类、压力等级变化、角色使用统计
- **移除**：具体文件路径（仅保留扩展名统计）、代码片段、API Key/Token、公司/项目名称、任何用户可识别信息
- session 分享脱敏走 `scripts/sanitize-session.py` 自动处理
