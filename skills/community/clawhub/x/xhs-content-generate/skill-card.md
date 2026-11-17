## Description:

Generates Xiaohongshu-style Chinese social posts from user-selected topics, RSS hot topics, or reference content using style analysis, opinionated drafting, and Chinese writing polish.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lifei68801](https://clawhub.ai/user/lifei68801)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and agents use this skill to draft Xiaohongshu-style posts with topic discovery, reference-style analysis, strong viewpoint generation, and final Chinese prose polishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can contact 36kr RSS feeds and may fetch user-provided reference links, which can expose private or sensitive URLs if supplied as inputs.

Mitigation: Use public reference links only, avoid sensitive or private URLs, and review any fetched source material before using it in generated content.

Risk: The RSS helper is not hardened against unusually large or stalled feed responses.

Mitigation: Run RSS fetching in a controlled agent environment and interrupt or retry stalled requests rather than relying on the helper for robust ingestion.

Risk: The skill intentionally produces strong, emotionally framed, and sometimes controversial social content that may overstate claims or create reputational risk.

Mitigation: Fact-check factual claims, review tone and brand fit, and edit generated drafts before publication.

## Reference(s):

- [XHS Content Generate ClawHub release](https://clawhub.ai/lifei68801/skills/xhs-content-generate)
- [lifei68801 publisher profile](https://clawhub.ai/user/lifei68801)
- [36kr RSS feed](https://36kr.com/feed)
- [Style analysis reference](references/style-analysis.md)
- [Writing templates reference](references/writing-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain Chinese text with optional shell command snippets for RSS topic fetching]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated content may include titles, short paragraphs, emoji, bold emphasis, opinionated framing, and interactive closing prompts.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
