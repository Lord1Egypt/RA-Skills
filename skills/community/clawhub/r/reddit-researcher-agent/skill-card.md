## Description:

Scans Reddit for posts matching keywords, summarizes findings, and extracts themes and pain points from Reddit discussions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kryzl19](https://clawhub.ai/user/kryzl19)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and product teams use this skill to collect Reddit posts for supplied keywords, inspect community feedback, and export concise markdown research summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outbound requests to search engines and Reddit can expose search terms and depend on third-party service availability.

Mitigation: Review keywords before use, run only in environments approved for external network access, and select the documented search mode that fits the deployment.

Risk: Cached Reddit content and exported reports can persist fetched discussion data and user-provided keywords on local storage.

Mitigation: Store outputs in an approved workspace, review generated markdown before sharing, and clear local cache or exports when retention is not needed.

Risk: Generated summaries are extraction-oriented and may miss context or reflect imprecise search results.

Mitigation: Validate important conclusions against the linked Reddit posts and treat the output as research input rather than a final analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kryzl19/skills/reddit-researcher-agent)
- [Publisher profile](https://clawhub.ai/user/kryzl19)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown reports and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write cached Reddit content and exported markdown reports locally.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
