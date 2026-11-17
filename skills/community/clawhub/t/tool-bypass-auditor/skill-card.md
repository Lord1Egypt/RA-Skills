## Description:

Detect tool bypass attempts and exec/shell overuse in local session/evolution artifacts, then produce a concise bypass audit report with low/medium/high findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[147258xuan](https://clawhub.ai/user/147258xuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace operators use this skill to review local session and evolution JSONL artifacts for likely tool bypass patterns, repeated exec or shell use, and unsafe execution indicators, then receive severity-tagged findings and recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security review confidence is medium because scanner coverage was partial; the clean verdict does not cover two paths missing from the scanned bundle.

Mitigation: Review the complete release contents and source before relying on the audit result.

Risk: The skill includes executable code and does not declare a tool scope; it reads JSONL files under the selected workspace and includes file paths in its report.

Mitigation: Inspect the code and run it only against the intended workspace, taking care with sensitive session artifacts.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/147258xuan/skills/tool-bypass-auditor)
- [Publisher profile: 147258xuan](https://clawhub.ai/user/147258xuan)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON report with severity-tagged findings and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only report over JSONL files found recursively under the selected workspace.]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
