## Description:

Syléa is a French-first personal life coach and decision assistant that analyzes dilemmas with probability-based option scoring, tracks life goals across five psychological dimensions, runs well-being check-ins, and stores data locally in ~/.sylea/.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clotilde563](https://clawhub.ai/user/clotilde563)

### License/Terms of Use:

MIT-0

## Use Case:

External users use Syléa for structured personal coaching, including onboarding, dilemma analysis, life-goal probability estimates, and daily well-being check-ins. It is French-first and keeps coaching records in local Markdown files under ~/.sylea/.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create a long-term local coaching journal containing identity details, goals, dilemmas, routines, and well-being scores in plaintext Markdown files.

Mitigation: Use restrictive file and directory permissions for ~/.sylea/, avoid highly sensitive disclosures, and periodically review or delete stored files that are no longer needed.

Risk: Broad coaching triggers and limited privacy controls may lead users to record more personal information than intended.

Mitigation: Confirm what will be saved before using persistent protocols and keep ~/.sylea/ local rather than sharing it externally.

## Reference(s):

- [Syléa ClawHub Skill Page](https://clawhub.ai/clotilde563/skills/sylea)
- [clotilde563 ClawHub Publisher Profile](https://clawhub.ai/user/clotilde563)
- [Syléa Homepage](https://sylea-ai.com)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown, Shell commands, Files]

**Output Format:** [Markdown with tables, concise coaching guidance, inline shell commands, and local Markdown records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [French by default; English-aware; may save profile, dilemma, goal, and check-in files under ~/.sylea/.]

## Skill Version(s):

0.1.0 (source: release metadata and CHANGELOG.md, released 2026-04-20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
