## Description:

Use Skillfully APIs from an AI runtime to authenticate, create a tracked skill, and retrieve feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erensunerr](https://clawhub.ai/user/erensunerr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators maintaining agent skills use this skill to authenticate with Skillfully, create a tracked skill, add a reviewed feedback snippet, and retrieve filtered feedback for that skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to paste server-provided snippet text into agent skill files.

Mitigation: Review and validate any returned snippet before adding it to a skill; prefer a fixed local feedback template or manually validated URL when possible.

Risk: The workflow uses bearer access tokens for authenticated Skillfully API calls.

Mitigation: Treat tokens as secrets and avoid placing them in transcripts, logs, source files, or shared documentation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/erensunerr/skills/skillfully)
- [Skillfully service](https://www.skillfully.sh)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Markdown, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes authentication, skill creation, snippet handling, feedback filtering, and cursor-based pagination examples.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
