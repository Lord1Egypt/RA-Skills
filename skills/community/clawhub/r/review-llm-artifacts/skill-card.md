## Description: <br>
Detects common LLM coding agent artifacts across tests, dead code, abstraction, and style over changed files or a full project, using parallel subagents when supported and sequential passes otherwise. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scan changed files or a project tree for cleanup issues commonly left by LLM coding agents, then review a structured report before verifying or fixing findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects repository source files and writes a local JSON report that can contain file paths and review findings. <br>
Mitigation: Review the .beagle/llm-artifacts-review.json report before sharing it or using a separate verification or fixing workflow. <br>
Risk: Using --all can broaden the scan to a full project. <br>
Mitigation: Use the default changed-files scope or pass a narrower target path when a broad project scan is not intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/review-llm-artifacts) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [JSON report plus Markdown summary with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a local .beagle/llm-artifacts-review.json report after tests, dead code, abstraction, and style reviews complete.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.json release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
