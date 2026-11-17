## Description:

Guides agents through an automated short drama promotion workflow that downloads MoboBoost content, identifies highlight moments, creates 15-second vertical clips with text overlays, and publishes to Facebook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ye4wzp](https://clawhub.ai/user/ye4wzp)

### License/Terms of Use:

MIT-0

## Use Case:

Content automation developers and social media operators use this skill to coordinate short-drama clipping, highlight selection, and social publishing workflows. It is suited to teams that can verify content rights, account permissions, and each scheduled post before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks users to store live MoboBoost and Facebook account cookies.

Mitigation: Use dedicated least-privileged accounts, keep cookie files out of source control and backups, restrict file permissions, rotate cookies, and prefer official OAuth or platform APIs where possible.

Risk: Scheduled publishing can post videos to Facebook without enough human review.

Mitigation: Keep the cron job disabled until content rights, captions, account permissions, and every post are manually reviewed.

Risk: The release package only submitted SKILL.md while referencing scripts that are not present in the artifact.

Mitigation: Inspect and scan any referenced scripts before running them, and treat command examples as proposals until verified in a controlled environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ye4wzp/skills/short-drama-publisher)
- [MoboBoost web application](https://ckoc.cdreader.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational steps for video clipping, cookie configuration, and publishing review.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
