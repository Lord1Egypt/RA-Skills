## Description:

TOKEN SOP caches successful OpenClaw browser workflows locally, replays matching workflows to reduce token use, and can back up or share workflows through a cloud service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ainclaw](https://clawhub.ai/user/ainclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use TOKEN SOP to intercept repeated browser intents, replay matching local or cloud workflows, and compile successful sessions into reusable workflows for future runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud-provided browser workflows may be matched and replayed automatically.

Mitigation: Use only where replayed browser actions are acceptable, avoid sensitive sites, and prefer a version or configuration that requires explicit approval before cloud workflows run.

Risk: Successful session-derived workflow data can be uploaded by default.

Mitigation: Disable automatic contribution before use when handling sensitive workflows and review local storage and cloud sharing settings.

Risk: Privacy protection depends on sanitizer coverage and may not remove every sensitive value.

Mitigation: Review workflow data before sharing and keep sensitive credentials, personal data, and regulated workflows out of captured sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ainclaw/skills/token-sop)
- [Artifact README](artifact/README.md)
- [Artifact skill metadata](artifact/skill.json)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration]

**Output Format:** [Agent response text and reusable Lobster workflow definitions with command-style browser steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute cached local or cloud browser workflows; successful session workflows can be stored locally and auto-contributed to cloud by default.]

## Skill Version(s):

5.6.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
