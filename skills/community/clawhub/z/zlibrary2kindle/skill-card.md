## Description: <br>
Search Z-Library for books, download them, and send them to your Kindle. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[semihum](https://clawhub.ai/user/semihum) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Z-Library, download EPUB-preferred books, and email downloaded files to a configured Kindle address. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to run an unpinned external package that handles Z-Library credentials, SMTP or Gmail app-password credentials, cached sessions, email sending, and file deletion. <br>
Mitigation: Install only after trusting or inspecting the package, prefer a dedicated or revocable app password, verify the Kindle recipient before sending, and delete cached sessions on shared or untrusted machines. <br>
Risk: Authentication sessions are cached on disk and could persist after the workflow completes. <br>
Mitigation: Remove cached session files when the workflow is finished, especially on shared systems. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and environment variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose commands that authenticate with Z-Library, download files to /tmp/zlibrary2kindle/downloads, send email through SMTP, and delete a file after sending.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
