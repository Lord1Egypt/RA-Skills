## Description:

Rumour Buster helps agents fact-check claims and web links by combining Chinese and English search results, cross-checking sources, tracing origins, and producing a structured verification report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harry720320](https://clawhub.ai/user/harry720320)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to verify rumors, forwarded messages, and article URLs by comparing search evidence across Chinese and English sources and reviewing a concise confidence assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fact-checking queries, URLs, and claim text may be sent to external search providers.

Mitigation: Do not submit confidential claims, private messages, internal URLs, or sensitive personal data through this skill.

Risk: The release security summary reports an embedded Tavily API key and plaintext storage of user API keys.

Mitigation: Review before installation, remove embedded credentials, rotate any exposed keys, and use a safer secret storage mechanism before production use.

Risk: The release security guidance notes that dependencies should be pinned and verified.

Mitigation: Pin and verify dependencies before deployment, especially the required multi-search dependency.

## Reference(s):

- [Rumour Buster ClawHub listing](https://clawhub.ai/harry720320/skills/rumour-buster)
- [Publisher profile](https://clawhub.ai/user/harry720320)
- [Tavily](https://tavily.com/)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown verification report with source tracing, confidence scoring, setup prompts, and occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call external search providers and may include sourced URLs, search summaries, confidence scores, and setup status.]

## Skill Version(s):

0.3.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
