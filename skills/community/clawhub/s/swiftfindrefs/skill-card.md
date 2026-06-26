## Description: <br>
Use swiftfindrefs (IndexStoreDB) to list every Swift source file referencing a symbol. Mandatory for "find references", "fix missing imports", and cross-module refactors. Do not replace with grep/rg or IDE search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michaelversus](https://clawhub.ai/user/michaelversus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to make agents rely on swiftfindrefs and Xcode IndexStore data when finding Swift symbol references, fixing imports after moving symbols, or planning cross-module refactors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the third-party swiftfindrefs CLI and its Homebrew/GitHub source. <br>
Mitigation: Review the swiftfindrefs CLI source and installation path before using the skill in sensitive Swift projects. <br>
Risk: If Xcode DerivedData or IndexStore resolution is stale or wrong, the returned file set may be incomplete or misleading. <br>
Mitigation: Build the project first, prefer an explicit data store path in deterministic environments, and stop rather than guessing when IndexStore resolution fails. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/michaelversus/swiftfindrefs) <br>
- [CLI reference](references/cli.md) <br>
- [Workflows](references/workflows.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be reviewed before execution, and file edits should be limited to paths returned by swiftfindrefs.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
