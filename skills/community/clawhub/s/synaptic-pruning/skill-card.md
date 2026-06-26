## Description: <br>
Identifies vestigial code, including dead feature branches, stale configurations, orphaned tests, and architectural remnants that no longer serve the codebase. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcools1977](https://clawhub.ai/user/jcools1977) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to review codebases for vestigial features, stale configuration, ineffective tests, compatibility shims, unreachable defenses, outdated documentation, and abandoned modules before planning removal work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may recommend removing code that appears vestigial but still supports rare, legacy, or undocumented workflows. <br>
Mitigation: Treat pruning recommendations as review input, confirm reachability with tests and production signals, and apply removals in small changes with rollback paths. <br>


## Reference(s): <br>
- [Synaptic Pruning on ClawHub](https://clawhub.ai/jcools1977/synaptic-pruning) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with analysis, scores, metrics, and recommended pruning steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces codebase maturity and vestigial burden findings for human review before code removal.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
