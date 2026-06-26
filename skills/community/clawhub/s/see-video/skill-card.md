## Description: <br>
Extracts representative frames from user-provided video files into a grid image with timestamp metadata for vision-capable LLM context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[john-ver](https://clawhub.ai/user/john-ver) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect video content with the same vision-capable model that is handling the conversation. It is useful when direct frame context is preferred over routing video through a separate description model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extracted video frames may expose sensitive, private, regulated, or third-party content to the multimodal model or platform used by the agent. <br>
Mitigation: Use only authorized videos and confirm provider retention, logging, and data handling policies before processing sensitive content. <br>
Risk: Frame sampling can miss details in long videos or unsupported/corrupt media may fail during extraction. <br>
Mitigation: Use highlight mode for broad scene coverage, use start and end ranges for detailed review, and retry with a complete supported file when extraction fails. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/john-ver/see-video) <br>
- [Publisher profile](https://clawhub.ai/user/john-ver) <br>
- [llm-frames](https://github.com/john-ver/llm-frames) <br>
- [llm-frames package](https://registry.npmjs.org/llm-frames/-/llm-frames-0.2.2.tgz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON output from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a temporary JPEG frame grid path plus XML timestamp metadata for agent context injection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
