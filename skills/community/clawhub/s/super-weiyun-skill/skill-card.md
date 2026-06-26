## Description: <br>
This skill helps agents manage Tencent Weiyun cloud storage through Python CLI and SDK workflows for authentication, file operations, sharing, space usage, and recycle-bin management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill to automate Tencent Weiyun file management from an agent, including login, upload, download, search, sharing, capacity checks, and recycle-bin actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Tencent Weiyun session cookies and stores them in cookies.json, which can grant account-level access if exposed. <br>
Mitigation: Use only on a trusted machine, restrict file permissions on cookies.json, rotate or remove cookies after use, and never paste Cookie headers into shared logs or agent transcripts. <br>
Risk: The skill supports high-impact file actions, including upload, overwrite, delete, permanent delete, share-link creation, and recycle-bin clearing. <br>
Mitigation: Require human review before executing upload, delete, share, permanent-delete, or clear-recycle commands, and avoid autonomous public sharing or permanent deletion. <br>
Risk: Network calls act against a live Tencent Weiyun account and may affect private cloud files. <br>
Mitigation: Run with the least sensitive account practical, test with noncritical folders first, and verify remote paths before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/subaru0573/super-weiyun-skill) <br>
- [Publisher profile](https://clawhub.ai/user/subaru0573) <br>
- [Tencent Weiyun](https://www.weiyun.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples, plus JSON-style command results from the toolkit.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke networked Tencent Weiyun actions and produce local files such as cookies.json, downloaded files, uploaded files, and QR-code images.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
