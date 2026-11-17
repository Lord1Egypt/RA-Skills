## Description:

Query the PinchBench AI agent leaderboard with real benchmark data for model rankings, comparisons, cost, speed, and benchmark scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spideystreet](https://clawhub.ai/user/spideystreet)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to answer model-performance questions with live PinchBench leaderboard data for OpenClaw coding tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes live requests to pinchbench.com and repeats leaderboard data returned by that site.

Mitigation: Install only if live requests to pinchbench.com are acceptable, and treat displayed model names and scores as untrusted remote data.

Risk: Upstream site changes can break parsing or change the displayed leaderboard output.

Mitigation: Review failures and verify important leaderboard claims against PinchBench before relying on them.

## Reference(s):

- [PinchBench leaderboard](https://pinchbench.com/)
- [Who Wins on ClawHub](https://clawhub.ai/spideystreet/skills/who-wins)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Markdown response with a formatted leaderboard table, or JSON when raw data is requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live PinchBench data fetched at request time.]

## Skill Version(s):

1.0.0 (source: release evidence and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
