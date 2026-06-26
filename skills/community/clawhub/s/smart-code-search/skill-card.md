## Description: <br>
Smart Code Search helps agents and developers find code and documentation by semantic meaning using local ColGREP and NextPlaid indexing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brettmhammond](https://clawhub.ai/user/brettmhammond) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to search unfamiliar or large codebases by concept, find implementations and patterns, and navigate related project documentation when exact keywords are not known. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the separately installed ColGREP Homebrew package. <br>
Mitigation: Install it only from a trusted source and verify the colgrep binary before using it in sensitive repositories. <br>
Risk: Indexing creates a local .colgrep/ directory that may contain searchable metadata for the project. <br>
Mitigation: Run indexing only in projects intended for semantic search and add .colgrep/ to .gitignore. <br>
Risk: Optional agent integration can cause coding agents to use semantic search automatically in indexed projects. <br>
Mitigation: Enable the integration only in agent environments where automatic semantic code search is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brettmhammond/smart-code-search) <br>
- [Publisher profile](https://clawhub.ai/user/brettmhammond) <br>
- [Advanced Usage and Architecture](references/advanced.md) <br>
- [ColGREP and NextPlaid on GitHub](https://github.com/lightonai/next-plaid) <br>
- [LateOn-Code benchmark notes](https://lighton.ai/lighton-blogs/lateon-code-colgrep-lighton) <br>
- [NextPlaid local-first multi-vector database](https://lighton.ai/lighton-blogs/introducing-lighton-nextplaid) <br>
- [BrowseComp-Plus retrieval results](https://lighton.ai/lighton-blogs/the-bloated-retriever-era-is-over) <br>
- [Reason-ModernColBERT retrieval notes](https://lighton.ai/lighton-blogs/lighton-releases-reason-colbert) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command-line examples and optional JSON output from ColGREP.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the colgrep binary; creates and updates a local .colgrep/ index inside each searched project.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
