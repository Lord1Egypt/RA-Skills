## Description:

Tracks recent hot topics from a user-provided theme, searches timely sources, identifies 3-5 newsworthy angles, writes a Chinese long-form article, and produces a fact-check report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianheihei002](https://clawhub.ai/user/tianheihei002)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, editors, and media operators use this skill to investigate a current topic, collect timely source material, extract high-interest angles, draft an 800-1500 word Chinese article, and review key facts before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled tracking may reuse the previous topic without clear user confirmation.

Mitigation: Confirm the tracked topic before scheduled runs and review any retained topic state before publishing results.

Risk: The skill creates and may edit local article files during its writing and fact-checking workflow.

Mitigation: Run it in a dedicated workspace and choose an output location where generated markdown or DOCX files cannot overwrite important content.

Risk: Web-sourced hot-topic writing can include outdated, weakly sourced, or misleading claims.

Mitigation: Review the source report and fact-check report, especially dates, numbers, names, and direct quotations, before distributing the article.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tianheihei002/skills/yq-hot-topic-tracker)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown article, topic summary, source report, and fact-check report; may also request a DOCX conversion when a conversion tool is available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Designed for Chinese-language hot-topic tracking and long-form new-media writing.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
