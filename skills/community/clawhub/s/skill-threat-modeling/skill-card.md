## Description: <br>
AI-native automated software risk analysis skill for threat modeling, security assessment, vulnerability analysis, security auditing, penetration test preparation, and compliance-oriented review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fr33d3m0n](https://clawhub.ai/user/fr33d3m0n) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and authorized reviewers use this skill to run an 8-phase STRIDE workflow over a codebase or design and produce security findings, risk validation, mitigation planning, and penetration-test planning deliverables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can generate exploit POCs, attack chains, penetration-test plans, and security test payloads. <br>
Mitigation: Use it only for authorized security work, and review any generated commands, scripts, or payloads before running them in an isolated lab or approved test environment. <br>
Risk: Debug mode can publish internal YAML, knowledge-base queries, evaluation details, and sensitive security-analysis context. <br>
Mitigation: Keep --debug output private, restrict access to generated reports, and avoid debug mode when analyzing confidential systems unless storage and sharing controls are in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fr33d3m0n/skill-threat-modeling) <br>
- [README](artifact/README.md) <br>
- [Workflow orchestration contracts](artifact/WORKFLOW.md) <br>
- [Report design](artifact/docs/REPORT-DESIGN.md) <br>
- [Architecture workflow guide](artifact/docs/ARCHITECTURE-WORKFLOW-GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with structured YAML working data and optional HTML report output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default mode publishes user-facing risk assessment, inventory, mitigation, penetration-test plan, and phase reports; debug mode can expose internal YAML and evaluation details.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release metadata, artifact README, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
