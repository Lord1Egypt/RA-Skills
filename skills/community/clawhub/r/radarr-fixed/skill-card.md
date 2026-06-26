## Description: <br>
Search and add movies to Radarr, with support for collections and search-on-add behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frannunpal](https://clawhub.ai/user/frannunpal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to search Radarr, check whether movies already exist, add individual movies or full collections, and remove library entries through Radarr API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a Radarr API key to modify the user's Radarr library. <br>
Mitigation: Install only when the publisher and artifact are trusted, and use Radarr credentials with the minimum access needed for the intended workflow. <br>
Risk: The remove command can delete media files when --delete-files is used. <br>
Mitigation: Confirm the selected movie and deletion intent before running removal commands that include --delete-files. <br>
Risk: The add-collection workflow can enable persistent monitoring and future automatic collection additions. <br>
Mitigation: Review collection additions and Radarr collection monitoring settings after use, especially when adding a full collection. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/frannunpal/radarr-fixed) <br>
- [Original Radarr skill](https://clawhub.com/jordyvandomselaar/radarr) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and command output text or JSON from Radarr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and Radarr credentials via configuration file or environment variables.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
