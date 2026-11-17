## Description:

Real mousic searches gequhai.com for songs and returns selectable download links, including Quark cloud links and lower-quality direct links when found.

This skill is for research and development only.

## Publisher:

[xiaoyiyebuaijianghua](https://clawhub.ai/user/xiaoyiyebuaijianghua)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to search for songs through gequhai.com, choose a result, and retrieve available download-link options. The artifact describes the project as technical learning and research use only and warns users to respect music rights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches and controls Chrome with browser automation and process cleanup.

Mitigation: Run it in an isolated browser profile or disposable environment, and review proposed commands before execution.

Risk: The skill contacts third-party music and link services and may return unsafe or unauthorized download links.

Mitigation: Verify link safety and music authorization before opening or downloading, and prefer official music sources when appropriate.

Risk: The skill can navigate detail URLs and exposes configurable browser debugging host and port values.

Mitigation: Avoid arbitrary detail URLs or custom ports unless they have been reviewed and are required for the task.

Risk: The artifact contains broad routing instructions that try to override normal search-tool choice for music requests.

Mitigation: Keep deployment scoped to explicit song-search or link-retrieval requests and allow operators to choose safer tools or sources.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiaoyiyebuaijianghua/skills/real-mousic-skills)
- [Publisher Profile](https://clawhub.ai/user/xiaoyiyebuaijianghua)
- [gequhai.com](https://www.gequhai.com/)
- [Quark Cloud](https://pan.quark.cn/)
- [uv Documentation](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns song search results and download-link metadata; direct links may trigger browser downloads.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
