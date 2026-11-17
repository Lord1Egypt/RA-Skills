## Description:

Monitor WhatsApp groups to dynamically detect people who should be congratulated. It identifies keywords (e.g., "birthday", "congratulations") and the person's name using a score-based system, then automatically sends a random customizable congratulatory message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero-astro](https://clawhub.ai/user/zero-astro)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal automation developers use this skill to monitor WhatsApp group messages for birthday or congratulatory context and send a configurable congratulation when confidence thresholds are met.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can monitor all WhatsApp groups, retain private message text, run on a schedule, and automatically send messages.

Mitigation: Keep simulation mode enabled until behavior is reviewed, use a group allowlist and explicit consent before live sending, and install only when scheduled WhatsApp access is acceptable.

Risk: Security evidence reports a command-injection flaw related to shell command execution.

Mitigation: Do not use the current script on sensitive accounts until shell command execution is fixed and reviewed.

Risk: Private message text can be retained in local state while the skill tracks processed messages and detected names.

Mitigation: Avoid sensitive accounts or groups until plaintext message retention is addressed, and review local state handling before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zero-astro/skills/whatsapp-happybday)
- [Project homepage](https://github.com/zero-astro/whatsapp-happybday)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and Python console output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send WhatsApp messages through wacli when simulation mode is disabled; otherwise emits dry-run and status text.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
