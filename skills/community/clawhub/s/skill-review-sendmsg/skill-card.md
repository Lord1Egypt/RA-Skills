## Description: <br>
Performs structured code reviews of diffs, patches, and pull requests, returning actionable findings about correctness, security, test coverage, and maintainability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dexing2635-tech](https://clawhub.ai/user/dexing2635-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review repository changes before merge or deployment and to summarize concrete issues for a human reviewer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository diffs may be sent to the configured LLM provider. <br>
Mitigation: Use the skill only with repositories approved for that provider, redact sensitive changes, or configure local-only REVIEW_MODE or a trusted self-hosted endpoint. <br>
Risk: Telegram notifications can disclose review status, project metadata, and log details to the configured chat. <br>
Mitigation: Use least-privilege bot tokens, restrict chat membership, and avoid configuring Telegram for sensitive repositories unless disclosure is approved. <br>
Risk: The runner can clone configured repositories and persist local review state. <br>
Mitigation: Run it in an isolated workspace with scoped repository credentials and review local state and logs before sharing the environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dexing2635-tech/skill-review-sendmsg) <br>
- [Publisher profile](https://clawhub.ai/user/dexing2635-tech) <br>
- [references/README.md](references/README.md) <br>
- [references/SKILL.original.md](references/SKILL.original.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown review findings with file and line references; helper scripts can emit JSON results and notification text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prioritizes high-severity findings, verdicts, and suggested fixes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
