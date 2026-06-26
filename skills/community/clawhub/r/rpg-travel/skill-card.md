## Description: <br>
Map game scenes to real-world travel plans with RPG-style adventure maps. Requires python3 and FlyAI CLI with configured credentials to query real flight/hotel/attraction data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaokunv1](https://clawhub.ai/user/shaokunv1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel planners use this skill to turn a game title or game-location travel intent into a game-themed itinerary. The skill maps virtual scenes to real-world places, queries travel options through FlyAI/Fliggy, and produces RPG-style questbook and adventure-map outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: FlyAI/Fliggy searches may involve third-party travel services and user travel preferences. <br>
Mitigation: Configure FlyAI credentials through the official CLI, not in chat, and install only if use of FlyAI/Fliggy is acceptable. <br>
Risk: Generated TXT and HTML itinerary files may contain personal trip details. <br>
Mitigation: Review generated files before sharing or publishing them. <br>
Risk: Opening generated HTML can contact third-party image hosts and store check-in progress in the browser. <br>
Mitigation: Open generated HTML in an appropriate local browser context and avoid sharing it without reviewing embedded image URLs and local-state behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shaokunv1/rpg-travel) <br>
- [Output format](references/output-format.md) <br>
- [Game locations](references/game-locations.md) <br>
- [FlyAI commands](references/flyai-commands.md) <br>
- [Fliggy links](references/fliggy-links.md) <br>
- [Style mapping](references/style-mapping.md) <br>
- [Pixel map template](references/pixel-map-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON payloads; runtime can write TXT questbook and HTML adventure map files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated itineraries may include travel links, embedded external image URLs, and browser-local check-in state.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
