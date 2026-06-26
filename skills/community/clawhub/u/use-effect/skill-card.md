## Description: <br>
Refactor React code away from direct useEffect usage by reviewing, rewriting, or preventing effect-driven patterns in React components, hooks, and frontend architecture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liyown](https://clawhub.ai/user/liyown) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to identify direct React useEffect usage, classify why it exists, and replace it with derived render values, event handlers, data-loading abstractions, keyed remounts, or narrow mount-only lifecycle wrappers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Refactors may change React lifecycle behavior, remount boundaries, request timing, or local state semantics. <br>
Mitigation: Review generated diffs and run relevant tests or targeted checks for loops, duplicate requests, stale state, and remount behavior. <br>
Risk: Broad lint-rule or contributor-guidance changes may affect many future edits. <br>
Mitigation: Review policy changes before adoption and prefer incremental rollout around touched files unless a full migration is requested. <br>


## Reference(s): <br>
- [Use Effect on ClawHub](https://clawhub.ai/liyown/use-effect) <br>
- [useEffect Replacement Patterns](artifact/references/patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with code examples and optional shell commands or configuration changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should preserve project conventions and call for relevant tests or targeted checks after refactors.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
