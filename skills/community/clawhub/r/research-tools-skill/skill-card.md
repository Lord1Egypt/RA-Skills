## Description:

Research Tools Skill helps researchers search literature, analyze data, and develop research code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonjiang96](https://clawhub.ai/user/jonjiang96)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and analysts use this skill to guide literature discovery, summarize papers, draft data-analysis workflows, and generate research code across scientific domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries and fetched paper URLs may be sent to external services.

Mitigation: Review search terms, URLs, and data sensitivity before allowing web search or fetch actions.

Risk: The skill includes examples that can run local commands or create project code when the user asks for that behavior.

Mitigation: Inspect generated commands before execution and run them in an appropriate workspace with normal least-privilege controls.

Risk: Generated summaries, analyses, or code can be incomplete or incorrect for a specific research task.

Mitigation: Validate literature summaries against source papers and verify generated analysis code with tests or independent review.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline command examples and generated code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples may rely on agent-provided search, fetch, command execution, and session-spawn tools, with optional local python, node, or git binaries.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
