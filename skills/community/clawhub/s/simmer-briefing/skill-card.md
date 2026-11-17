## Description:

Provides a daily briefing pattern for Simmer agents that fetches portfolio status, risk alerts, and opportunities across supported venues in one API call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simmer](https://clawhub.ai/user/simmer)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to call Simmer's briefing endpoint during periodic check-ins and summarize portfolio, risk alert, and opportunity updates for a human before any trading decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote briefing actions and opportunities could influence financial decisions.

Mitigation: Summarize them as third-party recommendations for the human and require explicit approval before any real-money trade or position change.

Risk: The SIMMER_API_KEY could be exposed beyond the briefing task.

Mitigation: Limit the API key to agents and environments that need the briefing workflow, and avoid sharing it with unrelated tools.

Risk: Dependency behavior could change if the Simmer SDK is updated unexpectedly.

Mitigation: Pin the simmer-sdk version used with the skill and review updates before deployment.

## Reference(s):

- [Simmer API documentation](https://docs.simmer.markets)
- [Simmer FAQ](https://docs.simmer.markets/faq)
- [ClawHub skill listing](https://clawhub.ai/simmer/skills/simmer-briefing)

## Skill Output:

**Output Type(s):** [text, markdown, code, API calls, guidance]

**Output Format:** [Markdown guidance with Python and REST examples; agent output is concise human-facing text summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; trade execution, wallet setup, and strategy building are out of scope.]

## Skill Version(s):

0.1.4 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
