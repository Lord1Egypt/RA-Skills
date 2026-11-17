## Description:

Open a TuneViva catalogue score for practice or retrieve its MusicXML. Use when a user supplies a TuneViva score link or asks to practise a selected catalogue score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omercelik](https://clawhub.ai/user/omercelik)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to find a TuneViva score, open a browser-based practice session, and retrieve its compressed MusicXML notation when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment has incomplete coverage because a referenced local path could not be matched to a bundled artifact.

Mitigation: Review whether the missing local reference is expected before installing; the scan guidance notes that benign findings do not eliminate risk.

## Reference(s):

- [TuneViva API documentation](https://tuneviva.com/docs/api)
- [TuneViva OpenAPI specification](https://tuneviva.com/docs/api/openapi.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Links, Files]

**Output Format:** [Markdown guidance and links; optionally a compressed MusicXML (.mxl) file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides a practice link when the selected score supports practice; MusicXML is supplied only when requested.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
