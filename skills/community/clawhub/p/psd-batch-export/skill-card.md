## Description:

PSD Batch Export helps agents analyze Photoshop PSD text layers, map Excel or CSV rows to editable fields, preview changes, export editable PSD and PNG batches, and verify results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luis1213899](https://clawhub.ai/user/luis1213899)

### License/Terms of Use:

MIT

## Use Case:

Design automation users, developers, and content operations teams use this skill to batch-generate PSD and PNG design assets from PSD templates and spreadsheet data while preserving editable text layers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional AI and network helpers can expose API keys or design prompt data.

Mitigation: Use LLM features only with explicit provider selection, trusted endpoints, nonsensitive design content, and limited-scope API keys; run offline for sensitive projects.

Risk: Legacy paths can write outside the chosen output folders.

Mitigation: Use fresh output directories, inspect preview and verification reports before production export, and avoid untrusted spreadsheet or JSON inputs.

Risk: The skill performs local PSD and image processing and can optionally download fonts.

Mitigation: Install dependencies and fonts from trusted sources, run diagnostics before production use, and review generated files before distribution.

## Reference(s):

- [PSD Batch Export ClawHub page](https://clawhub.ai/luis1213899/skills/psd-batch-export)
- [Template catalog](references/templates.json)
- [Runtime compatibility](references/runtime-compat.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON report references.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides local CLI workflows that create PSD, PNG, and JSON report files under user-selected output directories.]

## Skill Version(s):

4.4.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
