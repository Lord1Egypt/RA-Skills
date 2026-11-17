## Description:

Scrape AI-related articles from Substack search using browser automation and format the rendered search results as a numbered digest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search Substack for recent posts by topic, especially AI news, and return a concise numbered digest of matching articles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill opens Substack pages through browser automation.

Mitigation: Install and run it only in environments where browser automation to Substack is acceptable.

Risk: The helper may produce rough or raw search-result text rather than a polished article digest.

Mitigation: Review extracted results before relying on them, and use the documented manual browser flow when the helper output is incomplete.

## Reference(s):

- [Browser Automation Flow](artifact/references/browser-flow.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown numbered list, with optional JSON output from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search query with optional day, week, or month date range.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
