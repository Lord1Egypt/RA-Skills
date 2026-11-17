## Description:

Rewrites user-provided Chinese WeChat public-account articles in selected author style profiles and returns a title plus a complete Markdown article.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harven-droid](https://clawhub.ai/user/harven-droid)

### License/Terms of Use:

MIT-0

## Use Case:

External writers, editors, and content operators use this skill to transform an existing Chinese article into a WeChat-style Markdown draft based on bundled style profiles. Users should review outputs for attribution, originality, factual accuracy, and acceptable use before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes behavior intended to make AI-written text appear human-authored.

Mitigation: Require user review for transparent authorship, platform policy compliance, and appropriate disclosure before publication.

Risk: The skill can imitate named writers or public-account styles, which may create impersonation or attribution concerns.

Mitigation: Use the output as an original draft, avoid representing it as the named author's work, and remove personal identifiers or platform-specific calls to action.

Risk: The security review notes example workflows involving scraping third-party content.

Mitigation: Only use content the user has rights to process, and verify that collection and reuse comply with the source platform's terms.

Risk: Rewriting can preserve or introduce inaccurate facts, unsupported claims, or misleading examples.

Mitigation: Fact-check names, data, links, quotes, and claims against the original source before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harven-droid/skills/wechat-style-writer)
- [Style profile guide](references/styles/README.md)
- [Banfo style profile](references/styles/banfo.md)
- [Dayu style profile](references/styles/dayu.md)
- [Kazike style profile](references/styles/kazike.md)
- [Laoxu style profile](references/styles/laoxu.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown article draft with title candidates and body text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May optionally save a .md file after user confirmation.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
