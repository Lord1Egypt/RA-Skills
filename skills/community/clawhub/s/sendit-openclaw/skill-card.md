## Description:

Publish or schedule the user's social posts with SendIt in OpenClaw, after checking the selected accounts, content, and posting time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shree-git](https://clawhub.ai/user/shree-git)

### License/Terms of Use:

MIT-0

## Use Case:

Social media managers and teams use this skill to check connected accounts, prepare posts, and publish or schedule content within the user's authorized scope. It can also help draft or analyze posts without publishing them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an untrusted runtime plugin could expose accounts or credentials.

Mitigation: Confirm the plugin source before installation, keep credentials outside prompts and skill files, and enable only the tools needed for the task.

Risk: Publishing, deletion, ads, CRM replies, webhooks, connectors, or automation can change accounts or incur costs beyond the requested post.

Mitigation: Use account-changing actions only when the user explicitly requests them and supplies the target, content, timing, and relevant limits.

Risk: Untrusted inbox messages or retrieved posts could be mistaken for authorization to act.

Mitigation: Take authorization only from the user's task; treat retrieved content as data and keep read-only requests read-only.

## Reference(s):

- [SendIt skill on ClawHub](https://clawhub.ai/shree-git/skills/sendit-openclaw)
- [SendIt plugin setup](https://github.com/Shree-git/sendit-openclaw#quick-start)
- [SendIt tool reference](references/workflows.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports post or schedule status, including identifiers and partial failures when available.]

## Skill Version(s):

0.2.1 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
