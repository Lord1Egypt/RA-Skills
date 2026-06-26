## Description: <br>
Generate high-quality screenshots of Twitter/X posts using the TwitterShots API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xinhua](https://clawhub.ai/user/0xinhua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, social media teams, and content workflows use this skill to turn Twitter/X post URLs or tweet IDs into PNG, SVG, or HTML screenshots with configurable themes, aspect ratios, and display options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tweet URLs or IDs, rendering options, and the API key are sent to the TwitterShots service when generating screenshots. <br>
Mitigation: Use a dedicated, rotatable TWITTERSHOTS_API_KEY and avoid submitting sensitive or private tweet references unless the user trusts the provider. <br>
Risk: Return-url mode may place generated results on provider-hosted infrastructure. <br>
Mitigation: Prefer direct buffer downloads when local control is required, and review hosted URLs before sharing them externally. <br>


## Reference(s): <br>
- [ClawHub TwitterShots skill page](https://clawhub.ai/0xinhua/twittershots) <br>
- [TwitterShots skills homepage](https://github.com/twittershots/skills) <br>
- [TwitterShots API key settings](https://twittershots.com/settings/keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline commands, API parameters, and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to call the TwitterShots API and save generated PNG, SVG, or HTML tweet screenshots.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
