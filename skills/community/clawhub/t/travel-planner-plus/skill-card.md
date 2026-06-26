## Description: <br>
Generates personalized travel itineraries by collecting trip requirements, searching attractions, hotels, and food, using Baidu Maps for routing, and producing a Word document for delivery to the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ggyybb](https://clawhub.ai/user/ggyybb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and assistants use this skill to turn trip goals, destination, duration, audience, and constraints into a structured travel plan with attractions, meals, lodging suggestions, route timing, and a deliverable Word document. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trip details and itinerary preferences may be sent to web search providers, Baidu Maps APIs, and Feishu file delivery. <br>
Mitigation: Avoid including sensitive personal details, review the recipient before sending, and confirm the generated document before sharing. <br>
Risk: The skill requires a Baidu Maps API key for geocoding and routing. <br>
Mitigation: Use a dedicated Baidu Maps API key with limited quota and avoid storing or sharing broader credentials. <br>
Risk: Travel, restaurant, hotel, and routing details may become outdated or incomplete. <br>
Mitigation: Review the generated itinerary and verify important bookings, opening hours, reservations, and transport details before travel. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ggyybb/travel-planner-plus) <br>
- [Travel guide output template](references/output-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with API calls and a generated Word document] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces itinerary tables, transportation summaries, lodging and food recommendations, practical tips, and a disclaimer.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
