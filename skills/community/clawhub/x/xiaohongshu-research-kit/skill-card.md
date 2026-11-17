## Description:

Extract and analyze Xiaohongshu (Little Red Book) content using yt-dlp and gallery-dl for note metadata, image and video extraction, user profile analysis, and content research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuya227939](https://clawhub.ai/user/xuya227939)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and content researchers use this skill to inspect Xiaohongshu notes, profiles, and topic pages by running local yt-dlp and gallery-dl commands, parsing returned JSON, and presenting structured findings in Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser-cookie workflows can expose authenticated Xiaohongshu session data to local third-party tools.

Mitigation: Use a dedicated browser profile containing only the Xiaohongshu account needed for research and review commands before execution.

Risk: Cookie-derived outputs may include private, account-bound, or sensitive content.

Mitigation: Avoid sharing raw outputs and remove sensitive account or content details before publishing analysis.

Risk: Unpinned yt-dlp or gallery-dl installs may change extraction behavior over time.

Mitigation: Prefer pinned or isolated installs and record tool versions with research results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xuya227939/skills/xiaohongshu-research-kit)
- [Publisher Profile](https://clawhub.ai/user/xuya227939)
- [SnapVee Homepage](https://snapvee.com)
- [GitHub Issues](https://github.com/xuya227939/xiaohongshu-research-kit/issues)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell command blocks, JSON field mappings, and summary tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may depend on local yt-dlp/gallery-dl behavior and authenticated browser-cookie access.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
