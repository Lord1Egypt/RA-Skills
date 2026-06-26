## Description: <br>
Redacta pseudonymises medical and clinical documents by replacing patient identifiers with labelled tokens while preserving clinical meaning, then returns redacted text and a redaction report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickjlamb](https://clawhub.ai/user/nickjlamb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Healthcare, compliance, and AI-assisted documentation users use Redacta to pseudonymise clinical text before sharing it or sending it to another AI tool. It can also restore original identifiers from a token map when re-identification is intended. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reversible token maps contain or can restore sensitive PHI/PII. <br>
Mitigation: Protect token maps like the original clinical text, avoid sharing them with redacted output unless re-identification is intended, and delete or secure temporary files. <br>
Risk: Redaction may miss residual identifiers in clinical text. <br>
Mitigation: Review the redacted output and redaction report before sharing, and treat Redacta as a first line of defence rather than a substitute for formal data-protection review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nickjlamb/redacta) <br>
- [Redacta reference](reference.md) <br>
- [Redacta product page](https://www.pharmatools.ai/redacta) <br>
- [Agent Skills open standard](https://agentskills.io) <br>
- [redacta-mcp npm package](https://www.npmjs.com/package/redacta-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown response with redacted or re-identified text, a redaction report, an optional token map, and limits guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Token maps can restore original identifiers and should be separated from redacted output unless re-identification is intended.] <br>

## Skill Version(s): <br>
1.2.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
