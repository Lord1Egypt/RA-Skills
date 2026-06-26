## Description: <br>
Log into bollo.video or vibevideo.io, list Studio projects with web links, create a Studio episode from a script with style/aspect-ratio/project selection, and log out. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vibevideo](https://clawhub.ai/user/vibevideo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate VibeVideo or Bollo Studio from an agent workflow: authenticate, list projects, and create AI video episodes from prompts or scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates a real bollo.video or vibevideo.io Studio account and sends user-provided scripts to that service. <br>
Mitigation: Select the intended site explicitly and avoid submitting sensitive scripts unless that disclosure is intended. <br>
Risk: The login flow can retain a local session token by default. <br>
Mitigation: Use --no-save for an ephemeral session or run logout when the saved session is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vibevideo/vibevideo-core) <br>
- [VibeVideo Studio](https://vibevideo.io) <br>
- [Bollo Studio](https://bollo.video) <br>
- [Third-Party Agent Bridge Architecture](references/architecture.md) <br>
- [Provider Integration Checklist](references/provider-integration-checklist.md) <br>
- [Current System Map](references/current-system-map.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or remove VibeVideo/Bollo Studio session state and may return project or episode URLs.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
