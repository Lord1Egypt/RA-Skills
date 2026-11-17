## Description:

Generate AI-powered academic research reports via the Scholar API with literature review summaries, inline citations, paper evidence, and downloadable Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wahahaaaa123](https://clawhub.ai/user/wahahaaaa123)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and researchers use this skill to generate academic literature review reports, surveys, and state-of-the-art summaries from a research question or topic. The skill supports report creation, progress polling, and Markdown download with optional paper-level evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics, filters, and generated report data are sent to scholar.x49.ai.

Mitigation: Avoid confidential or regulated research content and review data-sharing expectations before use.

Risk: The skill includes a shared fallback API bearer token.

Mitigation: Prefer setting SCHOLAR_API_KEY with a user-controlled key instead of relying on the built-in shared key.

Risk: Generated Markdown may be saved into a project directory.

Mitigation: Confirm the save location and review generated content before adding it to a repository or workflow.

## Reference(s):

- [Scholar API key documentation](https://scholar.x49.ai/docs?section=api-keys)
- [Scholar API](https://scholar.x49.ai/api/v1)
- [ClawHub skill listing](https://clawhub.ai/wahahaaaa123/skills/scholar-report-x49)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with inline citations, command examples, and progress summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include paper evidence, references, research directions, and downloadable Markdown.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
