## Description: <br>
Analyzes driver-facing DMS video or video URLs to estimate eye state, blink rate, eye-closure duration, PERCLOS, fatigue level, warnings, and recommended cabin or fleet actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Fleet safety teams, vehicle-system developers, and safety operations staff use this skill to analyze driver camera video for blink-rate and eye-closure fatigue indicators, generate warning reports, and review historical fatigue events. It is intended as an auxiliary safety signal, not a medical diagnosis or a replacement for driver responsibility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may upload sensitive driver face videos, video URLs, and identifiers to external LifeEmergence/SMYX services. <br>
Mitigation: Use only with informed consent from recorded drivers, approved data-sharing terms, and documented retention, access, and deletion controls. <br>
Risk: The skill can retrieve cloud report history and may associate reports with usernames, phone numbers, or open-id values. <br>
Mitigation: Limit use to authorized operators, validate the open-id before each lookup, and avoid exposing historical report links to users who should not access them. <br>
Risk: ClawScan flagged account/token storage, unrelated health-analysis behavior, and dependency risk. <br>
Mitigation: Review the publisher's implementation before installation, remove unrelated outputs, document all data flows, and replace or validate risky dependencies before production deployment. <br>


## Reference(s): <br>
- [Driver fatigue detection API documentation](references/api_doc.md) <br>
- [SMYX analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports and tables, JSON analysis results, and shell commands for invoking the bundled Python scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include fatigue metrics, warning types, recommended actions, report links, and privacy or consent guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
