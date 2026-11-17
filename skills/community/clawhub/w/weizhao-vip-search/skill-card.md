## Description:

Searches VIP.com products by keyword by guiding users to provide a logged-in browser cookie and running a Python script against a VIP.com search endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miketobusy](https://clawhub.ai/user/miketobusy)

### License/Terms of Use:

MIT-0

## Use Case:

External users or shopping assistants use this skill to search VIP.com by keyword and summarize product names, prices, original prices, and discounts. The workflow depends on a user-provided logged-in VIP.com cookie.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A full logged-in VIP.com cookie can act like a temporary session password if pasted into chat, logs, shell history, or process arguments.

Mitigation: Avoid pasting raw session cookies into an agent or command line; use VIP.com directly or redesign the workflow around a protected secret-input mechanism.

Risk: The script relies on a VIP.com endpoint and response shape that may change, producing incomplete results or diagnostic output instead of product data.

Mitigation: Review returned data before acting on it and update the endpoint or parsing logic when VIP.com changes its API behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/miketobusy/skills/weizhao-vip-search)
- [VIP.com](https://www.vip.com/)
- [VIP.com search endpoint used by script](https://category.vip.com/ajax/getSuggest.php)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, JSON]

**Output Format:** [Markdown instructions and product summaries, with Python command examples and JSON or diagnostic text from the search script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a keyword and a user-provided VIP.com session cookie; search results depend on VIP.com endpoint availability and response format.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
