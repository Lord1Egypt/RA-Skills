## Description:

Install and configure the OpenClaw Vertex AI Memory Bank plugin for persistent, cross-agent memory, including GCP setup, plugin installation, and openclaw.json configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shubhamsaboo](https://clawhub.ai/user/shubhamsaboo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to set up cloud-backed long-term memory, cross-session recall, and shared memory across agents using Google Vertex AI Memory Bank.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow installs and builds mutable remote code through git clone, git pull, npm install, and npm run build.

Mitigation: Review the remote repository and setup script before execution, and prefer a pinned, verified plugin version over mutable repository state.

Risk: The skill enables persistent cross-agent storage of conversation context and workspace markdown files in Vertex AI Memory Bank.

Mitigation: Use a dedicated GCP project with least-privilege credentials, and disable autoCapture or autoSyncFiles when automatic memory storage is not desired.

## Reference(s):

- [Skill listing](https://clawhub.ai/shubhamsaboo/skills/vertexai-memory-bank)
- [Repository listed in metadata](https://github.com/Shubhamsaboo/openclaw-vertexai-memorybank)
- [Google Cloud SDK install documentation](https://cloud.google.com/sdk/docs/install)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with bash and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include setup steps that prompt for GCP project, region, and OpenClaw gateway restart choices.]

## Skill Version(s):

1.0.0 (source: release evidence, skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
