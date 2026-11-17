## Description:

Generates personalized Vedic horoscopes and birth charts based on birth data and astrological calculations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, astrology practitioners, wellness platforms, and applications use this skill to generate Vedic horoscope PDFs, birth charts, and city lookup or service status results from birth data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the subject's full name, phone number, parents' names, gender, exact birth time, and birthplace to the external mkkpro.com service.

Mitigation: Use only with informed user consent, minimize nonessential identifiers where possible, and confirm the provider's privacy, retention, and deletion practices before production use.

Risk: Generated PDF links may expose sensitive horoscope and identity data if retained or shared without access controls.

Mitigation: Treat returned pdf_url values as sensitive, limit distribution, and verify download access controls and retention policies with the provider.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-vedic-horoscope)
- [API Docs](https://api.mkkpro.com:8159/docs)
- [Kong Route](https://api.mkkpro.com/lifestyle/vedic-horoscope)
- [OpenAPI Specification](artifact/openapi.json)

## Skill Output:

**Output Type(s):** [Text, Files, Guidance]

**Output Format:** [JSON API responses and downloadable PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Horoscope generation returns success status, message, pdf_url, and generated_at when available.]

## Skill Version(s):

1.0.0 (source: release evidence and OpenAPI info.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
