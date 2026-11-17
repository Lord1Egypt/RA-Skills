## Description:

Create HTML slideshows from Markdown with live preview. Use when drafting slides, editing decks, optimizing layouts, scheduling talks, repurposing content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content creators, and presentation authors use this skill to draft, refine, outline, schedule, search, and export slide-related text from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The inspected artifacts are advertised as a Markdown slideshow generator, but the main script primarily stores, searches, and exports user-entered presentation text.

Mitigation: Verify installed behavior before relying on the skill for slideshow generation or live preview workflows.

Risk: Slide drafts and related text are retained as searchable local plaintext records.

Mitigation: Avoid confidential presentation material unless local plaintext retention is acceptable, and use a dedicated data directory when isolation is needed.

Risk: Exported JSON and CSV are produced from raw log values and should not be assumed safe for downstream tools.

Mitigation: Inspect or sanitize exported files before importing them into other applications or automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/slideshow-generator)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands]

**Output Format:** [Plain text command output with local log files and optional JSON, CSV, or TXT exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores timestamped entries as local plaintext under ~/.local/share/slideshow-generator/ by default; SLIDESHOW_GENERATOR_DIR can override the directory.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
