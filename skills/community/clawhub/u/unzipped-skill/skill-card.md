## Description:

Create Farcaster accounts and post casts autonomously. Official skill from the Farcaster team.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jozh-bit](https://clawhub.ai/user/jozh-bit)

### License/Terms of Use:


## Use Case:

External developers and operators use this skill to create and manage a Farcaster account, including FID registration, profile setup, and posting casts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move wallet funds while registering a Farcaster account and preparing paid API calls.

Mitigation: Use a throwaway wallet with only the minimum funds needed for setup and review each transaction before execution.

Risk: Private keys and Farcaster credentials may be printed or saved as plaintext credentials.

Mitigation: Prefer --no-save or a secure credential vault, restrict file permissions, and rotate or discard exposed keys.

Risk: The artifact claims official Farcaster affiliation while server evidence identifies a third-party publisher and unavailable provenance.

Mitigation: Verify the publisher and source before installation, and run dependency installation and execution in a sandbox.

## Reference(s):

- [Neynar Hub API](https://hub-api.neynar.com)
- [Neynar REST API](https://api.neynar.com)
- [Farcaster Fname Registry](https://fnames.farcaster.xyz)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to run Node.js commands, make network API calls, handle wallet keys, and write local credential files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
