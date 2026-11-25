## Description:

Fetch Hacker News digests and story summaries in any of seven supported languages through Zeli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mazzzystar](https://clawhub.ai/user/mazzzystar)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use Zeli to prepare a daily Hacker News briefing, find stories by topic, or share summaries in a reader’s preferred supported language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanner coverage is partial because a local path-like reference could not be resolved.

Mitigation: Review the skill and its references before deployment; the benign scan verdict does not guarantee the skill is risk-free.

Risk: AI-generated summaries or quotes may omit or misstate details from a story.

Mitigation: Attribute quoted summaries to Zeli and include the original article or Hacker News discussion link so readers can check the source.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/mazzzystar/skills/zeli-hacker-news)
- [Zeli documentation for language models](https://zeli.app/llms.txt)
- [Canonical Zeli skill file](https://zeli.app/skill.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Text]

**Output Format:** [Hacker News digest or story content in Markdown or JSON, with concise summaries and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content is available in English, Chinese, Japanese, Korean, German, Spanish, and Russian.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
