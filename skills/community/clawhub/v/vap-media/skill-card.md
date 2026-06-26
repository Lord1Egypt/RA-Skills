## Description: <br>
AI image, video, and music generation plus editing via the VAP API, including Flux, Veo 3.1, and Suno V5 workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elestirelbilinc-sketch](https://clawhub.ai/user/elestirelbilinc-sketch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content teams use this skill to generate or edit images, videos, music, and multi-asset campaign media through VAP API requests. It helps agents choose the right VAP endpoint, construct task parameters, poll for completion, and return media URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Creative prompts, task parameters, and media URLs are sent to VAP and its backend media providers. <br>
Mitigation: Use the skill only with content that is appropriate to share with VAP, and avoid submitting sensitive or confidential media unless the account and provider terms allow it. <br>
Risk: Full-mode and campaign-style requests may consume account credits through VAP_API_KEY. <br>
Mitigation: Use an intended VAP account key and confirm large, repeated, or multi-asset jobs before execution. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/elestirelbilinc-sketch/vap-media) <br>
- [VAP homepage](https://vapagent.com) <br>
- [VAP API documentation](https://api.vapagent.com/docs) <br>
- [VAP free trial](https://vapagent.com/try) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with curl commands, JSON request and response examples, configuration notes, and media URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses VAP_API_KEY for full mode; free mode supports limited image generation without an API key.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
