# Domotics Issues Log

Recurring smart-home failures, rule conflicts, stale occupancy signals, unreachable devices, and safety-relevant incidents.

**Triggers**: monitoring_alert | user_report | regression | integration_update | schedule_miss
**Areas**: lighting | climate | security | access_control | energy | sensors | routines | voice_assistants | integrations | network
**Categories**: automation_conflict | sensor_drift | device_unreachable | integration_break | energy_optimization | safety_rule_gap | occupancy_mismatch | latency_jitter

## Status Definitions

| Status | Meaning |
|--------|---------|
| `pending` | Not yet addressed |
| `in_progress` | Actively investigated or mitigated |
| `resolved` | Root cause fixed and behavior verified |
| `wont_fix` | Explicitly accepted with rationale |
| `promoted` | Converted into durable playbook/matrix/rule/safety automation |
| `promoted_to_skill` | Extracted to reusable skill |

## Safety Reminder

This log is reminder/documentation only.
Do not execute physical actuator actions directly from logging workflows.
Require human confirmation for door locks, alarms, gas/water shutoff, and heaters.

---
