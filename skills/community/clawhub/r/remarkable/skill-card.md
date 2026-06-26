## Description: <br>
Send files and web articles to a reMarkable e-ink tablet via the reMarkable Cloud, including PDF or EPUB uploads, article conversion, and cloud file management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickian](https://clawhub.ai/user/nickian) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to send local documents or converted web articles to a reMarkable e-ink tablet and manage files and folders in reMarkable Cloud through rmapi. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends documents and converted articles to a reMarkable Cloud account through a third-party rmapi tool with cached account access. <br>
Mitigation: Install a reviewed or pinned rmapi release, connect only the intended account, and protect or clear ~/.rmapi when needed. <br>
Risk: An incorrect URL, local file, or destination folder could send unintended content to the cloud. <br>
Mitigation: Confirm the source URL or file path and target folder before running upload or send-article commands. <br>
Risk: Web article conversion may fail or produce incomplete output when sites block scraping or alter page structure. <br>
Mitigation: Review the generated EPUB or PDF before upload when content fidelity matters, and use another source URL if extraction fails. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nickian/remarkable) <br>
- [Publisher profile](https://clawhub.ai/user/nickian) <br>
- [rmapi](https://github.com/ddvk/rmapi) <br>
- [reMarkable device login](https://my.remarkable.com/device/browser?showOtp=true) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands, file paths, and generated EPUB or PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses rmapi for cloud operations and caches account access in ~/.rmapi.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
