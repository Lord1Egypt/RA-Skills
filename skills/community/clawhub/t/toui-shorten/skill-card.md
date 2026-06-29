## Description: <br>
Shorten URLs with toui.io and read click statistics for toui.io short codes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thebrecht](https://clawhub.ai/user/thebrecht) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create toui.io short links through the toui MCP server or REST API, and to retrieve click statistics over REST when they have an appropriately scoped key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends URLs to toui.io and may require OAuth authorization or a TOUI_API_KEY for REST access. <br>
Mitigation: Confirm that sharing the target URL with toui.io is acceptable and use the minimum-scope API key needed for the task. <br>
Risk: Click statistics require a full-scope key over REST. <br>
Mitigation: Use a full-scope key only when statistics access is specifically required. <br>


## Reference(s): <br>
- [toui skill listing](https://clawhub.ai/thebrecht/toui-shorten) <br>
- [toui homepage](https://toui.io) <br>
- [toui admin](https://toui.io/admin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return short URL, short code, QR URL, and click statistics when supported by the selected toui access path.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
