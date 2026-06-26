## Description: <br>
Translates DOCX manuals into a target language while preserving document structure and supporting screenshot-oriented localization workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QianziTech](https://clawhub.ai/user/QianziTech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to localize product manuals by translating DOCX content, tables, and related document assets into a requested target language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Manual text may be sent to DeepLX or another configured translation service. <br>
Mitigation: Use only approved documents and a limited API key, and avoid confidential or regulated content unless third-party translation is authorized. <br>
Risk: The skill writes translated DOCX files to user-provided output paths. <br>
Mitigation: Choose explicit output paths and review generated files before replacing source manuals. <br>
Risk: Screenshot replacement workflows may require starting local or web applications. <br>
Mitigation: Only run or capture applications from trusted projects and environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QianziTech/translate-manual) <br>
- [DeepLX translation endpoint](https://api.deeplx.org/{API_KEY}/translate) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [DOCX output files with Markdown guidance and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a configured translation API key and writes translated output paths selected by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
