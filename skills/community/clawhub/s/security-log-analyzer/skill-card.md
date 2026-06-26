## Description: <br>
Analyzes security incident logs with an LLM, offering brief or detailed reports that identify threat level, indicators of compromise, and recommended response actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[43622283](https://clawhub.ai/user/43622283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security analysts and incident responders use this skill to summarize security logs, extract IOCs, assess threat severity, and generate response guidance through a configured external LLM provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive security logs are sent to the configured SiliconFlow/OpenAI-compatible provider. <br>
Mitigation: Manually redact secrets, tokens, internal hostnames, account data, and regulated information before analysis. <br>
Risk: Artifact documentation claims automatic sensitive-information redaction, but security evidence says that behavior is not implemented. <br>
Mitigation: Do not rely on automatic redaction; pre-sanitize logs and review submitted content before each run. <br>
Risk: The skill requires an API key stored in a local .env file. <br>
Mitigation: Protect the .env file, avoid committing credentials, and use scoped or rotated provider keys where possible. <br>
Risk: Python dependencies are specified with lower bounds rather than pinned versions. <br>
Mitigation: Use a lock file or pinned dependency set in controlled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/43622283/security-log-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/43622283) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown security analysis report with console status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports brief and detailed analysis modes; long logs may be truncated before analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
