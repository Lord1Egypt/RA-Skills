## Description:

Lightweight self-monitoring and self-constraining rules to prevent accidental file deletions, dangerous commands, and risky operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vaderyang](https://clawhub.ai/user/vaderyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to make file edits, shell commands, bulk updates, and destructive operations more conservative through pre-action checks, confirmation rules, and recovery breadcrumbs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation may interrupt routine coding tasks with extra confirmations or pauses.

Mitigation: Use it when conservative behavior around edits and commands is desired, and expect additional review steps during normal development.

Risk: Sensitive files may enter session context if a user asks the agent to read or preserve them.

Mitigation: Avoid requesting access to sensitive files unless that content is intentionally in scope for the session.

## Reference(s):

- [Self-Guardian Skill Page](https://clawhub.ai/vaderyang/skills/self-guardian)
- [vaderyang Publisher Profile](https://clawhub.ai/user/vaderyang)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Text or Markdown guidance with command recommendations and confirmation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Broad activation can add pauses or confirmations during routine file and shell workflows.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
