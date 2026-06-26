## Description: <br>
Searches a configured Xiaoya/Alist media library for movies or series and helps copy the selected result from a local WebDAV mount into a local download directory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanshojin](https://clawhub.ai/user/hanshojin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with a trusted Xiaoya/Alist server and local WebDAV mount use this skill to search media titles, review candidate versions, and copy the selected file into a dedicated local download directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill copies files from a configured Xiaoya/Alist WebDAV mount, so an untrusted server or mount can expose unwanted paths or content. <br>
Mitigation: Install only when the Xiaoya/Alist server and WebDAV mount are trusted, and confirm the selected media result before copying. <br>
Risk: Large media files or same-named destination files can consume substantial disk space or update existing files in the download directory. <br>
Mitigation: Use a dedicated DOWNLOAD_DIR, monitor available disk space, and review destination contents before running copy operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hanshojin/xiaoya-download) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided Xiaoya/Alist host, download directory, and optional WebDAV mount configuration.] <br>

## Skill Version(s): <br>
1.3.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
