## Description:

Qiqing Liuyu helps an agent write and respond in a strongly Chinese-localized, emotionally expressive voice with clearer opinions, tone rules, and AI-style text checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lniosy](https://clawhub.ai/user/lniosy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to shape Chinese writing, conversation, and review workflows that need human-like tone, explicit viewpoints, emotional response, and de-AI-style checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent personality overrides can take precedence over existing identity or behavior settings.

Mitigation: Keep the skill opt-in for writing and tone work; do not copy its recommended override into IDENTITY.md or SOUL.md unless that persistent behavior is deliberately desired.

Risk: Opinionated emotional style can create inappropriate certainty or bias in sensitive domains.

Mitigation: Preserve neutral handling for medical, legal, political, financial, and other high-impact topics, and review outputs before use.

## Reference(s):

- [Qiqing Liuyu on ClawHub](https://clawhub.ai/lniosy/skills/qiqing-liuyu)
- [Chinese Localization Guide](references/chinese-localization.md)
- [Emotion Response Rules](references/emotion-rules.md)
- [Opinion Expression Framework](references/opinion-framework.md)
- [De-AI Pattern Library](references/de-ai-patterns.md)
- [Seven Emotions and Six Desires Framework](references/seven-emotions-six-desires.md)
- [Human-Style Writing Guide](references/voice-guide.md)
- [OpenPersona](https://github.com/acnlabs/OpenPersona)
- [evolving_personality](https://github.com/agent-topia/evolving_personality)
- [SillyTavern](https://github.com/SillyTavern/SillyTavern)
- [soul.md community](https://openclawsoul.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Natural-language text or Markdown with optional shell command snippets and plain-text checker reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Strongly Chinese-localized and opinionated style guidance; includes an optional local text checker script.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
