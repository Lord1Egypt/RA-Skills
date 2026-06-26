## Description: <br>
Shorten URLs from terminal with custom slugs, local storage, and basic analytics. A self-contained CLI that maps long URLs to short slugs using a local JSON file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Derick001](https://clawhub.ai/user/Derick001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and terminal users use this skill to create and manage local short URL mappings, search them, export or import backups, and inspect basic click analytics without relying on an external URL-shortening service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shortened URLs and metadata are stored locally in plain JSON. <br>
Mitigation: Avoid storing sensitive private URLs, and protect or delete the local mappings file according to the user's security requirements. <br>
Risk: Importing mappings from an untrusted JSON file could add unwanted or misleading URL records. <br>
Mitigation: Import only JSON files from trusted sources and review imported mappings before relying on them. <br>
Risk: Delete, overwrite import, and cleanup commands can remove local mappings. <br>
Mitigation: Export a backup before destructive operations and use cleanup --dry-run before deleting entries in bulk. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Derick001/url-shortener-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Terminal text and optional JSON output from local CLI commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Python 3 and stores mappings in a local JSON file under the user's home directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
