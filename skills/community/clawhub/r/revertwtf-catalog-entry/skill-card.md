## Description: <br>
Add or update precise revert.wtf catalog entries, fixtures, source metadata, and matcher tests for one or a small set of EVM/RPC/provider/wallet/protocol errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrtdlgc](https://clawhub.ai/user/mrtdlgc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to add, fix, rename, deprecate, or verify specific entries in the revert.wtf error catalog, including source metadata, fixtures, matcher patterns, and validation commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Overly broad RPC, provider, or wallet error matches could make catalog results misleading. <br>
Mitigation: Review generated patterns before merging, prefer selectors or structured json_path matches when available, and use guard context such as requires for broad codes. <br>
Risk: Catalog or parser changes can regress matching behavior across CLI, MCP, and web result paths. <br>
Mitigation: Run the skill's targeted build, validation, duplicate-check, TypeScript, and parser tests when the local environment allows them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrtdlgc/revertwtf-catalog-entry) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline code, catalog entry structure, and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose repository edits, catalog metadata, matcher patterns, fixtures, and targeted validation commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
