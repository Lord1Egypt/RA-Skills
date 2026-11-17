## Description:

Diagnoses whether a small-scale result is likely to hold when scaled by testing it against false positives, population mismatch, situation mismatch, spillovers, and supply-side cost traps before committing to expansion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deciqai](https://clawhub.ai/user/deciqai)

### License/Terms of Use:

MIT-0

## Use Case:

Business operators, founders, investors, and strategy teams use this skill to pressure-test pilots, beta wins, single-market launches, franchise plans, and other scale decisions before investing in rollout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce overconfident scale guidance if the user cannot state the pilot's effect size, sample size, and selection method.

Mitigation: Apply the artifact's stop rule: stop at the false-positive vital sign, name the missing data, and require a confirmatory test before scale advice.

Risk: The skill shapes an agent toward a skeptical scale-readiness framework that may reject expansion until all five vital signs are addressed.

Mitigation: Use it for scale decisions where that posture is intended, and document which vital sign drives any recommendation to de-risk first or not scale.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deciqai/skills/voltage-effect)
- [Voltage Effect Sources](references/sources.md)
- [The Voltage Effect](https://www.penguinrandomhouse.com/books/652077/the-voltage-effect-by-john-a-list/)
- [What Can We Learn from Experiments?](https://www.aeaweb.org/articles?id=10.1257/aer.p20171115)
- [Why Economists Should Conduct Field Experiments and 14 Tips for Pulling One Off](https://www.aeaweb.org/articles?id=10.1257/jep.25.3.3)
- [Voltage Effect Machine-Readable Metadata](https://www.deciqai.com/s/voltage-effect.json)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown diagnosis with a structured vital-sign checklist, weakest-link assessment, de-risking test, and scale verdict.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May pause for user input in coach mode before completing the diagnosis.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
