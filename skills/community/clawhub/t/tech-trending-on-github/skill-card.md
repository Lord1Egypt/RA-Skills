## Description:

Analyzes public GitHub Trending pages to summarize popular repositories, highlight innovative open-source projects, and report technology trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meituskills](https://clawhub.ai/user/meituskills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to fetch public GitHub Trending data, compare current or weekly trends, and generate concise reports on notable repositories, innovation signals, and technology directions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trend-related trigger wording may activate the skill for general technology-trend questions.

Mitigation: Review and narrow trigger wording before deployment if the host environment needs the skill to activate only for explicit GitHub or open-source trend requests.

Risk: Reports depend on public GitHub Trending pages that change over time.

Mitigation: Treat generated reports as point-in-time summaries and refresh the data when current trend accuracy matters.

## Reference(s):

- [GitHub Trending](https://github.com/trending)
- [GitHub Trending for Python](https://github.com/trending/python)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report in Chinese or English, selected from the user's query language]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports typically include repository summaries, language distribution, star and fork signals, trend changes, innovation highlights, and technology recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
