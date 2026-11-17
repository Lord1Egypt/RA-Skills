## Description:

Coordinates Syft CLI based news workflows for personalized daily news digests, profile artifacts, storyline trees, storyline backfills, and durable editorial preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solatrader](https://clawhub.ai/user/solatrader)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run Syft CLI centered news workflows that turn followed topics and search results into reusable profiles, personalized daily briefings, storyline timelines, backfills, and durable editorial guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks users to install a global Syft CLI without pinning a verified package version.

Mitigation: Use a pinned and verified Syft CLI version where possible, and review where syft login stores credentials before running authenticated workflows.

Risk: The workflow can create persistent profile artifacts with inferred interests and demographic guesses from following data.

Mitigation: Generate profile summaries only with user consent, review or edit inferred profiles before reuse, and delete profiles or rulebooks that contain wrong, sensitive, or unwanted inferences.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/solatrader/skills/syft-news)
- [Bundle README](README.md)
- [Workflow Map](subskills/syft-news-pipeline/references/workflow-map.md)
- [Profile Summary Route](subskills/syft-news-pipeline/references/profile-summary.md)
- [Daily Briefing Route](subskills/syft-news-pipeline/references/daily-briefing.md)
- [Storyline Tree Route](subskills/syft-news-pipeline/references/storyline-tree.md)
- [Storyline Backfill Route](subskills/syft-news-pipeline/references/storyline-backfill.md)
- [Guidance Rulebook Route](subskills/syft-news-pipeline/references/guidance-rulebook.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, optional HTML and JSON artifacts, and inline Syft CLI shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final user-facing deliverables default to Simplified Chinese unless the user asks otherwise.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
