## Description:

Módulo del Autopilot F100K que corre diariamente: caza el HECHO más reaccionable del día - un lanzamiento de IA, una movida de marketing de una marca grande, o un formato viral sin cara - evitando reaccionar a creadores del mismo nicho, elige un ganador con scoring y filtro de exclusión, genera un guion de reacción listo para grabar con la voz del usuario, y envía el digest por el canal configurado.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and F100K operators use this skill to run a daily viral-content radar, select one timely AI, brand marketing, or faceless viral signal, and receive a ready-to-record Spanish reaction script plus digest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the user's F100K configuration, including niche, keywords, delivery address, voice profile, and radar sources.

Mitigation: Install only when this configuration access is expected, and review the configured destination before running the daily radar.

Risk: The skill may use external search services and Apify/TikTok scraping when APIFY_TOKEN is available.

Mitigation: Confirm external-search use is acceptable, skip the TikTok lane when APIFY_TOKEN is absent, and show Apify cost only when Apify actually ran.

Risk: The artifact contains an email-versus-Telegram delivery inconsistency.

Mitigation: Clarify before use whether this OpenClaw release should deliver through Telegram or create a Gmail draft.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/radar-virales-f100k)
- [Publisher profile](https://clawhub.ai/user/formula100k)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown-style digest with inline shell and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one selected viral candidate, selection rationale, a 45-60 second Spanish reaction script, delivery confirmation, and optional Apify cost line when Apify runs.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
