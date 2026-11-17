## Description:

Use when the user wants to run the Tock reservation sniper for a timed release or cancellation watch, locally on their Mac or on a remote node.

This skill is ready for commercial/non-commercial use.

## Publisher:

[murphykobe](https://clawhub.ai/user/murphykobe)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to gather reservation preferences, choose a local or remote execution target, and run a concrete t0cksn1per command for timed Tock releases or cancellation watches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill tells the agent to execute an unpinned third-party package that can change after review.

Mitigation: Prefer a pinned, reviewed t0cksn1per version and run it in a constrained user environment.

Risk: Unattended node use or CDP browser automation can act with the user's local permissions and browser context.

Mitigation: Use CDP only when explicitly requested, keep Playwright-managed launch as the default fallback, and review the command before unattended execution.

## Reference(s):

- [Command Examples](references/commands.md)
- [CDP Mode](references/cdp.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one concrete t0cksn1per command and may run it.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
