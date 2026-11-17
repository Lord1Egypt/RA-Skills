## Description:

Fix garbled text in PDF/SVG vector graphics for final editing in AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ec-cyber258](https://clawhub.ai/user/ec-cyber258)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-editing teams use this skill to analyze PDF/SVG vector files for garbled text, export editable JSON maps, and plan manual repairs while preserving layout context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release overclaims repaired PDF/SVG output; security evidence says to expect analysis results and JSON export only.

Mitigation: Use the skill for inspection and editable JSON export workflows, and manually verify any document changes before replacing source files.

Risk: Dependencies are ambiguous and unpinned.

Mitigation: Install in an isolated environment with a corrected, pinned dependency manifest using the intended packages such as PyMuPDF and beautifulsoup4.

Risk: The script reads local PDF/SVG inputs and writes output files in the workspace.

Mitigation: Run it in a sandboxed workspace with non-sensitive copies, then review generated files before broader use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ec-cyber258/skills/vector-text-fixer)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Code, Guidance]

**Output Format:** [Markdown guidance with CLI/Python examples and JSON export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local PDF/SVG inputs are analyzed and optional editable JSON exports can be written to the workspace.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
