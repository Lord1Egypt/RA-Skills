## Description:

Use when a Hermes Agent user asks to check xAI OAuth usage, remaining quota, or reset time without refreshing or modifying credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hirorylabo](https://clawhub.ai/user/hirorylabo)

### License/Terms of Use:

MIT-0

## Use Case:

Hermes Agent users and developers use this skill to check xAI OAuth weekly usage, remaining quota, and reset timing without changing credentials or billing settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a Hermes xAI OAuth access token to perform the quota check.

Mitigation: Run it only after user approval, report only sanitized quota fields, and never display or save tokens, auth store contents, or the raw API response.

Risk: Authorization headers could be exposed if the billing endpoint redirects.

Mitigation: Keep redirect rejection in place so the Authorization header is not followed to another host.

Risk: A failed credential check could lead to unnecessary credential changes.

Mitigation: After 401 or 403 responses, report the error and HTTP status only; do not automatically reauthenticate, refresh, reset, or top up.

Risk: The billing period could be mistaken for a model-specific limit.

Mitigation: Describe the result as xAI OAuth weekly quota unless the API response gives a narrower verified scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hirorylabo/skills/xai-oauth-usage)
- [xAI billing endpoint used by the skill](https://cli-chat-proxy.grok.com/v1/billing?format=credits)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Human-readable text or sanitized JSON from a Python CLI, normally summarized by the agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports usage percentage, remaining quota, reset time, approximate time remaining, product usage, source host, and HTTP status on errors; human output follows Japanese or English display language settings.]

## Skill Version(s):

1.2.1 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
