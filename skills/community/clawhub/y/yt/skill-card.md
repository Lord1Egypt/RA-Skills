## Description:

Provides quick YouTube lookups through TranscriptAPI for transcripts, search, channel latest uploads, and handle resolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[therohitdas](https://clawhub.ai/user/therohitdas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external agents use this skill when a task involves YouTube links, video IDs, @handles, transcripts, recent channel activity, or topic search. It helps the agent make authenticated TranscriptAPI requests and interpret common response and error conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow may ask the agent to handle third-party account signup, email OTP verification, and API-key storage.

Mitigation: Prefer creating the TranscriptAPI account yourself, provide the key through a scoped secret manager, and avoid broad shell-profile or global environment persistence unless access controls are understood.

Risk: The skill depends on TranscriptAPI as a third-party backend and requires an API key for requests.

Mitigation: Install only if the TranscriptAPI service and its account model are acceptable for the intended environment; scope, rotate, and revoke the API key according to local secret-management policy.

Risk: Requests without an identifying User-Agent may be blocked by the service.

Mitigation: Include both the Authorization bearer token and a clear User-Agent header on every TranscriptAPI request.

## Reference(s):

- [TranscriptAPI homepage](https://transcriptapi.com)
- [TranscriptAPI OpenAPI specification](https://transcriptapi.com/openapi.json)
- [ClawHub skill page](https://clawhub.ai/therohitdas/skills/yt)
- [Publisher profile](https://clawhub.ai/user/therohitdas)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl examples and API response handling notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TRANSCRIPT_API_KEY and internet access to transcriptapi.com; some API calls consume TranscriptAPI credits.]

## Skill Version(s):

1.5.2 (source: server release metadata; artifact frontmatter reports 1.5.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
