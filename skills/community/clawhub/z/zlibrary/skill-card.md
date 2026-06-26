## Description: <br>
Search and download books from Z-Library. Caches login session to ~/.zlibrary-session.json. Downloads book files (EPUB/PDF) to ~/Downloads/. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imnoahcook](https://clawhub.ai/user/imnoahcook) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Z-Library, inspect available book formats, and download selected files through an agent-assisted command workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Z-Library account credentials and may cache session tokens in ~/.zlibrary-session.json. <br>
Mitigation: Keep ZLIBRARY_EMAIL and ZLIBRARY_PASSWORD private, restrict permissions on ~/.zlibrary-session.json if it is created, and delete that file to clear the cached login. <br>
Risk: The skill downloads external book files to ~/Downloads/. <br>
Mitigation: Download only content you trust and are allowed to access, and review downloaded files before opening or sharing them. <br>
Risk: The service domain can change, which could expose credentials if the wrong domain is used. <br>
Mitigation: Verify the service domain before entering credentials or running login commands. <br>


## Reference(s): <br>
- [ClawHub Z-Library skill page](https://clawhub.ai/imnoahcook/zlibrary) <br>
- [Publisher profile](https://clawhub.ai/user/imnoahcook) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown with inline bash commands and downloaded book files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl, ZLIBRARY_EMAIL, ZLIBRARY_PASSWORD, and an optional ~/.zlibrary-session.json session cache; downloads files to ~/Downloads/ unless the user specifies otherwise.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
