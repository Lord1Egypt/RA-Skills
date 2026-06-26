# Key Metrics, Troubleshooting, Success Criteria & Tool Reference

Read this when setting team targets, diagnosing a sprint-analytics problem, checking whether coaching met its bar, or looking up the exact flags for any of the four Python tools.

## Key Metrics & Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Health Score | >80/100 | Sprint-level, 6 dimensions |
| Velocity Predictability (CV) | <20% | Rolling 6-sprint window |
| Commitment Reliability | >85% | Sprint goals achieved / attempted |
| Scope Stability | <15% change | Mid-sprint scope changes |
| Blocker Resolution | <3 days avg | Time from raised to resolved |
| Action Item Completion | >70% | Retro items done by next retro |
| Ceremony Engagement | >90% | Attendance + participation quality |
| Psychological Safety | >4.0/5.0 | Monthly pulse survey |

## Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|-------------|------------|
| Velocity drops for 2+ sprints without team change | Hidden scope creep, unclear definition of done, or tech debt accumulation | Run `sprint_health_scorer.py` to check scope stability score; tighten DoD and refinement process |
| CV exceeds 30% despite stable team | Inconsistent story sizing, mid-sprint scope injection, or unplanned absences | Analyze anomalies via `velocity_analyzer.py`; introduce reference stories for estimation calibration |
| Action item completion rate below 50% | Too many action items per retro, no owners assigned, or unrealistic scope | Cap new items at 2-3 per retro based on `retrospective_analyzer.py` historical completion data |
| Health score below 60 but team feels productive | Dimension weights may not match team context, or ceremony data is incomplete | Review dimension weights in HEALTH_DIMENSIONS config; ensure ceremony attendance data is populated |
| Monte Carlo forecast has wide confidence intervals | Insufficient historical data or high velocity volatility | Accumulate 6+ sprints of data; address root causes of volatility before relying on forecasts |
| Sprint capacity calculator overestimates | Focus factor set too high or ceremony overhead not calibrated | Adjust focus factor from 0.85 to 0.80; verify ceremony durations match actual team practices |
| Retrospective themes keep recurring across sprints | Systemic issues not addressed at root cause, or action items too superficial | Use `retrospective_analyzer.py` persistent issue detection; escalate recurring themes to management |

## Success Criteria

- Sprint health score consistently above 80/100 across 6-dimension assessment
- Velocity coefficient of variation (CV) maintained below 20% over rolling 6-sprint window
- Sprint commitment reliability exceeds 85% (completed vs. planned points)
- Action item completion rate from retrospectives exceeds 70% by next retro
- Blocker average resolution time under 3 working days
- Team maturity advances at least one Tuckman stage within 3-6 months of coaching
- Psychological safety score on Edmondson scale exceeds 4.0/5.0

## Tool Reference

### velocity_analyzer.py

Analyzes sprint velocity data with trend detection, Monte Carlo forecasting, and anomaly identification.

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `data_file` | positional | (required) | Path to JSON file containing sprint data |
| `--format` | choice | `text` | Output format: `text` or `json` |

### sprint_health_scorer.py

Scores sprint health across 6 weighted dimensions with composite grading and recommendations.

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `data_file` | positional | (required) | Path to JSON file containing sprint health data |
| `--format` | choice | `text` | Output format: `text` or `json` |

### retrospective_analyzer.py

Processes retrospective data to track action item completion, identify recurring themes, and assess team maturity.

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `data_file` | positional | (required) | Path to JSON file containing retrospective data |
| `--format` | choice | `text` | Output format: `text` or `json` |

### sprint_capacity_calculator.py

Calculates sprint capacity accounting for ceremony overhead, PTO, allocation percentages, and focus factor.

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `data_file` | positional | (optional) | Path to JSON file containing team capacity data |
| `--format` | choice | `text` | Output format: `text` or `json` |
| `--demo` | flag | off | Run with built-in sample data |
