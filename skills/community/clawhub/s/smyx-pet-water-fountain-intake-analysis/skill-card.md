## Description:

Analyzes pet water-fountain videos to estimate each pet’s drinking frequency, session duration, and daily intake, compare results with historical patterns, and flag notable changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Pet owners and caregivers can submit water-fountain footage to review estimated drinking patterns for each pet and compare them with historical records. Results provide health-related context, not a diagnosis or treatment recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Videos are processed remotely, and the skill may register an account and store personal details or tokens locally.

Mitigation: Share only footage you are authorized to submit, review the configured service destination and local data handling, and protect credentials from exposure.

Risk: Scanner coverage was partial, and the security review recommends checking for credential handling and behavior beyond pet-water analysis.

Mitigation: Review the skill and its configuration before use; proceed only if its data handling and service destination are acceptable.

Risk: Water intake is estimated from video observations and may not reflect a pet’s actual intake or health condition.

Mitigation: Treat changes as informational and consult a veterinarian about health concerns; do not use the report as a diagnosis or treatment plan.

## Reference(s):

- [Pet water fountain intake analysis API notes](references/api_doc.md)
- [Analysis API details](skills/smyx_analysis/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, JSON]

**Output Format:** [Structured analysis or historical report, returned as text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Drinking volume is estimated from observed frequency and duration; it is not directly measured and is not a medical diagnosis.]

## Skill Version(s):

1.0.15 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
