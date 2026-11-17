## Description:

Authoritative skill-creation standards (Boss). Use when creating or updating OpenClaw skills so they are portable, reproducible, include prerequisites checks, and have a guided installation/onboarding flow that persists machine-specific config in skill-local config files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moodykong](https://clawhub.ai/user/moodykong)

### License/Terms of Use:


## Use Case:

Developers and skill authors use Skill Father to create or update OpenClaw skills with prerequisite checks, portable configuration, guided onboarding, and reproducibility standards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated real config files may contain machine-specific values or secrets that are accidentally committed, logged, or summarized.

Mitigation: Exclude real config files from version control, write them with owner-only permissions, keep secrets out of logs and summaries, and prefer OS keychains or secret managers for tokens.

Risk: Child skills following this standard may edit sensitive local configuration such as SSH config, OpenClaw environment files, or PATH symlinks.

Mitigation: Review each child skill before allowing it to edit ~/.ssh/config, ~/.config/openclaw/env, or PATH symlinks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/moodykong/skills/skill-father)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of skill-local configuration and onboarding flows.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
