## Description:

Produce an English CI Tools digest for a complete calendar month, with release evidence, migration notes and clearly separated open work. Use for monthly reporting or an explicitly requested month.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xrowgmbh](https://clawhub.ai/user/xrowgmbh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and CI Tools users use the skill to prepare a monthly release digest with merge request evidence, migration notes, and separately dated open work. It supports monthly reporting or a requested calendar month.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The collector uses a subprocess and reaches GitLab, while the security review flags ambiguity in the network and shell scope.

Mitigation: Review the collector's GitLab commands and run it with a least-privilege GitLab token.

Risk: The security review was partial because a local path-like reference in SKILL.md could not be resolved; the benign verdict does not guarantee zero risk.

Mitigation: Resolve and review the referenced path before relying on the scan as a complete assessment.

Risk: The digest is required to be written entirely in English, which may not meet every audience's language needs.

Mitigation: Confirm that English is suitable for the intended readers and review the final digest for clarity.

## Reference(s):

- [CI Tools GitLab project](https://gitlab.com/xrow-public/ci-tools)

## Skill Output:

**Output Type(s):** [Markdown]

**Output Format:** [English Markdown digest with source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers a complete UTC calendar month; open merge requests are shown as a separately dated snapshot.]

## Skill Version(s):

5.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
