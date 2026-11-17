## Description:

OpenClaw Skills Weekly tracks trending ClawHub skills and generates GitHubAwesome-style YouTube video scripts with two-track ranking for Movers and Rockets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ademczuk](https://clawhub.ai/user/ademczuk)

### License/Terms of Use:


## Use Case:

Developers and content operators use this skill to snapshot ClawHub skill metrics, rank weekly movement, harvest source material, and produce Markdown reports plus voice-ready video scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default execution can install mutable Python dependencies and make multiple external API calls.

Mitigation: Run in an isolated environment, review dependencies before installation, and use limited-scope API tokens.

Risk: The full pipeline can attempt X/Twitter capture and use API keys from the environment.

Mitigation: Use --skip-x unless social signal capture is required, and provide only the environment variables needed for the selected mode.

Risk: The default runner can attempt Docker/container database access through its bridge step.

Mitigation: Use --no-bridge unless container history import is explicitly required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ademczuk/skills/skills-weekly)
- [ClawHub skills API](https://clawhub.ai/api/v1/skills)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, voice-ready text scripts, structured JSON, and terminal status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local SQLite history and dated report artifacts when run.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
