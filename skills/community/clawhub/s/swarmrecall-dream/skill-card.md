## Description:

Agent dreaming - memory consolidation, deduplication, pruning, contradiction resolution, and session summarization via the SwarmRecall API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waydelyle](https://clawhub.ai/user/waydelyle)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to consolidate, deduplicate, prune, summarize, and resolve contradictions in agent memory stores during idle periods or on explicit cleanup requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can rewrite, merge, summarize, or archive persistent agent memories.

Mitigation: Require manual review before enabling idle, periodic, or shared-pool memory changes, and review proposed merges or archives before applying them.

Risk: The bearer token can be sent to an environment-selected API host if SWARMRECALL_API_URL is overridden.

Mitigation: Keep SWARMRECALL_API_URL unset unless intentionally using a trusted endpoint, and store SWARMRECALL_API_KEY only in the environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/waydelyle/skills/swarmrecall-dream)
- [SwarmRecall](https://www.swarmrecall.ai)
- [SwarmRecall API Base URL](https://swarmrecall-api.onrender.com)
- [SwarmRecall API Registration Endpoint](https://swarmrecall-api.onrender.com/api/v1/register)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with JSON and HTTP request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SWARMRECALL_API_KEY for authenticated API access.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
