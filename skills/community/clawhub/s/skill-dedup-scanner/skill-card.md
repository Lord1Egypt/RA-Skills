## Description:

Scans installed skills for duplicates and naming conflicts, detects similar skills that may cause model confusion, and supports English and Chinese output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shyjsarah](https://clawhub.ai/user/shyjsarah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this agent skill to scan an installed skills directory before publishing, auditing, or troubleshooting trigger conflicts. It compares skill names and descriptions, then reports likely duplicate or overlapping skills with recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reads SKILL.md files under the directory selected by the user.

Mitigation: Run it against trusted local skill directories and avoid scanning paths that contain sensitive or unrelated files.

Risk: Reports can be influenced by metadata in the scanned skills and may contain misleading recommendations.

Mitigation: Review generated Markdown or JSON reports before acting on suggested renames, merges, or description changes.

Risk: PyYAML is a runtime dependency and the security evidence recommends pinning it before production use.

Mitigation: Pin and review PyYAML versions in production environments.

## Reference(s):

- [Skill Naming Best Practices](references/best_practices.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown report or JSON summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write the generated report to a user-specified output file.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
