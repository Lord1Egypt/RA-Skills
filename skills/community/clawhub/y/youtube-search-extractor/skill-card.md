## Description:

Extracts YouTube video links from keyword search results and saves a formatted link list for agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuai1iu](https://clawhub.ai/user/shuai1iu)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to search YouTube by keyword, collect matching video URLs, and produce reusable link files for research, curation, or content discovery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs an unpinned global browser-automation dependency.

Mitigation: Use a sandbox or disposable environment, pin agent-browser to a reviewed version, and prefer a local install over a global install.

Risk: Saved YouTube search-result HTML may contain personal page state, recommendations, or other session-adjacent data.

Mitigation: Delete generated HTML files when they are no longer needed and avoid running the skill in sensitive authenticated browsing contexts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shuai1iu/skills/youtube-search-extractor)
- [agent-browser Project](https://github.com/vercel-labs/agent-browser)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and generated text files containing YouTube URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also save a YouTube search-result HTML file and a timestamped link list.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
