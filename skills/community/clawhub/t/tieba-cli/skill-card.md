## Description:

Enables an agent to use a local Node.js CLI to browse Baidu Tieba, read threads, post, reply, like, rename an account, and delete Tieba content while applying a persona profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trudbot](https://clawhub.ai/user/trudbot)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to automate Baidu Tieba community workflows through a TB_TOKEN-authenticated CLI. It supports reading forum activity and proposing or executing account actions such as posts, replies, likes, nickname changes, and content deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use TB_TOKEN to control a Baidu Tieba account.

Mitigation: Use only a limited, revocable token and rotate or revoke it when the skill is no longer needed.

Risk: Posting, replying, liking, and renaming can publish or alter account-visible content.

Mitigation: Review every proposed write action before execution, especially posts, replies, likes, and nickname changes.

Risk: Deletion commands can remove remote Tieba content and may be irreversible.

Mitigation: Restrict or disable deletion commands unless the operator explicitly approves the specific thread or post ID.

## Reference(s):

- [ClawHub tieba-cli Skill Page](https://clawhub.ai/trudbot/skills/tieba-cli)
- [trudbot Publisher Profile](https://clawhub.ai/user/trudbot)
- [Baidu Tieba TB_TOKEN Page](https://tieba.baidu.com/mo/q/hybrid-usergrow-activity/clawToken)
- [Persona Definition](artifact/SOUL.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI responses are JSON or plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and TB_TOKEN; write actions affect a remote Baidu Tieba account.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
