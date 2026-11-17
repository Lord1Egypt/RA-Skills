## Description:

Isolated Kali Linux sandbox for running pentest tools and risky commands safely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c0ffeeoverdose](https://clawhub.ai/user/c0ffeeoverdose)

### License/Terms of Use:


## Use Case:

Developers and security engineers use this skill to run pentest tools, unknown scripts, and risky shell commands inside an isolated Kali Linux sandbox rather than on the host.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run offensive security tools and high-impact commands.

Mitigation: Use it only for systems that the user is explicitly authorized to test, and review commands before execution.

Risk: Command arguments may expose secrets or real credentials.

Mitigation: Avoid placing secrets, tokens, or production credentials in command arguments.

Risk: The sandbox control API is described as unauthenticated and plaintext.

Mitigation: Keep the API isolated, authenticated where possible, and unreachable by unintended network peers.

Risk: Reset operations can disrupt sandbox state.

Mitigation: Treat reset as destructive to current sandbox state and use it only when the sandbox is broken or blocked by a container-name conflict.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/c0ffeeoverdose/skills/prts-sandbox)
- [Publisher profile](https://clawhub.ai/user/c0ffeeoverdose)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with inline bash code blocks and command output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, curl, jq, and access to the configured sandbox API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
