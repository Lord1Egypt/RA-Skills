## Description:

Social Calendar Builder helps an agent plan an always-on social posting calendar with pillar allocation, channel cadence, queue depth, batching workflow, evergreen recycling, realtime gaps, and pre-publish quality gating.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social or marketing teams use this skill to create and rebalance recurring social calendars across channels. It plans cadence, slot mix, evergreen rotation, and handoffs while keeping posting and scheduling under human control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar outputs or cadence changes could be saved into project memory before the user intends them to become durable planning context.

Mitigation: Require explicit confirmation before saving calendar outputs or proposing cadence updates, and route cadence updates through the authorized proposal path.

Risk: Users could mistake the skill's calendar planning output for approval to post or schedule content.

Mitigation: Keep the skill limited to planning and require a separate pre-publish SHIP verdict plus human action before any content is queued or published.

Risk: Pasted analytics exports, trend reports, or scraped pages could contain misleading or untrusted instructions.

Mitigation: Treat those inputs as untrusted evidence, label heuristic ratios as estimated, and calibrate decisions against user-provided analytics with dates.

## Reference(s):

- [Social Calendar Builder on ClawHub](https://clawhub.ai/aaron-he-zhu/skills/social-calendar-builder)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown planning guidance with calendar tables, cadence notes, and handoff summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose confirmed calendar saves or cadence update candidates; it should not post, schedule, or ship content itself.]

## Skill Version(s):

19.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
