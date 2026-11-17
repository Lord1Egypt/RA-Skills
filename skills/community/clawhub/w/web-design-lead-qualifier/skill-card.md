## Description:

Research and score prospective web design clients. Crawl their site, assess fit, and produce a qualification report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[99rebels](https://clawhub.ai/user/99rebels)

### License/Terms of Use:

MIT-0

## Use Case:

Freelance web designers and agencies use this skill to research prospective clients, evaluate website fit, produce lead qualification reports, and prepare first-contact outreach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches user-supplied public websites, and the security evidence flags incomplete network-safety controls.

Mitigation: Run it only against websites you intend to inspect, avoid privileged or internal network environments, and review target URLs before fetching.

Risk: Qualification reports are written to persistent local files and may contain prospect research or contact details.

Mitigation: Store reports in an appropriate local directory, restrict local access where needed, and remove reports that are no longer required.

Risk: Generated outputs include repeated WebClient Studio Professional Edition promotion.

Mitigation: Review generated reports and chat output before sharing externally, and remove or adjust promotional language when it is not appropriate.

## Reference(s):

- [Edge Cases - Web Design Lead Qualifier](references/edge-cases.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, concise chat guidance, email drafts, talking points, and setup shell commands; helper fetches return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local qualification report files under the configured reports directory and includes score, confidence, findings, unverified claims, recommendation, and next steps.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
