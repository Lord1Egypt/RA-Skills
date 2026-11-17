## Description:

Performs Google searches through the Serper.dev API with web, news, images, videos, places, shopping, scholar, patents, autocomplete, Knowledge Graph, Answer Box, People Also Ask, and related search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minilozio](https://clawhub.ai/user/minilozio)

### License/Terms of Use:

MIT

## Use Case:

Agents, developers, and operators use this skill to retrieve Google Search results and specialized result types from Serper.dev when web, news, image, video, place, shopping, scholar, patent, or suggestion data is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Serper.dev and require a SERPER_API_KEY.

Mitigation: Run the skill only in environments where sending queries to Serper.dev is acceptable and where the API key can be provided through environment variables.

Risk: The documented runtime path can execute an unpinned npm package before the reviewed code runs.

Mitigation: Prefer a pinned, lockfile-backed local tsx installation or compiled JavaScript instead of running unpinned npx tsx commands directly.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/minilozio/skills/serper-google-search)
- [Serper.dev API Reference](references/serper-api.md)
- [Serper.dev](https://serper.dev)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Formatted terminal text or JSON when requested, usually presented in Markdown with shell command examples and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results may include titles, links, snippets, rich result fields, and Serper credit balance information.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
