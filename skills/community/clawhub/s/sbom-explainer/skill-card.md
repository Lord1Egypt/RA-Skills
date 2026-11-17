## Description:

Explains SBOMs or dependency lists as plain-language, reviewable risk summaries ordered by likely impact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and release teams use this skill to turn SBOMs, dependency lists, or known issue notes into structured Markdown briefings for management reporting, supply-chain risk communication, and release notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SBOMs and dependency lists can include sensitive dependency, environment, or product details.

Mitigation: Provide only files intended for local review and redact sensitive SBOM content when possible.

Risk: The helper script can create directories and overwrite the report path supplied with --output.

Mitigation: Use stdout or --dry-run first, then choose output paths deliberately before writing a report file.

Risk: Dormant audit modes are broader than the default structured SBOM explanation workflow.

Mitigation: Use the default structured_brief mode unless a local audit mode is explicitly needed and the target files are in scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/sbom-explainer)
- [ClawHub publisher profile](https://clawhub.ai/user/52yuanchangxing)
- [README](artifact/README.md)
- [Output specification](artifact/resources/spec.json)
- [Output template](artifact/resources/template.md)

## Skill Output:

**Output Type(s):** [analysis, markdown, code, shell commands, guidance]

**Output Format:** [Markdown briefing by default, with optional JSON output from the local helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include dependency overview, key risks, affected scope, priorities, mitigation advice, communication points, and confirmation items when inputs are incomplete.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
