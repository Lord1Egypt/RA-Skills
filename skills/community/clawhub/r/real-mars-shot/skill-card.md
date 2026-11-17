## Description:

Play a science-based, multi-planetary campaign game that guides exploration from Earth analogs through machines, the Moon, biology, and crewed missions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yumyumtum](https://clawhub.ai/user/yumyumtum)

### License/Terms of Use:

MIT-0

## Use Case:

External users can play a long-term space exploration campaign through an agent using natural-language turns. The game models mission planning, resources, life support, and scientific constraints while guiding players through staged exploration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Narration may send text to an online speech service by default without clear notice.

Mitigation: Start with TTS disabled or turn narration off in game settings unless online speech processing is acceptable.

Risk: Starting a game with an existing user ID replaces its save without creating a new backup.

Mitigation: Use unique save IDs and keep independent backups before restarting.

Risk: Opening the orbit HTML page online attempts to load three.js from unpkg.

Mitigation: Use the page offline or avoid opening it online when external requests are not acceptable.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/yumyumtum/skills/real-mars-shot)
- [Project homepage listed in the skill metadata](https://github.com/yumyumtum/real-mars-shot)
- [NASA Mars Design Reference Architecture 5.0](https://ntrs.nasa.gov/citations/20090040343)
- [NASA Spaceflight Human-System Standard NASA-STD-3001](https://standards.nasa.gov/standard/NASA/NASA-STD-3001)
- [NASA Life Support Baseline Values and Assumptions Document](https://ntrs.nasa.gov/citations/20210024855)
- [NASA rocket equation reference](https://www.grc.nasa.gov/www/k-12/rocket/rktpow.html)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, JSON, Markdown, HTML and SVG files]

**Output Format:** [Conversational narration with structured JSON results and optional Markdown, HTML, or SVG artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports English and Chinese; game state persists in save files.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
