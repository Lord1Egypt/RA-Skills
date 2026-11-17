## Description:

Set up Tamp token compression proxy for OpenClaw to reduce Anthropic API input token costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sliday](https://clawhub.ai/user/sliday)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install and configure Tamp so OpenClaw can route Anthropic requests through a local compression proxy to reduce input token usage and API costs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenClaw Anthropic traffic, including prompts, tool results, and API headers, passes through a third-party local proxy.

Mitigation: Use the skill only when this routing is intentional, start with a temporary foreground run, and review the Tamp package and dependencies before enabling persistent use.

Risk: Persistent service setup can make Tamp the default path for Anthropic traffic.

Mitigation: Avoid sudo, keep direct Anthropic access as the default or fallback, and know how to disable the service and remove the provider configuration before enabling persistence.

Risk: The prune compression stage removes npm lockfile and registry metadata that may be needed for full provenance review.

Mitigation: Remove prune from TAMP_STAGES when full dependency provenance or registry metadata must be preserved for review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sliday/skills/tamp)
- [Tamp Source](https://github.com/sliday/tamp)
- [Tamp Website](https://tamp.dev)
- [Tamp White Paper](https://tamp.dev/whitepaper.pdf)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash commands and JSON/systemd configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local proxy setup, OpenClaw provider configuration, and security guidance.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
