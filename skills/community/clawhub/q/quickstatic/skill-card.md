## Description: <br>
QuickStatic Skills helps agents publish, update, query, and delete anonymous public static sites from zip archives through the QuickStatic API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h5box](https://clawhub.ai/user/h5box) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to publish static HTML sites from zip files, reuse stable site keys for updates, inspect site state, and remove published sites when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded site contents are public and hosted by an unknown third-party service. <br>
Mitigation: Do not upload secrets, private data, credentials, or unpublished proprietary assets through this skill. <br>
Risk: The site_key controls future updates and deletion for a published site. <br>
Mitigation: Generate one stable site_key per project, store it privately, and avoid exposing it in public logs or repositories. <br>
Risk: A delete request removes the published site associated with the site_key. <br>
Mitigation: Query the site first and ask for explicit confirmation before sending a delete request. <br>


## Reference(s): <br>
- [QuickStatic ClawHub release](https://clawhub.ai/h5box/quickstatic) <br>
- [QuickStatic API base](https://667661.xyz) <br>
- [Source artifact: skills.md](artifact/skills.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl examples, API parameters, response fields, and error handling notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces API usage instructions for public static-site publishing; it does not include executable installer code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
