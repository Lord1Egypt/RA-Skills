## Description: <br>
Helps agents clarify incomplete travel requests in Chinese, propose budget-aware itineraries, and optionally use FlyAI CLI searches for hotels, points of interest, and flights when enough trip details are available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[david-cai-gpt](https://clawhub.ai/user/david-cai-gpt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to turn vague Chinese-language trip ideas into clarified constraints, destination directions, and itinerary-level recommendations. When dates, locations, and budget limits are known, it can guide FlyAI CLI searches for travel options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill's FlyAI command examples disable TLS certificate verification, which can expose online travel searches to interception or untrusted endpoints. <br>
Mitigation: Do not run FlyAI commands with NODE_TLS_REJECT_UNAUTHORIZED=0; resolve certificate or proxy trust issues before sharing travel details with the CLI or service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/david-cai-gpt/travel-schedule-brainstrom) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Chinese Markdown with optional bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the user's stated travel constraints directly and asks one clarification question at a time when required details are missing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
