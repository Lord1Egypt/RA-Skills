## Description:

Supplement Research helps agents answer supplement, dosing, safety, interaction, evidence-quality, stack-building, timing, experiment-tracking, and research-monitoring questions using the SupStack database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drbaher](https://clawhub.ai/user/drbaher)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to research supplements, compare evidence quality, check safety and interactions, build supplement stacks, manage supplement timing, track N-of-1 experiments, and monitor new supplement studies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can maintain a long-lived local health profile containing sensitive supplement, medication, condition, allergy, demographic, preference, interest, and experiment data.

Mitigation: Review or disable automatic profile writes before use, keep the workspace private, and periodically inspect or delete ~/.openclaw/workspace/supstack data.

Risk: The research monitor can create ongoing monitoring state and periodic research checks.

Mitigation: Confirm monitoring intent before setup, review or disable cron monitoring, and clear monitor state when updates are no longer wanted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/drbaher/skills/supstack)
- [Publisher Profile](https://clawhub.ai/user/drbaher)
- [SupStack Ashwagandha Page](https://supstack.me/supplements/ashwagandha)
- [SupStack Magnesium Page](https://supstack.me/supplements/magnesium)
- [SupStack Glycine Page](https://supstack.me/supplements/glycine)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell-command invocations and JSON-derived summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include supplement page links, evidence scores, safety notes, timing plans, research briefings, profile updates, and local monitoring state.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
