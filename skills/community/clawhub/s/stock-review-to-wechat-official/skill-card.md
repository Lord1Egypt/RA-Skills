## Description:

Converts informal long-form material such as chats, drafts, meeting notes, reading notes, industry analysis, and A-share market reviews into structured WeChat Official Account Markdown posts with standard or deep-review layouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ninetyhe-90](https://clawhub.ai/user/ninetyhe-90)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators use this skill to turn unstructured Chinese-language source material into publishable WeChat Official Account articles. It is especially suited to market-review style drafts, while also covering notes, meeting summaries, reading notes, and other long-form source text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated articles are written to disk automatically, including a default root-level Hermes path.

Mitigation: Review the output path and generated article title before use, and install only when automatic saving is acceptable.

Risk: Sensitive chats, notes, or draft material may be persisted if supplied as input.

Mitigation: Avoid using sensitive source material unless saving that content to disk is intended.

Risk: Market-review outputs may be mistaken for investment advice if published without review.

Mitigation: Keep the risk disclaimer, verify the generated analysis before publication, and ensure the post does not present personal review content as financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ninetyhe-90/skills/stock-review-to-wechat-official)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown article with headings, emphasized points, a fixed risk disclaimer, and an engagement outro.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated articles are saved to a user-specified WeChat article directory, defaulting to /root/.hermes/hermes-agent/gzh/[date]_[title].md.]

## Skill Version(s):

1.2.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
