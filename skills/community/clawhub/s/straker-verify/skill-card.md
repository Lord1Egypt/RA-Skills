## Description:

Straker Verify helps agents create translation projects, improve existing translations with AI quality boost, and request optional human review through Straker's Verify API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indy-at-straker](https://clawhub.ai/user/indy-at-straker)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to translate text or files, improve existing translations, request human verification, and track translation project status through Straker Verify.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected translation content and files may be uploaded to Straker's external service.

Mitigation: Review Straker's data handling terms before use and avoid submitting secrets, regulated data, or confidential business material unless approved.

Risk: Human verification workflows may expose submitted content for review.

Mitigation: Use human verification only for content that is approved for potential human review.

Risk: The skill relies on a Straker API key for authenticated requests.

Mitigation: Provide the key through STRAKER_VERIFY_API_KEY and do not include the token in prompts, files, or command output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/indy-at-straker/skills/straker-verify)
- [Straker.ai](https://straker.ai)
- [Straker Verify API documentation](https://api-verify.straker.ai/docs)

## Skill Output:

**Output Type(s):** [Text, Files, API Calls, Shell commands, Guidance]

**Output Format:** [Markdown with API request examples and JSON response descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STRAKER_VERIFY_API_KEY and may send selected content or files to Straker's external service for translation, quality boost, or human verification.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
