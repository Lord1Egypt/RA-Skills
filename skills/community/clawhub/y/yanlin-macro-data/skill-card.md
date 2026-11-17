## Description:

Yanlin Macro Data collects macro liquidity indicators such as rates, exchange rates, commodities, and selected U.S. equities, using Sina Finance where available and built-in classroom snapshots otherwise.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[caoling7878-arch](https://clawhub.ai/user/caoling7878-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Educators, students, and reviewers use this skill to demonstrate macro liquidity data collection and reporting. Its figures should be treated as classroom examples unless independently verified against authoritative market data sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial data may be misleading because hardcoded snapshots are mixed with live-looking output and the documentation contains contradictory northbound-flow claims.

Mitigation: Use only for classroom or demo workflows unless the publisher fixes provenance issues; independently verify figures before investment, trading, or automated reporting use.

Risk: The script may make outbound requests to Sina Finance when network access is available.

Mitigation: Run it only in environments where those outbound requests are allowed and monitored, or disable network access when using snapshot-only demonstrations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caoling7878-arch/skills/yanlin-macro-data)
- [Sina Finance](https://finance.sina.com.cn)
- [Sina Finance futures quote endpoint](https://hq.sinajs.cn/list=hf_CL,hf_GC)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Plain text or JSON emitted by a Python script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include a date and source-sensitive macro values; network failures fall back to built-in snapshots.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
