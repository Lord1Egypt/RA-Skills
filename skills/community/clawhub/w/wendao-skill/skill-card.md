## Description: <br>
Provides travel booking, itinerary planning, and local recommendation assistance through Ctrip Wendao. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trips-ai](https://clawhub.ai/user/trips-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to send natural-language travel requests to Ctrip Wendao for hotels, flights, train tickets, attraction recommendations, and itinerary planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the user's travel query and API token to an external Ctrip Wendao endpoint. <br>
Mitigation: Verify the publisher, Ctrip homepage, and endpoint before use; prefer WENDAO_API_KEY and do not log, persist, or echo complete tokens. <br>
Risk: Travel prompts may contain sensitive personal, schedule, location, or preference details. <br>
Mitigation: Avoid sharing highly sensitive details unless needed, and apply the operator's data-handling policy before submitting prompts. <br>
Risk: Returned Markdown may include third-party links, offers, marketing text, or travel information that could be inaccurate or unsuitable. <br>
Mitigation: Treat returned content as external content; review, filter, or summarize links and offers according to product policy before showing them to users. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/trips-ai/wendao-skill) <br>
- [Ctrip Wendao OpenClaw Homepage](https://www.ctrip.com/wendao/openclaw) <br>
- [Ctrip Wendao Skill Endpoint](https://wendao-skill-prod.ctrip.com/skill/query) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash and JSON-over-curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WENDAO_API_KEY plus curl and jq; sends the user's travel query and token to the disclosed Ctrip Wendao endpoint and returns Markdown that may include external links or offers.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
