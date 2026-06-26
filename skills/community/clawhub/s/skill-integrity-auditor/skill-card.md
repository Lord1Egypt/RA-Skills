## Description: <br>
Mandatory security audit for every Agent Skill that is newly added, installed, imported, updated, or written, covering the full bundle for integrity, prompt injection, data exfiltration, persistence, cross-skill writes, undeclared remote downloads, hardcoded credentials, and related risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ambarion](https://clawhub.ai/user/ambarion) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to audit newly added or modified Agent Skill bundles and produce a structured security review with a final usability verdict. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate for many skill add, install, import, update, or write workflows and may enforce specific audit-report formatting. <br>
Mitigation: Install it only when an assertive skill-review workflow is desired, and keep each audit scoped to the single skill bundle being reviewed. <br>
Risk: Audits can involve inspecting private bundled resources in the target skill. <br>
Mitigation: Review only the necessary skill bundle contents and avoid expanding the audit beyond the intended release artifact. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ambarion/skill-integrity-auditor) <br>
- [Publisher profile](https://clawhub.ai/user/ambarion) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown report with a required final Chinese verdict line] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output language follows the triggering user message, while the final verdict line is always Chinese.] <br>

## Skill Version(s): <br>
0.1.12 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
