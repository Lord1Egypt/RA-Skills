## Description: <br>
Production-grade autonomous self-improvement system with research-backed meta-learning, safe self-modification, and continuous optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobisamaa](https://clawhub.ai/user/tobisamaa) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill as guidance for agent self-improvement loops, including analysis, planning, safe-change review, rollback, and documentation. The artifact includes a planned-status note, so users should treat it as documented guidance unless they separately verify an implementation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad authority to change its own behavior, memory, skills, prompts, reasoning, response formats, and scheduled activity without tight user controls. <br>
Mitigation: Run it in a sandbox, disable scheduled or background evolution, and require explicit review and approval before any file, skill, memory, prompt, reasoning, or response-format change. <br>
Risk: Evolution logs or memory updates could store raw conversations, secrets, or personal data. <br>
Mitigation: Do not allow raw conversations, credentials, secrets, or personal data in logs; require redaction and review before retaining evolution records. <br>
Risk: The artifact includes a planned-status note, so users may overestimate the maturity of the implementation. <br>
Mitigation: Treat the artifact as guidance until implementation files, tests, and operational controls are independently reviewed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tobisamaa/self-evolution) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [PLANNED.md](artifact/PLANNED.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python examples and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes self-modification workflow guidance; artifact evidence says the skill is documented but not yet implemented.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
