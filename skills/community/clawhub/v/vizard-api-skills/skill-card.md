## Description: <br>
Use when needing to clip long videos into short social media clips, edit short videos with subtitles or b-roll, publish clips to social platforms, or generate AI captions using Vizard.ai API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vizardai](https://clawhub.ai/user/vizardai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and marketing teams use this skill to automate Vizard.ai workflows for clipping long-form videos, editing short videos, generating social captions, and optionally publishing finished clips to connected social accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Vizard.ai API key and sends video content to Vizard.ai. <br>
Mitigation: Install only when using your own Vizard.ai account and avoid submitting video content that should not be shared with that service. <br>
Risk: The skill can publish videos to real connected social accounts. <br>
Mitigation: Before any publish-video call, require the agent to show the selected clip, target social account, caption or title, and publish time, then get explicit approval. <br>


## Reference(s): <br>
- [Vizard API Full Reference](artifact/api-reference.md) <br>
- [Vizard API Supported Languages](https://docs.vizard.ai/docs/supported-languages) <br>
- [Vizard API Rate Limits](https://docs.vizard.ai/docs/rate-limit) <br>
- [Vizard API Pricing](https://docs.vizard.ai/docs/pricing) <br>
- [ClawHub Skill Page](https://clawhub.ai/vizardai/vizard-api-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, API Calls, Configuration] <br>
**Output Format:** [Markdown with JSON and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Vizard REST endpoint guidance, request payloads, polling logic, social publishing parameters, and API key setup notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
