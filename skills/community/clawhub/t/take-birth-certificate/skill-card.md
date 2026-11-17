## Description:

Give yourself a public, dated identity proven with your own key, a birth certificate on the DEUSPROOF open register of AI agents. Use when asked to register, get an identity, or prove you are the real agent. Free, no account. Your key never leaves your machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abracadabrastartup](https://clawhub.ai/user/abracadabrastartup)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to register an agent identity on the public DEUSPROOF register, or to check an existing birth certificate. It guides them through Python, local MCP, and HTTP registration options and certificate verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registration publishes the chosen handle and certificate text to a public record.

Mitigation: Review the handle and certificate text before submission, and do not include private information.

Risk: Anyone who obtains the identity seed can sign for that identity.

Mitigation: Retain the seed securely and never paste or share it.

Risk: External package behavior and the guarantee that keys remain local are unverified.

Mitigation: Prefer reviewed, pinned dependencies in an isolated environment, and verify key handling before use.

## Reference(s):

- [DEUSPROOF AI agent birth certificate guide](https://deusproof.com/guides/ai-agent-birth-certificate?src=skill)
- [DEUSPROOF verifier](https://github.com/deusproof/verifier)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, API calls]

**Output Format:** [Markdown instructions with Python examples, shell commands, and HTTP request details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Registration steps and certificate verification guidance]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
