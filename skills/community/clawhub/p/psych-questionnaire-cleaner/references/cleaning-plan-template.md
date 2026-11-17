# Cleaning plan template

Read this file when no complete cleaning protocol is supplied or when converting a protocol/codebook into an executable plan. Copy the template into the run output and replace placeholders with evidence-backed values. Omit sections that do not apply.

Do not treat the example values below as defaults.

```yaml
study:
  title: "<study name>"
  protocol_source: "<path, URL, preregistration, or user instruction>"
  analysis_unit: "<participant | session | response>"
  timezone: "<if timestamps are used>"

inputs:
  files:
    - path: "<input file>"
      table_or_sheet: "<sheet/table or null>"
  preserve_raw: true

identity:
  row_key: "<stable row key to create or existing key>"
  participant_id: "<column or null>"
  session_id: "<column or null>"
  duplicate_policy: "flag_only"
  duplicate_tiebreaker: null

privacy:
  direct_identifiers: []
  quasi_identifiers: []
  report_aggregation_only: true
  pseudonymization: "<none | salted_hash | project-specific method>"

missing_values:
  global_tokens: []
  per_column: {}
  structural_missing_rules: []

items:
  - name: "<column name>"
    scale: "<scale or null>"
    subscale: "<subscale or null>"
    valid_min: "<number>"
    valid_max: "<number>"
    reverse_keyed: false
    missing_tokens: []
    source: "<manual/codebook location>"

scoring:
  - score_name: "<derived score>"
    items: []
    method: "<sum | mean>"
    min_answered: "<count or null>"
    max_missing_fraction: "<fraction or null>"
    prorating: "<none or exact declared rule>"
    source: "<manual/codebook location>"

quality_indicators:
  completion_time:
    enabled: true
    duration_column: "<required duration column>"
    median_scope: "all parseable, finite, positive durations in the analysis cohort before exclusions"
    lower_rule: "duration >= median(duration) / 3"
    upper_rule: "duration <= median(duration) * 3"
    action: "exclude"
    rule_status: "confirmed"
  longstring:
    enabled: false
    ordered_items: []
    threshold: null
    action: "flag_only"
  within_person_variability:
    enabled: false
    items: []
    threshold: null
    action: "flag_only"
  attention_checks:
    enabled: true
    checks: []
    combined_rule: "any non-missing response mismatches its declared acceptable answer"
    mismatch_action: "exclude"
    missing_or_unparseable_action: "flag_only"
    rule_status: "confirmed"
  regular_response:
    enabled: true
    ordered_item_groups: []
    detect_longstring: true
    detect_repeating_cycle: true
    repeating_cycle_lengths: [2, 3, 4]
    detect_strict_monotonic_run: true
    min_run_length: 4
    action: "flag_only"
  missingness:
    enabled: true
    items: []
    threshold: null
    action: "flag_only"

exclusions:
  approved: false
  rules: []
  sensitivity_variants: []

outputs:
  format: "<csv | xlsx | parquet | preserve input format>"
  output_directory: "<new directory>"
  language: "zh-CN"
  rename_output_columns_to_chinese: true
  preserve_original_column_name_map: true
  include_item_level_cleaned_values: true
  include_flags: true
  include_exclusion_records: true
  include_audit_log: true
  include_quality_report: true
```

## Rule status

For every rule, record one of:

- `confirmed`: directly supported by the user, protocol, manual, or codebook;
- `structural`: mechanically verifiable and non-interpretive;
- `proposed`: useful but requires approval before it changes or excludes data;
- `disabled`: considered but not used.

Also record `source`, `reason`, and `action` (`report`, `flag`, `transform`, `exclude`, or `score`).

## Critical questions

Pause scoring or exclusion, but continue auditing, when any of these are unknown:

- Which columns are scale items versus metadata or attention checks?
- What are the valid response bounds and reverse-keyed items?
- How are subscales and total scores computed?
- Which missing codes have meanings distinct from item nonresponse?
- What is the unit of duplicate resolution and the tie-breaking rule?
- Which response-quality thresholds were preregistered or approved?
