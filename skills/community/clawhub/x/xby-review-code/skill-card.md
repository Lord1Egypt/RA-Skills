## Description: <br>
Xby Review Code is an MCP-based code review helper that supports whole-code, git diff, and single-file reviews with score parsing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alinklab](https://clawhub.ai/user/alinklab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to request structured code review assistance for full code snippets, git diffs, or individual files, and to extract review scores from returned review text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reviewed code is sent to an external XiaoBenYang service. <br>
Mitigation: Use the skill only when that provider is approved for the code being reviewed, and do not submit proprietary code, secrets, or regulated data unless approval covers that use. <br>
Risk: The skill stores the XBY_APIKEY value locally in a .env file. <br>
Mitigation: Protect the .env file, exclude it from version control, and rotate the API key if it may have been exposed. <br>


## Reference(s): <br>
- [Xby Review Code on ClawHub](https://clawhub.ai/alinklab/xby-review-code) <br>
- [XiaoBenYang API Key Portal](https://xiaobenyang.com) <br>
- [XiaoBenYang MCP API Endpoint](https://mcp.xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown or structured text derived from raw API response data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an XBY_APIKEY value and may return success, raw response data, and status messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
