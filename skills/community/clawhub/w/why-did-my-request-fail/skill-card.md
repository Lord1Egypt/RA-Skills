## Description:

Helps agents decide whether to retry, back off, switch tools, stop, or fix a failed network request using observed host-level request outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeneassoft](https://clawhub.ai/user/aeneassoft)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill before retrying failed web, API, browser, or network requests to choose a bounded next action and avoid blind retries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Useful operation depends on the clawphylax plugin and its local ledger of observed request outcomes.

Mitigation: Review the clawphylax plugin's data collection behavior separately before installing or relying on the skill.

Risk: Network retry guidance can still be misapplied if the agent ignores the original status code, host, or credential context.

Mitigation: Use the skill's evidence, confidence bounds, wait time, and scope fields before retrying, backing off, switching tools, or stopping.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aeneassoft/skills/why-did-my-request-fail)
- [Project homepage](https://github.com/aeneassoft/clawphylax)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with a single ACTION line and labeled evidence, next-step, confidence, and scope fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action values are constrained to RETRY_AFTER_FIXING_REQUEST, BACKOFF, SWITCH_TOOL, STOP, or TRY_ONCE.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
