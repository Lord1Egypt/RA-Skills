## Description:

A test-environment ecommerce assistant for shop authorization, 1688 image-based sourcing, product previews, and confirmed or explicitly requested automatic publishing.

This skill is for research and development only.

## Publisher:

[daiyangyang103240](https://clawhub.ai/user/daiyangyang103240)

### License/Terms of Use:

MIT-0

## Use Case:

Ecommerce sellers and developers use this development release to connect a test shop, find 1688 products from images, inspect shop status, and preview or publish selected products in the test environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shop authorization stores a sensitive local session token.

Mitigation: Keep the token in a private local session file and never include it in user-facing responses or saved preview data.

Risk: Publishing can change shop listings.

Mitigation: Preview and confirm before publishing unless the user explicitly requests automatic publishing; submit only preview-ready selected items.

Risk: This development release could be mistaken for the production service.

Mitigation: Verify the installed development slug and keep authorization and frontend links on the test environment.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/daiyangyang103240/skills/xtph-ecommerce-assistant-dev)
- [Agent API protocol](references/api-protocol.md)
- [Test-environment application](https://puhuo-test.huitun.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational text, Markdown product tables, and test-environment links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shows up to 10 image-search results in source order; omits session tokens and private payloads.]

## Skill Version(s):

1.0.16 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
