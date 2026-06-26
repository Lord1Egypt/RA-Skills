## Description: <br>
Download and normalize official documentation pages into local .mdx files at user-specified paths using markdown.new. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[multicul-silver-wolf](https://clawhub.ai/user/multicul-silver-wolf) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to snapshot official documentation pages as local MDX files for project docs, knowledge bases, or retrieval preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The source URL is sent to markdown.new during conversion. <br>
Mitigation: Use public or shareable documentation URLs and avoid sending private, internal, or credential-bearing URLs. <br>
Risk: The bundled script writes to the user-provided output path and overwrites existing files. <br>
Mitigation: Review the destination path before running and ask the agent to list planned .mdx and index.mdx file changes. <br>


## Reference(s): <br>
- [mdnew_to_mdx.sh reference](references/mdnew_to_mdx.md) <br>
- [ClawHub skill page](https://clawhub.ai/multicul-silver-wolf/sawana-multicul-official-docs-to-mdx) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated MDX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated MDX includes title, description, sourceUrl, and retrievedAt frontmatter; existing output files may be overwritten.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
