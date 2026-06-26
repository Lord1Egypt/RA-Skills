## Description: <br>
AI image, video, and music generation and editing via the VAP API, with support for Flux, Veo 3.1, and Suno V5. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elestirelbilinc-sketch](https://clawhub.ai/user/elestirelbilinc-sketch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to generate images, videos, and music, and to edit or enhance media through VAP API workflows. It can return generated media URLs, operation status, and curl-based API commands for free or authenticated usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Media prompts, media URLs, and editing instructions are sent to VAP and its backend providers. <br>
Mitigation: Avoid private or sensitive media links and prompts unless the user is comfortable sharing them with those services. <br>
Risk: Authenticated workflows use the user's VAP account features, quota, or balance. <br>
Mitigation: Set VAP_API_KEY only when the user intends to use account-backed generation or editing features. <br>


## Reference(s): <br>
- [VAP Homepage](https://vapagent.com) <br>
- [VAP API Docs](https://api.vapagent.com/docs) <br>
- [VAP Showcase Repository](https://github.com/vapagentmedia/vap-showcase) <br>
- [ClawHub Skill Page](https://clawhub.ai/elestirelbilinc-sketch/vap-multimedia-generation) <br>
- [Publisher Profile](https://clawhub.ai/user/elestirelbilinc-sketch) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown with curl commands, JSON response examples, and generated media URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require curl and VAP_API_KEY for authenticated image, video, music, and editing workflows.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
