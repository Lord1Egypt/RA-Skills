## Description:

Generate polished Chinese R&D weekly reports from recent work logs, chat history, commit notes, or development notes while automatically filtering deployment, environment, operations, installation, and troubleshooting details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lfc162874](https://clawhub.ai/user/lfc162874)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and product teams use this skill to convert noisy work logs, chat history, meeting notes, commit summaries, or issue notes into concise manager-facing Chinese R&D weekly reports. It is suited for R&D updates involving tender-agent, RAG, prompt, skill, document parsing, table parsing, scoring-standard, content-generation, export-center, and Agent work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source notes may include sensitive project, personal, or business information that could be summarized into the weekly report.

Mitigation: Review and redact source notes before using the skill, and provide only content appropriate for a manager-facing report.

Risk: The skill intentionally filters deployment, environment, operations, installation, and troubleshooting details, which may omit information needed for an unfiltered technical summary.

Mitigation: Use explicit instructions or another tool when operational details or a full technical summary are required.

Risk: Relative date ranges depend on the current date and timezone available in the conversation.

Mitigation: Provide an exact date range when the report period must be precise.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lfc162874/skills/weekly-report-skill)
- [Publisher Profile](https://clawhub.ai/user/lfc162874)
- [Example Input](artifact/examples/input.md)
- [Example Output](artifact/examples/output.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese manager-facing weekly report with dated or undated sections, highlights, and next-week plans when reportable R&D work is present.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
