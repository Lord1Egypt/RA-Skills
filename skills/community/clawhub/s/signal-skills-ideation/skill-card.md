## Description:

Turn findings already mined by podcast/review-scout into prioritized "build/test next" proposals, each citing the specific finding(s) that motivated it. Use when the user asks "what should we build next", "what's worth prioritizing", or wants a synthesis across research + reviews instead of another raw findings dump.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orensegal](https://clawhub.ai/user/orensegal)

### License/Terms of Use:

MIT-0

## Use Case:

Product and research teams use this skill to turn podcast and customer review findings into prioritized build, test, or further-research proposals. Each proposal cites its motivating findings and explains its effort, confidence, and a condition that could change the recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review has medium confidence and partial analysis; the skill changes proposal statuses, accesses local files, and writes reports.

Mitigation: Review the ledger status changes and local file access, and inspect generated reports before relying on their proposals.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/orensegal/skills/signal-skills-ideation)
- [Project homepage](https://github.com/OrenSegal/signal-skills)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, HTML]

**Output Format:** [Ranked proposal reports in Markdown or HTML]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Proposals cite source findings and describe effort, confidence, and a condition that could invalidate the idea.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
