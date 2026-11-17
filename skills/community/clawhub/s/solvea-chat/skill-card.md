## Description:

Connects an OpenClaw customer-service agent to the Solvea Web App chat API to produce customer-support replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[airoucat233](https://clawhub.ai/user/airoucat233)

### License/Terms of Use:

MIT-0

## Use Case:

External customer-service teams and OpenClaw operators use this skill to route channel messages, such as Feishu or DingTalk chats, to Solvea and return the resulting support response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores Solvea credentials and may expose them during setup or later review.

Mitigation: Review the setup script before installation, restrict permissions on .env files, and rotate any Solvea token shown by previous installer runs.

Risk: Customer chat content and session identifiers are logged or stored locally while replies depend on a remote Solvea service.

Mitigation: Use a dedicated OpenClaw agent and workspace, avoid sensitive customer data unless logging is reduced or disabled, and review memory files during operations.

Risk: Uninstall can remove an agent workspace if the operator approves the configured path.

Mitigation: Inspect the configured workspace path before approving deletion during uninstall.

## Reference(s):

- [Solvea Chat API Spec](references/api-spec.md)
- [Solvea Web App](https://solvea.cx)
- [OpenClaw](https://openclaw.ai)
- [ClawHub Skill Page](https://clawhub.ai/airoucat233/skills/solvea-chat)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text stdout for customer replies, with Markdown documentation and shell commands for setup and operation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses per-peer session state; errors are emitted to stderr with a non-zero exit code.]

## Skill Version(s):

0.5.7 (source: server release metadata; artifact frontmatter reports 0.5.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
