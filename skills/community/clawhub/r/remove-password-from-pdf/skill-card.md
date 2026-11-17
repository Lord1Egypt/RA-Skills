## Description:

Remove password protection from a PDF by uploading it, with its current password, to the Solutions API, polling until completion, then returning a download URL for the unlocked PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crossservicesolutions](https://clawhub.ai/user/crossservicesolutions)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to remove password protection from PDFs they are authorized to unlock. The skill submits the PDF and current password to the Solutions API, then returns job status and a download URL for the unlocked file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Protected PDFs and their current passwords are uploaded to a remote third-party service.

Mitigation: Use the skill only for PDFs you are allowed to upload, and avoid confidential documents unless the provider's retention and security terms are acceptable.

Risk: The Solutions API key is a bearer credential that could be exposed through unsafe handling.

Mitigation: Keep the API key in a protected environment variable or secret store, never echo or log it, and rotate it if exposure is suspected.

Risk: The base URL can be overridden, which could redirect documents, passwords, and credentials away from the intended service.

Mitigation: Use the default endpoint or restrict --base-url to a trusted HTTPS endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/crossservicesolutions/skills/remove-password-from-pdf)
- [Solutions API registration](https://login.cross-service-solutions.com/register)
- [Solutions API remove-password endpoint](https://api.xss-cross-service-solutions.com/solutions/solutions/api/33)

## Skill Output:

**Output Type(s):** [Text, Shell commands, API calls]

**Output Format:** [JSON containing job_id, status, download_url, file_name, and error details when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The output may include API error, polling timeout, missing credential, or invalid input details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
