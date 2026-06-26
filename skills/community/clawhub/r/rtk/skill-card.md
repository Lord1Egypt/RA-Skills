## Description: <br>
RTK (Rust Token Kit) is a CLI proxy that reduces LLM token consumption by compressing verbose command output from development tools such as git, file readers, search, tests, linters, Docker, and kubectl. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[radicalgeek](https://clawhub.ai/user/radicalgeek) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to decide when and how to prefix verbose development commands with rtk so command output is compressed before entering model context. It is suited for repeated shell workflows such as repository inspection, test runs, linting, build diagnostics, container logs, and Kubernetes output review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external rtk binary that is not contained in the artifact. <br>
Mitigation: Install and use rtk only from a trusted source, and verify the available binary before relying on its output. <br>
Risk: RTK can wrap mutating commands such as commits, pushes, deployments, Docker, and kubectl actions. <br>
Mitigation: Treat rtk as an output display layer; review command intent and permissions before executing mutating operations. <br>
Risk: Environment variables, logs, and retained tee files may expose secrets to terminal output, model context, local storage, or command history. <br>
Mitigation: Avoid running secret-bearing environment or log commands through rtk unless disclosure is acceptable, and manage tee-log retention according to local policy. <br>


## Reference(s): <br>
- [RTK Full Docs](references/rtk-full-docs.md) <br>
- [RTK GitHub Repository](https://github.com/rtk-ai/rtk) <br>
- [RTK Documentation](https://www.rtk-ai.app) <br>
- [RTK Troubleshooting](https://github.com/rtk-ai/rtk/blob/master/docs/TROUBLESHOOTING.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/radicalgeek/rtk) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on compressed terminal output; failed commands may reference retained full-output tee logs when RTK is configured to save them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
