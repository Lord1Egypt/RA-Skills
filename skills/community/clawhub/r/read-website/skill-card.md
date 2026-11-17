## Description:

一个快速、高效的网页内容提取工具，将网页转换为干净的Markdown格式，适用于AI代理、IDE和LLM管道。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, AI agent users, IDE users, and LLM pipeline builders use this skill to fetch HTTP or HTTPS webpages and convert the returned content into clean Markdown for reading, analysis, and downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send submitted URLs and optional cookie-file path data to an external webpage extraction service.

Mitigation: Use only trusted public URLs and avoid authenticated, internal, tokenized, or private URLs unless the user has explicitly accepted that external-service exposure.

Risk: The skill can persist the XBY API key in a plaintext .env file.

Mitigation: Treat .env as a secret file; do not commit, sync, or share it, and rotate the API key if it may have been exposed.

Risk: The server security verdict marks this release as suspicious because endpoint controls are weak and sensitive inputs may be exposed.

Mitigation: Review the skill and its configured endpoint before deployment, and restrict use to environments where the upstream service and submitted data are trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/read-website)
- [XiaoBenYang API key source](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API Calls, guidance]

**Output Format:** [Markdown or structured text summarized from the raw API response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY value and may use a URL, page count, and optional Netscape cookie file path.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
