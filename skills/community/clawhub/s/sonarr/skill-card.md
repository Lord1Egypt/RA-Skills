## Description: <br>
Search and add TV shows to Sonarr. Supports monitor options, search-on-add. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jordyvandomselaar](https://clawhub.ai/user/jordyvandomselaar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and media-library operators use this skill to search for TV shows, add them to a configured Sonarr library, check whether shows already exist, and remove library entries when directed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can remove Sonarr library entries and can delete associated media files when the delete-files option is used. <br>
Mitigation: Approve removal commands only when the target show is correct, and use delete-files only when media deletion is intended. <br>
Risk: The skill uses a Sonarr API key stored in a local credential file. <br>
Mitigation: Protect the credential file, verify the configured URL points to the intended Sonarr instance, and rotate the API key if it is exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jordyvandomselaar/sonarr) <br>
- [Publisher profile](https://clawhub.ai/user/jordyvandomselaar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, JSON, and Markdown links with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq, a configured Sonarr URL, and a Sonarr API key.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
