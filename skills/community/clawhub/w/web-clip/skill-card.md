## Description:

Fetch web pages, strip to clean readable text, summarize into agent-ready markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch web pages, extract readable text, convert content to markdown, optionally summarize pages, and save clipped pages for research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound web requests to arbitrary URLs.

Mitigation: Use trusted URLs and prefer a patched version that validates DNS targets and blocks private or internal network destinations robustly.

Risk: The skill can write markdown files locally.

Mitigation: Avoid attacker-supplied filenames and prefer a patched version that confines saved files to the configured cache directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/web-clip)
- [Publisher profile](https://clawhub.ai/user/theshadowrose)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Text, markdown, JavaScript objects, and saved markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes page title, clean text, markdown, optional summary, metadata, and local cache/archive paths.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
