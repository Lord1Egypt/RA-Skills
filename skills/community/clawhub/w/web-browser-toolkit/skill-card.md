## Description:

Openclaw Web Browser helps agents collect web content, extract structured data, monitor page changes, and recommend related official documents, with presets for aviation sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkbeomjun-gkgkgk](https://clawhub.ai/user/parkbeomjun-gkgkgk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to gather web pages, extract selected content into structured JSON, monitor changes over time, and find relevant official documents for a topic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network fetching and browser automation can access URLs selected by the user.

Mitigation: Use only explicit public URLs and run the skill from a constrained directory or sandbox.

Risk: Scheduled monitoring can repeatedly fetch sites and write local JSON state.

Mitigation: Review stored monitors before enabling cron or other recurring runs.

Risk: The skill documents an SSL diagnostic path that can bypass certificate checks.

Mitigation: Do not use --insecure except for isolated diagnostics.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/parkbeomjun-gkgkgk/skills/web-browser-toolkit)
- [Aviation Presets](references/aviation_presets.json)
- [CSS Selector Guide](references/selector_guide.md)
- [Official Document Knowledge Base](sub-skills/doc-recommender/references/doc_knowledge_base.json)
- [Document Recommender Keyword Mapping](sub-skills/doc-recommender/references/keyword_mapping.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local JSON collections, monitor snapshots, diffs, alerts, reports, and document recommendation files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
