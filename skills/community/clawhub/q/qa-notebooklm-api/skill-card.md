## Description:

Use NotebookLM CLI to manage notebooks, add text or URL sources, ask questions, summarize content, and generate learning materials such as slide decks, quizzes, and flashcards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chunkitcn](https://clawhub.ai/user/chunkitcn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate NotebookLM through the notebooklm CLI for notebook setup, source ingestion, Q&A, summaries, and study-material generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Notebook sources, prompts, and generated-study requests may be routed through an authenticated external NotebookLM workflow using a third-party CLI.

Mitigation: Use only when that external workflow is intended, verify the CLI package source, run it in an isolated environment, and avoid uploading secrets or confidential documents unless approved.

Risk: The skill can create notebooks, add sources, generate artifacts, and download files in the user's NotebookLM context.

Mitigation: Confirm before account-affecting actions such as creating notebooks, adding sources, generating artifacts, or downloading generated files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chunkitcn/skills/qa-notebooklm-api)
- [NotebookLM CLI Repository](https://github.com/tiangong-ai/notebooklm-cli)
- [NotebookLM CLI Quick Reference](references/quick-ref.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and command-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include NotebookLM artifact identifiers, polling commands, and download commands for generated study materials.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
