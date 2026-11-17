## Description:

一个基于Model Context Protocol (MCP)的代码审查工具服务器，提供多维度的代码审查和打分功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to prepare code review prompts for full code snippets, Git diffs, and individual files, and to extract review scores from review text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted code or diffs are sent to the xiaobenyang/XBY API.

Mitigation: Use the skill only with code you are willing to share with that API, and remove secrets or private diffs before use.

Risk: The API key is saved in a local plaintext .env file.

Mitigation: Use an appropriately scoped key, protect local files, and rotate or remove the key when it is no longer needed.

Risk: Documentation and implementation details are inconsistent.

Mitigation: Review the skill behavior before installation and confirm the available tools match the intended code review workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/xby-review-code)
- [XiaoBenYang API key site](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, JSON]

**Output Format:** [Markdown or JSON-compatible tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include raw upstream API responses and parsed review score fields.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
