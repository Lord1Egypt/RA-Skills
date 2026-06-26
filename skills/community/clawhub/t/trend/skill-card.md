## Description: <br>
Trend is a local content logging utility for drafting, editing, optimizing, searching, and exporting timestamped content entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use Trend to record content drafts, edits, publication plans, hashtags, hooks, calls to action, and related notes in local plain-text logs. It is best suited for simple local traceability and export workflows, not for trend, sentiment, popularity, or alerting analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may expect trend, sentiment, popularity, or alerting analytics, but the security evidence describes the skill as a local content logger. <br>
Mitigation: Use it only for simple local content logging and export workflows; do not rely on it for analytics or monitoring decisions. <br>
Risk: The skill stores entered text in plaintext under ~/.local/share/trend and includes that text in export files. <br>
Mitigation: Do not enter secrets, confidential drafts, regulated data, or other sensitive content unless local plaintext storage and export are acceptable. <br>


## Reference(s): <br>
- [Trend on ClawHub](https://clawhub.ai/xueyetianya/trend) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, configuration, guidance] <br>
**Output Format:** [Plain text command output and local log/export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores entered content under ~/.local/share/trend and can export accumulated entries as JSON, CSV, or TXT.] <br>

## Skill Version(s): <br>
2.0.1 (source: ClawHub release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
