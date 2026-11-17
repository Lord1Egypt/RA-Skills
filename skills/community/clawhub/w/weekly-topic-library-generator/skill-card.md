## Description:

Generates a weekly library of AI short-video topic ideas by collecting public trend signals, extracting non-copyright structures, creating prompt packs, and grading topics for editorial use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fsn021920-prog](https://clawhub.ai/user/fsn021920-prog)

### License/Terms of Use:

CC BY-SA 4.0

## Use Case:

External AI video creators use this skill to turn public short-video trend signals into compliant weekly topic briefs and reusable text-to-video prompt packs. It supports editorial planning while avoiding protected IP, real-person likenesses, copied captions, and performance guarantees.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses web search and public trend signals, which can include copyrighted IP, likenesses, brands, copied captions, or platform-sensitive content.

Mitigation: Review each generated topic and prompt for copyright, likeness, brand, and AI-label compliance before publishing.

Risk: The skill grades topics for replicability, spread-odds, and compliance, but those grades are not performance forecasts.

Mitigation: Treat grades as editorial filters and do not present them as guaranteed views or viral performance.

Risk: The skill writes local weekly Markdown and JSON output files in the working directory.

Mitigation: Run it in an appropriate workspace and inspect the generated files before sharing or importing them elsewhere.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/fsn021920-prog/skills/weekly-topic-library-generator)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown and JSON files containing topic teardowns, prompt packs, grades, risk flags, and suggested generators.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local weekly-topic-library Markdown and JSON outputs after web research; generated topics require review for copyright, likeness, brand, and platform AI-label compliance.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
