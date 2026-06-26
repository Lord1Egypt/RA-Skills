## Description: <br>
Post-completion self-review for coding agents that runs simplify, harden, and micro-documentation passes on non-trivial code changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pskoett](https://clawhub.ai/user/pskoett) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill after non-trivial coding tasks to perform a bounded self-review for cleanup, hardening, and concise comments before signaling completion. It is intended to complement, not replace, independent code review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can instruct agents to create durable learning records and promote rules into future agent instruction files. <br>
Mitigation: Require explicit human approval before writes to `.learnings/LEARNINGS.md`, `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, or similar persistent agent-instruction files. <br>
Risk: Automatic post-task cleanup and simple hardening edits can change recently completed code. <br>
Mitigation: Review the resulting diff and run the normal test or review gate before merging; require explicit approval for refactors and structural security changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pskoett/simplify-and-harden) <br>
- [Agent context snippets](artifact/references/agent-context-snippets.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration instructions] <br>
**Output Format:** [Markdown summary with structured YAML-style review output and optional code edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May add bounded code cleanup, hardening patches, and up to five explanatory comments within the modified-task scope.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
