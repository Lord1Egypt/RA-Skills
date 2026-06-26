## Description: <br>
同程旅行助手 lets an agent search Tongcheng travel options across hotels, flights, trains, buses, attraction tickets, multimodal transport, and vacation packages, returning current options with prices and booking links when available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel-focused agents and end users use this skill to compare Tongcheng travel search results for lodging, transport, attractions, and packaged trips. It is useful for itinerary planning and option discovery before the user completes any booking or payment on Tongcheng. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel search terms, dates, destinations, and preferences are sent to the skill publisher's cloud proxy. <br>
Mitigation: Avoid entering highly sensitive itinerary details unless the publisher's proxy is trusted. <br>
Risk: Prices, availability, and booking links may change after the skill returns results. <br>
Mitigation: Confirm current details and complete booking or payment only on the official Tongcheng page reached from returned links. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/tongcheng-travel-assistant) <br>
- [Publisher profile](https://clawhub.ai/user/travel-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-formatted travel search results with prices, schedules, ratings, availability summaries, and booking links when returned by the service.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are bounded result lists for Tongcheng travel categories; prices and availability can change, and booking or payment is completed outside the skill.] <br>

## Skill Version(s): <br>
1.2.0 (source: evidence.release.version and artifact/version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
