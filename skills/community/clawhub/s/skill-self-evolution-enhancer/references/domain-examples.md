# Domain Examples

Concrete examples for extracting domain config and generating evolution scaffolding. Use these as reference when enhancing skills.

---

## Example 1: 洗稿能手 (Content Rewriting Skill)

**Domain**: 文案 / 口播 / 短视频脚本改写

### Capability & Scenario Analysis

- **Capabilities**: Rewrite text for different formats (文案, 口播, 短视频); adapt style by scene (科普, 汇报, 直播)
- **Scenarios**: User provides source text; requests rewrite for specific format/scene; may correct style
- **Evolution directions**: User feedback on style ("不通顺", "不像口播") → learn scene-specific preferences; recurring corrections → promote to 专属进化规则

### Domain Config

```markdown
## Domain
- Name: 洗稿能手
- Use cases: 科普, 汇报, 直播, 短视频脚本, 口播稿
- Areas: 文案 | 口播 | 短视频脚本 | 科普 | 汇报 | 直播
- Language: zh

## Learning Triggers
- "改得不通顺"
- "不像口播"
- "风格不对"
- "太书面了"
- "读起来不顺"
- "语气不对"

## Error Triggers
- 改写后用户多次要求重改
- 风格与场景不匹配（如科普写成汇报风）
- 口播稿读起来拗口

## Promotion Targets
- 洗稿能手-专属进化规则.md
- 洗稿能手-最佳实践.md
```

### Generated EVOLUTION.md Quick Reference

| Situation | Action |
|-----------|--------|
| 用户说"改得不通顺" | Log to `.learnings/LEARNINGS.md` with category `style_mismatch` |
| 用户说"不像口播" | Log to `.learnings/LEARNINGS.md` with category `scene_adaptation` |
| 用户说"风格不对" | Log to `.learnings/LEARNINGS.md` with category `correction` |
| 改写后多次重改 | Log to `.learnings/ERRORS.md` |
| 风格与场景不匹配 | Log to `.learnings/LEARNINGS.md` with area 科普/汇报/直播 |

### Domain Categories

- correction
- style_mismatch
- scene_adaptation
- best_practice
- knowledge_gap

### Activation Conditions

- User says "改得不通顺", "不像口播", "风格不对"
- User requests rewrite for a specific scene (科普/汇报/直播)

---

## Example 2: 电脑加速 (PC Optimization Skill)

**Domain**: Windows 优化 / 卡慢 / 卡顿

### Capability & Scenario Analysis

- **Capabilities**: System optimization, startup speed, memory release; diagnose slowdowns
- **Scenarios**: User reports slow PC; agent suggests optimizations; some may fail or cause issues
- **Evolution directions**: "优化无效", "某些电脑不适用" → learn environment-specific solutions; safety issues → promote to 安全规范

### Domain Config

```markdown
## Domain
- Name: 电脑加速
- Use cases: 系统优化, 卡顿排查, 启动加速, 内存释放
- Areas: 系统优化 | 卡顿 | 报错 | 兼容性 | 安全
- Language: zh

## Learning Triggers
- "优化无效"
- "某些电脑不适用"
- "这样改有问题"
- "上次的方法不行"

## Error Triggers
- 优化后系统报错
- 某些电脑/系统版本不适用
- 操作导致异常或蓝屏
- 命令执行失败

## Promotion Targets
- 电脑加速-安全规范.md
- 电脑加速-最佳实践.md
```

### Generated EVOLUTION.md Quick Reference

| Situation | Action |
|-----------|--------|
| 用户说"优化无效" | Log to `.learnings/ERRORS.md` with area 系统优化 |
| 用户说"某些电脑不适用" | Log to `.learnings/LEARNINGS.md` with category `knowledge_gap` |
| 优化后报错 | Log to `.learnings/ERRORS.md` with area 报错 |
| 发现安全风险 | Log to `.learnings/LEARNINGS.md`, promote to 电脑加速-安全规范.md |

### Domain Categories

- correction
- knowledge_gap
- best_practice
- safety_constraint

### Activation Conditions

- User reports "优化无效", "报错", "某些电脑不适用"
- After suggesting optimization steps

---

## Extraction Tips

1. **Sparse skills**: If the target skill has little content, infer from the name and description. Add generic triggers like "用户纠正", "操作失败".
2. **Coding skills**: Use areas like frontend | backend | infra if the skill is coding-related; otherwise use domain-specific areas.
3. **Safety-critical domains** (e.g., 电脑加速): Always include a 安全规范 promotion target.
4. **Style domains** (e.g., 洗稿能手): Include style_mismatch, scene_adaptation categories.
5. **Language**: Infer from SKILL.md; generate all output in that language.
