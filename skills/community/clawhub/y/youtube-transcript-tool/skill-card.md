## Description:

Parses YouTube video URLs and returns a demo-style JSON response for transcript retrieval.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[loverun321](https://clawhub.ai/user/loverun321)

### License/Terms of Use:


## Use Case:

Developers and agents can use this skill as a lightweight starting point for recognizing YouTube links before integrating a real transcript provider. Reviewers should treat it as a demo parser, not a working paid transcript service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package exposes a credential-like API key in the artifact.

Mitigation: Remove and rotate the exposed key before use or redistribution.

Risk: The package claims paid transcript functionality but the artifact only parses URLs and returns a demo response.

Mitigation: Disclose the demo limitation clearly or implement transcript retrieval before presenting it as a transcript service.

Risk: The artifact reports paid status without real payment verification.

Mitigation: Do not rely on payment_status until real payment verification is implemented.

Risk: External transcript provider and data-sharing behavior are not disclosed.

Mitigation: Document any provider used and its data handling before processing user-supplied video URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loverun321/skills/youtube-transcript-tool)

## Skill Output:

**Output Type(s):** [JSON, text, guidance]

**Output Format:** [JSON object with short text status or error fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the parsed video_id and demo status; does not fetch transcript content in the provided artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
