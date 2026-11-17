## Description:

Bing Webmaster Tools + IndexNow extension. Microsoft Copilot citations are fed by the Bing index; this skill makes Bing visibility, link data, and IndexNow URL submission first-class.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asale-ai](https://clawhub.ai/user/asale-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to work with Bing Webmaster Tools and IndexNow for Bing-index visibility, URL submission, and link-data comparison for verified properties.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill references an installer that was not present in the artifact.

Mitigation: Inspect the installer separately before running it and confirm it matches the expected Bing Webmaster Tools and IndexNow setup behavior.

Risk: The workflows require Bing Webmaster Tools credentials and may use an IndexNow host key.

Mitigation: Configure only the required keys in the agent environment and avoid exposing them in prompts, logs, or shared command output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/asale-ai/skills/seo-bing)
- [Publisher profile](https://clawhub.ai/user/asale-ai)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls]

**Output Format:** [Markdown guidance with command routing and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BING_WEBMASTER_API_KEY; INDEXNOW_KEY is optional for IndexNow workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
