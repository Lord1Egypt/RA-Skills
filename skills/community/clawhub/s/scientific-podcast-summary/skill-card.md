## Description:

Automatically summarize scientific podcasts like Huberman Lab and Nature.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch Huberman Lab, Nature Podcast, or user-provided podcast pages and generate structured scientific briefings in Markdown or JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch any user-supplied URL.

Mitigation: Use only public podcast URLs from trusted domains and avoid private, internal, or sensitive URLs.

Risk: Extracted page content is sent to OpenAI or a configured compatible API endpoint.

Mitigation: Keep OPENAI_BASE_URL pointed at a trusted provider and avoid processing private or confidential content.

Risk: A user-specified output path can overwrite an existing writable file.

Mitigation: Choose output paths deliberately and check for existing files before writing summaries.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/scientific-podcast-summary)
- [Audit Reference](references/audit-reference.md)
- [Huberman Lab Podcast Episodes](https://hubermanlab.com/category/podcast-episodes/)
- [Nature Podcast Articles](https://www.nature.com/nature/articles?type=podcast)

## Skill Output:

**Output Type(s):** [text, markdown, json, files]

**Output Format:** [Markdown or JSON scientific podcast briefing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write to a user-specified output path; summaries include episode metadata, core topics, key scientific points, practical advice, and related links.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, artifact SKILL.md, and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
