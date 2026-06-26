## Description: <br>
Analyze Xcode build logs — timing, warnings, errors, slow compiles, and build history from DerivedData. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexissan](https://clawhub.ai/user/alexissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect Xcode DerivedData build history, summarize warnings and errors, identify slow build steps, and understand IDE or CLI build activity without modifying project files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose local Xcode project paths, compiler messages, app metadata, branch names, and worktree locations from DerivedData. <br>
Mitigation: Use it only when that local build metadata is acceptable to show in the agent session, and review outputs before sharing them outside the development context. <br>
Risk: DerivedData cleanup commands delete local build caches and force a future full rebuild. <br>
Mitigation: Review the printed path and size first, and run deletion only after intentionally deciding to remove that cache. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexissan/xcode-build-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only analysis guidance for local Xcode DerivedData; cleanup commands are presented separately for user review.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
