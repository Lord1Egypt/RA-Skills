## Description:

Fetches web pages and generates AI-powered summaries with a local Ollama model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and other external users can use this skill to fetch public web pages, clean page text, and produce brief, detailed, or bullet-point summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The URL fetcher can retrieve arbitrary user-supplied locations, including internal, local, authenticated, or otherwise sensitive pages.

Mitigation: Use the skill only on intended public HTTP or HTTPS pages, and avoid internal services, authenticated URLs, local files, and sensitive content.

Risk: A malicious or misleading page can influence the generated summary.

Mitigation: Treat generated summaries as untrusted analysis and review important conclusions against the original page.

Risk: If local summarization fails, the script may print raw page text.

Mitigation: Avoid summarizing pages that contain secrets, personal data, or confidential material, and review output handling before use.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text summary with optional bullet list; raw page text may be printed on summarization failure.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches user-supplied URLs with a 30 second curl timeout and truncates cleaned content before summarization.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
