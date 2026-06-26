## Description: <br>
Super Dev pipeline governance: research-first, commercial-grade AI coding delivery with 10 expert roles, quality gates, and audit artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shangyankeji](https://clawhub.ai/user/shangyankeji) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to run a governed AI coding pipeline from research and documentation through implementation, quality gates, deployment setup, and delivery artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for broad project access and routes work through an external Super Dev CLI/plugin. <br>
Mitigation: Install only when the publisher and CLI are trusted, use a branch or disposable worktree, and review generated diffs before merging. <br>
Risk: The documented super_dev_run command can execute arbitrary CLI commands and should be treated as high impact. <br>
Mitigation: Review each command before execution and avoid running it in secret-heavy projects unless offline and data-sharing behavior is clear. <br>


## Reference(s): <br>
- [Super Dev Pipeline Skill](https://clawhub.ai/shangyankeji/super-dev) <br>
- [Super Dev Homepage](https://superdev.goder.ai) <br>
- [Commands](references/commands.md) <br>
- [Pipeline Stages](references/pipeline-stages.md) <br>
- [Gate Interactions](references/gate-interactions.md) <br>
- [Expert Roles](references/expert-roles.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, generated project files, review artifacts, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the external super-dev CLI and OpenClaw plugin tools; generated artifacts are expected under output/, .super-dev/, frontend/, backend/, and deployment configuration paths.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
