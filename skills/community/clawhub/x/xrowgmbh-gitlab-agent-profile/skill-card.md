## Description: <br>
Maintain the GitLab agent profile page and static contribution performance chart. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xrowgmbh](https://clawhub.ai/user/xrowgmbh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to update GitLab profile assets with monthly merge request, direct commit, and contribution score statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated GitLab reads and optional pushes can affect repositories beyond the intended profile workflow if credentials or project settings are too broad. <br>
Mitigation: Use a GitLab token limited to the intended account and repositories, and enable recurring cron execution only when unattended updates and pushes are acceptable. <br>
Risk: The generated proof JSON may publish merge request titles, labels, reviewers, URLs, and commit metadata. <br>
Mitigation: Avoid running the skill on private projects unless publishing those proof records is acceptable. <br>
Risk: Configurable output paths write local SVG, WebP, and JSON files. <br>
Mitigation: Keep all output variables under the profile repository assets directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xrowgmbh/skills/xrowgmbh-gitlab-agent-profile) <br>
- [Publisher profile](https://clawhub.ai/user/xrowgmbh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands and generated SVG, WebP, and JSON asset files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires glab, python3, and GITLAB_TOKEN; output paths and GitLab projects are configurable through environment variables.] <br>

## Skill Version(s): <br>
1.62.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
