## Description: <br>
Recursive self-improvement engine. Think from first principles, let insights emerge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hsssgdtc](https://clawhub.ai/user/hsssgdtc) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use Ralph Evolver to analyze a target repository, collect project health and history signals, and generate prompts for iterative code or documentation improvements. It supports repeated cycles for repair, discovery, and self-improvement workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run a target project's build, test, lint, and pytest commands with local user permissions. <br>
Mitigation: Use it only on trusted repositories, or run it in a sandbox without secrets or sensitive credentials. <br>
Risk: Generated prompts may instruct an agent to edit repository files. <br>
Mitigation: Review the generated prompt and proposed changes before allowing an agent to modify files. <br>
Risk: The .ralph directory stores local run history, and --reset deletes that local state. <br>
Mitigation: Keep loop counts small, treat .ralph as disposable run history, and back it up before resetting if the history matters. <br>


## Reference(s): <br>
- [Ralph Evolver on ClawHub](https://clawhub.ai/hsssgdtc/ralph-evolver) <br>
- [Publisher profile: hsssgdtc](https://clawhub.ai/user/hsssgdtc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown prompt with inline code, shell commands, project-analysis findings, and iteration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local repository health summaries, git-history signals, TODO/FIXME findings, error-pattern snippets, and .ralph improvement-history guidance.] <br>

## Skill Version(s): <br>
1.0.6 (source: frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
