## Description: <br>
Comprehensive BubbleTea TUI code review for terminal applications. Use when reviewing charmbracelet/bubbletea, lipgloss, bubbles, or Wish SSH code; optionally reviews each area concurrently. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Go terminal user interface changes that use BubbleTea, Lipgloss, Bubbles, or Wish SSH. It guides agents through scoped code review, evidence checks, issue severity, and post-fix verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce incorrect or misleading code-review guidance if findings are not grounded in opened source files. <br>
Mitigation: Require file and line evidence for Critical and Major findings, re-read actual code before reporting issues, and remove unsupported or preference-only findings. <br>
Risk: The skill may suggest shell commands that use broad local repository access during review and post-fix verification. <br>
Mitigation: Review commands before execution and keep credentials scoped, consistent with the server security guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/review-tui) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown review report with issue severities, file-line references, rationale, fixes, good patterns, verdict, and verification commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review output is constrained to scoped code-review findings and post-fix verification guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata, released 2026-06-01) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
