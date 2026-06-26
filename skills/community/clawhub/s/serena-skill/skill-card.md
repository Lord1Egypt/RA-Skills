## Description: <br>
Use Serena-backed semantic code navigation and editing when working in existing software projects with non-trivial structure, especially multi-file repos where symbol-aware lookup and targeted edits are more reliable and token-efficient than brute-force file reading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juanclaw](https://clawhub.ai/user/juanclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use Serena to inspect structured software projects, trace symbol relationships, and make targeted code edits through Serena-backed semantic navigation tools when those tools are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward file edits, shell execution, or passthrough Serena capabilities when those tools are available. <br>
Mitigation: Use it in repositories where those actions are acceptable, keep edits narrow, and review broad commands or diffs before high-impact changes. <br>
Risk: Serena results may be unavailable, fail, or be ambiguous for a target project. <br>
Mitigation: Explain the failure or ambiguity, fall back to ordinary file tools, and avoid claiming semantic confirmation when it was not obtained. <br>


## Reference(s): <br>
- [Integration patterns](references/integration-patterns.md) <br>
- [ClawHub skill page](https://clawhub.ai/juanclaw/serena-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, shell commands, code] <br>
**Output Format:** [Markdown guidance with tool and command names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are workflow instructions for agents using available Serena tools; the skill itself does not declare runtime configuration.] <br>

## Skill Version(s): <br>
0.1.7 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
