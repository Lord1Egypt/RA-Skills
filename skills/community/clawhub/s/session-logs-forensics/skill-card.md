## Description: <br>
Analyze OpenClaw session JSONL history for cost spikes, tool-call anomalies, and behavior regressions with jq + rg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielsinewe](https://clawhub.ai/user/danielsinewe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to investigate historical session logs, isolate cost spikes, review tool-call anomalies, and compare behavior across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw session transcripts that may contain secrets, personal information, or sensitive operational details. <br>
Mitigation: Use narrow agent IDs, dates, keywords, or session IDs, and review any transcript extracts before sharing them. <br>
Risk: Broad searches across all session logs can expose more historical conversation content than needed for an investigation. <br>
Mitigation: Start with targeted filters and expand scope only when the incident question requires it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/danielsinewe/session-logs-forensics) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown, configuration] <br>
**Output Format:** [Markdown with jq and rg command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local access to OpenClaw session JSONL files and the jq and rg command-line tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
