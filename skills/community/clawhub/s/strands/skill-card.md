## Description: <br>
Build and run Python-based AI agents using the AWS Strands SDK for autonomous agents, multi-agent workflows, custom tools, MCP integrations, and provider-specific agent scaffolding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TrippingKelsea](https://clawhub.ai/user/TrippingKelsea) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to create, configure, and run Python-based Strands agents across local, direct API, Bedrock, and MCP-backed workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated agents can receive broad local file and shell access through the scaffolded tools. <br>
Mitigation: Review generated code before running it, remove or constrain shell and file-write tools, and run agents in a sandboxed project directory or container. <br>
Risk: Provider credentials and cloud permissions may be available to agents at runtime. <br>
Mitigation: Use least-privilege API and cloud credentials and avoid exposing unrelated environment variables to the agent process. <br>
Risk: MCP servers or imported agent files can extend the agent's effective capability surface. <br>
Mitigation: Connect only trusted MCP servers and load only reviewed local agent files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/TrippingKelsea/strands) <br>
- [Strands SDK repository](https://github.com/strands-agents/sdk-python) <br>
- [Strands SDK Cheatsheet](references/cheatsheet.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; scaffolded Python files and configuration when helper scripts are run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated agents may include local file-read, file-write, and shell-command tools.] <br>

## Skill Version(s): <br>
2.0.3 (source: server release metadata; artifact frontmatter lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
