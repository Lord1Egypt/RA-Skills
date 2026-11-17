## Description:

Lightweight website uptime monitor. Check if URLs are up, measure response times, detect content changes via hashing, and verify expected content. Zero dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[claudiodrusus](https://clawhub.ai/user/claudiodrusus)

### License/Terms of Use:


## Use Case:

Developers, site operators, and automation agents use this skill to check URL availability, measure response time, verify expected text, and detect page-content changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to user-supplied URLs and reads response bodies for hashing or text checks.

Mitigation: Use care with private or internal URLs, and review monitored targets before running the checker in shared or automated environments.

## Reference(s):

- [Website Monitor on ClawHub](https://clawhub.ai/claudiodrusus/skills/website-monitor)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands]

**Output Format:** [Plain text or JSON command output; agent-facing usage may include Markdown with shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns exit code 1 when any checked site is down or fails expectations.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
