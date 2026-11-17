## Description:

VAP Media API skill for image, video, music, and media editing through VAP. Uses VAP product keys with current Media API endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elestirelbilinc-sketch](https://clawhub.ai/user/elestirelbilinc-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to generate images, videos, and music, or to edit existing media through VAP Media API. It helps agents improve prompts, call the matching media endpoint, poll for completion, and return the final media URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and media URLs are sent to VAP as an external media provider.

Mitigation: Use only prompts and asset URLs that are approved for sharing with VAP, and avoid private, internal-network, or sensitive media URLs.

Risk: The skill requires VAP_API_KEY for authenticated API calls.

Mitigation: Store VAP_API_KEY as an environment secret and avoid exposing it in logs, generated commands, or chat output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elestirelbilinc-sketch/skills/vap-media)
- [VAP Developer Hub](https://vapagent.com/developer/)
- [VAP Media API key page](https://vapagent.com/developer/?key=media#keys)
- [VAP Room and Media plans](https://vapagent.com/new-dashboard/?billing=monthly#plans)
- [VAP AI](https://vapagent.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown status text with inline shell commands, JSON request examples, and final media URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns generated or edited media URLs after polling VAP Media API tasks or operations.]

## Skill Version(s):

1.0.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
