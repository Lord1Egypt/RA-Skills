## Description:

Tabstack helps agents read, extract, transform, research, and interact with web pages and PDF documents through the Tabstack API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lmorchard](https://clawhub.ai/user/lmorchard)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Tabstack to retrieve web and PDF content, extract structured data, generate summaries or transformations, conduct cited research, and automate browser tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Processed URLs, JSON schemas, instructions, research queries, and optional form data are sent to Tabstack.

Mitigation: Use the skill only with data approved for Tabstack processing, and avoid passwords, tokens, payment data, private intranet URLs, and sensitive documents unless organizational policy permits it.

Risk: Browser automation can click, navigate, fill forms, and submit data through a remote browser.

Mitigation: Use guardrails for automation tasks, especially when a workflow could submit forms or take external actions.

Risk: The skill depends on a TABSTACK_API_KEY and npm dependencies.

Mitigation: Protect the API key as a secret and install dependencies from the provided package-lock.json when deploying the skill.

## Reference(s):

- [Tabstack examples and recipes](references/examples.md)
- [Tabstack website](https://tabstack.ai)
- [ClawHub skill page](https://clawhub.ai/lmorchard/skills/tabstack)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON, and plain text returned through shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TABSTACK_API_KEY; web, PDF, research, and browser automation requests are handled by Tabstack.]

## Skill Version(s):

0.3.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
