## Description:

Remove metadata from one or multiple PDFs by uploading them to the Solutions API, polling until completion, then returning download URL(s) for the cleaned PDF(s) or a ZIP if multiple files are processed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crossservicesolutions](https://clawhub.ai/user/crossservicesolutions)

### License/Terms of Use:

MIT

## Use Case:

Developers and document-processing agents use this skill to remove metadata from one or more PDF files through the Cross-Service-Solutions API and return cleaned file download links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF contents are uploaded to a remote service for processing.

Mitigation: Use the skill only for PDFs that are acceptable to share with Cross-Service-Solutions under the provider's retention and access policies.

Risk: The base URL override can redirect PDFs and the API key away from the documented HTTPS endpoint.

Mitigation: Remove or tightly control base URL override support and verify the destination host before execution.

Risk: Passing an API key on the command line can expose it through shell history or process inspection.

Mitigation: Prefer the SOLUTIONS_API_KEY environment variable or a managed secret store, and avoid echoing or logging credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crossservicesolutions/skills/remove-metadata-from-pdf)
- [Cross-Service-Solutions registration](https://login.cross-service-solutions.com/register)
- [Solutions API base endpoint](https://api.xss-cross-service-solutions.com/solutions/solutions)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [JSON result with job status, output file names, download URL or URLs, and input file names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a single cleaned PDF URL, multiple cleaned PDF URLs, or a ZIP download URL for batch processing.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
