## Description:

Rewrites text into one of 10 requested tones while preserving meaning through a paid x402 tone-rewriting service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daisuke134](https://clawhub.ai/user/daisuke134)

### License/Terms of Use:


## Use Case:

Developers and AI agents use this skill to rewrite user-provided text for professional, casual, friendly, formal, empathetic, persuasive, academic, simple, witty, or urgent communication while preserving the original meaning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User text is sent to an external paid endpoint.

Mitigation: Confirm the text is appropriate to send to the endpoint before invocation, especially when it may contain sensitive or regulated content.

Risk: Each request is charged through x402 payment flow.

Mitigation: Use a low-risk payment setup and verify the exact request and cost before sending.

Risk: The skill asks users to install and authenticate a global payment CLI.

Mitigation: Install the CLI only from the expected package source and authenticate only in an environment approved for paid external service calls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/daisuke134/skills/tone-rewriter)
- [tone-rewriter x402 Endpoint](https://anicca-proxy-production.up.railway.app/api/x402/tone-rewriter)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON response containing rewritten text and tone metadata, with Markdown usage guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Input text is documented with a 2000 character maximum; each request is a paid x402 call.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
