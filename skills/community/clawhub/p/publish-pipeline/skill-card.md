## Description:

Helps agents publish content, code, or packages through a repeatable release path that validates inputs, builds, deploys, verifies the live target, and records the release.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tooled-app](https://clawhub.ai/user/tooled-app)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, release operators, and agent users use this skill to turn recurring or first-time publishing tasks into a checklist covering preflight, validation, manifest updates, build, deploy, live verification, rollback, and announcement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through production build, deploy, announcement, rollback, and scheduled publishing workflows.

Mitigation: Confirm production targets, credentials, announcement channels, rollback commands, and any cron automation before allowing the agent to proceed.

Risk: A publish may appear successful even when the build failed, the deployment target is wrong, or the live content is not rendered.

Mitigation: Require a successful build before deployment and verify the live URL for both HTTP success and rendered content before declaring success.

Risk: Manifest or ledger updates may create duplicate entries or encoding problems during repeated publishes.

Mitigation: Check for existing manifest entries, preserve documented encoding requirements, and make repeated publish runs idempotent.

Risk: A failed production verification can leave users on a broken release.

Mitigation: Use staging for high-risk publishes when available and roll back to the previous known-good version when live verification fails.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tooled-app/skills/publish-pipeline)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with command examples and release checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires project-specific source-of-truth files, credentials, deploy targets, rollback commands, announcement channels, and verification URLs to be confirmed before execution.]

## Skill Version(s):

1.1.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
