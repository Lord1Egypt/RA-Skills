## Description: <br>
Publish any SKILL.md to 4 skill markets (ClawHub, Anthropic Skills, ECC Community, skills.sh) with one command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to publish SKILL.md-compatible agent skills to ClawHub, Anthropic Skills, ECC Community, and skills.sh. It guides quality checks, token verification, platform adaptation, pull request creation, conflict handling, retries, and result reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for powerful GitHub and ClawHub tokens and can create remote uploads, branches, and pull requests. <br>
Mitigation: Use dedicated short-lived or fine-grained tokens, grant only required scopes, avoid unnecessary workflow or private-repository access, and revoke tokens after publishing. <br>
Risk: Publishing actions can expose files or create public pull requests on unintended platforms. <br>
Mitigation: Confirm the target platforms, files, repositories, branches, pull requests, and publication visibility before each run. <br>


## Reference(s): <br>
- [API Request Templates](references/templates.md) <br>
- [Publishing Playbooks](references/playbooks.md) <br>
- [Error Recovery Paths](references/fallbacks.md) <br>
- [Execution Log Schema](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, status summaries, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports quality-gate results, publication status by platform, retry guidance, and PR or release identifiers from actual API responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
