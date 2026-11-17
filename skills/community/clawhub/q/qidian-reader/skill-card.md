## Description:

Qidian Reader helps an agent find novels on Qidian, browse genre rankings, give personalized book recommendations, and distinguish live ranking results from fallback recommendations when browser automation is blocked.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and reading assistants use this skill to discover Qidian novels by genre, popularity, completion status, length, and similarity to books they already like. It can gather current ranking data through browser automation and fall back to clearly labeled recommendations when live access is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill opens Qidian ranking pages in a real browser to collect current book data, which may encounter anti-bot checks or dynamic-rendering failures.

Mitigation: Use browser automation at a controlled pace, stop when verification or empty results appear, and clearly label any fallback recommendations as not based on current live rankings.

Risk: Book recommendations may be misleading if live ranking extraction fails or partial data is mixed with model knowledge.

Mitigation: Separate live ranking results from classic or taste-based recommendations and disclose the data source in the response.

## Reference(s):

- [Qidian Ranking URL List](references/urls.md)
- [Qidian Categories and chn Parameters](references/categories.md)
- [Qidian Rankings](https://www.qidian.com/rank/)
- [Qidian Finished Works](https://www.qidian.com/finish/)
- [Qidian Free Works](https://www.qidian.com/free/)
- [Qidian Reader Skill Page](https://clawhub.ai/tobewin/skills/qidian-reader)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with structured recommendation lists and optional browser automation commands or extraction guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations should label whether they come from live Qidian ranking data or fallback knowledge.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
