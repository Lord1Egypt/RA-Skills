## Description:

Fetch and summarize a webpage by extracting markdown, removing extraneous content, truncating if needed, and returning a concise summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tfops22](https://clawhub.ai/user/tfops22)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Web Trim to research or summarize user-requested web pages while reducing boilerplate and returning only the essential content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetching private, internal, or sensitive URLs can expose requested web content through the web-fetch workflow.

Mitigation: Use the skill only on URLs appropriate for external processing unless the tool's access and data-handling behavior has been reviewed.

Risk: Summaries of long pages may omit relevant context because content over 10,000 characters can be truncated.

Mitigation: Review the original page or request targeted sections when completeness matters.

Risk: A fetched page can contain misleading or irrelevant material that affects the final summary.

Mitigation: Treat summaries as condensed guidance and verify important claims against the source page.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tfops22/skills/web-trim)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Concise Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries are capped at 500 words, and source content over 10,000 characters may be truncated to relevant sections.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
