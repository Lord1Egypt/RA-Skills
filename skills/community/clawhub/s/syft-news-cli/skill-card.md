## Description:

Help users to access the global news pipeline of Syft News, which offers AI pre-recalled and summarized by-topic news pools, free keyword search and news extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solatrader](https://clawhub.ai/user/solatrader)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to retrieve Syft News topics, searches, and top-story pools, then turn them into profile-aware briefings, storyline trees, backfills, or durable editorial guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and relies on an unpinned third-party Syft CLI that can access account-linked news and profile data.

Mitigation: Review the Syft CLI dependency before installation and prefer a pinned or otherwise verified CLI version.

Risk: The skill can produce or update local profile, briefing, storyline, and guidance artifacts.

Mitigation: Ask the agent to confirm before writing or overwriting saved files.

Risk: Some Syft commands depend on login state, followed topics, local saved profile data, or paid account features.

Mitigation: Confirm account status and command requirements with `syft status` and relevant command output before relying on results.

## Reference(s):

- [Syft News Pool (CLI) on ClawHub](https://clawhub.ai/solatrader/skills/syft-news-cli)
- [solatrader Publisher Profile](https://clawhub.ai/user/solatrader)
- [@orionarm/syft-cli package](https://www.npmjs.com/package/@orionarm/syft-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and optional Markdown, HTML, or JSON artifact files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create reusable profile, briefing, storyline, and guidance artifacts when the user requests saved outputs.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
