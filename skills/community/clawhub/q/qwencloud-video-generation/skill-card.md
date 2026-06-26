## Description: <br>
Qwencloud Video Generation helps agents generate and edit videos with QwenCloud Wan models across text-to-video, image-to-video, first-and-last-frame, reference-based role-play, and VACE editing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cuixiaoyang123](https://clawhub.ai/user/cuixiaoyang123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative agents use this skill to submit, poll, and retrieve QwenCloud video-generation jobs for short clips, animated images, character-reference videos, and VACE edits. It is suited for workflows where prompts and selected media may be processed by QwenCloud and billable requests are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected media may be sent to QwenCloud/DashScope for processing. <br>
Mitigation: Use the skill only when external processing is approved and avoid sensitive local files unless disclosure is acceptable. <br>
Risk: Video generation uses API credentials and may incur per-second cloud charges. <br>
Mitigation: Use scoped API keys, check credential configuration without printing secrets, and confirm pricing or quota before submitting jobs. <br>
Risk: Custom QWEN_BASE_URL or OSS settings can redirect requests or uploads outside the expected provider path. <br>
Mitigation: Review endpoint and OSS environment settings before execution and prefer least-privilege storage credentials. <br>
Risk: Optional update-check and configuration steps may run npx installers or modify agent settings. <br>
Mitigation: Review installer commands, agent-config edits, and deletion commands before allowing them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cuixiaoyang123/qwencloud-video-generation) <br>
- [Qwen Video Generation API Supplementary Guide](references/api-guide.md) <br>
- [Qwen Video Generation Official Documentation](references/sources.md) <br>
- [Execution Guide](references/execution-guide.md) <br>
- [Request Fields by Mode](references/request-fields.md) <br>
- [Workflow Recommendations](references/workflows.md) <br>
- [Task Polling Guide](references/polling-guide.md) <br>
- [Prompt Guide](references/prompt-guide.md) <br>
- [Local Media Merging Guide](references/merge-media.md) <br>
- [QwenCloud Video Models Documentation](https://docs.qwencloud.com/developer-guides/getting-started/video-models) <br>
- [QwenCloud Model Pricing](https://docs.qwencloud.com/developer-guides/getting-started/pricing) <br>
- [QwenCloud Model List](https://www.qwencloud.com/models) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with JSON request examples, shell commands, API responses, and optional downloaded video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Asynchronous QwenCloud jobs are submitted and polled; generated video URLs expire and outputs may be saved under output/qwencloud-video-generation.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
