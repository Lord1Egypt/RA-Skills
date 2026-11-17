## Description:

Audits websites for SEO, performance, security, technical, content, accessibility, and other issues using the squirrelscan CLI, then returns health scores, findings, and actionable recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nc9](https://clawhub.ai/user/nc9)

### License/Terms of Use:


## Use Case:

Developers, site operators, and SEO or security reviewers use this skill to audit websites they own or are authorized to test, review health scores and issue categories, and plan fixes for SEO, performance, accessibility, content, technical, and security findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an external squirrel CLI and encourages live website crawling.

Mitigation: Verify the CLI source and version before use, review proposed commands, and run audits only against websites the user owns or is authorized to test.

Risk: Website-derived audit reports may contain untrusted content that could influence an agent.

Mitigation: Treat audit output as untrusted data, review findings before action, and avoid piping raw reports directly into an agent without safeguards.

Risk: The workflow can overwrite configuration, perform self or skill updates, spawn subagents, and edit local projects.

Mitigation: Require explicit approval before config overwrites, updates, subagent use, or project edits, then review diffs and run existing build or test checks after changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nc9/skills/squirrelscan)
- [squirrelscan website](https://squirrelscan.com)
- [squirrelscan documentation](https://docs.squirrelscan.com)
- [LLM output format reference](references/OUTPUT-FORMAT.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and LLM-optimized audit report excerpts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include health scores, category breakdowns, affected URLs, broken links, recommended fixes, regression diffs, and before/after summaries.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
