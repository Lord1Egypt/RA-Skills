## Description:

Compile markdown documents with plugin tags into editorial-quality HTML pages using Wurd.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vreff](https://clawhub.ai/user/vreff)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical authors use this skill to create Wurd markdown documents, configure layouts and themes, compile them into self-contained HTML pages, and add or debug deterministic and LLM-powered plugins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running commands through unpinned npx can introduce supply-chain uncertainty.

Mitigation: Pin tsx or use a lockfile-backed project install before running Wurd commands.

Risk: LLM-powered plugins may send document content to a configured model provider.

Mitigation: Avoid LLM plugins for confidential documents unless the provider terms and data handling are acceptable.

Risk: Cached LLM-generated content can remain on disk after compilation.

Mitigation: Clear .cache/llm/ when cached generated content should not remain on disk.

## Reference(s):

- [Wurd GitHub repository](https://github.com/vreff/Wurd)
- [Wurd skill page](https://clawhub.ai/vreff/skills/wurd)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides creation and compilation of Wurd documents; generated HTML output is produced by the Wurd tool.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
