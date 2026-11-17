## Description:

All-in-one Chinese fortune-telling covering BaZi, ZiWei DouShu, QiMen DunJia, I Ching, feng shui, marriage compatibility, and daily horoscope push, built on local Node.js tooling without an external API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiajiaoy](https://clawhub.ai/user/jiajiaoy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use Yunshi to produce Chinese astrology and divination readings, register local birth-profile context, compare relationship compatibility, assess feng shui questions, and configure daily fortune pushes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive birth details and preferences may persist in OpenClaw memory and, when push is enabled, scheduled runtime jobs.

Mitigation: Collect only necessary profile details, avoid family or children's exact birth details without permission, and delete profile memory after disabling push jobs.

Risk: Daily fortune push scheduling has weak cleanup and scheduling safeguards.

Mitigation: Use only normal HH:MM push times, review enabled push channels, and turn off scheduled pushes before removing profile records.

Risk: Fortune-telling output may be mistaken for reliable health, financial, legal, or relationship advice.

Mitigation: Present readings as interpretive guidance only and require professional advice for high-impact decisions.

## Reference(s):

- [Yunshi ClawHub listing](https://clawhub.ai/jiajiaoy/skills/yunshi)
- [Publisher profile](https://clawhub.ai/user/jiajiaoy)
- [OpenClaw](https://openclaw.ai)
- [Registration workflow](docs/注册流程.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured text with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Node.js >=18, the iztro package, optional OPENCLAW_KNOWLEDGE_DIR reference material, and OpenClaw-managed memory or scheduled push state.]

## Skill Version(s):

1.3.1 (source: server release metadata, package.json, _meta.json, and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
