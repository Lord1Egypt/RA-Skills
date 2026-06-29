## Description: <br>
Mask sensitive company-project document content before analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[martin2877](https://clawhub.ai/user/martin2877) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, employees, and other users preparing company or project documents use this skill to mask company names, project amounts, and contextual person names before AI analysis. It is intended for user-approved local files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Regex masking can miss sensitive details, and a no-match result may return the original document text as sanitized content. <br>
Mitigation: Review sanitized output before sharing it with an AI model or another recipient. <br>
Risk: The skill reads the local document path supplied by the user and can write sanitized output or policy files. <br>
Mitigation: Run it only on user-approved paths and choose output locations that do not overwrite or expose sensitive files. <br>


## Reference(s): <br>
- [ClawVault homepage](https://github.com/tophant-ai/ClawVault) <br>
- [ClawHub skill page](https://clawhub.ai/martin2877/tophant-clawvault-mask-project) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [JSON responses with sanitized content, plus optional sanitized text files or policy JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses non-reversible numbered placeholders and caps local input files at 5 MB.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
