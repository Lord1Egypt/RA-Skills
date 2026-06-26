## Description: <br>
Cloud Share Downloader helps an agent identify supported cloud share links, attempt retrieval, and return a new share link when transfer succeeds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SxLiuYu](https://clawhub.ai/user/SxLiuYu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users provide a supported cloud drive or media share link so an agent can detect the service, attempt download or transfer handling, and provide a resulting share link or next-step guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask for cloud-drive session cookies or private share links. <br>
Mitigation: Provide credentials only through a scoped authentication flow, confirm the destination account and share visibility, and avoid raw session cookies unless operationally necessary. <br>
Risk: Automatic copying and re-sharing can expose private or licensed content without enough user control. <br>
Mitigation: Require explicit confirmation before each transfer, disclose retention and deletion expectations, and review destination permissions before creating a new share link. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/SxLiuYu/share-transfer-tool) <br>
- [Publisher profile](https://clawhub.ai/user/SxLiuYu) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text status messages with optional command-line usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request cloud-drive cookies for services that require authenticated access.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
