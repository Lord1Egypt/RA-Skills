## Description: <br>
CPU-based autonomous optimization loop for skill quality improvement. Runs experiments, evaluates results, keeps improvements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sjj2026](https://clawhub.ai/user/sjj2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this agent skill to run local optimization loops that modify experiment code, execute tests, compare results, and keep improvements after review. It is intended for skill package optimization, strategy backtesting, and content-creation testing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to edit experiment code and run local subprocesses in a target directory. <br>
Mitigation: Use a clean branch or disposable worktree, review diffs at each checkpoint, and install only when comfortable with local code execution. <br>
Risk: External run_loop.py implementations could perform behavior beyond the instruction-only skill text. <br>
Mitigation: Do not run any external implementation unless it is trusted and reviewed. <br>


## Reference(s): <br>
- [Karpathy Autoresearch](https://github.com/karpathy/autoresearch) <br>
- [OpenClaw Skills](https://github.com/openclaw/skills) <br>
- [ClawHub Skill Page](https://clawhub.ai/sjj2026/shike-autoresearch) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and code-oriented instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose file edits, experiment commands, git commands, and appended result records for a local optimization loop.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
