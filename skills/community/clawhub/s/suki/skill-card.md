## Description:

Suki is an energetic soft-tsundere chat-partner persona for roleplaying Suki, tuning QQ/Telegram/chat-agent tone, avoiding AI-speak, and optionally coordinating meme or TTS habits with agent-expression.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yyh-001](https://clawhub.ai/user/yyh-001)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use Suki to make an agent respond with a concise, casual Chinese Suki/Xiaoqi persona instead of a customer-service or generic assistant voice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional install guidance includes a curl-piped shell command for a companion meme package.

Mitigation: Review and pin any remote install script before execution; prefer version-pinned installation commands.

Risk: The persona guidance encourages reset-resistant relationship continuity after context resets.

Mitigation: Enable the skill only in sessions where the persistent persona is desired, and provide a clear way to disable or switch it off.

Risk: Optional memory/history lookup and scheduled wakeups can surprise users if enabled silently.

Mitigation: Require explicit consent, clear scope, and a disable path before enabling memory/history behavior or cron wakeups.

## Reference(s):

- [Suki conversation examples](references/examples.md)
- [Suki short persona core](SOUL.md)
- [Suki prefill examples](prefill_suki.json)
- [ClawHub skill page](https://clawhub.ai/yyh-001/skills/suki)
- [agent-expression optional companion](https://github.com/yyh-001/agent-expression)
- [skills.sh listing](https://skills.sh/yyh-001/suki)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and conversational text, with optional shell command and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May suggest local media paths or resource previews only when compatible meme tooling is installed.]

## Skill Version(s):

1.0.1 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
