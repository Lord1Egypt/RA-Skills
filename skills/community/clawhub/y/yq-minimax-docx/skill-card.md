## Description:

Yq Minimax Docx helps agents create, edit, format, and validate Word DOCX documents using OpenXML SDK-based CLI and C# workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianheihei002](https://clawhub.ai/user/tianheihei002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-producing agents use this skill to generate new Word documents, fill or edit existing DOCX files, and apply document templates while checking structure and business rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run installer workflows or modify shell startup files.

Mitigation: Review setup.sh before execution, avoid running it as root, prefer trusted package managers for .NET, pandoc, and LibreOffice, and inspect $HOME/.bashrc after setup.

Risk: Template handling may preserve external links in generated or edited DOCX files.

Mitigation: Use trusted templates and inspect generated documents for external links before sharing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tianheihei002/skills/yq-minimax-docx)
- [Publisher Profile](https://clawhub.ai/user/tianheihei002)
- [Scenario A: Create](artifact/references/scenario_a_create.md)
- [Scenario B: Edit Content](artifact/references/scenario_b_edit_content.md)
- [Scenario C: Apply Template](artifact/references/scenario_c_apply_template.md)
- [OpenXML Element Order](artifact/references/openxml_element_order.md)
- [XSD Validation Guide](artifact/references/xsd_validation_guide.md)
- [Typography Guide](artifact/references/typography_guide.md)
- [Design Principles](artifact/references/design_principles.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, C# code, JSON configuration examples, and generated DOCX file workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify DOCX files through local CLI and C# tooling.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
