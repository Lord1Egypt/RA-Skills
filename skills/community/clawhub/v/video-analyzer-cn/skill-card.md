## Description: <br>
Analyzes Bilibili, Douyin, and Toutiao video links by downloading video content, extracting frames, and using a local minicpm-v model to summarize the frame content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[murrayhoung](https://clawhub.ai/user/murrayhoung) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content reviewers use this skill to summarize Chinese-platform video links locally. The skill guides an agent through downloading media, extracting representative frames, analyzing frames with local Ollama minicpm-v, and producing a consolidated video summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads video URLs supplied to the agent and may open Douyin pages through browser tooling. <br>
Mitigation: Use explicit prompts and only provide video links from sources you intend the agent to access. <br>
Risk: Video downloads and extracted frames are written to a local temporary workspace. <br>
Mitigation: Avoid unknown or very large links and periodically clean the declared temporary workspace after analysis. <br>
Risk: Extracted frames are sent to the user's local Ollama service for minicpm-v image analysis. <br>
Mitigation: Use the skill only when local Ollama processing is intended and acceptable for the video content being analyzed. <br>


## Reference(s): <br>
- [Video Download Reference](artifact/references/download.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/murrayhoung/video-analyzer-cn) <br>
- [Publisher Profile](https://clawhub.ai/user/murrayhoung) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python snippets, and narrative video summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local workflow guidance and summarized frame analysis; temporary video and image files are created during use.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
