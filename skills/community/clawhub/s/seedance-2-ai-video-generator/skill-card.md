## Description: <br>
Generates videos from text prompts, image references, and other media references through the Loova Seedance 2.0 API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hjianfeng](https://clawhub.ai/user/hjianfeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to submit Loova Seedance 2.0 video generation jobs from prompts or media references, poll for completion, and return the resulting video URL or API response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, media URLs, and local files passed with --files are sent to Loova. <br>
Mitigation: Use the skill only with media approved for Loova processing, avoid sensitive or regulated content unless approved, and disclose the third-party API transfer to users. <br>
Risk: The Loova API key grants access to a third-party video generation service. <br>
Mitigation: Use a dedicated Loova API key loaded from the environment or .env, never hardcode credentials, and rotate the key if exposed. <br>
Risk: Python dependencies are installed from package indexes at setup time. <br>
Mitigation: Install in a virtual environment and pin or review dependency versions before production use. <br>


## Reference(s): <br>
- [Loova API](https://api.loova.ai/api) <br>
- [Loova account API page](https://loova.ai/api) <br>
- [ClawHub skill page](https://clawhub.ai/hjianfeng/seedance-2-ai-video-generator) <br>
- [API reference](reference.md) <br>
- [Quick start](QUICK_START.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May print task status and final result JSON, including a video URL when generation succeeds.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
