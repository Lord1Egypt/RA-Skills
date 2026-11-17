## Description:

SSOT Check audits documentation-heavy repositories for hand-copied facts, helps propose a `.ssot.yaml` manifest of canonical locations, and verifies that known copies still match.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conorbronsdon](https://clawhub.ai/user/conorbronsdon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and repository maintainers use this skill before documentation commits or during audits to find duplicated facts, identify canonical sources, and surface drift with proposed manifest entries or copy fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A project-supplied manifest can direct the skill to read files outside the audited repository or capture sensitive values in reports.

Mitigation: Review `.ssot.yaml` before use, reject unexpected `../` or absolute paths, avoid broad regexes, and exclude secrets or configuration files from checks and reports.

Risk: Cross-repository checks can involve sibling clones and may produce misleading results if freshness cannot be established.

Mitigation: Approve sibling repositories explicitly, rely on read-only local refs by default, and report facts as UNVERIFIED when a value cannot be established without a user-approved fetch.

## Reference(s):

- [Skill instructions](artifact/SKILL.md)
- [README](artifact/README.md)
- [Discovery prompt pattern](artifact/patterns/discovery-prompt.md)
- [Worked discovery report](artifact/examples/cot-production-discovery/discovery-report.md)
- [Proposed SSOT manifest example](artifact/examples/cot-production-discovery/proposed-ssot.yaml)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with YAML manifest snippets, shell commands, and proposed diffs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only by default; proposed edits require explicit approval.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
