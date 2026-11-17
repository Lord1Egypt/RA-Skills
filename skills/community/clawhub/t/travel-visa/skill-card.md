## Description:

A travel visa consultation and pre-trip verification advisor for outbound travelers who know their destination and need visa requirements, application locations, and itinerary coordination guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to check visa requirements, identify application paths and locations, plan timing, and coordinate nearby itinerary needs such as lodging or transit. It is intended for actionable pre-trip checklists and visa-path recommendations, not broad destination inspiration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install a mutable third-party CLI globally.

Mitigation: Prefer a local, pinned CLI install where possible, avoid administrator or root execution, and review generated commands before running them.

Risk: Visa information and provider links may be incomplete, outdated, or commercially routed.

Mitigation: Verify visa requirements, timelines, and links against official government or consular sources before booking travel or taking application action.

## Reference(s):

- [FlyAI homepage](https://open.fly.ai/)
- [Playbooks](references/playbooks.md)
- [Templates](references/templates.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with headings, checklists, comparison tables, links, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include provider image URLs and booking or jump links when returned by FlyAI/Fliggy data.]

## Skill Version(s):

1.0.0 (source: SKILL.md metadata.version and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
