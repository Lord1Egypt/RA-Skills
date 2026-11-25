## Description:

A CLI and MCP server for managing Tokei pre-launch, waitlist, giveaway, and referral campaigns through the Tokei v1 REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gilesdawe](https://clawhub.ai/user/gilesdawe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and campaign operators use it from a CLI or connected agent to manage campaign pages, entrants, media, webhooks, and campaign analytics in Tokei.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is marked suspicious with medium confidence because installation can run an unpinned package that may change after review; the scan covered only part of the artifact.

Mitigation: Avoid installing until the package version is pinned and reviewed, and disclose the participant creation and point assignment capabilities before use.

Risk: Write operations can publish or change campaign pages, create entries, and subscribe webhooks that act on live events.

Mitigation: Use a read-only API key for monitoring and get human approval before publishing pages or making other public or email-triggering changes.

## Reference(s):

- [Tokei Agent documentation](https://tokei.io/agent)
- [Tokei API reference](https://tokei.io/docs/api)
- [tokei-agent on npm](https://www.npmjs.com/package/tokei-agent)
- [ClawHub release page](https://clawhub.ai/gilesdawe/skills/tokei-agent)
- [Tokei](https://tokei.io)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON responses, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Response contents depend on the selected command and may include participant data.]

## Skill Version(s):

0.3.9 (source: server-resolved release metadata; package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
