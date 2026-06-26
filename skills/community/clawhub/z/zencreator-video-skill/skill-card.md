## Description: <br>
Guides an agent through using ZenCreator.pro to generate AI videos from images or videos with model selection, credit awareness, and browser automation steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Makforce](https://clawhub.ai/user/Makforce) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agent users and developers use this skill to operate a logged-in ZenCreator.pro session for image-to-video, video-to-video, and lipsync generation. It is most relevant when the user has a ZenCreator account, available credits, and media prompts or files ready for generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to operate a logged-in ZenCreator browser session. <br>
Mitigation: Use a dedicated Chrome profile logged into only ZenCreator and review each browser action before it is performed. <br>
Risk: The workflow can involve sensitive media uploads and adult-content generation. <br>
Mitigation: Confirm the exact media file and prompt before upload, and avoid identifying, non-consensual, regulated, or otherwise sensitive content. <br>
Risk: Generation may spend paid credits. <br>
Mitigation: Verify the selected model, quality setting, duration, and credit cost before starting generation. <br>


## Reference(s): <br>
- [ZenCreator.pro](https://zencreator.pro) <br>
- [ZenCreator App](https://app.zencreator.pro) <br>
- [ClawHub Skill Page](https://clawhub.ai/Makforce/zencreator-video-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Browser automation steps] <br>
**Output Format:** [Markdown with inline shell commands and browser action examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output for operating a browser session, selecting generation options, uploading media, and downloading generated results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
