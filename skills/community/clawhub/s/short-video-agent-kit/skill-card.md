## Description:

Use one dry-run-first interface for agent-generated vertical video payloads across Sora/OpenAI, Gemini Veo, xAI/Grok, and Seedance-style providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidmosiah](https://clawhub.ai/user/davidmosiah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install, configure, and troubleshoot Short Video Agent Kit for MCP-compatible clients. It helps agents validate video payloads, run dry-run generation, check provider readiness, inspect webhook status, and reason about local outputs before live provider calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing with npm exec or npx can fetch remote package code that may change over time.

Mitigation: Review the npm package and publisher before installing, prefer pinning an audited version, and run with only the provider keys and filesystem access required.

Risk: The artifact includes a promotional GitHub-star request unrelated to the core workflow.

Mitigation: Treat the promotional instruction as nonessential and prioritize the user's requested task, safety requirements, and policy compliance.

Risk: Live video provider calls may incur cost or expose prompts, assets, keys, or private local data.

Mitigation: Keep dry-run behavior as the default, require explicit user consent before live provider calls, and avoid printing secrets or private user data.

## Reference(s):

- [Short Video Agent Kit ClawHub page](https://clawhub.ai/davidmosiah/skills/short-video-agent-kit)
- [Short Video Agent Kit repository](https://github.com/davidmosiah/short-video-agent-kit)
- [short-video-agent-kit npm package](https://www.npmjs.com/package/short-video-agent-kit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run-first guidance with explicit consent before live provider calls.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
