# Domain Config for: [skill-name]

Fill this template when extracting domain from a target skill. Use the extracted values to parameterize LEARNINGS.md, ERRORS.md, FEATURE_REQUESTS.md, and EVOLUTION.md.

## Capability & Scenario Analysis (before extraction)

**Capabilities** (what the skill does):
- Primary outputs:
- Secondary/edge capabilities:
- Dependencies:

**Scenarios** (when and how it is used):
- User personas:
- Typical tasks:
- Input/output patterns:

**Evolution directions** (what can improve):
- User feedback patterns:
- Failure modes:
- Recurring corrections → domain rules:

---

## Domain

- **Name**: (human-readable domain name, e.g., 洗稿能手, 电脑加速)
- **Use cases**: (comma-separated scenarios, e.g., 科普、汇报、直播)
- **Areas**: (domain-specific areas for filtering, e.g., 文案 | 口播 | 短视频脚本)
- **Language**: (target language for generated files: zh | en)

## Learning Triggers (user feedback phrases)

Phrases that indicate user correction or style mismatch → log to LEARNINGS.md:

- "phrase1"
- "phrase2"
- "phrase3"

## Error Triggers (failure modes)

Situations that indicate operation failure → log to ERRORS.md:

- failure1
- failure2
- failure3

## Promotion Targets

Files to promote learnings to when they prove broadly applicable:

- **专属进化规则**: [skill-name]-专属进化规则.md
- **最佳实践 / 安全规范**: [skill-name]-最佳实践.md (or [skill-name]-安全规范.md)

## Domain Categories (optional)

If the skill needs categories beyond correction | insight | knowledge_gap | best_practice:

- category1
- category2

## Notes

- Use kebab-case for skill-name in file paths
- Areas should partition the skill's output/workflow scope
- Add 3+ learning triggers and 2+ error triggers for effective capture
- Storage: same as self-improving-agent — `.learnings/` directly (LEARNINGS.md, ERRORS.md, FEATURE_REQUESTS.md)
