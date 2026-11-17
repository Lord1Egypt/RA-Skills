## Description:

Drafts Zhihu answers by selecting hot or keyword-matched questions, collecting discussion context, generating Chinese answer text through zhihuiapi, and saving validated output as drafts without publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joly123456](https://clawhub.ai/user/joly123456)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content operators use this skill in OpenClaw to prepare Zhihu draft answers from hot or keyword-filtered topics while keeping final publishing under manual control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted Zhihu or user text can become shell execution if interpolated into the documented curl command literally.

Mitigation: Pass collected text through stdin, a secure request file, or a structured HTTP client instead of embedding it directly in shell source.

Risk: The skill controls a logged-in Zhihu browser session.

Mitigation: Use a dedicated browser profile, keep automated login disabled, and verify the workflow only saves drafts.

Risk: Selected Zhihu question and comment data is sent to zhihuiapi for answer generation.

Mitigation: Install only when that provider data flow is acceptable, and avoid using the skill on sensitive or private material.

Risk: Generated drafts may still be inaccurate, unsafe, or legally risky.

Mitigation: Review saved drafts manually before publishing and retain the schema, safety, and anti-copy validation steps.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/joly123456/skills/zhihu-draft-writer)
- [Setup](references/setup.md)
- [Runtime Options](references/runtime-options.md)
- [Answer Generation Prompt](references/answer-generation.md)
- [Answer Schema](references/answer-schema.json)
- [Manual Test Checklist](references/manual-test-checklist.md)
- [Zhihu Hot List](https://www.zhihu.com/hot)
- [zhihuiapi Chat Completions Endpoint](https://cc.zhihuiapi.top/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON contracts, shell commands, Chinese draft text, and an end-of-run status report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated answer output is expected as JSON with answer_text, then validated for length, safety, non-copying, and draft-only handling before being written to Zhihu.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
