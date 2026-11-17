## Description:

SkillTree helps an agent personalize itself by analyzing recent conversation history, recommending a role, tracking ability growth, and showing concise progress cards and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xraini](https://clawhub.ai/user/0xraini)

### License/Terms of Use:


## Use Case:

External users and agent operators use SkillTree to make an assistant adapt its tone, depth, speed, and personalization over time. It is intended for agents that can analyze prior conversations, maintain profile or snapshot data, and present progress through text cards, growth paths, and quick commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically profiles recent conversations and stores profile or snapshot data for personalization.

Mitigation: Enable it only with user awareness, keep profile data inspectable, and provide clear reset, rollback, and deletion paths.

Risk: The efficiency path encourages fewer confirmation prompts and can affect actions such as email, calendar, file, message, purchase, sharing, or deletion workflows.

Mitigation: Require explicit confirmation for external, sensitive, financial, irreversible, or destructive actions, and provide undo where possible.

Risk: Companion memory may retain personal preferences or emotional context from conversations.

Mitigation: Avoid enabling persistent Companion memory unless users can review and delete remembered details.

## Reference(s):

- [SkillTree ClawHub listing](https://clawhub.ai/0xraini/skills/skilltree)
- [README.en.md](artifact/README.en.md)
- [SKILL.en.md](artifact/SKILL.en.md)
- [ABILITIES.en.md](artifact/ABILITIES.en.md)
- [CLASSES.en.md](artifact/CLASSES.en.md)
- [GROWTH.en.md](artifact/GROWTH.en.md)
- [DISPLAY.en.md](artifact/DISPLAY.en.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown and plain-text conversation cards with command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces profile summaries, class and growth-path recommendations, ability cards, weekly reports, rollback/reset prompts, and short status outputs.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
