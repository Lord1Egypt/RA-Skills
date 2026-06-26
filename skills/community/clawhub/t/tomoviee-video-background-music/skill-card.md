## Description: <br>
Generate music tailored to video content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wondershare-boop](https://clawhub.ai/user/wondershare-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to call Tomoviee/Wondershare video soundtrack workflows, submit a video URL with optional style guidance, and retrieve generated background music results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video URLs and prompts are sent to Tomoviee/Wondershare for external media processing. <br>
Mitigation: Use public or non-sensitive media where possible and avoid submitting confidential prompts or private video URLs. <br>
Risk: Generated Basic auth tokens can expose API credentials if copied into logs, shell history, or shared transcripts. <br>
Mitigation: Handle tokens as secrets, avoid printing them in shared contexts, and rotate credentials if exposure is suspected. <br>
Risk: Broad bundled reference documents may describe APIs outside this skill's video soundtrack workflow. <br>
Mitigation: Treat the references as background and use this skill only for the Tomoviee video soundtrack API behavior described in the skill. <br>


## Reference(s): <br>
- [Tomoviee Developer Portal](https://www.tomoviee.ai/developers.html) <br>
- [Tomoviee API Documentation](https://www.tomoviee.ai/doc/) <br>
- [Tomoviee Audio Generation APIs](references/audio_apis.md) <br>
- [Tomoviee Prompt Engineering Guide](references/prompt_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown guidance with Python and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow uses Tomoviee API credentials, submits external video URLs and prompts for processing, and polls asynchronous task results.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
