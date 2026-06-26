## Description: <br>
Runtime Monitor checks AI agent runtime I/O for prompt injection, data leakage, dangerous commands, and risk scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liwiw](https://clawhub.ai/user/liwiw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect prompts, tool inputs, and tool outputs for risky patterns before or during agent workflows. It supports triage and audit workflows by returning risk levels, scores, detections, and block decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monitoring reports can contain excerpts of inspected prompts, tool inputs, or tool outputs. <br>
Mitigation: Treat reports and audit logs as sensitive data, limit access to them, and avoid sending them to untrusted systems. <br>
Risk: Pattern-based detection and block thresholds can produce false positives or miss novel attacks. <br>
Mitigation: Test the configured block threshold in representative workflows and use the monitor as one control in a broader review and security process. <br>


## Reference(s): <br>
- [Runtime Monitor ClawHub page](https://clawhub.ai/liwiw/runtime-monitor) <br>
- [liwiw publisher profile](https://clawhub.ai/user/liwiw) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Python objects and dictionaries for monitoring reports, plus integration guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include total checks, detections, maximum risk level, maximum risk score, and block status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
