## Description:

Combine web and academic search into one smart AISA search mode for balanced research across public web coverage and academic depth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and external users use this skill to run a balanced research pass that combines public web coverage with academic retrieval for one query.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search prompts, selected URLs, and generated result bundles may be sent to AISA-hosted endpoints.

Mitigation: Use the skill only with queries and URLs appropriate for external processing, and review the provider's data handling terms before deployment.

Risk: Extract and sonar modes can process user-provided URLs or prompts through external services.

Mitigation: Avoid private, signed, internal, or sensitive URLs and restrict enabled modes to the release's intended research workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/smart-search-aisa)
- [AISA API service](https://api.aisa.one/apis/v1)
- [AISA API key signup](https://aisa.one)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text or Markdown search summaries with URLs, citations, and command-line status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; search prompts, selected URLs, and result bundles may be sent to AISA-hosted endpoints.]

## Skill Version(s):

1.0.0 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
