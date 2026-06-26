## Description: <br>
Static analysis security scanner for third-party OpenClaw skills. Detects eval/spawn risks, malicious dependencies, typosquatting, and prompt injection patterns before installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[britrik](https://clawhub.ai/user/britrik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect OpenClaw skills from local paths, URLs, or ClawHub before installation. It helps surface code execution, dependency, typosquatting, prompt injection, and metadata risks that require review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner reads the skill directories or downloaded archives that the user points it at. <br>
Mitigation: Run it from a scoped workspace or disposable container when inspecting untrusted skills or archives. <br>
Risk: Remote URL and ClawHub vetting invoke external tools and handle downloaded content. <br>
Mitigation: Use remote vetting only for sources intended for inspection, and ensure git, curl, tar, and clawhub on PATH are trusted. <br>
Risk: Automatic pre-install vetting can block or prompt during installation workflows. <br>
Mitigation: Leave autoVet disabled unless automatic scans are desired and the review threshold is configured for the environment. <br>
Risk: The included AI pull-request review workflow can send PR diffs to an external AI service if the repository workflow is reused. <br>
Mitigation: Review or disable the workflow before forking or reusing the repository. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/britrik/vettr) <br>
- [Publisher profile](https://clawhub.ai/user/britrik) <br>
- [Project homepage from ClawHub metadata](https://github.com/britrik/skill-vettr) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown-style text reports with risk scores, recommendations, findings, metadata, and optional approval or rejection notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands return textual vetting reports and may prompt for approval when findings require review.] <br>

## Skill Version(s): <br>
2.0.4 (source: ClawHub release evidence; artifact frontmatter and package metadata report 2.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
