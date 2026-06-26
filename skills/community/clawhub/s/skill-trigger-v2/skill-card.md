## Description: <br>
Framework-only skill trigger reference. Runtime matching implementation has been removed from the published artifact. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[halfmoon82](https://clawhub.ai/user/halfmoon82) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Skill Trigger V2 as a framework reference for declaring how user intent maps to skill routing, dependencies, and first-line routing declarations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is presented as documentation-only, but the artifact still ships Python code that can influence skill routing and setup behavior. <br>
Mitigation: Install only when an active routing component is intended, review Python files before running setup commands, and require user confirmation or an allowlist before wiring automatic skill execution. <br>
Risk: Routing decisions depend on local skill index and router state that may be incorrect or untrusted. <br>
Mitigation: Keep the local skill index and semantic router configuration reviewable, versioned, and limited to trusted skills before enabling dispatch behavior. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/halfmoon82/skill-trigger-v2) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional Python and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce routing declarations and configuration guidance; the artifact also includes runnable Python routing and setup code.] <br>

## Skill Version(s): <br>
2.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
