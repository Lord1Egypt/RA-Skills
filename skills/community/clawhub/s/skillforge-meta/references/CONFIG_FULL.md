# SkillForge — Full Configuration Reference

> 配置文件路径：`{workspace}/.workbuddy/skillforge/config.yaml`
> 大部分参数使用默认值即可，只需调整你关心的部分。

```yaml
# SkillForge 配置文件
# 路径: {workspace}/.workbuddy/skillforge/config.yaml

# ═══════════════════════════════════════════
# Scout 引擎参数
# ═══════════════════════════════════════════
scout:
  lookback_days: 14                  # 回溯多少天的 daily log
  max_fingerprints_per_day: 20       # 每天最多提取多少个操作指纹
  min_step_count: 2                  # 少于多少步的操作不提取

  similarity_weights:
    intent: 0.40
    domain: 0.15
    tools: 0.25
    keywords: 0.20

  similarity_threshold: 0.65         # 相似度 ≥ 此值归为同一模式
  min_cluster_size: 3                # 一个簇至少多少个指纹才算"重复模式"
  strong_time_window: 7              # 强信号时间窗口（天）

  strong_repeat_keywords:
    - "每次都"
    - "又要"
    - "老流程"
    - "照旧"
    - "老样子"
    - "重复做"
    - "always"
    - "again"

  weak_signal_threshold: 3

  ftrvo:
    strong_recommend: 20
    recommend: 15
    observe: 10

# ═══════════════════════════════════════════
# Smith 引擎参数
# ═══════════════════════════════════════════
smith:
  relevance_weights:
    keyword_overlap: 0.35
    domain_match: 0.15
    trigger_overlap: 0.25
    tool_overlap: 0.25

  merge_threshold: 0.70
  ask_user_threshold: 0.40

  skill_name_max_length: 30
  description_max_length: 200
  min_trigger_keywords: 3
  max_trigger_keywords: 10
  min_workflow_steps: 3
  max_workflow_steps: 15
  min_examples: 1
  max_examples: 3

  max_changes_per_merge: 5
  preserve_existing_behavior: true
  max_regen_attempts: 2
  readability_threshold: 0.70

  drafts_dir: "skillforge-drafts"

# ═══════════════════════════════════════════
# Sensei 引擎参数
# ═══════════════════════════════════════════
sensei:
  usage_lookback_days: 30
  zombie_threshold_days: 30
  small_skill_threshold: 2
  drift_sample_size: 5
  drift_warning_threshold: 0.30
  min_usage_for_satisfaction: 3

  health_weights:
    usage_freq: 0.30
    coverage: 0.20
    drift: 0.25
    satisfaction: 0.25

  health_thresholds:
    green: 4.0
    yellow: 3.0
    orange: 2.0

  archive_dir: "~/.workbuddy/skills-archive"

# ═══════════════════════════════════════════
# 通用参数
# ═══════════════════════════════════════════
general:
  auto_scan_enabled: true
  auto_scan_rrule: "FREQ=WEEKLY;BYDAY=FR;BYHOUR=17;BYMINUTE=0"
  realtime_detection: true
  realtime_min_steps: 3
  report_format: "markdown"
  max_patterns_per_report: 10
  never_auto_install: true
  never_delete_skills: true
  privacy_no_raw_quotes: true
```
