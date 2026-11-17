# Changelog

## 1.1.0 — 2026-10-05

### Added
- 功能四：课件PPT大纲（`generate_slides_outline`）
- 功能五：说课稿，含评委追问预案（`generate_lesson_talk`）
- 学段自适应：小学 / 初中 / 高中 / 高职 / 本科 / 研究生；中小学按新课标核心素养表述目标
- SKILL.md 补齐 ClawHub / SkillHub 发布字段：`slug`、`displayName`、`summary`、`license`、`homepage`、`user_invocable`、`metadata.openclaw`
- 输出原则：以用户提供的教材为准，不编造页码；事实性内容不确定时标注"请核对"

### Fixed
- 教学环节时间分配：正确识别 `分钟` / `小时` / `学时` / `课时` / 小数 / 中文数字（原来 `2小时` 被当成 90 分钟、`1.5小时` 被当成 45 分钟）
- 小学按 40 分钟/课时计算
- OpenWebUI 未传 `__user__` 或 valves 为 dict 时不再报错
- 出题数量下限保护
- `__user__` 可变默认参数改为 `None`

## 1.0.0 — 2026-03-16
- 首个版本：教案、智能出题、课程大纲
