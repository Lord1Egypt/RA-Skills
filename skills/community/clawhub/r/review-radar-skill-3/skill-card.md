## Description:

Extracts structured monitor review intelligence from Bilibili or YouTube review video links, including tested data, pros and cons, reviewer conclusions, and competitor mentions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ford828](https://clawhub.ai/user/ford828)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, and research analysts use this skill to turn monitor review videos or fallback transcript text into structured review cards and cross-review comparison inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports that one helper script can run unintended local code from crafted inputs.

Mitigation: Review, fix, or avoid scripts/submit_text.sh before installation, and avoid untrusted file names or titles.

Risk: The skill sends video URLs, transcripts, and report requests to a separate Review Radar service.

Mitigation: Keep RR_BASE_URL pointed at a trusted local endpoint and review that service's data handling before submitting private transcripts or URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ford828/skills/review-radar-skill-3)
- [Publisher profile](https://clawhub.ai/user/ford828)

## Skill Output:

**Output Type(s):** [markdown, shell commands, code, guidance]

**Output Format:** [Markdown reports, JSON status or report data, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include source references, timestamps, validation status, source type, pros and cons, conclusions, and competitor mentions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
