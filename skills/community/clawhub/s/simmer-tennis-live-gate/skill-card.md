## Description:

Gates Simmer/Polymarket tennis market entries on live match state from the Live Tennis API, returning an observe-only trade/no-trade decision and suggested size without placing orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bensynapse](https://clawhub.ai/user/bensynapse)

### License/Terms of Use:

MIT

## Use Case:

Developers and trading-system operators use this skill as a read-only precondition gate before sizing tennis market positions. It helps skip or downsize decisions when live state is stale, undetermined, stopped, or at a break point.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys are required for live data paths, and misuse or overbroad credentials could expose account or service access.

Mitigation: Use least-privilege Live Tennis and Simmer keys, keep them in environment variables or a managed secret store, and rotate them according to local policy.

Risk: Missing, invalid, or future timestamps may cause stale live-state checks to be treated too permissively.

Mitigation: Fix timestamp handling so unverifiable timestamps fail closed before relying on decisions in any workflow that can move money.

Risk: Overriding LIVETENNIS_BASE_URL can redirect live-state requests to an untrusted endpoint.

Mitigation: Do not set LIVETENNIS_BASE_URL in production unless the endpoint is explicitly trusted and reviewed.

Risk: The skill is a decision-support gate, not a validated trading edge or financial advice.

Mitigation: Treat allowed decisions as one input to a separate strategy review, require an independent probability estimate, and keep order execution outside this skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bensynapse/skills/simmer-tennis-live-gate)
- [Publisher profile](https://clawhub.ai/user/bensynapse)
- [Live Tennis API docs](https://docs.livetennisapi.com)
- [Live Tennis API](https://livetennisapi.com)
- [Simmer Markets](https://simmer.markets)
- [Polymarket Tennis toolkit](https://github.com/livetennisapi/polymarket-tennis)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell snippets; runtime gate decisions are returned as structured Python values.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Observe-only; returns a trade/no-trade decision and suggested size, and does not submit orders.]

## Skill Version(s):

0.1.0 (source: frontmatter and changelog, released 2026-08-18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
