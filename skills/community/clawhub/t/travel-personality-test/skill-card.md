## Description: <br>
Runs a 10-question travel personality quiz and recommends destinations that match the user's travel style, using FlyAI-backed live travel signals when available and local fallback recommendations when needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gwhite-qi](https://clawhub.ai/user/gwhite-qi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to explore their current travel style through a lightweight quiz and receive destination recommendations based on the resulting persona. Agents can also provide travel planning guidance, including flight and hotel prompts, after the quiz is complete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and use the external FlyAI dependency for live travel recommendations without sufficiently clear approval. <br>
Mitigation: Require explicit user approval before running any FlyAI installation or external query, and review the FlyAI dependency separately before deployment. <br>
Risk: FlyAI usage may require an API key and can expose secrets if users paste credentials into chat or shell history. <br>
Mitigation: Store FlyAI credentials in an approved secret store or environment management system, and avoid placing API keys in chat transcripts or command history. <br>


## Reference(s): <br>
- [FlyAI skill dependency](https://github.com/alibaba-flyai/flyai-skill) <br>
- [ClawHub release page](https://clawhub.ai/gwhite-qi/travel-personality-test) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown conversational responses with optional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use FlyAI for live destination, search trend, flight, and hotel signals after quiz completion; falls back to local city recommendations when FlyAI is unavailable.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
