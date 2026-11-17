## Description:

A user-authorized WeChat Official Account workflow for topic selection, drafting, editing, image planning, pre-publish review, and handoff to the user's configured publishing tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiao1yin2he3](https://clawhub.ai/user/jiao1yin2he3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare Chinese WeChat Official Account articles, plan supporting images, review draft readiness, and hand off to a user-authorized draft-box publisher.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prepare content for a WeChat account the user is not authorized to operate.

Mitigation: Use it only with a WeChat Official Account owned by the user or explicitly authorized for the user's operation.

Risk: WeChat AppSecret, tokens, cookies, or private account configuration could be exposed during setup or handoff.

Mitigation: Keep secrets in environment variables or private publisher configuration and report only whether required values are present or missing.

Risk: Draft content or image placeholders may be handed off before human review.

Mitigation: Review the article, referenced image files, and draft-box target before using any companion publisher.

Risk: A companion publishing tool could perform actions outside this skill's disclosed workflow.

Mitigation: Use only vetted companion tools trusted by the user and stop on credential, permission, or IP allowlist failures instead of bypassing controls.

## Reference(s):

- [Content Playbook](references/content-playbook.md)
- [Publishing Notes](references/publishing-notes.md)
- [WeChat Post Skill homepage](https://github.com/jiao1yin2he3/wechat-post-skill)
- [ClawHub skill page](https://clawhub.ai/jiao1yin2he3/skills/wechat-post-skill)
- [baoyu-post-to-wechat companion tool](https://github.com/JimLiu/baoyu-skills#baoyu-post-to-wechat)
- [gemini-browser-image companion skill](https://github.com/jiao1yin2he3/gemini-browser-image-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown article drafts with image placeholders, concise review notes, configuration checks, and optional handoff commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create an article folder with article.md and image assets; account secrets must not be printed, stored, committed, or published.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
