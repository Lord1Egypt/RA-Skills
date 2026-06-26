## Description: <br>
Creates, edits, formats, and validates DOCX files using OpenXML SDK (.NET) through guided pipelines for new documents, content edits, and template application. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yhlorra](https://clawhub.ai/user/yhlorra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document automation agents use this skill to create Word documents, update existing DOCX content, apply templates, and validate OpenXML structure before delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup can install or configure .NET, NuGet packages, pandoc, LibreOffice, zip tooling, and shell path settings. <br>
Mitigation: Review setup.sh before running it, prefer the minimal setup path, and use an isolated environment when possible. <br>
Risk: The skill may be invoked broadly for formal document tasks even when the user did not explicitly request DOCX automation. <br>
Mitigation: Confirm that DOCX output or DOCX editing is intended before running setup or document-modification commands. <br>
Risk: Working with untrusted templates or source documents can preserve external document links or unwanted embedded content. <br>
Mitigation: Use trusted templates, inspect document links and embedded content before distribution, and run the documented preview and validation steps. <br>


## Reference(s): <br>
- [Scenario A: Create](artifact/references/scenario_a_create.md) <br>
- [Scenario B: Edit Content](artifact/references/scenario_b_edit_content.md) <br>
- [Scenario C: Apply Template](artifact/references/scenario_c_apply_template.md) <br>
- [OpenXML Element Order](artifact/references/openxml_element_order.md) <br>
- [XSD Validation Guide](artifact/references/xsd_validation_guide.md) <br>
- [Troubleshooting](artifact/references/troubleshooting.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/yhlorra/yh-minimax-docx) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, markdown] <br>
**Output Format:** [Markdown guidance with shell commands, C# code patterns, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation or modification of DOCX files through local .NET and OpenXML tooling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
