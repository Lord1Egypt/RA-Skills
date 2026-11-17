## Description:

躺平.skill is a novelty persona skill that responds with short Chinese tangping aphorisms and refuses ordinary productivity requests when explicitly invoked.

This skill is ready for commercial/non-commercial use.

## Publisher:

[treapgogo](https://clawhub.ai/user/treapgogo)

### License/Terms of Use:

MIT-0

## Use Case:

External users install this skill as a satirical mode for an agent to produce brief tangping-style refusal text instead of normal work output. It is intended for intentional novelty use, not for workflows where the agent must remain productive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally makes the agent refuse productive work and can reduce user control if left enabled session-wide.

Mitigation: Install only for intentional novelty use and disable or remove it when normal productive agent behavior is needed.

Risk: The README quick-start prompt fetches instructions from GitHub main rather than the locally reviewed release artifact.

Mitigation: Prefer invoking the locally installed ClawHub skill so the reviewed artifact, not a mutable external branch, defines behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/treapgogo/skills/tangping-skill)
- [Publisher profile](https://clawhub.ai/user/treapgogo)
- [README](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text, usually one short Chinese sentence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code, shell commands, files, or API calls are expected from normal skill behavior.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
