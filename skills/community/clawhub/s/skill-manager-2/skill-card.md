## Description:

Install and manage OpenClaw agent skills. Learn how to find, install, and configure new capabilities from ClawHub and GitHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xu-fengxie](https://clawhub.ai/user/xu-fengxie)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to find, install, verify, and configure agent skills from ClawHub, Vercel Skills, and GitHub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npm or npx installation commands can install code that changes after the skill is published.

Mitigation: Pin exact package versions before use and avoid elevated privileges when running installation commands.

Risk: Direct GitHub installs can place unreviewed repositories into the active OpenClaw skills directory.

Mitigation: Stage GitHub-sourced skills outside the active skill directory, review their contents, and scan them before enabling them.

Risk: The skill does not provide detailed rollback steps for removing untrusted installed tools or skills.

Mitigation: Track installed global CLIs and skill directories during setup so they can be removed if trust or behavior is unclear.

## Reference(s):

- [Source tutorial video](https://www.bilibili.com/video/BV1PbFUzZEvN)
- [ClawHub skill page](https://clawhub.ai/xu-fengxie/skills/skill-manager-2)
- [Publisher profile](https://clawhub.ai/user/xu-fengxie)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command examples for installing, listing, and verifying OpenClaw skills.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
