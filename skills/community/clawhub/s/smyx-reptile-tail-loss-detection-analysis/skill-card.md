## Description:

Analyzes gecko and lizard tail images or videos for apparent tail shortening, wounds, and scabs, and returns a structured analysis report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Reptile keepers and enclosure operators use this skill to review gecko and lizard tail images or videos for apparent tail loss and receive structured event records and alerts. Results are visual estimates; the skill documentation says injury assessment should be confirmed by a reptile veterinarian.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious, citing reported mismatches between its monitoring purpose and account-management behavior, undisclosed media uploads, and analysis that still runs in export-only mode.

Mitigation: Before considering use, obtain clear explanations of account and credential handling, the external media destination and data practices, and export-only behavior. ClawScan marks coverage partial because a referenced local path was missing.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/18072937735/skills/smyx-reptile-tail-loss-detection-analysis)
- [Tail loss API reference](artifact/references/api_doc.md)
- [Analysis API reference](artifact/skills/smyx_analysis/references/api_doc.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Structured analysis report in JSON or text, with Markdown history listings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tail measurements, visual findings, alert level, suggested actions, and report links.]

## Skill Version(s):

1.0.18 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
