## Description:

Log health symptoms, track patterns, and chart trends. Use when logging symptoms, tracking frequency, charting trends, reviewing patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use Symptom to log health and wellness entries locally, review recent activity, search prior notes, and summarize symptom patterns over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Symptom entries may contain sensitive health information stored as plaintext files under the user's home directory.

Mitigation: Install only on machines where local file access is appropriately restricted, and avoid use on shared or heavily synced systems unless file permissions are managed separately.

Risk: The release evidence reports misleading or broken export behavior.

Mitigation: Review export behavior before relying on exported JSON, CSV, or text files for backup, transfer, or analysis.

## Reference(s):

- [Symptom ClawHub listing](https://clawhub.ai/xueyetianya/skills/symptom)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and local file output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local plaintext logs and advertised JSON, CSV, or text exports under the user's home directory.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
