## Description: <br>
Professional technical documentation translation expert, proficient in internet industry terminology. Translates user-provided files, preserves original formatting, and performs professional accuracy and format validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and documentation maintainers use this skill to translate technical documentation, API references, READMEs, blogs, specifications, and structured documentation files while preserving formatting and protected technical content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Translations are written to the workspace root and may overlap with existing language-suffixed files or folders. <br>
Mitigation: Check the workspace destination before folder mode and review generated paths before relying on the output. <br>
Risk: URL inputs require the agent to fetch external content. <br>
Mitigation: Use trusted URLs and avoid URL mode when network access or external content handling is not acceptable. <br>
Risk: Validation may identify terminology, format, or protected-content issues without automatically retranslating. <br>
Mitigation: Review the validation summary and confirm flagged issues before publishing or using translated documentation. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Translated files in the workspace root plus a concise validation summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves source structure for folders, writes language-suffixed outputs, and reports format, terminology, and professional-accuracy checks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
