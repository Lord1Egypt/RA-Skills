## Description:

Read and summarize X/Twitter links with low-token routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuolicong](https://clawhub.ai/user/zuolicong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to read, summarize, extract, or inspect X/Twitter tweets, authored threads, and X article links while keeping normal tweet reads lightweight.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article mode may open and extract content from non-X URLs crafted to look like X article links.

Mitigation: Use only trusted links and require strict URL validation so browser-based article extraction can load only approved X/Twitter hosts, excluding local or private-network pages.

Risk: The skill consumes local X session cookies.

Mitigation: Review before installing and prefer a secondary X account instead of a primary or high-value account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zuolicong/skills/xlink-reader)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Structured JSON for tweet, thread, or article content, with text or markdown fields for summaries and extracted content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summary mode limits normal response text for token efficiency; full mode can include expanded text or markdown.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
