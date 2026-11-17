## Description:

Converts SRT subtitle files into structured Markdown documents, with a local subtitle-to-text step, content analysis, and optional supplemental search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[syajask](https://clawhub.ai/user/syajask)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn uploaded or provided .srt subtitle files into readable Markdown notes or articles, including summaries, structure, key points, concepts, people, and optional extension links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplemental search may send terms extracted from subtitle content to web search tools.

Mitigation: For confidential subtitles, run only the local conversion and skip search enrichment.

Risk: The final document may combine transcript-derived analysis with supplemental search results.

Mitigation: Review sources and keep supplemental material clearly attributed in the Markdown output.

## Reference(s):

- [Search Strategy](references/search_strategy.md)
- [ClawHub Skill Page](https://clawhub.ai/syajask/skills/srt-to-md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown document plus a time-stamped subtitles text file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source URLs for supplemental research when web search enrichment is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
