## Description: <br>
Transform YouTube videos into beautifully formatted ebook articles with transcripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cclam5](https://clawhub.ai/user/cclam5) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and content teams use this skill to set up a local workflow that fetches YouTube channel videos, extracts transcripts, rewrites them into articles, and packages them as EPUB ebooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uses API keys and sends video URLs, transcripts, and metadata to external services. <br>
Mitigation: Use a virtual environment, keep .env out of version control, prefer dedicated API keys, and review what data is sent before running the workflow. <br>
Risk: Optional Gmail delivery can email generated content and depends on stored Gmail credentials. <br>
Mitigation: Use a Gmail app password, confirm the recipient configuration, and enable email delivery only when the account and destination are intended. <br>
Risk: Optional macOS launchd automation can run the workflow on a schedule. <br>
Mitigation: Review the LaunchAgent plist path, command, and schedule before loading it. <br>
Risk: Dependencies are declared without pinned versions. <br>
Mitigation: Consider pinning dependencies and reviewing updates before using the workflow in a production environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cclam5/youtube-to-ebook) <br>
- [README](README.md) <br>
- [Skill Instructions](SKILL.md) <br>
- [Google Cloud Console](https://console.cloud.google.com/) <br>
- [Anthropic Console](https://console.anthropic.com/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python code references, and local configuration steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of a local .env file, channel list, EPUB output, optional Streamlit dashboard, optional Gmail delivery, and optional macOS launchd automation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
