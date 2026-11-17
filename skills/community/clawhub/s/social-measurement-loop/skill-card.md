## Description:

Builds a weekly organic-social measurement readout with locked engagement-rate denominators, median per-post rollups, optional EMV translation kept out of scores, community-health metrics, and keep/stop/try learnings for the next cycle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing and community operators use this skill to run weekly organic-social measurement readouts, lock engagement-rate denominators, compare median per-post performance, and carry keep/stop/try learnings into the next planning cycle.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Social analytics exports can include personal or confidential data unrelated to the measurement task.

Mitigation: Provide only the channel, GA4/GSC, or community exports needed for the period and remove unrelated personal or confidential fields before use.

Risk: Saved readouts and promoted learnings may retain sensitive campaign observations across sessions.

Mitigation: Use save and promote steps only when retention is intended, and review what will be written to memory before confirming.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/social-measurement-loop)
- [Source homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown readout with metric dictionary, channel rollups, hypotheses, and write-back list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rates name their numerator and denominator; organic and boosted metrics are separated; EMV is labeled as estimated translation only when requested.]

## Skill Version(s):

19.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
