## Description:

MiniMax DOCX helps agents create, edit, and format Word DOCX documents using OpenXML SDK (.NET) workflows for new documents, content edits, template application, and validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhlorra](https://clawhub.ai/user/yhlorra)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document automation users use this skill to produce, modify, reformat, and validate formal DOCX documents such as reports, proposals, contracts, forms, academic papers, and CJK official documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can install packages, use sudo, fetch a remote .NET installer, modify shell startup files, and restore NuGet packages.

Mitigation: Review setup.sh before execution, provision .NET and optional tools through trusted channels when possible, and use the minimal setup path when optional dependencies are unnecessary.

Risk: Untrusted DOCX templates or documents can carry external links, relationships, or formatting that affect generated outputs.

Mitigation: Review or strip external relationships from untrusted documents and run the skill's preview, diff, and validation checks before using the output.

## Reference(s):

- [MiniMax DOCX Skill Page](https://clawhub.ai/yhlorra/skills/yh-minimax-docx)
- [Scenario A: Create Documents](artifact/references/scenario_a_create.md)
- [Scenario B: Edit Content](artifact/references/scenario_b_edit_content.md)
- [Scenario C: Apply Template](artifact/references/scenario_c_apply_template.md)
- [OpenXML Element Order](artifact/references/openxml_element_order.md)
- [XSD Validation Guide](artifact/references/xsd_validation_guide.md)
- [Typography Guide](artifact/references/typography_guide.md)
- [CJK Typography](artifact/references/cjk_typography.md)
- [Design Principles](artifact/references/design_principles.md)
- [Troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with C# and shell command examples, plus generated or modified DOCX files when the agent executes the bundled tools.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires environment setup and validation steps before delivering generated DOCX outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
