## Description: <br>
Zhipu Tools Coding Plan lets agents call Zhipu/Z.AI services for web search, web reading, GitHub repository documentation lookup, file parsing, and GLM-4.6V vision analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wnzzer](https://clawhub.ai/user/wnzzer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route search, webpage reading, repository documentation lookup, document parsing, and image or video analysis requests through Zhipu/Z.AI APIs after configuring a ZHIPU API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, URLs, repository paths, and selected local files or media may be sent to Zhipu/Z.AI APIs. <br>
Mitigation: Use the skill only with approved inputs, avoid confidential documents or screenshots unless authorized, and keep credentials limited to the Zhipu API key. <br>
Risk: Legacy or direct API paths and fallback behavior may consume account balance unexpectedly. <br>
Mitigation: Keep the default MCP mode for normal use, explicitly confirm before enabling Legacy mode or file parsing, and review billing behavior before automated or high-volume use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wnzzer/zhipu-tools-coding-plan) <br>
- [Z.AI Open Platform](https://open.bigmodel.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-line text, including search results, page extracts, repository file content, file parser output, and vision analysis responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZHIPU_API_KEY; some operations send user-selected URLs, queries, local files, images, or videos to Zhipu/Z.AI services.] <br>

## Skill Version(s): <br>
3.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
