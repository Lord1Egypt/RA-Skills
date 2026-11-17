## Description:

Search Hugging Face models matching the user's query. Use when the user asks to use Hugging Face for this purpose.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruchir17-cmd](https://clawhub.ai/user/ruchir17-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and model evaluators use this skill to navigate Brave to Hugging Face model search results for a user-provided query while avoiding credential handling and account-modifying actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can navigate an existing Brave browser session to Hugging Face search results.

Mitigation: Use it only for model search/navigation and stop if authentication is required.

Risk: Browser sessions may already be authenticated.

Mitigation: Do not enter passwords, authentication codes, API keys, payment details, or other credentials.

## Reference(s):

- [Hugging Face Models](https://huggingface.co/models)
- [ClawHub skill page](https://clawhub.ai/ruchir17-cmd/skills/search-huggingface)
- [Publisher profile](https://clawhub.ai/user/ruchir17-cmd)

## Skill Output:

**Output Type(s):** [guidance, configuration]

**Output Format:** [Markdown instructions and browser navigation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces browser navigation behavior for Hugging Face model search; does not produce files or modify accounts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
