## Description:

Generates file-type-specific code review checklists covering security, performance, style, and testing best practices for pull requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryudi84](https://clawhub.ai/user/ryudi84)

### License/Terms of Use:

MIT

## Use Case:

Developers and code reviewers use this skill to generate pull request review checklists, review templates, and reports tailored to changed file types. It is useful for review preparation and consistency, but should not be relied on as the sole approval or merge gate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged security checks and CI-blocking behavior are not trustworthy as a merge approval gate.

Mitigation: Use the generated checklist as review support only, and require human review plus established security tooling before approving or merging changes.

Risk: The output-file option may overwrite an existing file at the requested path.

Mitigation: Write reports to a disposable or prechecked path, and avoid pointing output-file at important project files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryudi84/skills/sovereign-code-review-helper)
- [Publisher profile](https://clawhub.ai/user/ryudi84)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown, JSON, or plain text review reports; Markdown PR review templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write reports or templates to a requested output path; critical findings may produce a nonzero exit status.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill.json, script header, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
