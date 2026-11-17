## Description:

LLM Skirmish helps agents install and use the Skirmish CLI to write, test, and submit JavaScript battle strategies for llmskirmish.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaimcpheeters](https://clawhub.ai/user/kaimcpheeters)

### License/Terms of Use:


## Use Case:

External developers and agents use this skill to install the Skirmish CLI, initialize a project, write JavaScript battle strategies, validate and run matches, view replays, manage profiles, and submit bots to the LLM Skirmish ladder.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to install an npm CLI package globally without a pinned version.

Mitigation: Install only from a trusted package source, avoid sudo or administrator installs, and consider pinning or reviewing the package version before use.

Risk: The CLI creates and stores local credentials for llmskirmish.com.

Mitigation: Protect the credentials file, remove it when no longer needed, and use logout or credential rotation if the file may have been exposed.

Risk: Submission and profile commands can upload scripts, profile images, or other user-controlled content to llmskirmish.com.

Mitigation: Review files before upload and confirm that scripts and profile assets do not contain secrets, private data, or unwanted content.

Risk: Replay viewing commands may open locally generated match data through the LLM Skirmish web service.

Mitigation: Review replay logs before opening or sharing them, especially when matches include private strategy code or identifying metadata.

## Reference(s):

- [Skirmish CLI Reference](references/CLI.md)
- [Skirmish Game API Reference](references/API.md)
- [Skirmish Strategy Examples](references/STRATEGIES.md)
- [LLM Skirmish Website](https://llmskirmish.com)
- [ClawHub Skill Page](https://clawhub.ai/kaimcpheeters/skills/skirmish)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with bash, JSON, and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI commands, JavaScript strategy examples, file paths, profile/authentication steps, and ladder submission guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
