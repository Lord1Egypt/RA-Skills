## Description:

LinkedIn Inbox Manager helps agents search, filter, summarize, and manage LinkedIn conversations through Linxa using token-based access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vdybenko](https://clawhub.ai/user/vdybenko)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to review LinkedIn inbox conversations, identify leads, fetch message threads, receive next-action recommendations, add CRM-style comments, and mark conversations as read.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill lets an agent access LinkedIn-derived inbox and lead data through LINXA_TOKEN.

Mitigation: Install only if you are comfortable with Linxa and agent access to that data, protect the bearer token, and revoke it when it is no longer needed.

Risk: Adding comments and marking conversations as read can change LinkedIn inbox or lead-management state.

Mitigation: Confirm the target conversation or lead before allowing comment creation or marking a conversation as read.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vdybenko/skills/smart-linkedin-inbox)
- [Linxa application](https://app.uselinxa.com/)
- [Linxa MCP setup](https://app.uselinxa.com/setup-mcp)
- [Linxa Chrome Extension](https://chromewebstore.google.com/detail/ai-smart-inbox-for-linked/ggkdnjblijkchfmgapnbhbhnphacmabm)
- [OpenAPI specification](artifact/openapi.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with optional shell commands, configuration snippets, and API-derived text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include chronological message summaries, prioritized next actions, filter results, troubleshooting guidance, and confirmation prompts before mutating inbox state.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
