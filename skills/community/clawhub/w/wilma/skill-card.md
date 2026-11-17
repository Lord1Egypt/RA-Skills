## Description:

Access Finland's Wilma school system from AI agents, for parents (and students with their own login). Fetch schedules, homework, exams, grades and the gradebook, lesson notes (merkinnät) and absence summaries, messages with replies, news, printouts and linked news resources — through the WilmAI MCP tools (`wilma_*`) when connected, or the wilma CLI. Start with a summary, drill into messages and news, and fetch linked attachments. Requires wilma-cli 2.0+.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aikarjal](https://clawhub.ai/user/aikarjal)

### License/Terms of Use:

MIT-0

## Use Case:

Parents and guardians, or students using their own Wilma login, use the skill to review school schedules, assignments, grades, lesson notes, messages, news, and related documents. It can turn those records into concise, actionable summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retrieve sensitive school records, including grades, absences, lesson notes, messages, and contact information.

Mitigation: Use a Wilma account authorized for the intended student, select only the records needed, and check that contact access is appropriate for the task.

Risk: Wilma credentials may be saved in a local configuration file, and the skill relies on installing the Wilma CLI.

Mitigation: Review the CLI installation source and protect the saved login or agent secret settings. Follow the skill's keychain guidance only on an interactive personal computer; keep file-based credentials on unattended servers.

Risk: The security review was partial because one referenced local path was unresolved.

Mitigation: Review the complete release contents and confirm the referenced files are present before installation.

## Reference(s):

- [WilmAI website](https://wilm.ai)
- [WilmAI project repository (linked by the skill)](https://github.com/aikarjal/wilmai)

## Skill Output:

**Output Type(s):** [JSON data, Text summaries, Guidance]

**Output Format:** [Structured Wilma records with concise text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available records depend on the connected Wilma accounts, selected student, and information provided by the school.]

## Skill Version(s):

2.5.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
