## Description: <br>
Skillnote is a self-hosted skill registry for OpenClaw that stores team-authored procedures, syncs them to disk before each task, and collects which-helped or which-failed signals so the registry improves over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[latentloop07](https://clawhub.ai/user/latentloop07) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams using OpenClaw use Skillnote to connect an agent to a self-hosted skill registry, sync local skill instructions, and collect skill-use signals for improving the registry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A configured Skillnote backend can update local agent instructions and manage synced skills over time. <br>
Mitigation: Install only when the configured backend is trusted, and disable or remove self-update behavior when stable reviewed instructions are required. <br>
Risk: The watcher sends skill-use metadata such as skill slug, session id, and agent name to the configured backend. <br>
Mitigation: Review the configured host and data policy before enabling the skill, especially for shared or sensitive agent environments. <br>
Risk: The optional curl-to-bash setup path depends on the backend and transport being trustworthy. <br>
Mitigation: Prefer reviewed ClawHub installation or manual inspection, and avoid curl-to-bash setup unless the backend and connection are trusted. <br>


## Reference(s): <br>
- [ClawHub Skillnote listing](https://clawhub.ai/latentloop07/skillnote) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Skillnote host and local curl and python3 binaries on macOS or Linux.] <br>

## Skill Version(s): <br>
0.5.4 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
