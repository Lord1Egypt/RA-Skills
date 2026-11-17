## Description:

Xhs Rental Ocr helps agents extract structured rental, housing price, and tabular data from Xiaohongshu or social media images using Apple Vision OCR, optional long-image slicing, and Excel or CSV export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangkai258](https://clawhub.ai/user/yangkai258)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to run local OCR workflows that convert real estate or tabular image content into structured spreadsheet data. It is intended for macOS environments with Python and Apple Vision bindings installed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spreadsheet exports may include attacker-controlled image filenames that can trigger formula interpretation in spreadsheet software.

Mitigation: Use a virtual environment, review files before opening exports, and rename untrusted input files so they do not start with formula-triggering characters such as =, +, -, @, or tabs.

Risk: OCR and regular-expression extraction can produce incorrect, incomplete, or mismatched rental records.

Mitigation: Manually review extracted rows before making pricing, rental, or operational decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangkai258/skills/xhs-rental-ocr)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and generated Excel or CSV files from the skill scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on image quality, OCR confidence, selected languages, slicing options, and macOS Apple Vision availability.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
