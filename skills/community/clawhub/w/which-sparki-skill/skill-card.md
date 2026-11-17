## Description:

AI-powered video editing guidance that helps an agent route users to the right Sparki workflow, configure Sparki access, upload videos, start edits, poll status, and retrieve finished video results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fischerlam](https://clawhub.ai/user/fischerlam)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to choose an appropriate Sparki video-editing workflow, provide upload and editing instructions, and run Sparki CLI commands for style-guided or prompt-driven edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Videos and prompts may be sent to Sparki or Telegram services.

Mitigation: Use the skill only with media the user is comfortable sharing with those services, and avoid sensitive or confidential videos unless the deployment has approved that transfer.

Risk: Credential handling requires care because the scanner notes plaintext local config behavior.

Mitigation: Prefer SPARKI_API_KEY for short-lived use, avoid saving keys unnecessarily, and rotate the key if it may have been exposed.

Risk: Endpoint scoping can change when --base-url is used.

Mitigation: Use the default Sparki endpoint unless the replacement endpoint is explicitly trusted and approved.

Risk: Downloaded video outputs and result links can expose user media.

Mitigation: Write outputs only to expected locations, review files before sharing, and download promptly because result URLs are described as expiring after 24 hours.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fischerlam/skills/which-sparki-skill)
- [Sparki homepage](https://sparki.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; Sparki CLI commands return JSON and may download video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SPARKI_API_KEY, reads local video paths, writes Sparki config and downloaded video outputs, and calls the Sparki API.]

## Skill Version(s):

1.0.0 (source: frontmatter, pyproject.toml, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
