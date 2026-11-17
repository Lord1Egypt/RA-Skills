## Description:

Set up and use ViralQuery's protected HTTP API to build a private video inspiration feed for one app, website, or niche.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tfcbot](https://clawhub.ai/user/tfcbot)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use ViralQuery to configure tenant-scoped video research, verify API access, run a scroll, and retrieve library, outlier, trend, and hook signals for one app, website, or niche.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow includes an unpinned `npx viralquery` command that may handle a live API key.

Mitigation: Use an environment variable or secret store for the key and prefer a pinned or manually verified CLI setup path before running commands.

Risk: The skill treats mutable remote documentation as the source of truth for operational API details.

Mitigation: Treat remote documentation as reference material and constrain API actions to the intended ViralQuery tenant and workspace.

## Reference(s):

- [ViralQuery LLM Documentation](https://viralquery.com/llms.txt)
- [ViralQuery Documentation](https://viralquery.com/docs)
- [ClawHub Skill Page](https://clawhub.ai/tfcbot/skills/viralquery)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source URLs from retrieved ViralQuery results when reporting research findings.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
