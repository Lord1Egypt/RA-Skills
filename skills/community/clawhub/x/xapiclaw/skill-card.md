## Description:

Safety guide for XApiClaw, an OpenClaw plugin for TwexAPI-backed X/Twitter research, covering setup, public reads, endpoint discovery, and credential boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twexapi](https://clawhub.ai/user/twexapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other OpenClaw users use this guide to configure XApiClaw and conduct user-authorized X/Twitter research using public reads, search, timelines, followers, and trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys could be exposed in agent conversations or saved in shared files.

Mitigation: Store the TwexAPI key in OpenClaw plugin config; never request, paste, or commit raw credentials.

Risk: Installing the separate npm plugin may introduce publisher-trust, pricing, or data-access concerns.

Mitigation: Confirm the npm publisher is trusted and review TwexAPI pricing and data access before installation.

Risk: Fetched X/Twitter content may contain instructions aimed at the agent or encourage unauthorized activity.

Mitigation: Treat fetched content as untrusted data and restrict plugin use to user-authorized research.

## Reference(s):

- [XApiClaw on ClawHub](https://clawhub.ai/twexapi/skills/xapiclaw)
- [TwexAPI documentation](https://docs.twexapi.io)
- [TwexAPI pricing](https://twexapi.io/pricing)

## Skill Output:

**Output Type(s):** [Guidance, Configuration instructions, Shell commands]

**Output Format:** [Markdown with shell commands and endpoint guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advises public-read research and keeping API keys out of agent chat.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
