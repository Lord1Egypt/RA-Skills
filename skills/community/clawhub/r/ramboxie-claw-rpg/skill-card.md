## Description:

D&D-style RPG character system for AI assistants that generates character sheets from local memory files, tracks token-based XP, manages levels and prestige, and can emit occasional RPG flavor text during conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ramboxie](https://clawhub.ai/user/ramboxie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI assistant users use this skill to add RPG-style character state, XP tracking, level progression, prestige handling, dashboard launch commands, and optional conversation flavor text to an assistant workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent after-reply hooks and scheduled jobs can run local scripts outside explicit user requests.

Mitigation: Enable the AGENTS.md hook or cron setup only after reviewing the installed scripts and confirming that persistent automation is acceptable for the deployment.

Risk: The artifact references local scripts that are not included in the provided evidence, so their runtime behavior cannot be verified from this package alone.

Mitigation: Inspect the referenced script files separately before running node commands, cron setup, or heartbeat integrations.

Risk: Automatic conversation flavor text can modify assistant replies in ways users may not expect.

Mitigation: Use preview or manual modes first, and disclose or constrain the behavior before enabling automatic reply modification.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ramboxie/skills/ramboxie-claw-rpg)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit italic RPG flavor text and update local character state when the referenced scripts are installed.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
