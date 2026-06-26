## Description: <br>
Tool Registry is a token-based tool registration and discovery system for routing tool queries through weighted matching, permission filtering, and agent-type allowlists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xhmqq616](https://clawhub.ai/user/xhmqq616) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to register, discover, filter, and execute local tools by token match, permission level, and allowed agent type. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Built-in file-writing and shell-command tools can modify files or run commands if invoked by an untrusted caller. <br>
Mitigation: Disable or remove write_file and bash unless they are required, and enforce permission checks, path limits, command allowlists, and explicit confirmation before writes or shell actions. <br>
Risk: Token-based routing can select a more capable tool than intended when aliases, keywords, or descriptions are broad. <br>
Mitigation: Constrain tools by agent type and permission level, and require callers to inspect the selected tool and permission before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xhmqq616/tool-registry) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples and CLI text or JSON results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a JavaScript module that can return registry matches, tool metadata, execution results, and tool statistics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
