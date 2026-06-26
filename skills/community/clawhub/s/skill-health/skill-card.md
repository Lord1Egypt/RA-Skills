## Description: <br>
Analyze wearable health CSV exports (steps, heart rate, sleep, calories, SpO2, exercise, distance) and produce compact JSON reports for hourly, daily, weekly, monthly, sleep (last 30h) and cross-temporal alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[javiersgjavi](https://clawhub.ai/user/javiersgjavi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and health-data analysts use this skill to run local analyses over wearable CSV exports and produce compact hourly, daily, weekly, monthly, sleep, and cross-temporal alert reports. The outputs help explain metric semantics, data quality, and caveats for downstream review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive wearable health exports and stores derived local JSON reports. <br>
Mitigation: Use a dedicated input and output folder with the minimum necessary files, restrict local access to those folders, and remove derived reports when no longer needed. <br>
Risk: The skill produces medical-adjacent wellness alerts such as possible illness, sleep apnea, or burnout signals. <br>
Mitigation: Treat alerts as wellness signals for review, not medical advice or diagnosis, and confirm any health concern with an appropriate professional. <br>
Risk: Incomplete, sparse, or incorrectly time-zoned source data can make generated metrics and alerts misleading. <br>
Mitigation: Set the intended IANA timezone, review the output data_quality fields, and avoid relying on metrics marked low or unavailable without inspecting the source data. <br>


## Reference(s): <br>
- [Skill Health overview](references/overview.md) <br>
- [Operations and execution](references/operations.md) <br>
- [ClawHub skill page](https://clawhub.ai/javiersgjavi/skill-health) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Compact JSON emitted to stdout and optional JSON files written to an output directory] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include compact time_window and data_quality fields; cross-alert output contains an alerts array and count.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
