## Description:

Xtranslate translates PDF, Word, Excel, PowerPoint, TXT, and RTF documents with format preservation, layout optimization, batch processing, and selectable cloud, Ollama, or Python translation engines.

This skill is for research and development only.

## Publisher:

[guotao1980](https://clawhub.ai/user/guotao1980)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-workflow users use this skill to translate individual files or folders across common office formats while preserving structure where supported. It is suited to research and development workflows because the artifact states the tool is for personal learning and research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud translation mode can send extracted document text to configured external providers.

Mitigation: Use local Ollama mode for sensitive documents or confirm that the selected provider, endpoint, and data-handling terms are approved before using cloud mode.

Risk: Translation monitor, summary, output, and temporary conversion files can retain local document paths, timing data, or translated content.

Mitigation: Run the skill in an isolated workspace, review generated files before sharing, avoid committing monitor or summary files, and delete temporary conversion files after use.

Risk: Bundled API-key encryption uses a fixed local derivation and should not be treated as strong credential protection.

Mitigation: Prefer environment variables or a managed secret store for API keys, and rotate any key that may have been stored or shared in generated configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guotao1980/skills/xtranslate)
- [Publisher profile](https://clawhub.ai/user/guotao1980)
- [Project structure reference](artifact/references/project-structure.md)
- [Naming convention reference](artifact/references/naming-convention.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Translated document files, plain text or JSON monitor records, and Markdown or shell-command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write translated_* output files, tmp conversion files, translation_monitor.json, and periodic performance summary text files.]

## Skill Version(s):

3.2.0 (source: ClawHub release metadata; artifact frontmatter lists 3.2 and config lists V3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
