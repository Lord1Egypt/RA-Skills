## Description: <br>
Save articles to Readeck (self-hosted read-it-later app). Use when the user wants to save an article for later reading, add something to their reading list, or send a page to Readeck. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickian](https://clawhub.ai/user/nickian) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to save a supplied article URL to their configured self-hosted Readeck read-it-later instance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A misconfigured READECK_URL could send submitted URLs and the bearer token to an unintended server. <br>
Mitigation: Configure READECK_URL only for a trusted Readeck instance and verify the endpoint before use. <br>
Risk: Submitted private or internal URLs may be stored by Readeck and fetched by that server. <br>
Mitigation: Save private or internal URLs only when the user intends for the configured Readeck server to store and process them. <br>
Risk: The Readeck API token could be abused if exposed. <br>
Mitigation: Use a revocable or least-privileged token where available and keep READECK_API_TOKEN out of shared logs and files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nickian/readeck-save) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, API calls, text, configuration] <br>
**Output Format:** [Plain text status output from a shell script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires READECK_URL and READECK_API_TOKEN; sends the provided URL to the configured Readeck server.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
