## Description:

Access Vaaya's paid API catalog for web search and research, scraping, image/video/audio generation, LLMs, lead enrichment, live data, code sandboxes, browser automation, email, storage and tokenized shares.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marupelkar](https://clawhub.ai/user/marupelkar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to connect an agent to Vaaya's paid tool catalog for research, data access, media generation, compute, commerce, communications, and other external actions with quoted per-call costs and spending ceilings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can route broad paid tool use, purchases, stock buys, email automation, phone calls, uploads, browser sessions, and other high-impact actions.

Mitigation: Use strict spend caps, review each proposed action against the user's explicit task, and require explicit approval for purchases, trades, outbound messages, uploads, calls, browser use, and top-ups.

Risk: Persistent Vaaya API keys, refresh tokens, and user identifiers can grant continued access to the user's paid account.

Mitigation: Prefer OAuth where available, keep credentials out of shared repos, logs, chat messages, and generic agent memory, and revoke leaked or unneeded grants from the Vaaya account controls.

Risk: Local installation or MCP configuration changes may connect Vaaya to future agent sessions with broad tool access.

Mitigation: Review MCP configuration changes before enabling the server, pin or verify npm installers before running them, and remove or disable the connector when it is no longer needed.

Risk: Remote browser sessions, data uploads, screen recordings, and logged-in workflows can expose sensitive user data.

Mitigation: Confirm the minimum necessary data before upload or browser automation, avoid sharing credentials directly with the agent, and require user approval before using logged-in browser sessions or recording workflows.

## Reference(s):

- [Vaaya Skill Page](https://clawhub.ai/marupelkar/skills/vaaya)
- [Vaaya Homepage](https://vaaya.ai/?utm_source=clawhub&utm_medium=agent&utm_campaign=skill)
- [Vaaya API Catalog](https://vaaya.ai/api/catalog)
- [Vaaya Recipes](https://vaaya.ai/recipes)
- [Vaaya Tool Reference](https://vaaya.ai/llms-full.txt)
- [Vaaya Agent-Readable Index](https://vaaya.ai/llms.txt)
- [Setup - connecting Vaaya to your agent](references/setup.md)
- [Tools - the exact params of every Vaaya MCP tool](references/tools.md)
- [Research with Vaaya - OneSearch + the research playbooks](references/research.md)
- [Data - picking the right paid data call](references/data.md)
- [Media generation - images, video, music, voice, demo videos](references/media.md)
- [GTM playbook - outbound with Vaaya](references/gtm.md)
- [Compute, browser, files, memory, LLM, phone calls](references/compute.md)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration, Code, Markdown]

**Output Format:** [Markdown with inline shell commands, JSON request examples, API call plans, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include paid service calls, cost ceilings, OAuth or API-key setup steps, MCP configuration, and user approval prompts.]

## Skill Version(s):

1.2.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
