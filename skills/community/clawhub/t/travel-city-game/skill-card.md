## Description: <br>
Generates a three-node, game-like travel itinerary H5 page for a city using FlyAI travel product search results, AI-written narrative copy, and real Fliggy booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hongweisong1999](https://clawhub.ai/user/hongweisong1999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-content builders use this skill to turn a city name into an interactive travel route that combines real FlyAI search results, narrative itinerary copy, booking links, and a local HTML preview. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill invokes the third-party FlyAI CLI and may use FLYAI_API_KEY when configured. <br>
Mitigation: Install FlyAI only from a trusted source, review its permissions before use, and keep API keys in the local environment instead of embedding them in generated files. <br>
Risk: The skill writes generated HTML under outputs and starts a local preview server that opens a browser tab. <br>
Mitigation: Review the generated itinerary and links before sharing, and stop the preview server when it is no longer needed. <br>
Risk: The optional deployment step can make the generated itinerary publicly accessible. <br>
Mitigation: Deploy only after confirming the content, booking links, and any destination-specific details are suitable for public access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hongweisong1999/travel-city-game) <br>
- [FlyAI dependency skill](https://clawhub.ai/yealexchen/flyai) <br>
- [FlyAI platform](https://flyai.open.fliggy.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON-like data structures, and generated HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a static H5 itinerary page under outputs and may start a localhost preview server.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
