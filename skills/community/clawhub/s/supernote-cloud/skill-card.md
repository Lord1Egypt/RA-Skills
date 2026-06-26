## Description: <br>
Access a self-hosted Supernote Private Cloud instance to browse files and folders, upload PDF, EPUB, and note files, convert web articles to EPUB or PDF, check storage capacity, and navigate the directory tree. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickian](https://clawhub.ai/user/nickian) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Supernote users use this skill to manage documents on a self-hosted Supernote Private Cloud instance, including browsing folders, uploading files, and sending converted web articles to an e-reader. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Supernote account credentials and account-level file access. <br>
Mitigation: Install only if the Supernote server and account context are trusted, and use it only for files intended to be uploaded or managed through that account. <br>
Risk: The security evidence reports token caching in a shared temporary path. <br>
Mitigation: Remove /tmp/.supernote_token after use, especially on shared systems. <br>
Risk: The security evidence reports unsafe command-script input handling. <br>
Mitigation: Use caution with filenames, directory names, URLs, and passwords containing quotes or other special characters until the script is hardened. <br>
Risk: The skill connects to a self-hosted Supernote service and may use non-public, reverse-engineered API behavior. <br>
Mitigation: Prefer HTTPS or a trusted local network and expect endpoints to require review if Supernote firmware or server behavior changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nickian/supernote-cloud) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or upload EPUB, PDF, HTML, and document files through the Supernote command scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
