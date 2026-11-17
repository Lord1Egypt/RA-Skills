## Description:

Analyzes OpenClaw session JSONL files to report token usage, cache activity, skill-level success rates, and performance metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingyu24](https://clawhub.ai/user/qingyu24)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to analyze OpenClaw session logs, understand token consumption, compare skill-level performance, and generate usage reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw session logs that may contain sensitive conversation or project data.

Mitigation: Run it only on logs you are authorized to review, store generated reports securely, and avoid sharing reports outside the intended audience.

Risk: The security evidence reports an unsafe HTML report path that can render unescaped session-derived content.

Mitigation: Prefer JSON or Markdown output and avoid opening HTML reports from untrusted session files until the escaping issue is fixed.

Risk: Untrusted JSONL input can influence generated report contents.

Mitigation: Do not run the analyzer on untrusted JSONL files; review input source and use least-privilege file paths.

## Reference(s):

- [OpenClaw Session File Format](references/session-format.md)
- [ClawHub Skill Page](https://clawhub.ai/qingyu24/skills/qy-token-monitor)
- [Publisher Profile](https://clawhub.ai/user/qingyu24)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands]

**Output Format:** [JSON, Markdown, or HTML reports; may include shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local OpenClaw JSONL session files and can write a report to a specified output path.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
