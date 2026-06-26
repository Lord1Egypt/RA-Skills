## Description: <br>
Design elegant AI wedding invitations, save-the-dates, RSVP cards, bridal shower invites, and engagement announcements from text prompts using the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omactiengartelle](https://clawhub.ai/user/omactiengartelle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, wedding planners, stationery designers, and sellers use this skill to generate wedding stationery image concepts such as invitations, save-the-dates, RSVP cards, bridal shower invites, and engagement announcements from short text prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wedding prompt text, optional reference IDs, and the user-provided Neta/Tales of AI token are sent to api.talesofai.com. <br>
Mitigation: Use the skill only when that external transfer is acceptable, avoid sensitive personal details in prompts, and prefer a limited-use token. <br>
Risk: Passing the token with --token can expose it in shell history or process listings. <br>
Mitigation: Use a limited-use token and handle shell history and process visibility according to local security practices. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/omactiengartelle/wedding-invitation-generator) <br>
- [Neta AI Token Signup](https://www.neta.art/open/) <br>
- [Neta/Tales of AI Image API](https://api.talesofai.com/v3/make_image) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Text] <br>
**Output Format:** [Plain text image URL with progress and error messages on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token supplied with --token; optional size and reference image UUID parameters adjust generated image dimensions and style inheritance.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
