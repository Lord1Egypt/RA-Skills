## Description: <br>
Pack a local or remote codebase with repomix-rs and analyze the generated output for high-level exploration, structure summaries, or pattern discovery when targeted edits are not needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sopaco](https://clawhub.ai/user/sopaco) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to package local or remote repositories with repomix-rs, then inspect the generated output for structure, metrics, and cross-file patterns before choosing targeted files to read or edit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Packing private repositories or enabling git diffs/logs can expose sensitive source code or history in generated output. <br>
Mitigation: Confirm the repository and flags are appropriate before packing, keep generated output in a temporary path when possible, and review the output before sharing it with an agent. <br>
Risk: The skill relies on the external repomix-rs CLI and its installed command behavior. <br>
Mitigation: Confirm the installed package is repomix-rs, use explicit npx commands when needed, and review command output before relying on the generated pack. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sopaco/repomix-rs-explorer) <br>
- [repomix-rs repository](https://github.com/sopaco/repomix-rs) <br>
- [repomix-rs npm package](https://www.npmjs.com/package/repomix-rs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and analysis guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to create and inspect repomix output files in XML, Markdown, JSON, or text formats.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
