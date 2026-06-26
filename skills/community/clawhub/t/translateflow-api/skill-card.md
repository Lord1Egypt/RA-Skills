## Description: <br>
Provides guidance and curl examples for using VCG's TranslateFlow API to translate text, documents, websites, and localized content across many languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jbennett111](https://clawhub.ai/user/Jbennett111) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to prepare translation requests, manage API-key setup, and call TranslateFlow endpoints for text, batch, document, website, and domain-specific translation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route user email addresses, text, documents, URLs, and CMS content to an external translation service without clear privacy or consent boundaries. <br>
Mitigation: Have the agent ask before sending user content to the provider and confirm the provider's privacy and retention terms before use. <br>
Risk: Legal, medical, confidential, or regulated material may require stricter handling than the skill documents. <br>
Mitigation: Avoid using the skill for regulated or sensitive material unless the user has verified that the provider and workflow satisfy applicable requirements. <br>
Risk: API keys used in curl commands could be exposed if pasted into shared logs, shell history, or generated files. <br>
Mitigation: Store keys securely, avoid printing them in shared outputs, and use placeholders when showing commands back to the user. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Jbennett111/translateflow-api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Text] <br>
**Output Format:** [Markdown guidance with curl commands and JSON request/response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided TranslateFlow API key and may send user-provided content to an external API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
