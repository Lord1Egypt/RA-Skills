## Description:

Turkiye AFAD deprem verisini kullanarak zaman, buyukluk ve bolge filtreli deprem ozeti uretir.

This skill is ready for commercial/non-commercial use.

## Publisher:

[barancaki](https://clawhub.ai/user/barancaki)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to retrieve recent AFAD earthquake data for Turkiye and summarize it by time range, minimum magnitude, and region.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The network-enabled helper script can be pointed at arbitrary URLs through a custom source URL.

Mitigation: Use the default AFAD endpoint or constrain egress to deprem.afad.gov.tr; avoid wrappers that pass custom source URLs from prompts.

Risk: Live AFAD endpoint behavior or availability can affect returned earthquake summaries.

Mitigation: Surface AFAD access errors to the user and retry later rather than treating missing data as authoritative.

## Reference(s):

- [AFAD Source Notes](references/afad_source.md)
- [Project homepage](https://github.com/barancaki/turkey_earthquake_skill)
- [AFAD earthquake portal](https://deprem.afad.gov.tr/)
- [AFAD event service](https://deprem.afad.gov.tr/event-service)
- [AFAD event filter endpoint](https://deprem.afad.gov.tr/apiv2/event/filter)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summary with a short table; helper script output is JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Turkish user-facing summaries; network access is required for live AFAD data.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
