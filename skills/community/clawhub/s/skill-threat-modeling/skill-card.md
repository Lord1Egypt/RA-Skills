## Description:

Threat Modeling helps agents perform code-first STRIDE security analysis and produce risk assessments, DFDs, threat inventories, attack path validation, mitigation plans, and penetration test plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fr33d3m0n](https://clawhub.ai/user/fr33d3m0n)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to assess application designs and codebases, plan penetration testing, and generate security review deliverables. It supports both full 8-phase threat modeling and focused security consultation, vulnerability analysis, and test generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can overwrite global Claude settings or install a persistent write hook.

Mitigation: Prefer project-local installation, manually merge any hook configuration after review, and remove or disable hooks when finished.

Risk: Generated POC and penetration testing guidance could be misused outside an authorized assessment.

Mitigation: Use exploit, POC, and pentest outputs only for systems where testing is explicitly authorized.

Risk: Generated HTML reports may contain untrusted browser content, especially when Mermaid diagrams are present.

Mitigation: Prefer Markdown or offline viewing, or sanitize and bundle browser dependencies before sharing HTML reports.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fr33d3m0n/skills/skill-threat-modeling)
- [README](artifact/README.md)
- [Workflow](artifact/WORKFLOW.md)
- [Report Design](artifact/docs/REPORT-DESIGN.md)
- [Architecture Workflow Guide](artifact/docs/ARCHITECTURE-WORKFLOW-GUIDE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, YAML data files, HTML reports, code snippets, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default mode publishes user-facing reports; debug mode can expose internal YAML data and evaluation files.]

## Skill Version(s):

3.1.0 (source: server release metadata and artifact version banner)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
