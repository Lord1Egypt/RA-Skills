## Description: <br>
Analyzes v3.5 production deployer logs to generate test reports and statistics for monitoring, version comparison, strategy analysis, and AI agent performance evaluation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rf-ai-wh](https://clawhub.ai/user/rf-ai-wh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and AI agent evaluators use this skill to inspect v3.5 production log data, compare v3.5 and v3.0 behavior, and summarize performance indicators for experiments or operational reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The disclosed local log path may contain identifiers, secrets, customer data, or sensitive operational details. <br>
Mitigation: Review or redact /tmp/agent_v35_production.log before running the skill or sharing generated reports. <br>
Risk: Generated statistics may be incomplete or misleading when the production log format differs from the expected v3.5 and v3.0 patterns. <br>
Mitigation: Compare generated summaries against the source log before using them for performance decisions or external reporting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rf-ai-wh/v35-test-report) <br>
- [Publisher profile](https://clawhub.ai/user/rf-ai-wh) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and plain-text report output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads /tmp/agent_v35_production.log and prints aggregate report statistics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, artifact frontmatter, and artifact changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
