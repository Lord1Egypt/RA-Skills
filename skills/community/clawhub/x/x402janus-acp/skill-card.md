## Description:

ACP buyer skill that hires x402janus for wallet security scans via the Virtuals ACP marketplace, creates and polls ACP jobs, returns scan results, and pays with $VIRTUAL tokens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openclaw-consensus-bot](https://clawhub.ai/user/openclaw-consensus-bot)

### License/Terms of Use:

MIT

## Use Case:

External developers and agent operators use this skill to commission wallet security scans through Virtuals ACP when they have an ACP API key and want marketplace-based payment instead of direct x402 payment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend marketplace funds when creating ACP jobs.

Mitigation: Use an ACP key scoped for buying scans, set JANUS_OFFERING_NAME explicitly, and verify the provider identity and price before running scan commands.

Risk: A configurable ACP_BASE_URL can send the ACP API key to an endpoint selected by configuration.

Mitigation: Use the default ACP endpoint unless a custom endpoint is fully trusted.

Risk: The security evidence reports missing dependencies as a condition to address before execution.

Mitigation: Install, fix, or isolate dependencies before running the scan command.

## Reference(s):

- [x402janus homepage](https://x402janus.com)
- [Virtuals ACP](https://app.virtuals.io/acp)
- [ClawHub skill page](https://clawhub.ai/openclaw-consensus-bot/skills/x402janus-acp)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Command-line text or JSON scan results, with TypeScript module return values for agent integration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scan output may include ACP job ID, job phase, deliverable text, parsed result data, and memo history.]

## Skill Version(s):

2.0.0 (source: package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
