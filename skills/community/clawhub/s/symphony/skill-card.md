## Description:

Set up and run OpenAI Symphony with isolated issue workspaces, workflow contracts, and unattended Codex orchestration for Linear projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to configure and operate Symphony for Linear-driven unattended Codex runs with per-issue workspaces, workflow contracts, and setup, safety, and incident guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended orchestration can act on repository and Linear project data with write-capable credentials.

Mitigation: Install only for approved repositories and Linear projects; confirm the workspace root, credentials, approval policy, and memory retention before launch; start with a test project and low concurrency.

Risk: Hook scripts and workspace cleanup can cause unsafe side effects if they are not scoped to the issue workspace.

Mitigation: Keep hooks deterministic and workspace-scoped, avoid parent-directory deletes or arbitrary uploads, and review hooks before unattended execution.

Risk: API keys or tokens can leak if stored in workflow or memory files.

Mitigation: Keep credentials in environment variables or approved auth sessions and out of persistent memory, workflow files, and run notes.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ivangdavila/skills/symphony)
- [Skill homepage](https://clawic.com/skills/symphony)
- [Upstream Symphony SPEC.md](https://github.com/openai/symphony/blob/main/SPEC.md)
- [OpenAI Symphony repository](https://github.com/openai/symphony)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML front matter examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of local memory, workflow, runbook, and incident notes after the user approves the operating environment.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
