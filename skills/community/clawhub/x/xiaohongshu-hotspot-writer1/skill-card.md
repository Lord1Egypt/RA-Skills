## Description:

Generates daily Xiaohongshu-style AI and technology hotspot copy by fetching public TopHub titles, selecting relevant AI topics, and producing Chinese post drafts and a daily report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ztnt-816](https://clawhub.ai/user/ztnt-816)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and operators of Chinese AI or technology Xiaohongshu accounts use this skill to turn current AI-related hot-topic headlines into short post drafts, hashtags, and a daily content report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Xiaohongshu requests may route into this AI-hotspot workflow even when the user intended a different Xiaohongshu writing task.

Mitigation: Confirm that the requested task is an AI or technology hotspot daily report before relying on the generated workflow.

Risk: The skill generates Chinese copy by default, which may not match users expecting another language or locale.

Mitigation: Ask for the desired language or audience locale when the publishing context is not Chinese-language Xiaohongshu content.

Risk: Hot-topic titles fetched from a public ranking page can be incomplete, transient, or unsuitable for publication without review.

Mitigation: Review the selected headlines, generated claims, and hashtags before posting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ztnt-816/skills/xiaohongshu-hotspot-writer1)
- [TopHub AI Hot Topics Source](https://tophub.today/n/MZd7azPorO)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-like Chinese chat output with short titles, body copy, hashtags, and a daily report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Direct conversation output; no file writes, command execution, credential use, or persistence are indicated by the security evidence.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
