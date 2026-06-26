## Description: <br>
Fetch personalized daily horoscope forecasts from zodiac-today.com API based on natal chart calculations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dowands](https://clawhub.ai/user/dowands) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and their agents use this skill to set up a zodiac-today.com profile, fetch personalized daily horoscope data, and turn ratings, favorable activities, lucky colors, and date ranges into practical planning guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup can cross a sensitive account boundary if an agent retrieves the email verification code from the user's mailbox. <br>
Mitigation: Use manual email verification and have the user provide the one-time code directly. <br>
Risk: The skill collects email, birth date, and birth city for the third-party horoscope service. <br>
Mitigation: Get explicit consent before collecting personal data and avoid logging or exposing it in shared contexts. <br>
Risk: API keys and temporary session cookies can grant access to the user's horoscope account. <br>
Mitigation: Store credentials only in environment variables or a secure secret store, and delete the temporary cookie file immediately after setup. <br>


## Reference(s): <br>
- [Zodiac Today API Reference](references/api.md) <br>
- [Zodiac Horoscope ClawHub Page](https://clawhub.ai/dowands/zodiac-horoscope) <br>
- [Zodiac Today API](https://zodiac-today.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZODIAC_API_KEY and ZODIAC_PROFILE_ID environment variables.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
