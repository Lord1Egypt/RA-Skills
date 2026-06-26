## Description: <br>
Video Edit - Pro Pack on RunComfy routes existing-video edit requests to matching RunComfy model endpoints for restyling, background or outfit swaps, motion transfer, color grading, and similar transformations up to 1080p. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content teams use this skill to convert natural-language video edit requests into RunComfy CLI runs for existing clips. It helps select a suitable RunComfy endpoint and prepare the prompt, media URL inputs, and output settings for video editing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video, reference images, prompts, and related URLs may be sent to RunComfy for processing. <br>
Mitigation: Review inputs before running the CLI and avoid submitting sensitive media unless the user's policy allows RunComfy processing. <br>
Risk: Video edit runs may consume RunComfy account credits. <br>
Mitigation: Confirm the selected route, input media, and requested edit before executing the generated RunComfy command. <br>
Risk: User-provided media URLs may point to untrusted or unintended content. <br>
Mitigation: Inspect or restrict external URLs according to the deployment's content-handling policy before using them in RunComfy requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kalvinrv/video-edit-runcomfy) <br>
- [RunComfy homepage](https://www.runcomfy.com) <br>
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=video-edit-runcomfy) <br>
- [RunComfy model catalog](https://www.runcomfy.com/models?utm_source=clawhub&utm_medium=skill&utm_campaign=video-edit-runcomfy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the RunComfy CLI, RunComfy authentication, and user-provided video or image URLs.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
