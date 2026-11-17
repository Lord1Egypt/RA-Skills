## Description:

Audit installed Agent Skills: which actually load, what they cost in context, where they conflict, and which are unused.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gold3bear](https://clawhub.ai/user/gold3bear)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to audit installed agent skills for runtime visibility, context cost, conflicts, dormant skills, and security-relevant findings across supported hosts. It guides concrete remediation while preserving host-specific evidence boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports, snapshots, and deep log-probe output may expose private local paths, usernames, skill names, descriptions, and local project context.

Mitigation: Keep outputs local by default and use the documented redaction flags before sharing scan results.

## Reference(s):

- [Host Evidence and Degradation](references/hosts.md)
- [The Judgment Doctor Withholds](references/judgment.md)
- [Skill Vitals Chinese Guide](references/guide.zh-CN.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline shell commands and evidence-backed findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local JSON reports and snapshots when the bundled scan commands are run.]

## Skill Version(s):

1.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
