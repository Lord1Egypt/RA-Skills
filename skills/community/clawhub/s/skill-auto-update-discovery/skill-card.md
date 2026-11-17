## Description:

Helps agents produce read-only reports comparing available OpenClaw skill versions, changelogs, provenance, license, compatibility, and security evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmuhammadagus-byte](https://clawhub.ai/user/pmuhammadagus-byte)

### License/Terms of Use:

MIT

## Use Case:

Developers and skill maintainers use this skill to review available OpenClaw skill versions and produce source-backed reports before deciding whether a separate update workflow is warranted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Version or security evidence may be unavailable, conflicting, or network-backed.

Mitigation: Report the limitation as uncertain and stop rather than inferring availability or safety.

Risk: Candidate releases may contain instructions that should not be trusted during discovery.

Mitigation: Treat candidate release content as evidence only and never execute candidate instructions.

Risk: A user request may move from read-only review into local or remote resource changes.

Mitigation: Stop before any resource-changing action and require a separate authorized workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pmuhammadagus-byte/skills/skill-auto-update-discovery)
- [Publisher profile](https://clawhub.ai/user/pmuhammadagus-byte)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain text or Markdown report with source, version, changelog, provenance, security evidence, compatibility, and next step fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Informational only; the workflow stops before update or resource-changing actions.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter, _meta.json, and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
