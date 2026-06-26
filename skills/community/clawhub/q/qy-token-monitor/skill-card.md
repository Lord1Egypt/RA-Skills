## Description: <br>
Token Monitor analyzes OpenClaw session JSONL files to report token usage, cache activity, success rates, tool calls, and latency by skill or project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qingyu24](https://clawhub.ai/user/qingyu24) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect local OpenClaw sessions, compare token consumption across skills, and generate usage reports for performance and cost review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session logs and generated reports may expose usage patterns, tool names, local skill names, and other sensitive workflow details. <br>
Mitigation: Analyze only the narrowest session file or project directory needed, store reports carefully, and review generated Markdown, JSON, or HTML before sharing. <br>
Risk: The analyzer reads local OpenClaw session files and also loads installed skill names to classify activity. <br>
Mitigation: Run it in a local environment where that file access is acceptable and avoid pointing it at unrelated project directories. <br>


## Reference(s): <br>
- [OpenClaw Session File Format](references/session-format.md) <br>
- [ClawHub release page](https://clawhub.ai/qingyu24/qy-token-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, HTML, Shell commands] <br>
**Output Format:** [Markdown report by default, with optional JSON or HTML report output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local OpenClaw session JSONL files and can filter by session file, project directory, recent days, and skill name.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
