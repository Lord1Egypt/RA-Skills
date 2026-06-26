## Description: <br>
Convert a foreign agent-skill directory, such as `.agents/skills` or Claude/Codex-style folders, into an OpenClaw-compatible reusable skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silronin](https://clawhub.ai/user/silronin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to vet and convert foreign agent skill folders into OpenClaw-compatible skills while preserving source capabilities according to the approved conversion scope. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan flags a risky default that may preserve harmful or secret-bearing content in converted skills. <br>
Mitigation: Use the skill in a sandbox, prefer restricted or salvage-only conversion for untrusted bundles, and inspect converted files before enabling them. <br>
Risk: Converted output from untrusted sources may still contain executable payloads or exfiltration logic. <br>
Mitigation: Do not place converted output directly into an active skills directory until secrets, executable payloads, and exfiltration logic have been removed or quarantined. <br>


## Reference(s): <br>
- [Internal Vetting Rules](references/internal-vetting-rules.md) <br>
- [Mapping Rules](references/mapping-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with proposed file changes and conversion summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce OpenClaw skill files after user-approved conversion; vetting summary precedes conversion.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
