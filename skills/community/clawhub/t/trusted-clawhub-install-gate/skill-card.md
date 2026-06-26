## Description: <br>
Audit a local OpenClaw or ClawHub skill directory before installation, classify it as PASS, REVIEW, or BLOCK, check active-project impact, and optionally run the clawhub-install-gate CLI to write a receipt or install after explicit user approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect local OpenClaw or ClawHub skill artifacts before installation, understand PASS, REVIEW, or BLOCK findings, and decide whether to stage, install, or stop. It is intended to keep installation decisions explicit by checking destination, replacement, dependency, script, and lockfile impact before any install. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can support installation or replacement decisions for local skills, including workflows that may involve privileged accounts or broad local review permissions. <br>
Mitigation: Require user-directed action, review moderation and autoreview guidance before use, perform the active-project impact check, and do not install artifacts classified as BLOCK. <br>
Risk: A REVIEW result may still contain residual findings that affect the active project if installed without understanding destination, dependencies, scripts, hooks, or lockfile changes. <br>
Mitigation: Install REVIEW artifacts only after explicit approval for both the residual findings and the destination-specific impact, and confirm any --allow-review or --replace flag for the specific artifact. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zack-dev-cm/trusted-clawhub-install-gate) <br>
- [Project homepage](https://github.com/zack-dev-cm/trusted-clawhub-install-gate) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown audit guidance with PASS, REVIEW, or BLOCK classification and inline shell commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include active-project impact checks, install or verify command suggestions, and receipt guidance after explicit user approval.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
