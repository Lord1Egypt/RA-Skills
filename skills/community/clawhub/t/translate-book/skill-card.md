## Description: <br>
Translate books (PDF/DOCX/EPUB) into any language using parallel sub-agents. Converts input -> Markdown chunks -> translated chunks -> HTML/DOCX/EPUB/PDF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deusyu](https://clawhub.ai/user/deusyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to translate PDF, DOCX, and EPUB books into a target language while preserving structure and producing web, document, ebook, and PDF outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the named book file and writes a temporary workspace containing source chunks, translated chunks, metadata, and generated outputs. <br>
Mitigation: Run it only on files you are allowed to process, keep intermediates only when needed for audit or recovery, and clean the workspace after completion when those files are no longer needed. <br>
Risk: The skill runs local Calibre, Pandoc, and ebook-convert binaries from PATH. <br>
Mitigation: Use trusted installations of those tools and verify the runtime PATH before starting the pipeline. <br>
Risk: Book chunks are sent through sub-agents for translation. <br>
Mitigation: Avoid sensitive or proprietary books unless the agent runtime and sub-agent handling meet the applicable data policy. <br>
Risk: If the glossary is edited after some chunks are translated, existing translated chunks are not automatically invalidated in this release. <br>
Mitigation: Delete affected output_chunk files or use a fresh temp directory before rerunning when glossary edits must be reflected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deusyu/translate-book) <br>
- [Project homepage](https://github.com/deusyu/translate-book) <br>
- [Calibre](https://calibre-ebook.com/) <br>
- [Pandoc](https://pandoc.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Translated Markdown plus generated HTML, DOCX, EPUB, and PDF files in a temporary workspace; may also include JSON glossary, manifest, and per-chunk metadata files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a cwd-local book temp workspace, uses local Calibre/Pandoc tooling, and can run parallel sub-agents for chunk translation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
