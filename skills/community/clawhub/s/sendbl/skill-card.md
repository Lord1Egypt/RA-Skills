## Description: <br>
Create sendbl file-exchange links -- request files from someone, send a file, check link status, list files in a link, or delete a link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antonefremov](https://clawhub.ai/user/antonefremov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and assistant users use this skill to create Sendbl file-transfer links, collect files from a counterparty, share a file, inspect link status, list uploaded files, or delete links after confirming the action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Sendbl personal access token and can expose sensitive owner tokens, upload URLs, and download URLs if outputs are shared carelessly. <br>
Mitigation: Keep SENDBL_API_KEY and generated tokens or links private, store the API key only in the environment, and revoke or rotate tokens if they are exposed. <br>
Risk: Deleting a link removes the link and uploaded files. <br>
Mitigation: Confirm the exact link and user intent before issuing delete requests. <br>
Risk: File-transfer requests may involve unintended recipients, filenames, or file contents. <br>
Mitigation: Review recipients, filenames, purpose text, and generated URLs with the user before approving actions. <br>


## Reference(s): <br>
- [Sendbl](https://sendbl.com) <br>
- [Sendbl API base URL](https://api.sendbl.com/v1) <br>
- [Sendbl token management](https://sendbl.com/account/tokens) <br>
- [Sendbl pricing and limits](https://sendbl.com/pricing) <br>
- [ClawHub skill page](https://clawhub.ai/antonefremov/sendbl) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SENDBL_API_KEY for authenticated calls; owner tokens, upload URLs, and download URLs should be treated as sensitive.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence; artifact _meta.json lists 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
