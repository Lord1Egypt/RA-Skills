## Description:

TokFlow lets an agent query a local TokFlow backend for LLM token usage, model costs, provider balances, and prompt optimization suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyaok1](https://clawhub.ai/user/wangyaok1)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use TokFlow to monitor token consumption, model spend, paid-provider balances, and prompt efficiency from a local TokFlow installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reveal local OpenClaw usage, cost, prompt-metric, and provider balance data to the agent.

Mitigation: Use it only in trusted agent sessions and limit questions to the usage, cost, balance, and optimization data needed for the task.

Risk: The skill depends on a local TokFlow backend at localhost:8001, so an untrusted or unexpected local service could provide sensitive or misleading data.

Mitigation: Run the TokFlow backend locally from a trusted installation and confirm the local endpoint before using the skill.

Risk: Command-line token login can expose credentials in shell history or process listings.

Mitigation: Prefer browser-based login or safer secret handling, and use pinned ClawHub CLI versions when installing or publishing.

## Reference(s):

- [TokFlow ClawHub skill page](https://clawhub.ai/wangyaok1/skills/tokflow)
- [TokFlow publisher profile](https://clawhub.ai/user/wangyaok1)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON from the query script, typically summarized by the agent as Markdown or plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted local TokFlow backend at http://localhost:8001/api.]

## Skill Version(s):

0.5.0 (source: frontmatter, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
