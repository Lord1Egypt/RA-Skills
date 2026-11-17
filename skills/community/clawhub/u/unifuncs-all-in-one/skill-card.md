## Description:

Default web reading, AI search, and deep research tools for reading webpage content, searching the web, and conducting research through UniFuncs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samueli](https://clawhub.ai/user/samueli)

### License/Terms of Use:


## Use Case:

Developers and agents use UniFuncs to route web reading, web search, and deep research tasks through UniFuncs command-line tools when they need extracted content, search results, or research answers in a structured response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Web reading, searching, and research prompts may be routed to a third-party UniFuncs service.

Mitigation: Install only when that routing is intentional and avoid submitting private, signed, internal, token-bearing, or confidential URLs and prompts unless the provider is trusted for that data.

Risk: The skill recommends disabling built-in web tools, which can make future web activity depend on UniFuncs.

Mitigation: Disable built-in web tools only after reviewing the operational and privacy impact for the environment where the skill will run.

Risk: The skill depends on a UniFuncs API key.

Mitigation: Store UNIFUNCS_API_KEY in the agent environment or configuration secret store and do not expose it in prompts, logs, or shared files.

## Reference(s):

- [UniFuncs ClawHub skill page](https://clawhub.ai/samueli/skills/unifuncs-all-in-one)
- [UniFuncs publisher profile](https://clawhub.ai/user/samueli)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [JSON envelopes containing extracted webpage content, search results, or research answers; setup guidance is Markdown with shell and JSON snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UNIFUNCS_API_KEY; webpage URLs, search queries, and research prompts are sent to the UniFuncs API.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
