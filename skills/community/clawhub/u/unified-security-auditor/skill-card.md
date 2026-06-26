## Description: <br>
Unified application security skill for Coding Agent systems like OpenCode, used when reviewing or writing code that touches authentication, authorization, user input, payments, database access, secrets, deployment, dependencies, or AI/agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[selimerunkut](https://clawhub.ai/user/selimerunkut) <br>

### License/Terms of Use: <br>
CC-BY-SA-4.0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit codebases, review security-sensitive changes, and produce prioritized remediation guidance for application, dependency, deployment, and agentic AI risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to save a dated security audit report into the current project. <br>
Mitigation: Confirm whether the report should remain in chat or be written to disk, and confirm the destination path before creating a file. <br>


## Reference(s): <br>
- [claude-code-owasp](https://github.com/agamm/claude-code-owasp) <br>
- [trailofbits/skills](https://github.com/trailofbits/skills) <br>
- [vibe-security-skill](https://github.com/raroque/vibe-security-skill) <br>
- [VibeSec-Skill](https://github.com/BehiSecc/VibeSec-Skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown with structured findings, prioritized recommendations, and optional diff snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save a dated markdown audit report when the user requests a file output.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
