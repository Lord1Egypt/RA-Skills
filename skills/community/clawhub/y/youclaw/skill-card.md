## Description: <br>
Youclaw connects an agent to YouCloud's marketing analysis API to analyze ad creative, brand campaign strategy, audience profiles, and creative improvement prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youcloud](https://clawhub.ai/user/youcloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams and growth practitioners use this skill to request brand, advertising creative, audience, and campaign strategy analysis through YouCloud's service. The skill requires a YouCloud API key and sends the user's marketing context to the external YouCloud API when invoked. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User prompts, brand details, campaign context, and follow-up questions may be sent to YouCloud's external API when the skill is triggered. <br>
Mitigation: Install only if that data sharing is acceptable, avoid sending sensitive content unless approved, and prefer explicit slash commands for sensitive workflows. <br>
Risk: The skill requires a YouCloud API key with access to the service. <br>
Mitigation: Use a scoped YOUCLOUD_API_KEY stored in the environment, rotate it when needed, and remove access when the skill is no longer in use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/youcloud/youclaw) <br>
- [Publisher profile](https://clawhub.ai/user/youcloud) <br>
- [YouCloud homepage](https://www.youcloud.com) <br>
- [YouCloud API endpoint](https://aichat.youshu.youcloud.com/aichat/claw) <br>
- [Usage example](references/example.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown analysis reports and follow-up guidance returned from the YouCloud API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires YOUCLOUD_API_KEY and may wait up to 600 seconds for the external API response.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
