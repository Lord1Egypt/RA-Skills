## Description:

Make real phone calls via Stringclaw when the user asks to be called or wants to talk by voice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oscarwoha](https://clawhub.ai/user/oscarwoha)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to initiate an outbound Stringclaw voice call when the user explicitly asks to be called or wants a live voice session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real outbound phone calls and may consume Stringclaw minutes.

Mitigation: Require explicit user confirmation before each call and confirm the account has expected calling permissions and minutes.

Risk: The skill starts a background bridge that uses API and local gateway credentials.

Mitigation: Use scoped, rotatable credentials, avoid elevated privileges, and stop the bridge when finished.

Risk: The bridge executable dependency is not pinned in the skill instructions.

Mitigation: Pin or verify the bridge package before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oscarwoha/skills/stringclaw)
- [Publisher profile](https://clawhub.ai/user/oscarwoha)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON status examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May start a local bridge process and initiate an outbound phone call through Stringclaw.]

## Skill Version(s):

0.0.9 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
