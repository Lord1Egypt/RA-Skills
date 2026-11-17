## Description:

End-to-end Xiaohongshu (RedNote) operations skill for configuring a content style, saving an operating profile, generating posts and visual assets, and publishing through a dedicated independent browser flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spencer17x](https://clawhub.ai/user/spencer17x)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, operators, and developers use this skill to configure a reusable Xiaohongshu operating profile, generate platform-style post copy and image assets, and prepare or execute publishing through a dedicated browser profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish to a real Xiaohongshu account through a persistent logged-in browser session.

Mitigation: Use the review-before-publish flow unless direct publishing is explicitly intended, and keep the dedicated browser profile separate from daily browsing sessions.

Risk: The one-shot workflow can bypass the profile's review-before-publish setting.

Mitigation: Avoid running scripts/run_ops_once.js until review enforcement is fixed; use scripts/xhs_publish.js or manual review flows for drafts.

Risk: The independent publish helper terminates existing processes that match the dedicated browser profile path.

Mitigation: Inspect or remove the pkill behavior before use on workstations that may have other active browser or automation sessions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/spencer17x/skills/rednote-ops)
- [Workflow](references/workflow.md)
- [Content Rules](references/content-rules.md)
- [Content Output Format](references/content-output-format.md)
- [Image Sources](references/image-sources.md)
- [Cards Usage](references/cards-usage.md)
- [Publish Usage](references/publish-usage.md)
- [Independent Browser Publish Path](references/publish-independent-browser.md)
- [Auto Learning](references/auto-learning.md)
- [Profile Schema](references/profile-schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration, generated post assets, and shell commands for helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create temporary post, page, image, and publishing assets under local runtime directories.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
