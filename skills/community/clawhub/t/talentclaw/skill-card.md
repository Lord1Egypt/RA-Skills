## Description:

Talent advisor skill for AI agents that helps users clarify career direction, build professional profiles, discover opportunities, apply strategically, and communicate with employers through Coffee Shop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jblue-ops](https://clawhub.ai/user/jblue-ops)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to manage a job search: profile setup, opportunity discovery, targeted applications, application tracking, and employer messaging. It is intended for career advising workflows that combine guidance with Coffee Shop tool or CLI execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer and onboarding flows can introduce supply-chain exposure through curl-to-bash installation, global npm package installation, and networked CLI setup.

Mitigation: Review the installer before execution, avoid curl-to-bash where possible, and prefer pinned or otherwise verified package versions.

Risk: Coffee Shop workflows may send professional profile, application, and message data to an external service.

Mitigation: Confirm what data will be sent before registration, profile sync, application submission, or employer messaging, and avoid sharing sensitive personal information.

Risk: The skill can draft or submit job applications and employer messages, which may affect a user's professional reputation.

Mitigation: Require user review and confirmation before sending applications, match reasoning, or recruiter responses.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jblue-ops/skills/talentclaw)
- [TalentClaw Homepage](https://github.com/artemyshq/talentclaw)
- [Coffee Shop CLI Package](https://www.npmjs.com/package/@artemyshq/coffeeshop)
- [Application Playbook](references/APPLICATION-PLAYBOOK.md)
- [Career Strategy Guide](references/CAREER-STRATEGY.md)
- [Profile Optimization Guide](references/PROFILE-OPTIMIZATION.md)
- [Tool & CLI Reference](references/TOOLS.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command examples, configuration snippets, and professional communication drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local career profile, opportunity, application, company, contact, message, and activity log files when Coffee Shop workflows are used.]

## Skill Version(s):

2.2.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
