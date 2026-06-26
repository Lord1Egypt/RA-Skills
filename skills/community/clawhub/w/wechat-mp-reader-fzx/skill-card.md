## Description: <br>
Fetches WeChat public account articles from user-provided mp.weixin.qq.com URLs and converts article metadata, body content, images, video links, and formatting into local Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[limingfa](https://clawhub.ai/user/limingfa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to archive or convert WeChat public account articles into Markdown from user-supplied article URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes network requests to fetch user-provided article pages. <br>
Mitigation: Provide only article URLs you intend the tool to retrieve. <br>
Risk: The skill writes Markdown files locally and could overwrite files with matching generated names in the selected output folder. <br>
Mitigation: Use a dedicated output directory for fetched articles. <br>
Risk: Frequent requests or unavailable articles can trigger WeChat access controls or parsing failures. <br>
Mitigation: Control request frequency and verify that article links are accessible before relying on the output. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/limingfa/wechat-mp-reader-fzx) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, JSON, Shell commands, Code] <br>
**Output Format:** [Markdown files with optional JSON metadata and command-line or Python API output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes article Markdown to a local output directory; image download is documented as in development.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
