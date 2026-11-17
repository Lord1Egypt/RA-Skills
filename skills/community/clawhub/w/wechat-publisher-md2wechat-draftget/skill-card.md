## Description:

Orchestrate the official WeChat draft publishing path for already-prepared article HTML or Markdown using md2wechat, with mandatory draft/get verification before reporting success.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryxn](https://clawhub.ai/user/jerryxn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to push already prepared WeChat Official Account article HTML or Markdown into the draft box through md2wechat, then verify the draft with WeChat draft/get before reporting success.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create WeChat Official Account drafts and upload article assets.

Mitigation: Use it only when draft creation is intended, and confirm the article, cover, and images are approved for upload to WeChat before execution.

Risk: The workflow requires WeChat AppID/AppSecret credentials and produces verification files that may contain unpublished draft content and metadata.

Mitigation: Protect md2wechat configuration and generated verification artifacts as sensitive material.

Risk: A local conversion, preview, or media_id receipt can be mistaken for a completed draft push.

Mitigation: Report success only after create_draft succeeds and draft/get verification confirms the backend draft and expected fields.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jerryxn/skills/wechat-publisher-md2wechat-draftget)
- [README.md](README.md)
- [Troubleshooting](references/troubleshooting.md)
- [Themes and Layout Notes](references/themes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON files, guidance]

**Output Format:** [Markdown guidance with bash commands, configuration examples, and JSON verification artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The publish workflow writes md2wechat inspection, conversion, upload, draft creation, and draft/get verification JSON files next to the article.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
