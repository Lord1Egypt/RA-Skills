## Description:

Use when searching the web, documentation, or current information where token efficiency matters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[briefness](https://clawhub.ai/user/briefness)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to answer web, documentation, pricing, and current-information questions with a token-conscious search pipeline that checks a local cache, rewrites queries, probes source credibility, and assembles concise answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Web probing and source-validation safeguards may be insufficient in environments with access to internal networks.

Mitigation: Review and fix source checks before enabling network probes; restrict use to trusted URLs and external networks until reviewed.

Risk: The local semantic cache can store recent query text and assembled snippets.

Mitigation: Keep cache storage owner-restricted, avoid sensitive search topics, and clear cached data according to local data-handling policy.

Risk: Source checks should not be relied on alone for prompt-injection resistance.

Mitigation: Treat retrieved fragments as untrusted content and require the host agent to preserve its own citation, instruction-hierarchy, and safety controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/briefness/skills/vryfik-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/briefness)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or text answers with helper-command results used during search]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include caution notes for unverified sources or incomplete assembled results.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
