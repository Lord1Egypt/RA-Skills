## Description: <br>
Helps agents design mobile apps, create and edit screens, manage Sleek projects, and return rendered screenshots through the Sleek API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stefanofa](https://clawhub.ai/user/stefanofa) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to create or modify mobile app screens in Sleek, manage Sleek projects, and retrieve rendered screenshots for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Sleek API key to access and manage projects. <br>
Mitigation: Use a revocable SLEEK_API_KEY with only the scopes required for the requested task. <br>
Risk: Prompts or image URLs sent to Sleek may contain sensitive content. <br>
Mitigation: Avoid sending sensitive prompts or private image URLs unless the user explicitly approves sharing them with Sleek. <br>
Risk: The skill can delete Sleek projects when the API key has project write access. <br>
Mitigation: Require explicit user confirmation before deleting any Sleek project. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stefanofa/sleek-design-mobile-apps) <br>
- [Sleek](https://sleek.design) <br>
- [Sleek API keys](https://sleek.design/dashboard/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Markdown] <br>
**Output Format:** [Markdown with HTTP request examples and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SLEEK_API_KEY; may return PNG or WebP screenshots through Sleek.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
