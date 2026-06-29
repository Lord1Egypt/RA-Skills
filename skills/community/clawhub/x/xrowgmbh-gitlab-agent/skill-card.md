## Description: <br>
An agent for interacting with GitLab. Supports gitlab.com and self-hosted instances. Requires no GitLab DUO. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xrowgmbh](https://clawhub.ai/user/xrowgmbh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to automate GitLab issue, merge request, branch, label, comment, and CI follow-up work through GitLab CLI workflows. It is intended for GitLab.com or self-hosted GitLab projects where autonomous changes are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can drive broad autonomous GitLab changes, including issue, merge request, branch, CI, label, and comment updates. <br>
Mitigation: Use a dedicated least-privilege GitLab token, limit it to approved projects, and monitor the resulting GitLab activity. <br>
Risk: The bundled recurring job could repeatedly execute automation after setup. <br>
Mitigation: Keep the recurring job disabled until a manual run has been reviewed and GitLab authentication has been confirmed. <br>
Risk: Agent-generated GitLab updates may be incorrect, overly broad, or misaligned with project workflow expectations. <br>
Mitigation: Review merge requests, issue comments, labels, and CI actions before relying on them for production workflow decisions. <br>


## Reference(s): <br>
- [GitLab default roles](https://docs.gitlab.com/user/permissions/#default-roles) <br>
- [CI Tools Components Catalog for GitLab](https://ci-tools.xrow.de/) <br>
- [CI Tools label component](https://ci-tools.xrow.de/Components/label) <br>
- [OpenClaw creating skills](https://docs.openclaw.ai/tools/creating-skills) <br>
- [xrow public skills project](https://gitlab.com/xrow-public/skills) <br>
- [ClawHub skill page](https://clawhub.ai/xrowgmbh/skills/xrowgmbh-gitlab-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, shell commands, code changes, configuration snippets, and GitLab issue or merge request updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the glab CLI and GITLAB_TOKEN; may create or update remote GitLab resources when used by an agent.] <br>

## Skill Version(s): <br>
1.62.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
