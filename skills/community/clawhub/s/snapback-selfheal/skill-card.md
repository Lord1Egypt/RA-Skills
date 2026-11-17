## Description:

Helps agents diagnose failed runs and identify loops or budget overruns during a run, with suggested fixes and optional self-healing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ra1labsworkx-wq](https://clawhub.ai/user/ra1labsworkx-wq)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Snapback to diagnose failed or looping agent runs, monitor live runs for budget warnings, and consider suggested recovery actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent traces and steps sent to the hosted service may contain sensitive prompts, outputs, or credentials.

Mitigation: Pre-redact secrets and personal data, and start with non-sensitive test traces rather than relying solely on server-side scrubbing.

Risk: The optional Python interceptor with auto_apply enabled can act on diagnosis results in environments with state-changing tools.

Mitigation: Review the separate package before installing it, leave auto-apply disabled until approved, and require human review for consequential changes.

Risk: A compromised access token or unapproved wallet payment flow could expose account access or incur charges.

Mitigation: Scope and rotate SNAPBACK_TOKEN, and avoid wallet payment flows without explicit approval.

## Reference(s):

- [Snapback MCP endpoint](https://api.snapback.sh/mcp)
- [Snapback MCP tool discovery](https://snapback.sh/.well-known/mcp.json)
- [Snapback agent guide](https://snapback.sh/llms.txt)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Configuration instructions]

**Output Format:** [Markdown guidance and structured JSON tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include failure classifications, suggested fixes, confidence scores, and live-run warnings.]

## Skill Version(s):

1.8.4 (source: skill frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
