## Description:

Demand-side client to find, claim, and deliver RustChain RIP-302 agent jobs based on skills, rewards, and reputation in an escrow marketplace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scottcjn](https://clawhub.ai/user/scottcjn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and autonomous-agent operators use rtc-work to discover RIP-302 jobs matching skills and reward thresholds, claim jobs, deliver results, and inspect reputation against a RustChain node.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned remote CLI execution can install code that differs from the reviewed 0.1.1 release.

Mitigation: Install only from the reviewed, pinned release and avoid unpinned `uvx rtc-work` in sensitive environments.

Risk: `claim`, `deliver`, and `watch --auto` can change job-market state for the configured wallet and node.

Mitigation: Keep confirmation prompts enabled by default; use `--yes` or `watch --auto` only in trusted workflows after testing with the intended `--node`.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scottcjn/skills/rtc-work)
- [RustChain ecosystem](https://rustchain.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confirmation prompts and node/wallet configuration guidance; no structured binary output.]

## Skill Version(s):

0.1.1 (source: server release metadata and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
