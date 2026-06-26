## Description: <br>
RHSkill lets OpenClaw agents call the RunningHub AI Platform directly for text-to-image, image-to-image, video, audio, storage, and chained workflow tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[airix315](https://clawhub.ai/user/airix315) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and OpenClaw users use this skill to submit RunningHub AI app jobs, query task status, pass outputs between chained workflows, and optionally route generated media to Baidu Netdisk or Google Drive. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, input media, and generated outputs may be sent to RunningHub and, when cloud storage is selected, to Baidu Netdisk or Google Drive. <br>
Mitigation: Use storage mode none for sensitive work, avoid regulated or confidential media, and review third-party service terms before deployment. <br>
Risk: The skill can download outputs, extract ZIP files, and invoke local shell commands for cloud upload paths. <br>
Mitigation: Review outputs before extraction or upload, restrict project names to safe values, and run the skill in a least-privilege agent environment. <br>


## Reference(s): <br>
- [RunningHub](https://www.runninghub.cn) <br>
- [RunningHub International](https://www.runninghub.ai) <br>
- [OpenClaw Docs](https://docs.openclaw.ai) <br>
- [RHMCP GitHub](https://github.com/AIRix315/RHMCP) <br>
- [Shared RunningHub Apps](references/shared-apps.json) <br>
- [Configuration Template](references/config-template.json) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [JSON task results, URLs, cloud storage links, and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RUNNINGHUB_API_KEY and may return RunningHub-hosted URLs, local paths, or cloud storage URLs depending on storage mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
