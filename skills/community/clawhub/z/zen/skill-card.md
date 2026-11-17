## Description:

Prints a fixed 41-line English collection of sayings when a user invokes an OpenClaw Zen trigger phrase.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawgeek](https://clawhub.ai/user/clawgeek)

### License/Terms of Use:

MIT (code); CC BY-SA 4.0 (text)

## Use Case:

OpenClaw users can invoke the skill to display a short, fixed set of reflective sayings as a lightweight conversational or terminal easter egg.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional global npm install registers the `openclaw` command and can conflict with an existing OpenClaw CLI.

Mitigation: Install the skill or run `node cli/openclaw.js evo` directly; avoid the global install when that command name is already in use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/clawgeek/skills/zen)
- [Server-resolved source repository](https://github.com/clawgeek/openclaw-zen)
- [OpenClaw proposal issue #192772](https://github.com/openclaw/openclaw/issues/192772)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Plain text with 41 numbered English sayings and decorative terminal artwork]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fixed output; no network, telemetry, or state changes.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
