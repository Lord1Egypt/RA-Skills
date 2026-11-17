## Description:

Maps game scenes to real-world travel plans with RPG-style adventure maps, using Python and FlyAI CLI to query flight, hotel, attraction, and food data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaokunv1](https://clawhub.ai/user/shaokunv1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel planners use this skill to turn a selected video game into a real-world pilgrimage itinerary with flights, hotels, attractions, food stops, Fliggy purchase links, an HTML adventure map, and a text questbook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generator can write files outside the intended folder.

Mitigation: Run it in an isolated working directory and constrain or review output paths and generated filenames before execution.

Risk: Generated maps can persist unsafe HTML from travel data.

Mitigation: Review generated HTML before opening it and require filename sanitization, HTML escaping, and URL allowlisting before broad deployment.

Risk: Travel searches may send user travel details through FlyAI.

Mitigation: Use only travel data the user is comfortable sending through FlyAI, and confirm remembered personal details before searches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shaokunv1/skills/rpg-travel)
- [Package metadata and runtime requirements](artifact/clawhub.json)
- [README](artifact/README.md)
- [Output format reference](artifact/references/output-format.md)
- [Pixel map template reference](artifact/references/pixel-map-template.md)
- [Style mapping reference](artifact/references/style-mapping.md)
- [Game locations reference](artifact/references/game-locations.md)
- [FlyAI command reference](artifact/references/flyai-commands.md)
- [Fliggy link reference](artifact/references/fliggy-links.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown-style guidance with JSON inputs, shell commands, and generated TXT/HTML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a questbook TXT file and an interactive HTML adventure map in the selected output directory; requires Python 3 and FlyAI CLI with user-configured credentials.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
