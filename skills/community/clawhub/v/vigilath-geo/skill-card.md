## Description:

Vigilath GEO helps agents check website GEO and SEO readiness, query AI-search visibility, review brand monitoring data, and generate optimization guidance through the Vigilath service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dz1995](https://clawhub.ai/user/dz1995)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to run no-login website GEO/SEO checks and, after authorization, retrieve brand visibility metrics, reports, sentiment monitoring, wallet status, and optimization guidance from Vigilath. It is intended for brand visibility analysis and operational marketing workflows, not for direct uncontrolled publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer supply-chain risk from piping a remote install script into a shell.

Mitigation: Review the artifact before installing and prefer OpenClaw's local-directory installer or a verified release instead of `curl | bash`.

Risk: The installer can place the skill into multiple agent environments.

Mitigation: Use `--dir` to install only into the intended agent environment.

Risk: Stored Vigilath credentials can grant account-level access through the skill.

Mitigation: Treat the token like an API key, verify `VIGILATH_BASE` before authorizing, and remove or rotate the token when it is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dz1995/skills/vigilath-geo)
- [Publisher profile](https://clawhub.ai/user/dz1995)
- [Server-resolved GitHub import](https://github.com/dz1995/GEO-skills/tree/main/vigilath-geo)
- [Homepage](https://github.com/dz1995/GEO-skills)
- [Vigilath skill installation page](https://vigilath.cn/skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, JSON snippets, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some commands return structured JSON cards or metric payloads; authorized workflows require a Vigilath account token.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
