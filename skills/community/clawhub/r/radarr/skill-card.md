## Description: <br>
Search and add movies to Radarr. Supports collections, search-on-add option. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jordyvandomselaar](https://clawhub.ai/user/jordyvandomselaar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to search Radarr, add individual movies or collections, check library status, inspect configuration choices, and remove movies through Radarr API commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can remove movies from a Radarr library and can delete associated files when that option is used. <br>
Mitigation: Confirm the exact movie before removal and keep files unless deletion is intentional. <br>
Risk: Adding a collection can enable monitoring and search-on-add behavior for future automatic additions in Radarr. <br>
Mitigation: Review collection monitoring settings after adding a collection and use no-search options when immediate or future searches are not desired. <br>


## Reference(s): <br>
- [ClawHub Radarr skill page](https://clawhub.ai/jordyvandomselaar/radarr) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and plain text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq, plus a local Radarr URL, API key, and default quality profile configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
