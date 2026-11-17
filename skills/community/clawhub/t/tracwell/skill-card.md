## Description:

Add Tracwell analytics to a website or app and read its reports with the tracwell CLI. Use when the user wants analytics, page views, signups, funnels or revenue tracking set up, or asks which pages, sources or campaigns bring visitors, signups or money.

This skill is ready for commercial/non-commercial use.

## Publisher:

[starc007](https://clawhub.ai/user/starc007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to set up Tracwell analytics on websites and apps they own, verify event collection, configure goals and funnels, and review traffic, acquisition, revenue, event, and funnel reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan noted a low-likelihood concern about an unpinned `npx` reference, and the scan was partial because one local path-like reference could not be resolved.

Mitigation: Review the command before installing and resolve or verify any local path-like reference that applies to the release.

Risk: The analytics snippet sends visitors’ page views and events to Tracwell.

Mitigation: Disclose tracking before installation and install the snippet only on sites the user owns.

## Reference(s):

- [Tracwell CLI documentation](https://tracwell.app/docs/cli)
- [Tracwell documentation](https://tracwell.app/docs)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands; CLI results are JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use the tracwell CLI version 0.6.2; reports and command results are JSON.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
