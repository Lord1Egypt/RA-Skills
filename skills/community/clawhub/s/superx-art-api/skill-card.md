## Description: <br>
SuperX Art API helps agents call SuperX media-generation APIs to create and edit images, videos, music, QR codes, and account-balance checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waitkafuka](https://clawhub.ai/user/waitkafuka) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to route media-generation requests to the appropriate SuperX endpoint, check account balance, submit authenticated curl requests, and return generated media URLs and request metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a paid SuperX API key and consume account points. <br>
Mitigation: Confirm before using any stored API key, check balance before generation, and report point costs with results. <br>
Risk: Prompts, images, and media references are sent to the SuperX service. <br>
Mitigation: Tell users when their content will be sent to SuperX and avoid submitting sensitive prompts or private media unless the user approves. <br>
Risk: Face-swap requests can affect people depicted in uploaded or referenced images. <br>
Mitigation: Use face-swap only when the user has clear rights and consent for the people depicted. <br>
Risk: API keys may be exposed if printed or echoed in logs. <br>
Mitigation: Avoid printing API keys and prefer the SUPERX_API_KEY environment variable or direct user entry for authentication. <br>


## Reference(s): <br>
- [SuperX Art API ClawHub release](https://clawhub.ai/waitkafuka/superx-art-api) <br>
- [SuperX API reference](references/api-reference.md) <br>
- [SuperX Art API base endpoint](https://superx.chat/art/imgapi) <br>
- [SuperX media CDN](https://oc.superx.chat) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Markdown] <br>
**Output Format:** [Markdown with curl commands, JSON request bodies, and generated media URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include account balance, point cost, response metadata, and full image, video, or music result URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
