## Description: <br>
AI video generation workflow on Volcengine. Use when users need text-to-video, image-to-video, generation parameter tuning, or async task troubleshooting for video jobs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to plan and operate Volcengine text-to-video or image-to-video generation jobs, tune generation parameters, poll asynchronous task status, and handle retry or failure guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, input media, task IDs, and resulting URLs may be handled through Volcengine during normal use. <br>
Mitigation: Avoid sensitive or rights-restricted media unless use of Volcengine for that content matches privacy and licensing requirements. <br>
Risk: Video generation jobs can fail or require retries during asynchronous processing. <br>
Mitigation: Log task IDs, use bounded polling intervals, surface failure reasons, and provide rerun suggestions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinience/volcengine-ai-video-generation) <br>
- [sources.md](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown guidance with optional shell commands, API workflow steps, task metadata, and final video URL or path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task IDs, polling status, failure reasons, retry suggestions, and resulting video URLs or paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
