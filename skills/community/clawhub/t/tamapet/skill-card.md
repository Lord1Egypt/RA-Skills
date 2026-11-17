## Description:

Virtual pet game (Tamagotchi-style) with Telegram Mini App, social visits, friendship, playdates, mortality, and deep-link based launch behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mturac](https://clawhub.ai/user/mturac)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to launch and operate a Telegram Mini App virtual pet game with feeding, play, sleep, social visits, friendship, playdates, memorials, and shareable pet cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that the public backend can allow unauthenticated users to modify or access other users' pet data.

Mitigation: Do not expose the backend publicly until Telegram initData validation and user ID validation are implemented and reviewed.

Risk: The security guidance identifies possible storage path escape and output handling concerns.

Mitigation: Add path containment checks, output escaping, and data retention controls before public deployment.

Risk: The security guidance calls out missing CORS restrictions for public exposure.

Mitigation: Restrict CORS and deployment origins to the intended Telegram Mini App and reviewed hosting environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mturac/skills/tamapet)
- [Telegram Mini App](https://t.me/OpenClawTamagotchi_bot/pet)
- [README](README.md)
- [SKILL](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with plain-text Telegram deep links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces launch instructions and runtime guidance for a Telegram Mini App backed by local JSON storage and optional PNG card rendering.]

## Skill Version(s):

0.2.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
