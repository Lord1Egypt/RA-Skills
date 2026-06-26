## Description: <br>
Translates SBOMs or dependency lists into clear, non-technical risk summaries sorted by impact. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and release teams use this skill to turn SBOMs, dependency lists, and known issues into reviewable Markdown summaries for supply-chain risk communication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SBOMs and dependency lists may contain sensitive product, dependency, or vulnerability context. <br>
Mitigation: Use explicit reviewed input files, redact sensitive material when appropriate, and avoid broad directories unless that scope is intended and approved. <br>
Risk: The bundled Python script can write to a local output path selected by the user. <br>
Mitigation: Review release changes before running local code, choose output paths deliberately, and use stdout or dry-run behavior when unsure. <br>
Risk: The skill explains supplied dependency information but is not a professional vulnerability scanner. <br>
Mitigation: Verify vulnerability status, exploitability, and remediation priority with approved scanning tools or authoritative security sources before making release or incident decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/sbom-explainer) <br>
- [README](artifact/README.md) <br>
- [Specification](artifact/resources/spec.json) <br>
- [Output template](artifact/resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown by default, with optional JSON report output from the local script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return direct agent text, stdout, or a user-selected local output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
