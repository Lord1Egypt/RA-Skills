## Description: <br>
Professional DOCX document creation, editing, and formatting using OpenXML SDK (.NET), with workflows for creating new documents, editing existing documents, and applying template formatting with validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianheihei002](https://clawhub.ai/user/tianheihei002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, document automation users, and agents use this skill to create, edit, reformat, and validate Word DOCX files through OpenXML-based CLI commands or C# scripts. It is intended for report, proposal, contract, form-fill, template-application, and other printable document workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be invoked for broad writing requests even when the user did not explicitly ask for a DOCX workflow. <br>
Mitigation: Use it only when the requested output is a Word/DOCX document or the user asks for DOCX transformation, formatting, or validation. <br>
Risk: Initial setup can install .NET or optional document tools, change shell PATH configuration, and trigger NuGet restores. <br>
Mitigation: Review setup steps before running them and execute setup only in an environment where those installation and network actions are acceptable. <br>
Risk: DOCX templates from other people may preserve external relationships or document metadata. <br>
Mitigation: Treat third-party templates as untrusted inputs and inspect generated DOCX files, relationships, and metadata before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tianheihei002/yq-minimax-docx) <br>
- [Scenario A: Create](references/scenario_a_create.md) <br>
- [Scenario B: Edit Content](references/scenario_b_edit_content.md) <br>
- [Scenario C: Apply Template](references/scenario_c_apply_template.md) <br>
- [OpenXML Element Order](references/openxml_element_order.md) <br>
- [OpenXML Units](references/openxml_units.md) <br>
- [Typography Guide](references/typography_guide.md) <br>
- [CJK Typography](references/cjk_typography.md) <br>
- [Track Changes Guide](references/track_changes_guide.md) <br>
- [XSD Validation Guide](references/xsd_validation_guide.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON examples, C# code snippets, and DOCX file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify DOCX files and should run document validation before delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
