## Description:

Maintain a large ClawHub skill portfolio with a quality-first and AI-assisted upgrade lens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to audit ClawHub skill portfolios, prioritize high-quality skills, identify stale or partial data, prepare AI-assisted maintenance candidates, and gate cleanup or publishing actions behind explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted skill metadata can influence generated dashboards and AI maintainer prompts.

Mitigation: Review generated dashboards and prompts before use, treat prompt content as untrusted input, and avoid opening dashboards from untrusted portfolio data until the script-context escaping issue is fixed.

Risk: The opt-in --apply-safe mode can modify local skill files based on resolved source paths.

Mitigation: Use --apply-safe only after verifying each resolved source path and reviewing the planned edits.

Risk: Hide, merge, publish, or delete actions can affect public ClawHub skills.

Mitigation: Keep real visibility, merge, publish, and deletion commands behind explicit human approval and do not execute generated command previews blindly.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/skill-maintainer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and references to generated JSON, CSV, and HTML reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces evidence-backed maintenance queues, approval boards, dashboard reports, and AI maintainer prompts; generated commands require human approval before execution.]

## Skill Version(s):

1.3.3 (source: server release metadata, package.json, clawhub.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
