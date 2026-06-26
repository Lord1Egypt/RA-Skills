## Description: <br>
Generate images using curl and the SkillBoss API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MarjorieBroad](https://clawhub.ai/user/MarjorieBroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate an image from a text prompt through the SkillBoss API and inspect the returned image URL or JSON response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The image generation command sends the prompt and API key to SkillBoss. <br>
Mitigation: Use a limited or revocable SKILLBOSS_API_KEY and avoid sensitive prompts unless the external service is trusted for the intended use. <br>
Risk: The optional Check IP helper contacts httpbin.org and exposes the caller's public IP to that service. <br>
Mitigation: Run the helper only when public-IP disclosure to httpbin.org is acceptable. <br>


## Reference(s): <br>
- [Quick Img V2 on ClawHub](https://clawhub.ai/MarjorieBroad/quick-img) <br>
- [MarjorieBroad publisher profile](https://clawhub.ai/user/MarjorieBroad) <br>
- [SkillBoss](https://www.skillboss.co) <br>
- [SkillBoss run API endpoint](https://api.heybossai.com/v1/run) <br>
- [httpbin IP check endpoint](https://httpbin.org/get) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash and JavaScript command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The image generation command prints an image URL when present, otherwise the API JSON response; the optional IP helper prints the caller's public IP origin.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
