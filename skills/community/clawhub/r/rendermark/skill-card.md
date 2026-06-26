## Description: <br>
RenderMark helps agents render, export, publish, share, validate, compare, and sync styled markdown documents through an MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jmsaavedra](https://clawhub.ai/user/jmsaavedra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and external users use this skill when they need an agent to turn markdown into styled documents, exports, hosted pages, shareable previews, visual diffs, or synchronized documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Published, shared, or synchronized documents may send content outside the user's machine or expose it to unintended recipients. <br>
Mitigation: Confirm document content, destination, sharing recipients, and visibility settings before publishing, syncing, or sending invites. <br>
Risk: API keys and optional provider credentials stored in ~/.rendermark/config.json could be exposed or misused. <br>
Mitigation: Protect the config file, prefer environment-specific credentials, and rotate keys if they may have been disclosed. <br>
Risk: PDF, image, and Google Docs publishing depend on additional browser, Browserless, or OAuth configuration. <br>
Mitigation: Verify Chrome or Browserless setup for PDF/image export and complete Google OAuth setup before using Google Docs publishing. <br>


## Reference(s): <br>
- [RenderMark Website](https://rendermark.app) <br>
- [Setup Guide](references/setup-guide.md) <br>
- [Tools Reference](references/tools-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tool names, parameters, file paths, URLs, and setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce exported document files, hosted document URLs, preview images, rendered HTML, document diffs, validation results, and configuration guidance.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
