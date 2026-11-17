## Description:

Extracts existing rebar quantity tables from DWG/DXF structural drawings and checks their arithmetic, reporting discrepancies with drawing references rather than declaring design errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongsheng123132](https://clawhub.ai/user/dongsheng123132)

### License/Terms of Use:

MIT-0

## Use Case:

Structural engineers and quantity surveyors use this skill to review existing rebar quantity tables in tunnel and underground-structure DWG/DXF drawings, export the recovered rows, and investigate arithmetic discrepancies against the original drawing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Drawing text in generated XLSX cells may be interpreted as spreadsheet formulas.

Mitigation: Treat XLSX output from third-party drawings as untrusted; prefer the JSON evidence or Markdown report, or open spreadsheets with formulas and external links disabled until formula-like strings are escaped.

Risk: A configured DWG converter executable may be untrusted.

Mitigation: Point ODA_FILE_CONVERTER and LIBREDWG_DWG2DXF only to trusted converter binaries.

Risk: Unparsed tables or unfamiliar symbol mappings can leave quantities unchecked.

Mitigation: Review reported evidence gaps and symbol mappings, then confirm questionable values against the original drawing before relying on results.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dongsheng123132/skills/rebar-table-audit)
- [Project homepage (listed in skill metadata; not verified import provenance)](https://github.com/dongsheng123132/rebar-table-audit)
- [Rebar symbol mapping reference](references/symbols.md)

## Skill Output:

**Output Type(s):** [JSON, Spreadsheet, Markdown]

**Output Format:** [JSON evidence, XLSX workbook, and Markdown audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cell values and findings include drawing entity handles; unresolved parsing gaps are reported rather than treated as successful checks.]

## Skill Version(s):

0.1.0 (source: ClawHub release, skill frontmatter, CHANGELOG, pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
