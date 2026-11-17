## Description:

Scans documents, code, and logs for common personal identifiers, secrets, internal paths, and project codes, then masks matches and can produce an audit report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Developers and release authors use this skill to check documents, code, or logs before sharing them externally. It masks detected sensitive strings and can provide a report of the detected items for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional --report output can expose personal details and secret excerpts.

Mitigation: Keep report output local and do not share it; review the sanitized text separately before release.

Risk: Pattern-based detection can miss sensitive content or match unrelated text.

Mitigation: Manually review the full result and add project-specific terms with --extra when needed.

Risk: Host enforcement of the declared file-access restrictions is unverified.

Mitigation: Limit execution to explicitly selected inputs and confirm the host sandbox limits file access.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zhaoxinghua09-cell/skills/zz-pipeline-smoke)
- [LGD ecosystem hub](https://zhaoxinghua09-cell.github.io/lgd-hub/)
- [LGD theory](https://github.com/zhaoxinghua09-cell/LGD)
- [Formal paper](https://doi.org/10.5281/zenodo.22456647)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Sanitized text with an optional JSON report on standard output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The optional report may include sensitive excerpts from the input.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
