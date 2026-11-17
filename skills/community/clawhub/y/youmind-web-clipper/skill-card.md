## Description:

Save any URL to a YouMind board from an agent workflow using the YouMind CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dophinl](https://clawhub.ai/user/dophinl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to save webpages, articles, videos, and documents into a YouMind board from an agent or terminal workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided URLs are sent to and stored in YouMind.

Mitigation: Use the skill only for URLs intended for YouMind storage and avoid private, signed, or sensitive links.

Risk: The workflow installs the YouMind CLI globally without a pinned package version.

Mitigation: Review or pin the CLI package before global installation in managed environments.

Risk: The skill asks for YouMind account access through YOUMIND_API_KEY.

Mitigation: Configure the API key outside chat and do not paste secrets into agent conversations.

Risk: Broad trigger phrases may invoke the skill for generic save or bookmark requests.

Mitigation: Use explicit YouMind-scoped commands when invoking the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dophinl/skills/youmind-web-clipper)
- [YouMind CLI package](https://www.npmjs.com/package/@youmind-ai/cli)
- [Setup](references/setup.md)
- [Error Handling](references/error-handling.md)
- [YouMind issue tracker](https://github.com/YouMindInc/youmind/issues)
- [Publisher profile](https://clawhub.ai/user/dophinl)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands and YouMind links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the YouMind CLI and YOUMIND_API_KEY; sends user-provided URLs to YouMind for storage.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
