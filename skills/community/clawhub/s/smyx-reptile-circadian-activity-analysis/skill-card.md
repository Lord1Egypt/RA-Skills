## Description:

Analyzes reptile enclosure video to report hourly activity patterns and potential circadian disruptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Reptile keepers and husbandry teams use the skill to review enclosure video, compare activity with species-specific day/night patterns, and inspect reports and historical results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Enclosure videos or their URLs are sent to an external cloud service.

Mitigation: Use a dedicated workspace and avoid sensitive media; review the service's uploaded-media retention before use.

Risk: The skill creates or reuses a persistent local identity and stores tokens for report history.

Mitigation: Review local identity and token storage before installation and use a dedicated account.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/18072937735/skills/smyx-reptile-circadian-activity-analysis)
- [Reptile circadian analysis API documentation](references/api_doc.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Report links]

**Output Format:** [JSON or Markdown text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured activity results, alerts, and optional saved report file or historical report links.]

## Skill Version(s):

1.0.16 (source: ClawHub release; bundled frontmatter lists 1.0.17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
