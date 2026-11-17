## Description:

Generate and edit video with Veo 3 through RunAPI, using the RunAPI CLI for one-off generation and SDK guidance for app or backend integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to create, edit, or transform video with Veo 3 through RunAPI, including one-off CLI jobs and SDK-oriented integration planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow installs and uses an unpinned third-party RunAPI CLI from a Homebrew tap.

Mitigation: Install only in trusted environments, review the CLI source or release provenance when available, and pin a known version where the environment supports it.

Risk: The CLI may access RunAPI authentication state, selected local media files, generated outputs, and billable Veo jobs.

Mitigation: Use environment authentication or saved CLI configuration, validate authentication before submitting, avoid unnecessary interactive login, and require user authorization before any replacement paid request.

## Reference(s):

- [RunAPI Veo 3.1 homepage](https://runapi.ai/models/veo-3.1)
- [Model overview, pricing, and rate limits](https://runapi.ai/models/veo-3.1.md)
- [Provider overview](https://runapi.ai/providers/google.md)
- [Full model catalog](https://runapi.ai/models.md)
- [SDK integration](https://github.com/runapi-ai/veo-3.1-sdk)
- [ClawHub skill page](https://clawhub.ai/runapi-ai/skills/runapi-veo-3-1)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, JSON, Files]

**Output Format:** [Markdown guidance with shell commands, JSON request and response files, and downloaded media deliverables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local media inputs and can produce downloaded video files after verifying response contracts and MIME types.]

## Skill Version(s):

0.2.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
