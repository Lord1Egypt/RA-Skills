## Description:

Access Xona's x402 creative resource APIs on api.xona-agent.com for design research, image generation, video generation, X news extraction, and PumpFun token intelligence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xona-labs](https://clawhub.ai/user/xona-labs)

### License/Terms of Use:


## Use Case:

Developers and creative agents use this skill to call paid Xona x402 APIs for creative direction, image and video generation, X account news extraction, and PumpFun token trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wallet-enabled fetch script can make automatic paid API calls without built-in per-call or session spending limits.

Mitigation: Use a dedicated low-balance Solana wallet and enforce per-call and session spending limits before use.

Risk: The helper script can be directed to arbitrary URLs, which may send wallet-enabled paid requests outside approved Xona API paths.

Mitigation: Restrict calls to approved api.xona-agent.com endpoints and validate payment recipients and amounts.

Risk: The x402 wallet dependency is version-ranged rather than pinned.

Mitigation: Pin and review the wallet dependency before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xona-labs/skills/x402-creative-resources)
- [Xona API Base](https://api.xona-agent.com)
- [Xona x402 Resource Discovery](https://api.xona-agent.com/x402-resources)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, JSON]

**Output Format:** [Markdown guidance with bash examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return paid API results such as image_url, video_url, banner_url, tweet_draft, design direction, and token intelligence.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
