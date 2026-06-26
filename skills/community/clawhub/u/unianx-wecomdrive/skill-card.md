## Description: <br>
wecomdrive helps agents operate WeCom Drive and WeCom Docs through the official web interface, including login QR capture, document export, local file processing, report generation, and upload back to WeCom Drive. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[junjiantech](https://clawhub.ai/user/junjiantech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to access user-provided WeCom Drive or Docs links, preserve authenticated browser sessions, export files for local processing, generate reports, and upload finished files back through the WeCom web app. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retain an authenticated enterprise browser session and local document artifacts. <br>
Mitigation: Use the skill only on specific user-provided links, avoid highly sensitive documents unless local processing is acceptable, and delete the skill's .state and .outputs directories when saved sessions, QR screenshots, and reports should be cleared. <br>
Risk: Browser-based access to a WeCom workspace can expose enterprise documents to local processing and generated outputs. <br>
Mitigation: Review generated files before upload and confirm that the requested document handling is appropriate for the workspace and data sensitivity. <br>


## Reference(s): <br>
- [wecomdrive ClawHub release page](https://clawhub.ai/junjiantech/unianx-wecomdrive) <br>
- [Publisher profile: junjiantech](https://clawhub.ai/user/junjiantech) <br>
- [ClawHub homepage](https://clawhub.ai) <br>
- [WeCom web notes](references/wecom-web-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON script output, screenshots, and generated local files such as HTML, DOCX, XLSX, or CSV.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser-session state, QR-code screenshots, exported WeCom files, and generated analysis reports under local state or output directories.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
