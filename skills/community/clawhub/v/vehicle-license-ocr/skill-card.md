## Description:

Extracts structured OCR data from vehicle license main and secondary pages, including plate number, owner, vehicle model, VIN, engine number, archive number, passenger capacity, mass, and inspection records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to send vehicle license images or PDFs to the Scnet OCR API and receive structured JSON recognition results for the main or secondary page of a vehicle license.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vehicle license files may contain sensitive personal and vehicle information and are uploaded to a remote OCR API.

Mitigation: Use the skill only with files the user is authorized to process and disclose that the document image is sent to Scnet before invocation.

Risk: The upload endpoint can be changed through SCNET_API_BASE.

Mitigation: Keep SCNET_API_BASE unset or set only to the trusted HTTPS Scnet API endpoint.

Risk: The skill requires a Scnet API key.

Mitigation: Store SCNET_API_KEY in a protected local environment or config file and do not paste it into chat.

## Reference(s):

- [Sugon-Scnet OCR API documentation summary](references/api-docs.md)
- [Vehicle license OCR field summary](assets/templates/fields-summary.md)
- [Scnet website](https://www.scnet.cn)
- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/vehicle-license-ocr)

## Skill Output:

**Output Type(s):** [JSON, API Calls, Shell commands, Guidance]

**Output Format:** [Structured JSON recognition results with error messages emitted as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCNET_API_KEY and accepts an OCR type plus a local file path.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.yaml, changelog, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
