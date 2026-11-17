## Description:

Scans existing skill bundles to identify duplicates, coverage gaps, responsibility conflicts, and the highest-priority missing skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to audit a skills directory, find overlapping responsibilities and missing roles, and draft publishing recommendations before changing a skill bundle.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads user-specified local directories, so reports can include names or snippets from sensitive files if pointed at a broad workspace.

Mitigation: Run it only against the intended skills root and avoid home directories or repositories containing unrelated secrets.

Risk: The generated audit report may be incomplete or misleading when the input directory is incomplete or stale.

Mitigation: Review the report before using it for publishing, configuration, or bundle planning decisions.

Risk: The bundled script can write a report file when an output path is supplied.

Mitigation: Use stdout or dry-run behavior for review first, and choose a controlled output path when writing files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/skill-gap-finder)
- [Publisher profile](https://clawhub.ai/user/52yuanchangxing)
- [resources/spec.json](artifact/resources/spec.json)
- [resources/template.md](artifact/resources/template.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Structured Markdown by default, with optional JSON output from the bundled script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write the report to a user-specified output file; otherwise prints to stdout.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
