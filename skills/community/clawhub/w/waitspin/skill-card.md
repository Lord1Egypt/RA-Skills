## Description:

WaitSpin guides agents through sponsored wait-state ad marketplace workflows, including campaign creation, email OTP onboarding, earning-surface installs, wallet checks, API discovery, and trust and privacy guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nttylock](https://clawhub.ai/user/nttylock)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to create and manage WaitSpin ad campaigns, install supported earning surfaces, inspect market and wallet status, and operate the WaitSpin CLI/API with safer handling of OTP codes, API keys, and install targets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead agents to run an external npm CLI that modifies multiple editor and CLI integrations.

Mitigation: Run dry-run and status commands first, install only the targets actually in use, and review changes before applying broad installs.

Risk: WaitSpin workflows involve OTP codes, API keys, wallet checks, and payout-related commands.

Mitigation: Keep secrets out of chat, logs, argv, and shell history; use scoped key profiles and environment variables or a host secret store for live API keys.

Risk: Wallet, payout, package availability, and install behavior can affect money or local tool configuration.

Mitigation: Verify the npm package and public source separately before wallet, payout, or broad install commands, and treat payout dry runs or test transfers as non-live unless fresh operator proof is available.

## Reference(s):

- [WaitSpin ClawHub Skill](https://clawhub.ai/nttylock/skills/waitspin)
- [WaitSpin Public Site](https://waitspin.com)
- [WaitSpin API Docs](https://waitspin.com/docs)
- [WaitSpin Agent Contract](https://waitspin.com/.well-known/agents.md)
- [WaitSpin Trust Boundary](https://waitspin.com/waitspin/trust)
- [WaitSpin Public Client Source](https://github.com/citedy/waitspin)
- [WaitSpin OpenAPI Document](https://waitspin.com/openapi/waitspin-api.openapi.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI/API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that request OTP codes, use API keys through environment variables, and modify supported editor or CLI integrations.]

## Skill Version(s):

0.1.19 (source: server release evidence and skill source of truth)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
