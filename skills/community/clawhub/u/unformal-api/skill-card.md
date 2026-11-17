## Description:

Unformal API helps agents create AI-powered conversational Pulses that collect information through shareable links and return structured responses, transcripts, exports, analytics, and aggregate insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonasboury](https://clawhub.ai/user/jonasboury)

### License/Terms of Use:

MIT-0

## Use Case:

External teams, developers, and operators use this skill to create Unformal Pulses for surveys, feedback requests, user interviews, lead qualification, intake, onboarding, and other respondent data collection workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pulse configuration, respondent answers, transcripts, exports, and webhook payloads may be sent to Unformal.

Mitigation: Use the skill only with respondent consent and an approved service and retention model; avoid regulated or highly sensitive data unless your organization has approved that use.

Risk: The skill recommends replacing its reviewed instructions from a remote URL.

Mitigation: Keep a pinned, reviewed skill version and review changes before replacing local skill files.

Risk: The skill recommends unpinned latest, npx, or global npm CLI installs.

Mitigation: Prefer a pinned and reviewed @unformal/cli version over latest, npx, or global installs.

Risk: Exports, transcripts, and webhook integrations can expose respondent data outside the chat session.

Mitigation: Limit collected fields, protect webhook endpoints, and handle exported files as sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jonasboury/skills/unformal-api)
- [Publisher profile](https://clawhub.ai/user/jonasboury)
- [Unformal website](https://unformal.ai)
- [Unformal API reference](https://unformal.ai/docs/api)
- [Unformal integration guide](https://unformal.ai/integrate)
- [Unformal llms.txt](https://unformal.ai/llms.txt)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, JSON]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include shareable Pulse links, API request bodies, response examples, CLI commands, export instructions, webhook guidance, and analytics or aggregate insight retrieval steps.]

## Skill Version(s):

1.4.0 (source: evidence release version and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
