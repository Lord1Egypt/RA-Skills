## Description: <br>
Converts HTTP or HTTPS web pages into clean, readable Markdown, with support for single-page conversion, batch conversion, frontmatter, templates, and local image downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rwonly](https://clawhub.ai/user/rwonly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, documentation maintainers, and knowledge-base builders use this skill to convert static HTML pages into Markdown for local reference, archiving, documentation, or batch export workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches remote web content and can send URLs or embedded credentials to remote servers. <br>
Mitigation: Only provide URLs and authentication tokens for destinations you trust; avoid secrets in URLs and prefer short-lived or least-privilege tokens. <br>
Risk: Fetching private internal endpoints can expose sensitive network locations or content through agent-driven requests. <br>
Mitigation: Do not fetch private internal endpoints unless the user understands what will be sent to the remote server. <br>
Risk: Static HTML conversion does not execute JavaScript and may lose fidelity on complex, login-required, paywalled, or rate-limited pages. <br>
Mitigation: Use the output as a readable conversion artifact and review it when page structure, access controls, or repeated requests may affect completeness. <br>


## Reference(s): <br>
- [URL to Markdown on ClawHub](https://clawhub.ai/rwonly/url2md) <br>
- [rwonly ClawHub Profile](https://clawhub.ai/user/rwonly) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown output, optional Markdown files, and CLI guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include YAML frontmatter, templated Markdown content, resolved links, localized image references, and batch-created Markdown files.] <br>

## Skill Version(s): <br>
2.1.2 (source: server release metadata and script version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
