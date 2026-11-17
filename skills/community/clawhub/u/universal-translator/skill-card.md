## Description:

Framework for translating Word, PDF, Excel, PowerPoint, HTML, Markdown, TXT documents. Provides document parsing code; the AI agent's own LLM performs the actual translation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to translate supported document files or folders while preserving document structure, with translation performed by the agent's configured LLM.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document contents may be processed by the LLM configured in OpenClaw, which may be local or remote.

Mitigation: Use only with documents appropriate for the configured LLM environment, and avoid sensitive files unless the data-handling path is approved.

Risk: PDF and HTML support are documented but incomplete in the provided parsing code.

Mitigation: Treat PDF and HTML workflows as incomplete until verified or updated by the publisher.

Risk: Python document-processing dependencies are installed on demand.

Mitigation: Install required packages in an isolated environment with pinned versions before processing documents.

## Reference(s):

- [Universal Translator ClawHub page](https://clawhub.ai/tobewin/skills/universal-translator)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with Python code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces document parsing and translation workflow guidance; translated files are created by the agent using local Python libraries and the configured LLM.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
