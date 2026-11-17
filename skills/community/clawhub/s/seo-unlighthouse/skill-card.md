## Description:

Multi-page Lighthouse audit via the MIT-licensed Unlighthouse CLI that runs locally as a free-tier alternative to auditing every site URL through PageSpeed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site owners use this skill to run local, multi-page Lighthouse audits for SEO and web performance checks without relying on PageSpeed API quota. It supports route caps, mobile or desktop audits, custom output directories, and CI-style regression checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can crawl a target site, consume local compute, and write audit reports.

Mitigation: Confirm the target URL, route cap, device mode, and output directory before running audits, especially in CI or persistent report locations.

Risk: The workflow depends on the expected Unlighthouse wrapper and installer being available from the intended project source.

Mitigation: Confirm the referenced wrapper and installer source before installing or pre-warming dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asale-ai/skills/seo-unlighthouse)

## Skill Output:

**Output Type(s):** [shell commands, configuration, analysis, json, markdown]

**Output Format:** [Markdown guidance with command examples and parsed Lighthouse audit results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce JSON and HTML audit reports in a temporary or user-selected output directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
