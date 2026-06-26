## Description: <br>
Guide staged text-to-video generation from a rough user idea to ranked video type options, parameter tuning, prompt preview, and final Volcengine Ark video generation via bundled helper scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xxxxxxxxxxxxxxxxxxx20gex](https://clawhub.ai/user/xxxxxxxxxxxxxxxxxxx20gex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn a rough video idea into ranked video type choices, tuned parameters, a transparent prompt preview, and a confirmed Volcengine Ark generation request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video prompts and generation requests are sent to Volcengine Ark and may contain sensitive personal or business information. <br>
Mitigation: Review the final prompt before confirmation and avoid including secrets or sensitive personal or business data. <br>
Risk: The generator uses Ark API credentials and supports an alternate task endpoint through ARK_VIDEO_TASKS_URL. <br>
Mitigation: Use a dedicated Ark API key and leave ARK_VIDEO_TASKS_URL unset unless the alternate endpoint is trusted. <br>
Risk: Generated video results can fail remotely, time out during polling, or differ from the user's intent. <br>
Mitigation: Use the staged preview and explicit confirmation flow before generation, then inspect the returned status, task id, output path, and video URL. <br>


## Reference(s): <br>
- [Usage Guide](references/usage-guide.md) <br>
- [Video Types](references/video-types.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and generated JSON from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow asks for final prompt confirmation before generation and reports the downloaded file path, task id, status, and video URL when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
