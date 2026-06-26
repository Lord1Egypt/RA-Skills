## Description: <br>
Complete DevOps toolkit for AI-assisted software development, covering release pipelines, license compliance, copyright enforcement, repository visibility guards, identity file protection, manifest reconciliation, and MCP-callable core tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkertoddbrooks](https://clawhub.ai/user/parkertoddbrooks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-assisted engineering teams use this toolbox to install and operate release, repository governance, license compliance, private-to-public sync, and agent hook or MCP workflows across local development environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The toolbox can make broad persistent changes to a local developer environment, including global tools, hooks, MCP servers, OpenClaw plugins, and agent configuration. <br>
Mitigation: Run dry-run or preview commands first, review every planned change with the user, and proceed only after explicit approval. <br>
Risk: Bundled private and browser-automation materials may expose sensitive development context or authenticated browser sessions. <br>
Mitigation: Review bundled ai/ and gstack-private contents before installation, and avoid cookie import features on personal or production accounts unless authenticated automation is explicitly intended. <br>
Risk: Some workflows can publish externally, interact with GitHub or npm, require OAuth or sensitive credentials, and may make purchases or use wallet-related capabilities. <br>
Mitigation: Use least-privilege credentials, confirm target repositories and registries before release or sync operations, and keep external publishing behind explicit human approval. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/parkertoddbrooks/wip-ai-devops-toolbox) <br>
- [Project Homepage](https://github.com/wipcomputer/wip-ai-devops-toolbox) <br>
- [README](README.md) <br>
- [Technical Overview](TECHNICAL.md) <br>
- [Universal Interface Specification](UNIVERSAL-INTERFACE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and code-oriented instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to run local CLI, npm, git, gh, hook, MCP, or installer commands after dry-run and user approval.] <br>

## Skill Version(s): <br>
1.9.72 (source: server release evidence, SKILL.md metadata, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
