## Description: <br>
Uploads local files to Wenshushu and returns share links, pickup codes, and optional management links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gcdd1993](https://clawhub.ai/user/gcdd1993) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to upload specified local files to Wenshushu and receive downloadable sharing details in the conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload arbitrary local files to a public third-party file-sharing service. <br>
Mitigation: Confirm the exact file path before every upload and avoid sensitive files unless they are encrypted. <br>
Risk: Pickup codes, public links, management links, and Wenshushu tokens can grant access to uploaded files or account actions. <br>
Mitigation: Treat pickup codes, sharing links, management links, and tokens as secrets; share them only with intended recipients. <br>
Risk: The skill may install or run external upload tooling during setup or execution. <br>
Mitigation: Install only after reviewing the dependency setup and run it in an environment appropriate for third-party file sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gcdd1993/wenshushu-uploader) <br>
- [Publisher profile](https://clawhub.ai/user/gcdd1993) <br>
- [Wenshushu service](https://www.wenshushu.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style status text with download links, pickup codes, management links, and setup commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include public file-sharing URLs and management URLs that should be treated as sensitive.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
