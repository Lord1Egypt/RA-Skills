## Description: <br>
Generates images through the NanaBanana 2 or NanaBanana Pro models using the api.wuyinkeji.com image service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Riage](https://clawhub.ai/user/Riage) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users ask an agent to create images for daily drawing tasks, text images, drafts, high-quality product artwork, cinematic images, or realistic final artwork. The skill guides the agent to choose NanaBanana 2 by default and NanaBanana Pro when the user explicitly requests higher quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to a third-party image service and may contain private or sensitive details. <br>
Mitigation: Use only prompts appropriate for the service and avoid sensitive, private, or regulated content. <br>
Risk: The API key is included in API requests and polling URLs. <br>
Mitigation: Use a dedicated key with limited exposure, avoid sharing request URLs, and rotate the key if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Riage/skill-paintinginterface) <br>
- [Wuyin Keji API host](https://api.wuyinkeji.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, guidance] <br>
**Output Format:** [Text and Markdown-style instructions with JSON request examples and <qqimg> image URL markup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a user-provided API key, English image prompts, optional size and aspect-ratio parameters, and polling for up to about 60 seconds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
