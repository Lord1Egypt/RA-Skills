## Description:

Orient an unknown repository or directory: enumerate, measure size distribution, locate source-of-truth files, compare sibling versions, and inspect git. Produces orientation, a fact table, and a risk report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyunlai](https://clawhub.ai/user/zuoyunlai)

### License/Terms of Use:

MIT

## Use Case:

Developers and repository maintainers use this skill to understand an unfamiliar directory or repository, including its structure, size, source-of-truth files, related versions, and Git health. It provides an evidence-backed orientation and suggested next steps without making changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags reported file-permission changes in a workflow described as read-only.

Mitigation: Remove automatic permission changes and report mode differences instead.

Risk: The security review was partial because a local path-like reference could not be resolved.

Mitigation: Review the unresolved reference and complete the security review before installation.

## Reference(s):

- [Git state triage reference](references/git-state-triage.md)
- [ClawHub release page](https://clawhub.ai/zuoyunlai/skills/repo-orientation)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown report with tables, file paths, risks, and suggested next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence-backed, read-only orientation report with four optional next steps.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
