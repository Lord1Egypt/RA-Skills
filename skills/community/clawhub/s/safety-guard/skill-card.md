## Description:

Uses the safety-guard CLI to scan URLs, local files, and YouTube links with configurable AI providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[john-niu-07](https://clawhub.ai/user/john-niu-07)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to invoke the safety-guard CLI from an agent for scanning URLs, local documents, media files, and YouTube links with configurable model providers and optional structured output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Use may send selected URLs, files, and YouTube content to configured AI providers or optional extraction services.

Mitigation: Avoid private, regulated, or confidential material unless the selected providers, services, and tokens are approved for that data.

Risk: Installation depends on a third-party Homebrew tap for the safety-guard binary.

Mitigation: Install only when the safety-guard Homebrew tap and publisher are trusted.

## Reference(s):

- [Safety Guard homepage](https://safety-guard.sh)
- [OpenClaw Safety Guard on ClawHub](https://clawhub.ai/john-niu-07/skills/safety-guard)
- [john-niu-07 publisher profile](https://clawhub.ai/user/john-niu-07)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with bash and JSON examples; CLI output may be plain text or JSON when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports configurable output length, token limits, extraction-only mode, and optional fallback extraction services.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
