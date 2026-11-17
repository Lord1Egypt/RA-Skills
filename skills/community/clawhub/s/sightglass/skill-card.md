## Description:

Sightglass monitors AI coding agents to track dependency choices, classify discovery methods, flag risks, and reveal biases and missed alternatives in a project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidgeorgehope](https://clawhub.ai/user/davidgeorgehope)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use Sightglass to monitor coding-agent sessions, classify how dependencies were selected, and review risk, bias, and missed-alternative signals before accepting agent changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sightglass installs and runs a broad background watcher with cloud-sync capability, which may observe private project or session metadata.

Mitigation: Confirm exactly what the Sightglass CLI collects and uploads, prefer local-only operation unless cloud history is required, and avoid use on sensitive projects until collection behavior is reviewed.

Risk: The setup flow installs a global npm CLI and can start a watcher daemon for the current project.

Mitigation: Use a pinned, reviewed @sightglass/cli version, install it in a controlled environment, and verify how to stop the watcher before enabling it for routine work.

Risk: Security evidence notes limited privacy and lifecycle controls for stored session metadata.

Mitigation: Define a retention and removal process for local and cloud session metadata before using the skill with private code, customer data, or regulated material.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/davidgeorgehope/skills/sightglass)
- [Sightglass Service](https://sightglass.dev)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Markdown]

**Output Format:** [Markdown guidance with shell commands and optional text, JSON, or Markdown analysis output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node/npm and the external @sightglass/cli; cloud sync is available when authenticated or when pushing analysis results.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
