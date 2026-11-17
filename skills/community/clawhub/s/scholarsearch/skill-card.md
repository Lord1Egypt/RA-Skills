## Description:

Academic literature search and briefing generation with Tavily API, PubMed, and Google Scholar for topic-specific paper discovery, Top 10 relevance-ranked reports, Obsidian saving, and Feishu summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flying-baozi](https://clawhub.ai/user/flying-baozi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and analysts use Scholarsearch to search academic literature on chosen topics and produce relevance-ranked Top 10 briefing reports. The skill can save the briefing to an Obsidian daily note path and send the complete content through Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Complete briefing content may be saved to an Obsidian path and sent through Feishu, which can expose confidential research topics or summaries.

Mitigation: Use approved Obsidian storage locations and Feishu destinations before running the workflow with confidential or sensitive research topics.

Risk: The generated report includes a CoffeeDog footer, which may be inappropriate when neutral attribution or organizational branding is required.

Mitigation: Remove or override the footer before sharing reports that require neutral attribution or official branding.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown briefing with paper links, abstracts, relevance scores, summaries, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts comma-separated or space-separated keywords; reports are intended for Obsidian storage and Feishu delivery when configured.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
