## Description: <br>
Helps agents create temporary email addresses and retrieve mailbox message lists and individual message details through MaxHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[new-ironman](https://clawhub.ai/user/new-ironman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, testers, and users can use this skill to create disposable email addresses, check incoming messages, and read message details for privacy-preserving signups or email-verification testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner marked this release suspicious because under-scoped instructions and unrelated fallback guidance could make an agent act outside a clear temporary-email workflow. <br>
Mitigation: Review before installing, prefer explicit temporary-mail prompts, and verify routing behavior before relying on the skill. <br>
Risk: The skill requires a sensitive MaxHub API key and may process temporary-mail contents through the upstream service. <br>
Mitigation: Use it only if you trust MaxHub with the configured API key and mailbox contents, keep credentials out of outputs, and rotate or revoke the key if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/new-ironman/tempmail-aggregate-scraper) <br>
- [MaxHub website](https://www.aconfig.cn) <br>
- [Email Operations API](references/api-email.md) <br>
- [Parameter Mapping Reference](references/param-mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown responses with optional shell commands and API result summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAXHUB_API_KEY and curl; credential values should not be included in responses.] <br>

## Skill Version(s): <br>
3.6.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
