## Description: <br>
Video Ai Process helps an agent plan and run a video-processing workflow that transcribes video, analyzes rough and fine cuts, segments and composes clips, records results in Feishu Bitable, and supports customer-ranked custom edits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuchenggong19851114-design](https://clawhub.ai/user/zhuchenggong19851114-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, video editors, and operations teams use this skill to coordinate an AI-assisted workflow for Chinese-language video transcription, cut analysis, clip generation, Feishu review, customer scoring, and final version selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can send video-derived data and generated file paths to Feishu automatically. <br>
Mitigation: Require explicit confirmation before remote writes, use only approved Feishu workspaces, and avoid confidential videos unless Feishu handling is approved. <br>
Risk: Security evidence reports an unsafe shell command path in the video-processing workflow. <br>
Mitigation: Use only trusted local video paths, review generated shell commands before execution, and avoid passing untrusted file names or paths into FFmpeg commands. <br>
Risk: Feishu app tokens and table IDs can be exposed through configuration or logs. <br>
Mitigation: Provide Feishu values through environment variables, mask them in logs, and avoid committing credentials or printing full token values. <br>
Risk: Heartbeat polling and generated media persistence can create unintended remote activity or retained video artifacts. <br>
Mitigation: Require user approval before heartbeat polling or media persistence, and define retention and cleanup rules for generated clips and final videos. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with Python, Bash, YAML, and JSON examples plus a Python pipeline script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local transcripts, subtitle files, segmented MP4 clips, composed final videos, and Feishu Bitable record payloads when its workflow is executed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
