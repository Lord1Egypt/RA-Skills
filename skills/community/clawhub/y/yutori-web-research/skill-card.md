## Description: <br>
Yutori research uses Yutori's Research and Browsing APIs to research topics, collect sources, navigate sites, and extract structured facts from the web. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juanpin](https://clawhub.ai/user/juanpin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to delegate web research, source collection, site navigation, and structured fact extraction to Yutori cloud agents when local browsing tools are not ideal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, URLs, and browsing tasks are sent to Yutori's cloud service. <br>
Mitigation: Use a limited Yutori API key and avoid sending confidential URLs, internal data, or secrets unless approved. <br>
Risk: Browsing tasks may include form submission or other state-changing actions. <br>
Mitigation: Confirm with the user before form submission or other state-changing browsing tasks. <br>
Risk: The configured Yutori endpoint may point to a development or production environment. <br>
Mitigation: Verify YUTORI_API_BASE points to the intended endpoint before running research or browsing tasks. <br>


## Reference(s): <br>
- [Yutori website](https://yutori.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text with bullet lists and source URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires YUTORI_API_KEY; long-running tasks may return a view URL for later polling.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
