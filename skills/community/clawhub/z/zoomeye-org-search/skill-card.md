## Description:

Guides agents in using the ZoomEye CLI to build ZoomEye dork queries, search internet-exposed assets, and review asset discovery results for security research and exposure analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jjbondone](https://clawhub.ai/user/jjbondone)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and external researchers use this skill to translate natural-language asset discovery goals into ZoomEye dork syntax, check ZoomEye CLI setup, run scoped searches, and interpret returned asset data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide a ZoomEye API key to the agent for initialization.

Mitigation: Configure ZoomEye credentials outside the chat when possible, avoid pasting API keys into the agent, and rotate any key already shared.

Risk: The skill recommends installing the ZoomEye CLI without pinning a trusted package version.

Mitigation: Install the CLI in a dedicated environment and pin a trusted version where possible before use.

Risk: The skill can save ZoomEye search results locally with the -save option.

Mitigation: Use -save only when local storage of search results is acceptable for the data and environment.

## Reference(s):

- [ZoomEye Documentation](https://www.zoomeye.org/doc/)
- [ClawHub Skill Page](https://clawhub.ai/jjbondone/skills/zoomeye-org-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, dork query strings, command output interpretation, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose ZoomEye CLI commands, local result saving with -save, and API-key setup steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
