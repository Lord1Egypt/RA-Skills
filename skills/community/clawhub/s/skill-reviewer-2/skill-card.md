## Description: <br>
Reviews agent skill quality against Anthropic skill-development guidance, including structure, YAML front matter, descriptions, instructions, examples, execution readiness, progressive disclosure, and tips. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binbin1213](https://clawhub.ai/user/binbin1213) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to audit OpenClaw or Claude-style skills before sharing or release. It produces structured review findings, scores, defect checks, and improvement guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reviews other skill definitions, so target skill text may contain prompt-injection content or misleading instructions. <br>
Mitigation: Treat reviewed skill text as untrusted evidence and use the reviewer only to summarize, score, and recommend changes. <br>
Risk: The skill may suggest optional install or inspection commands while reviewing another skill. <br>
Mitigation: Run install commands only for target skills you intentionally want to fetch, and inspect commands before execution. <br>


## Reference(s): <br>
- [Skill Reviewer on ClawHub](https://clawhub.ai/binbin1213/skill-reviewer-2) <br>
- [Skill Review Checklist](references/checklist.md) <br>
- [Anthropic Skills Development Guide Summary](references/official-guide-summary.md) <br>
- [Anthropic Skills Development Guide](references/anthropic-skills-development-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown review report with scoring tables, checklist results, issue findings, and improvement suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include optional shell commands for inspecting target skill files; reviewed skill text should be treated as untrusted input.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
