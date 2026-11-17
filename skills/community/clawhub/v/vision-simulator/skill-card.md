## Description:

Vision Simulator predicts marketing campaign, product launch, and market reaction outcomes using multi-agent simulation and optional live news, trend, and competitor data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dorongss](https://clawhub.ai/user/dorongss)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, product teams, and campaign strategists use this skill to forecast likely campaign or launch outcomes, estimate success probability, identify risks, and produce prioritized action items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pro simulations may expose scenario-derived keywords to live web, news, or trend sources.

Mitigation: Avoid confidential campaign, product-launch, or competitor-sensitive details unless those terms are approved for live search.

Risk: Forecast probabilities, 1-10 scores, and market recommendations can be mistaken for deterministic outcomes.

Mitigation: Treat reports as directional planning support and require human review before campaign, launch, or budget decisions.

Risk: Reports are designed for Korean-language output.

Mitigation: Confirm the intended audience can review Korean reports or request translation before relying on the output.

## Reference(s):

- [Vision Simulator Skill Page](https://clawhub.ai/dorongss/skills/vision-simulator)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown prediction report in Korean with scores, risks, and prioritized action items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include success probability and 1-10 scores; Pro simulations may incorporate live news, trend, and competitor-search summaries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
