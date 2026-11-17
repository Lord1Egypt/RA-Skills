## Description:

Saike is an Indonesian-language WhatsApp bot assistant persona for concise coding, debugging, research, writing, and technical help with owner-only handling for sensitive actions and anti-jailbreak behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danzu0x](https://clawhub.ai/user/danzu0x)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and bot operators use Saike to give a WhatsApp assistant a concise Indonesian persona for user support, coding and debugging help, research, writing cleanup, and safe handling of sensitive bot actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill loads automatically and broadly changes the assistant's identity, disclosure behavior, and response style.

Mitigation: Install it only in a dedicated Saike WhatsApp bot environment where this persona is intended for all sessions.

Risk: The skill describes owner-only access rules but depends on external owner checks that are not implemented in the package.

Mitigation: Verify the host bot enforces owner authorization separately before relying on the skill for sensitive actions.

## Reference(s):

- [Saike ClawHub skill page](https://clawhub.ai/danzu0x/skills/saike-ai)
- [danzu0x ClawHub publisher profile](https://clawhub.ai/user/danzu0x)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Natural-language responses with Markdown and code blocks when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Concise Indonesian persona; structured formats are used only when helpful.]

## Skill Version(s):

1.0.0 (source: artifact/SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
