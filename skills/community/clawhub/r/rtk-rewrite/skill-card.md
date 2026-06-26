## Description: <br>
RTK Rewrite intercepts OpenClaw exec tool calls and delegates command rewrites to rtk rewrite to reduce token usage while preserving command intent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luw2007](https://clawhub.ai/user/luw2007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this OpenClaw plugin to automatically rewrite supported shell commands through RTK before execution, primarily to reduce token usage while keeping command intent aligned. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin can automatically change shell commands before they run. <br>
Mitigation: Install only when RTK command rewriting is intended, and review the installed rtk tool and rewrite rules before enabling the plugin. <br>
Risk: Optional verbose or audit logging can expose command text that contains tokens, credentials, private paths, or proprietary operational details. <br>
Mitigation: Keep audit and verbose logging disabled unless needed for troubleshooting, and avoid enabling them around sensitive commands. <br>


## Reference(s): <br>
- [RTK Rewrite on ClawHub](https://clawhub.ai/luw2007/rtk-rewrite) <br>
- [luw2007 ClawHub Publisher Profile](https://clawhub.ai/user/luw2007) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, text] <br>
**Output Format:** [Rewritten command strings and optional text audit log entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the rtk command-line tool in PATH; optional audit logging may store original and rewritten command text locally.] <br>

## Skill Version(s): <br>
0.15.3 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
