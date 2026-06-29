## Description: <br>
Use when preparing a Skill folder for public release to SkillHub, ClawHub, or another agent-skill marketplace, especially before publishing third-party installable skills, scripts, references, metadata, or examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[debtvc2022](https://clawhub.ai/user/debtvc2022) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this skill to audit agent skill folders before public marketplace release. It checks structure, discovery metadata, safety, scripts, links, and packaging, then reports a READY, READY_WITH_WARNINGS, or BLOCKED decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The auditor reads files in the candidate skill folder, which may include sensitive or private content if pointed at the wrong directory. <br>
Mitigation: Run it only against skill folders intended for review or publication, and review generated findings before sharing them. <br>
Risk: Python compile checks may create normal bytecode cache files while inspecting scripts. <br>
Mitigation: Run the audit in a disposable copy or clean generated __pycache__ files after the review if the package must stay unchanged. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/debtvc2022/skillhub-publish-auditor) <br>
- [release-checklist.md](references/release-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, JSON, shell commands] <br>
**Output Format:** [Markdown or JSON audit report with file-level findings and a release decision] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are labeled blocker, warn, or info; final decisions are READY, READY_WITH_WARNINGS, or BLOCKED.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
