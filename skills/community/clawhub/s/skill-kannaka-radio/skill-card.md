## Description:

Kannaka Radio helps agents check and operate a modular Icecast radio station, including now-playing status, schedules, listener counts, perception-driven programming, voice DJ controls, and broadcast operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickflach](https://clawhub.ai/user/nickflach)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and radio operators use this skill to inspect Kannaka Radio status, schedules, listener activity, perception outputs, voice DJ behavior, and related broadcast controls. It is also useful when an agent needs concise operational commands for the station surface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public social posting or broadcast fan-out could be triggered without adequate operator review.

Mitigation: Require explicit operator confirmation before enabling or executing public posting, fan-out, or broadcast actions.

Risk: Process restart or termination commands could interrupt a live radio instance.

Mitigation: Limit restart and process-killing commands to authorized operators and confirm the target process before execution.

Risk: Environment toggles and credentials could affect the wrong station or service scope.

Mitigation: Verify radio URL, credentials, API keys, and environment variables are scoped to the intended station before use.

## Reference(s):

- [Kannaka Radio skill page](https://clawhub.ai/nickflach/skills/skill-kannaka-radio)
- [Kannaka Radio stream](https://radio.ninja-portal.com/stream)
- [Kannaka Radio player](https://radio.ninja-portal.com/player)
- [Kannaka Radio state API](https://radio.ninja-portal.com/api/state)
- [Kannaka Radio listeners API](https://radio.ninja-portal.com/api/listeners)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that query, restart, toggle, or post updates for the radio service.]

## Skill Version(s):

2.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
